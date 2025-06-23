from flask import Flask
from flask_cors import CORS
from database.db import DataBase
import os
from dotenv import load_dotenv
from .routes import register_routes

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def create_app():
    app = Flask(__name__)
    CORS(app)  # allows access from frontend (React)

    # Database init
    app.db = DataBase(DB_NAME, DB_USER, DB_PASSWORD)

    # Routes
    register_routes(app)

    return app
