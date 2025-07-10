from database.db import DataBase
from app_flask import create_app
import sys

DB_FILE = "database/movies_db.db"

if __name__ == '__main__':
    if DB_FILE is None:
        print("# Error: Database file is not found. Exiting.")
        sys.exit()

    try:
        db = DataBase(DB_FILE)
    except Exception as e:
        print(f"# Error initializing DB: {e}")
        sys.exit()

    # db.insert_movies("C:/Users/asus/PycharmProject/movies-web-app/backend/src/database/movies.txt")
    # db.insert_movies_csv("C:/Users/t4i4k/OneDrive/Desktop/Projects/Python Projects/movies-web-app/backend\src\database/filtered_movies.csv")
    app = create_app(db)
    app.run(debug=True)
