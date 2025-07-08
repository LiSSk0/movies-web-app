from database.db import DataBase
from app_flask import create_app
import sys
import os

DB_FILE = "movies_db.db"

if __name__ == '__main__':
    if DB_FILE is None:
        print("# Error: Database file is not found. Exiting.")
        sys.exit()

    try:
        db = DataBase(DB_FILE)
    except Exception as e:
        print(f"# Error initializing DB: {e}")
        sys.exit()

    app = create_app(db)
    app.run(debug=True)
