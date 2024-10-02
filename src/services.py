import datetime
import logging
import os
from typing import Any, Dict, List

logger = logging.getLogger("services")
file_handler = logging.FileHandler(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "services.log"), "w", encoding="utf-8"
)
file_formatter = logging.Formatter("%(asctime)s %(module)s %(funcName)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def investment_bank(month_: str, transactions:  Any, limit: int) -> float:
    """Функция, которая возвращает сумму, которую удалось бы отложить в Инвесткопилку"""

    try:
        year_month = datetime.datetime.strptime(month_, "%Y-%m")
    except ValueError:
        logger.error("Месяц должен быть указан в формате 'ГГГГ-ММ'")
        raise ValueError("Месяц должен быть указан в формате 'ГГГГ-ММ'")

    # Инициализируем общую сумму, которую нужно сохранить
    total_saved = 0.0

    for transaction in transactions:
        try:
            transaction_date = datetime.datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")
            transaction_date = datetime.datetime.strftime(transaction_date, "%Y-%m-%d")
            transaction_date = datetime.datetime.strptime(transaction_date, "%Y-%m-%d")
            # Проверяем, произошла ли транзакция в указанном месяце
            if transaction_date.year == year_month.year and transaction_date.month == year_month.month:
                amount = transaction["Сумма операции"]

                # Рассчитываем округленную сумму
                rounded_amount = ((amount + limit - 1) // limit) * limit
                saved_amount = rounded_amount - amount

                # Добавляем к общей сумме
                total_saved += saved_amount

                logger.debug(
                    f"Транзакция на {transaction['Дата операции']} на сумму {amount} ₽,"
                    f"округленная до {rounded_amount} ₽. Сэкономлено: {saved_amount} ₽."
                )

        except ValueError:
            logger.error(f"Дата транзакции должна быть в формате «ГГГГ-ММ-ДД» для транзакции {transaction}.")
            continue

    logger.info(f"Общая сумма сбережений за месяц {month_}: {total_saved} ₽")
    return round(total_saved, 2)
