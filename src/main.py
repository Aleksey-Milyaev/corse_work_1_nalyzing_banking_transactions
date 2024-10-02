import logging
import os
from datetime import datetime

import pandas as pd

from src.reports import spending_by_category
from src.services import investment_bank
from src.views import main_page

logger = logging.getLogger("main")
file_handler = logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                "logs", "main.log"), "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(module)s %(funcName)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

transactions = pd.read_excel(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.xlsx"))

if __name__ == "__main__":

    logger.info("Функция начала свою работу.")
    print(
        """Выберите категорию для отображения
            1 Главная страница
            2 Сервис фильтрации по переводам (физическим лицам)
            3 Отчет по категории трат"""
    )
    menu = ""
    while menu not in ("1", "2", "3"):
        menu = input("Введите номер категории\n")
        if menu not in ("1", "2", "3"):
            print("Некорректный ввод.Введите 1, 2, или 3. \n")
        if menu == "1":
            print("Главная страница")
            user_date = input("Введите дату в формате: 'ГГГГ-ММ-ДД ЧЧ:ММ:СС'")
            logger.info("Функция обрабатывает данные транзакций.")
            print(main_page(user_date))
            logger.info("Функция успешно завершила свою работу.")
        elif menu == "2":
            print("Выбран сервис который возвращает сумму, которую удалось бы отложить в Инвесткопилку")
            transactions = transactions.to_dict(orient="records")
            month = input("Введите месяц в формате: 'ГГГГ-ММ'")
            limit = int(input("Введите лимит: 10/50/100"))
            logger.info("Функция обрабатывает данные транзакций.")
            print(f"Total saved: {investment_bank(month, transactions, limit)} ₽")
            logger.info("Функция успешно завершила свою работу.")
        elif menu == "3":
            print("Выбран очет по категории трат")
            category = input("Введите категорию трат\n")
            try:
                date = input("Введите дату для формирования отчета в формате 'ДД.ММ.ГГГГ ЧЧ:ММ:СС'")
            except ValueError:
                print("Введена некорректная дата. Была использована текущая дата")
                date = datetime.now()
            logger.info("Функция обрабатывает данные транзакций.")
            result_js = spending_by_category(transactions, category, date)
            print(result_js)
            logger.info("Функция успешно завершила свою работу.")
