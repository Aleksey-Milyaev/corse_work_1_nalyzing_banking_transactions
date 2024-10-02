import json
import logging
import os
import time
from collections import Counter
from datetime import datetime
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "utils.log"), "w")
file_formater = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)

# Пути до файлов
PATH_USERS_SETTINGS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "users_settings.json")
PATH_TRANSACTIONS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.xlsx")
PATH_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "main_page.json"
)  # Временная для сохранения файла ответа
load_dotenv()


def users_settings(currencies: list, stocks: list) ->Any:
    """Функция записывающая настройки пользователя в json файл"""
    try:
        if currencies == [] or stocks == []:
            logger.warning("список валют и(или) список акций не был переданы")
        else:
            logger.info(f"Пользовательские настройки записаны: currencies - {currencies}, stocks - {stocks}")
        currencies = [currency.upper() for currency in currencies]
        stocks = [stock.upper() for stock in stocks]
        users_settings_dict = {"user_currencies": currencies, "user_stocks": stocks}

        with open(PATH_USERS_SETTINGS, "w", encoding="UTF8") as file:
            file.write(json.dumps(users_settings_dict, indent=4))
    except Exception as ex:
        logger.error(f"users_settings: ошибка {ex}")


def get_gritting(user_date: str) -> Any:
    """Функция возвращающая приветствие"""
    logger.info(f"пользователь указал дату {user_date}")
    try:
        time_ = datetime.strptime(user_date, "%Y-%m-%d %H:%M:%S")
        hour = time_.hour

        if 0 <= hour < 6:
            return "Доброй ночи"
        elif 5 < hour < 13:
            return "Доброе утро"
        elif 12 < hour < 19:
            return "Добрый день"
        else:
            return "Добрый вечер"

    except Exception as ex:
        logger.error(f"ошибка {ex}")


def read_transactions(user_date: str) -> Any:
    """Функция чтения excel файла и вывода списка транзакций по дате"""

    try:
        date = datetime.strptime(user_date, "%Y-%m-%d %H:%M:%S")
        excel_transactions = pd.read_excel(PATH_TRANSACTIONS)
        transactions_from_date = []
        for i in range(date.day):
            day = f"{date.year}-{date.month}-{i + 1} 00:00:00"
            exp = excel_transactions[
                excel_transactions["Дата платежа"]
                == datetime.strftime(datetime.strptime(day, "%Y-%m-%d %H:%M:%S"), "%d.%m.%Y")
            ]
            transactions_from_date.append(exp.to_dict(orient="records"))

        transaction = []
        for item in transactions_from_date:
            for i in item:
                transaction.append(i)

        logger.info("Данные в указанный период успешно прочитаны")
        return transaction

    except Exception as ex:
        logger.error(f"read_transactions: ошибка {ex}")


def count_card(transactions: list) -> Any:
    """Функция вывода количества карт и их номеров"""
    try:
        card_number_list = []

        for transaction in transactions:
            if str(transaction["Номер карты"]) == "nan":
                continue
            else:
                card_number_list.append(transaction["Номер карты"])

        counted_card = Counter(card_number_list)
        logger.info("Все номера карт успешно считаны")
        return list(counted_card.keys())

    except Exception as ex:
        logger.error(f"count_card: ошибка {ex}")


def card_info(transactions: list, card_number: list) -> Any:
    """Функция вывода информации по карте"""
    try:
        all_expenses = 0

        for transaction in transactions:
            if card_number == transaction["Номер карты"]:
                all_expenses += int(transaction["Сумма операции"])

        info = {"card_number": card_number, "expenses": all_expenses, "cashback": abs(all_expenses / 100)}
        logger.info(f"информация по карте {card_number} успешно передана")
        return info

    except Exception as ex:
        logger.error(f"card_info: ошибка {ex}")


def top_transaction(transactions: list) -> Any:
    """Функция возвращающая пять наибольших операций"""
    try:
        transactions = sorted(transactions, key=lambda x: abs(x["Сумма операции"]), reverse=True)
        top_five = transactions[:5]
        logger.info("топ 5 транзакций успешно переданы")
        return top_five

    except Exception as ex:
        logger.error(f"top_transaction: ошибка {ex}")


def currency_rate(rate: list) -> Any:
    """Функция вывода курса валют с сайта 'Abstract API'"""
    try:
        currency = []
        abstract_api_key = os.getenv("abstract_api")
        for item in rate:
            content = requests.get(
                f"https://exchange-rates.abstractapi.com/v1/live/?api_key={abstract_api_key}&base={item}&target=RUB"
            )
            response = content.json()
            currency.append({"currency": item, "rate": round(response["exchange_rates"]["RUB"], 2)})
            time.sleep(1)
        logger.info("Курс валют успешно передан")
        return currency
    except Exception as ex:
        logger.error(f"currency_rate: ошибка {ex}")


def stock_prices(stock: list) -> Any:
    """Функция вывода стоимости акций с сайта 'marketstack'"""
    try:
        stocks = []
        marketstack_api_key = os.getenv("marketstack_api")
        for item in stock:
            content = requests.get(
                f"http://api.marketstack.com/v1/eod?access_key={marketstack_api_key}&symbols={item}"
            )
            response = content.json()
            stocks.append({"stock": item, "price": response["data"][0]["open"]})

        logger.info("Стоимость акций успешно передан")
        return stocks

    except Exception as ex:
        logger.error(f"stock_prices: ошибка {ex}")
