import json
import logging
import os
from utils import (card_info, read_transactions, count_card, get_gritting, top_transaction, currency_rate,
                   stock_prices)

logger = logging.getLogger("views")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "views.log"), "w")
file_formater = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)

PATH_MAIN_PAGE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "main_page.json")
PATH_USERS_SETTINGS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "users_settings.json")


def main_page(user_date: str):
    """Функция возвращающая json файл с информацией по картам, транзакциям, курсе валют, акциях"""
    try:
        with open(PATH_USERS_SETTINGS, encoding="UTF8") as file:
            content = file.read()
            rate_stock = json.loads(content)

        rats = rate_stock["user_currencies"]
        stock = rate_stock["user_stocks"]
        transactions = read_transactions(user_date)
        card_count = count_card(transactions)
        information_card = []
        top_five = top_transaction(transactions)
        top_transactions = []
        currency = currency_rate(rats)
        stocks = stock_prices(stock)
        for card in card_count:
            information_card.append(card_info(transactions, card))

        for item in top_five:
            operation = {"date": item['Дата платежа'], "amount": item['Сумма операции'],
                         "category": item['Категория'], "description": item['Описание']}
            top_transactions.append(operation)

        response = [{"gritting": get_gritting(user_date), "cards": information_card},
                    {"top_transactions": top_transactions}, {"currency_rates": currency}, {"stock_prices": stocks}]
        logger.info("json ответ с результатами успешно передан")

        return response

    except Exception as ex:
        logger.error(f"views: ошибка {ex}")
