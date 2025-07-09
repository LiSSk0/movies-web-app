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
            return "Error: User not found", 404

        return render_template("profile.html", user=user, email=email)

    # @app.route("/add_rate", methods=["POST"])
    # def add_rate():
    #     email = request.form.get("email")
    #     movie_id = int(request.form.get("movie_id"))
    #     rate = float(request.form.get("rate"))
    #
    #     app.db.add_rate(email, movie_id, rate)
    #     return redirect(url_for('profile', email=email))

    @app.route("/movies", methods=["GET"])
    def movies():
        email = request.args.get("email")
        if not email or not app.db.get_user_by_email(email):
            # If the email isn't correct - redirecting on index page
            return redirect(url_for("index"))

        page = request.args.get('page', default=1, type=int)
        query = request.args.get('q', default="", type=str).strip()
        per_page = 100

        if query:
            movies100 = app.db.search_movies_by_name(query, page, per_page)
            next_movies = app.db.search_movies_by_name(query, page + 1, per_page)
        else:
            movies100 = app.db.get_movies_page(page, per_page)
            next_movies = app.db.get_movies_page(page + 1, per_page)

        hasNext = len(next_movies) > 0

        # Getting user's rates by email
        user_ratings = app.db.get_user_ratings(email)
        # Creating dict: key - movie ID, value - rate
        user_rates = {}
        for rating in user_ratings:
            user_rates[rating.movie_id] = rating.rate

        return render_template(
            "movies.html",
            movies=movies100,
            page=page,
            hasNext=hasNext,
            query=query,
            email=email,
            user_rates=user_rates
        )

    @app.route("/add_rate", methods=["POST"])
    def add_rate():
        email = request.form.get("email")
        movie_id = request.form.get("movie_id", type=int)
        rate = request.form.get("rate", type=float)

        # Check validity
        if not email or movie_id is None or rate is None:
            return "Error: Invalid data", 400

        # Adding rating to DB
        app.db.add_rate(email=email, movie_id=movie_id, rate=rate)

        # Redirecting back to the movies page, saving the params
        page = request.args.get("page", 1)
        query = request.args.get("q", "")
        return redirect(url_for("movies", email=email, page=page, q=query))

    @app.route("/recommendations", methods=["POST"])
    def recommendations():
        email = request.form.get("email")
        # recs = get_recommendations(email, app.db)
        # return render_template("index.html", recommendations=recs, no_user=not recs)
        return None
