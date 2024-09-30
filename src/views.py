import json
import os
from page_utils import card_info, read_transactions, count_card, get_gritting

PATH_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "main_page.json")


def main_page(user_date: str):
    """Функция возвращающая json файл с информацией по картам, транзакциям, курсе валют, акциях"""

    transactions = read_transactions("2018-12-30 22:13:13")
    card_count = count_card(transactions)
    information_card = []
    for card in card_count:
        information_card.append(card_info(transactions, card))
    response = [{"gritting": get_gritting(user_date)}, {"cards": information_card}, {"top_transactions": []}]
    with open(PATH_FILE, "w", encoding="UTF8") as file:
        json.dump(response, file, indent=4, ensure_ascii=False)


main_page("2020-12-12 22:13:13")
