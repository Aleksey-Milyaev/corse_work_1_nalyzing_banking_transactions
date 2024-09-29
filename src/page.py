import os
import pandas as pd
from collections import Counter


PATH_TRANSACTIONS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.xlsx")


def read_transactions() -> list:
    """Функция чтения excel файла и вывода списка транзакций"""

    excel_transactions = pd.read_excel(PATH_TRANSACTIONS)
    transactions = excel_transactions.to_dict(orient='records')

    return transactions


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


def card_info(transactions: list, card_number: list) -> str:
    """Функция вывода информации по карте"""
    all_expenses = 0
    for transaction in transactions:
        if card_number == transaction["Номер карты"]:
            all_expenses += int(transaction["Сумма операции"])
    return f"""Карта {card_number}
    Общая сумма расходов: {all_expenses}
    Кешбэк: {abs(all_expenses / 100)}"""





