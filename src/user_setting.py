import json
import os


PATH_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "users_settings.json")


def users_settings(currencies: list, stocks: list):
    currencies = [currency.upper() for currency in currencies]
    stocks = [stock.upper() for stock in stocks]
    """Функция записывающая настройки пользователя в json файл"""
    users_settings_dict = {"user_currencies": currencies, "user_stocks": stocks}
    with open(PATH_FILE, "a", encoding="UTF8") as file:
        file.write(json.dumps(users_settings_dict))
