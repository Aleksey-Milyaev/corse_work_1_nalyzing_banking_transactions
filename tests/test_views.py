import json
from unittest.mock import patch

import pandas as pd
import pytest

from src.views import main_page

expected = [
    {"gritting": "Доброе утро", "cards": []},
    {"top_transactions": []},
    {"currency_rates": {"USD": 90}},
    {"stock_prices": {"AAPL": 1500}},
]
expected = json.dumps(expected, indent=4, ensure_ascii=False)
transactions = pd.DataFrame(
    [
        {
            "Дата операции": "28.03.2018 09:24:15",
            "Дата платежа": "29.03.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -150.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -150.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Связь",
            "MCC": 4814.0,
            "Описание": "МТС",
            "Бонусы (включая кэшбэк)": 3,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 150.0,
        },
        {
            "Дата операции": "28.03.2018 08:23:56",
            "Дата платежа": "30.03.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -197.7,
            "Валюта операции": "RUB",
            "Сумма платежа": -197.7,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Супермаркеты",
            "MCC": 5411.0,
            "Описание": "Billa",
            "Бонусы (включая кэшбэк)": 3,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 197.7,
        },
    ]
)


@patch("src.views.currency_rate")
@patch("src.views.stock_prices")
def test_views(mock_stocks_price, mock_currency_rate):
    "Тестирование функции вывода json отчета"
    mock_currency_rate.return_value = {"USD": 90}
    mock_stocks_price.return_value = {"AAPL": 1500}

    assert main_page("2024-07-06 10:42:30") == expected


def test_views_with_wrong_date():
    """Функция тестирования неправильной даты"""
    with pytest.raises(Exception) as exc_info:
        main_page(transactions, "ABC")
        assert str(exc_info.value) == []
