from flask import Flask
from flask_cors import CORS
# from database.db import DataBase
import os
from .routes import register_routes

DB_FILE = "movies_db.db"


def create_app(db):
    app = Flask(__name__)
    CORS(app)  # allows access from frontend (React)

    app.db = db

    # Routes
    register_routes(app)

    return app
