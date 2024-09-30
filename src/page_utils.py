import json
import os
import time

from collections import Counter
from datetime import datetime
import requests
from dotenv import load_dotenv
import pandas as pd

PATH_TRANSACTIONS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.xlsx")
PATH_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "main_page.json")
load_dotenv()


def get_gritting(user_date: str):
    """Функция возвращающая приветствие"""

    time = datetime.strptime(user_date, "%Y-%m-%d %H:%M:%S")
    hour = time.hour

    if 0 <= hour < 6:
        return "Доброй ночи"
    elif 5 < hour < 13:
        return "Доброе утро"
    elif 12 < hour < 19:
        return "Добрый день"
    else:
        return "Добрый вечер"


def read_transactions(user_date: str) -> list:
    """Функция чтения excel файла и вывода списка транзакций по дате"""
    date = datetime.strptime(user_date, "%Y-%m-%d %H:%M:%S")
    excel_transactions = pd.read_excel(PATH_TRANSACTIONS)
    transactions_from_date = []
    for i in range(date.day):
        day = f"{date.year}-{date.month}-{i+1} 00:00:00"
        exp = excel_transactions[excel_transactions["Дата платежа"] ==
                                 datetime.strftime(datetime.strptime(day, "%Y-%m-%d %H:%M:%S"), "%d.%m.%Y")]
        transactions_from_date.append(exp.to_dict(orient='records'))

    transaction = []
    for item in transactions_from_date:
        for i in item:
            transaction.append(i)

    return transaction


def count_card(transactions: list) -> list:
    """Функция вывода количества карт и их номеров"""

    card_number_list = []

    for transaction in transactions:
        if str(transaction['Номер карты']) == "nan":
            continue
        else:
            card_number_list.append(transaction['Номер карты'])

    counted_card = Counter(card_number_list)

    return list(counted_card.keys())


def card_info(transactions: list, card_number: list) -> dict:
    """Функция вывода информации по карте"""

    all_expenses = 0

    for transaction in transactions:
        if card_number == transaction["Номер карты"]:
            all_expenses += int(transaction["Сумма операции"])

    info = {"card_number": card_number, "expenses": all_expenses, "cashback": abs(all_expenses / 100)}

    return info


def top_transaction(transactions: list) -> list:
    """Функция возвращающая пять наибольших операций"""

    transactions = sorted(transactions, key=lambda x: abs(x['Сумма операции']), reverse=True)
    top_five = transactions[:5]

    return top_five


def currency_rate(rate: list) -> list:
    """Функция вывода курса валют с сайта 'Abstract API'"""

    currency = []
    abstract_api_key = os.getenv("abstract_api")
    for item in rate:
        content = requests.get(f"https://exchange-rates.abstractapi.com/v1/live/?api_key={abstract_api_key}&base={item}&target=RUB").text
        response = json.loads(content)
        currency.append({"currency": item, "rate": round(response["exchange_rates"]["RUB"], 2)})
        time.sleep(1)

    return currency


def stock_prices(stock: list) -> list:
    """Функция вывода стоимости акций с сайта 'marketstack'"""

    stocks = []
    marketstack_api_key = os.getenv("marketstack_api")
    for item in stock:
        content = requests.get(f"http://api.marketstack.com/v1/eod?access_key={marketstack_api_key}&symbols={item}").text
        response = json.loads(content)
        stocks.append({"stock": item, "price": response["data"][0]['open']})

    return [stocks]
