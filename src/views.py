import json
import os
from datetime import datetime
from page import card_info, read_transactions, count_card


PATH_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "main_page.json")

def main_page(date_time: str):
    """Функция возвращающая json файл с информацией по картам, транзакциям, курсе валют, акциях"""

    # Приветствие
    transactions = read_transactions()
    card_count = count_card(transactions)
    time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    hour = time.hour
    if 0 <= hour < 6:
        gritting = "Доброй ночи"
    elif 5 < hour < 13:
        gritting = "Доброе утро"
    elif 12 < hour < 19:
        gritting = "Добрый день"
    else:
        gritting = "Добрый вечер"

    # Данные по картам
    cards_information = []
    for card in card_count:
        if card == "nan":
            continue
        else:
            cards_information.append(card_info(transactions, card))


main_page("2024-12-12 22:13:13")






