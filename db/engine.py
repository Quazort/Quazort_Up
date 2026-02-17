from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

from core.config import db_config

engine = create_engine(db_config.DB)


def check_db():
    """Функция проверяет подключение к бд"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Подключение успешно:", result.scalar())
    except OperationalError as e:
        print("Ошибка подключения к БД:\n", e)
    except Exception as e:
        print("Произошла ошибка:", e)

check_db()