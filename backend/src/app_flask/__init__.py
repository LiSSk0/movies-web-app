from flask import Flask
from flask_cors import CORS
from .routes import register_routes


def create_app(db):
    app = Flask(__name__)
    CORS(app)  # allows access from frontend

    app.db = db

    # Routes
    register_routes(app)

    return app
