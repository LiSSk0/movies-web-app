from flask import render_template, request, redirect, url_for
from recommender_ai.model import Recommender


def register_routes(app):
    # Creating Recommender object
    recommender = Recommender(app.db, "recommender_ai/movie_vectors.pkl")

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

    @app.route("/profile", methods=["GET", "POST"])
    def profile():
        email = request.args.get("email")
        if not email:
            return redirect("/")

        user = app.db.get_user_by_email(email)
        rated_movies = app.db.get_user_rated_movies(email)

        recommendations = None
        rec_error = None

        if request.method == "POST":
            # Getting recommendations
            success, recs_or_msg = recommender.user_recommendations(email, 10)
            if success:
                rec_ids = recs_or_msg  # list of movies' ids
                # Getting movies from DB by id
                recommendations = []
                for movie_id in rec_ids:
                    movie = app.db.get_movie_by_id(movie_id)
                    if movie:
                        recommendations.append(movie)
            else:
                rec_error = recs_or_msg

        return render_template(
            "profile.html",
            user=user,
            email=email,
            rated_movies=rated_movies,
            recommendations=recommendations,
            rec_error=rec_error,
        )

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

        # Check validity: email and movie_id are required
        if not email or movie_id is None:
            return "Error: Invalid data", 400

        # Updating rate (add/change/delete) в БД
        app.db.add_rate(email=email, movie_id=movie_id, rate=rate)

        # Redirect back to movies with params
        page = request.args.get("page", 1)
        query = request.args.get("q", "")
        return redirect(url_for("movies", email=email, page=page, q=query))
