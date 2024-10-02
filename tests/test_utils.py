import os
import json
from unittest.mock import Mock, patch

import pandas as pd
from dotenv import load_dotenv

from src.utils import (users_settings, get_gritting, read_transactions, count_card, card_info, top_transaction,
                       currency_rate, stock_prices)
import pytest


@pytest.fixture
def transaction():
    """Фикстура транзакций"""
    return ([{'Дата операции': '01.01.2021 18:08:23', 'Дата платежа': '01.01.2021', 'Номер карты': '*7197',
              'Статус': 'OK', 'Сумма операции': -815.68, 'Валюта операции': 'RUB', 'Сумма платежа': -815.68,
              'Валюта платежа': 'RUB', 'Кэшбэк': 100, 'Категория': 'Супермаркеты', 'MCC': 5411.0, 'Описание': 'Дикси',
              'Бонусы (включая кэшбэк)': 16, 'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 815.68},
             {'Дата операции': '28.02.2018 22:52:20', 'Дата платежа': '01.03.2018', 'Номер карты': '*4556',
              'Статус': 'OK', 'Сумма операции': -41.0, 'Валюта операции': 'RUB', 'Сумма платежа': -41.0,
              'Валюта платежа': 'RUB', 'Кэшбэк': 50, 'Категория': 'Супермаркеты', 'MCC': 5411.0, 'Описание': 'Дикси',
              'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 41.0}])


def test_users_settings():
    """Тест функции записывающей настройки пользователя"""
    users_settings(['c_1', 'c_2'], ['s_1', 's_2'])
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users_settings.json')
    with open(path, encoding="UTF8") as file:
        content = file.read()
    content = json.loads(content)
    assert content == {"user_currencies": ["C_1", "C_2"], "user_stocks": ["S_1", "S_2"]}


@pytest.mark.parametrize("user_date, expected", [('2020-10-10 02:00:00', "Доброй ночи"),
                                                 ('2020-10-10 13:00:00', "Добрый день"),
                                                 ('2020-10-10 10:00:00', "Доброе утро"),
                                                 ('2020-10-10 19:00:00', "Добрый вечер")])
def test_get_gritting(user_date, expected):
    """Тест функции возвращающей приветствие"""
    assert get_gritting(user_date) == expected


def test_read_operation_xlsx(transaction):
    """Тест функции считывания операций из файла.xlsx"""
    mock_read = Mock(
        return_value=pd.DataFrame(transaction))
    pd.read_excel = mock_read
    assert read_transactions("2021-01-01 00:00:00") == [{'Дата операции': '01.01.2021 18:08:23',
                                                         'Дата платежа': '01.01.2021', 'Номер карты': '*7197',
                                                         'Статус': 'OK', 'Сумма операции': -815.68,
                                                         'Валюта операции': 'RUB', 'Сумма платежа': -815.68,
                                                         'Валюта платежа': 'RUB', 'Кэшбэк': 100,
                                                         'Категория': 'Супермаркеты', 'MCC': 5411.0,
                                                         'Описание': 'Дикси', 'Бонусы (включая кэшбэк)': 16,
                                                         'Округление на инвесткопилку': 0,
                                                         'Сумма операции с округлением': 815.68}]
    mock_read.assert_called_once()


def test_count_card(transaction):
    """Тест функции подсчета количества карт"""
    assert count_card(transaction) == ['*7197', '*4556']


def test_card_info(transaction):
    """Тест функции выводящей информацию по карте"""
    assert card_info(transaction, '*7197') == {'card_number': '*7197', 'cashback': 8.15, 'expenses': -815}


def test_top_transaction(transaction):
    """Тест функции возвращающей топ 5 транзакций"""
    assert top_transaction(transaction) == [{'Дата операции': '01.01.2021 18:08:23', 'Дата платежа': '01.01.2021',
                                             'Номер карты': '*7197', 'Статус': 'OK', 'Сумма операции': -815.68,
                                             'Валюта операции': 'RUB', 'Сумма платежа': -815.68,
                                             'Валюта платежа': 'RUB', 'Кэшбэк': 100, 'Категория': 'Супермаркеты',
                                             'MCC': 5411.0, 'Описание': 'Дикси', 'Бонусы (включая кэшбэк)': 16,
                                             'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 815.68},
                                            {'Дата операции': '28.02.2018 22:52:20', 'Дата платежа': '01.03.2018',
                                             'Номер карты': '*4556',
                                             'Статус': 'OK', 'Сумма операции': -41.0, 'Валюта операции': 'RUB',
                                             'Сумма платежа': -41.0,
                                             'Валюта платежа': 'RUB', 'Кэшбэк': 50, 'Категория': 'Супермаркеты',
                                             'MCC': 5411.0, 'Описание': 'Дикси',
                                             'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0,
                                             'Сумма операции с округлением': 41.0}]


@patch("requests.get")
def test_currency_rate(mock_get):
    """Тест функции возвращающей курс валют"""
    load_dotenv()
    api_key = os.getenv("abstract_api")
    mock_get.return_value.json.return_value = {"base":"USD","last_updated":1646054100,"exchange_rates":{"RUB":104.99999999999999}}
    assert currency_rate(["USD"]) == [{'currency': 'USD', 'rate': 105.0}]
    mock_get.assert_called_once_with(
        f"https://exchange-rates.abstractapi.com/v1/live/?api_key={api_key}&base=USD&target=RUB",)


@patch("requests.get")
def test_stocks_price(mock_get):
    """Тест функции возвращающей стоимость акций"""
    load_dotenv()
    api_key = os.getenv("marketstack_api")
    mock_get.return_value.json.return_value = {"data": [{"open": 229.52}]}
    assert stock_prices(["AAPL"]) == [{'stock': 'AAPL', 'price': 229.52}]
    mock_get.assert_called_once_with(
        f"http://api.marketstack.com/v1/eod?access_key={api_key}&symbols=AAPL")
