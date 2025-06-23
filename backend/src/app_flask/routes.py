from flask import render_template, request


# then there will be an AI call
def get_recommendations(email, db):
    if email == "lissk0@mail.ru":
        return [
            {"name": "Inception", "rating": 9.1},
            {"name": "Dune", "rating": 8.7},
        ]
    return None


def register_routes(app):
    @app.route("/", methods=["GET", "POST"])
    def index():
        recommendations = None
        no_user = False

        if request.method == "POST":
            email = request.form.get("email")
            recs = get_recommendations(email, app.db)
            if recs:
                recommendations = recs
            else:
                no_user = True

        return render_template("index.html", recommendations=recommendations, no_user=no_user)