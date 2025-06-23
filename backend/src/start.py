from dotenv import load_dotenv
from database.db import DataBase
# from app import create_app
import sys
import os

# Loading environment vars from .env
load_dotenv()

# Getting DB data
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# app = create_app()


if __name__ == '__main__':
    # Checking the correctness of DB data
    if DB_USER is None or len(DB_USER) == 0 or DB_NAME is None:
        print("# Error: Wrong DB credentials (.env). Exiting the program.")
        sys.exit()

    try:
        db = DataBase(DB_NAME, DB_USER, DB_PASSWORD)
    except Exception:
        sys.exit()

    # Для добавления отдела и отладки:
    # db.add_department("Отдел веб-технологий")
    # db.print(db.users_table)
    # db.print(db.departments_table)

    # app.run(debug=True)
