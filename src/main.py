from user_setting import users_settings
from views import main_page
from datetime import datetime

if __name__ == '__main__':

    # Настройка валют и акций
    user_currencies = input("Введите, через пробел, название валют, чтобы узнать их курс.\n")
    user_stocks = input("Введите, через пробел, название акций, чтобы узнать их курс.\n")
    users_settings(user_currencies.split(), user_stocks.split())
