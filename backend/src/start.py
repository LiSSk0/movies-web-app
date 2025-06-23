from dotenv import load_dotenv
from database.db import DataBase
from app_flask import create_app
import sys
import os

# Loading environment vars from .env
load_dotenv()

# Getting DB data
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


if __name__ == '__main__':
    # Checking the correctness of DB data
    if DB_USER is None or DB_NAME is None or DB_PASSWORD is None:
        print("# Error: Wrong DB credentials (.env). Exiting the program.")
        sys.exit()

    try:
        db = DataBase(DB_NAME, DB_USER, DB_PASSWORD)
    except Exception:
        sys.exit()

    app = create_app()
    app.run(debug=True)
