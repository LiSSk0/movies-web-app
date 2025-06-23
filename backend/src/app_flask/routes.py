from flask import jsonify


def register_routes(app):
    @app.route("/")
    def index():
        return jsonify({"message": "Welcome to the recommendation movie web-app!"})

    @app.route("/recommendations", methods=["GET"])
    def get_recommendations():
        # Тут пока заглушка - возвращаем список фильмов
        movies = [
            {"id": 1, "name": "Inception", "rating": 9.1},
            {"id": 2, "name": "The Matrix", "rating": 8.7}
        ]
        return jsonify(movies)