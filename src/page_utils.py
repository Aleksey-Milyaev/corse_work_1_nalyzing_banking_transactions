import json
import os

from collections import Counter
from datetime import datetime

import pandas as pd

PATH_TRANSACTIONS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.xlsx")
PATH_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "main_page.json")

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
        exp = excel_transactions[excel_transactions["Дата платежа"] == datetime.strftime(datetime.strptime(day, "%Y-%m-%d %H:%M:%S"), "%d.%m.%Y")]
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
    top_five = []
    for transaction in transactions:


        return []
