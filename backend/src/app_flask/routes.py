from flask import render_template, request
from flask import render_template, request, redirect, url_for


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
        if request.method == "POST":
            email = request.form.get("email")

            user = app.db.get_user_by_email(email)
            if not user:  # if no such user then adding it to DB
                app.db.add_user(email)

            # Redirecting to user's profile
            return redirect(url_for('profile', email=email))

        return render_template("index.html")

    @app.route("/profile")
    def profile():
        email = request.args.get("email")
        user = app.db.get_user_by_email(email)

        if not user:
            return "User not found", 404

        return render_template("profile.html", user=user, email=email)

    @app.route("/add_rate", methods=["POST"])
    def add_rate():
        email = request.form.get("email")
        movie_id = int(request.form.get("movie_id"))
        rate = float(request.form.get("rate"))

        app.db.add_rate(email, movie_id, rate)
        return redirect(url_for('profile', email=email))

    @app.route("/recommendations", methods=["POST"])
    def recommendations():
        email = request.form.get("email")
        # recs = get_recommendations(email, app.db)
        # return render_template("index.html", recommendations=recs, no_user=not recs)
        return None
