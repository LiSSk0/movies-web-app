import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class Recommender:
    def __init__(self, db, pickle_file):
        self.db = db
        self.pickle_file = pickle_file

        # Trying to get vectors from pkl
        try:
            with open(pickle_file, "rb") as f:
                self.movie_ids, self.titles, self.vectors = pickle.load(f)
        # If no data found, building vectors
        except FileNotFoundError:
            self._build_vectors()

    # Helping func to build vectors
    # NOTE: should work once for each movies' DB
    def _build_vectors(self):
        movies = self.db.get_movies()
        ids = [m.id for m in movies]
        names = [m.name for m in movies]
        descriptions = [m.description for m in movies]

        vectorizer = TfidfVectorizer(stop_words="english")
        self.vectors = vectorizer.fit_transform(descriptions)

        with open(self.pickle_file, "wb") as f:
            pickle.dump((ids, names, self.vectors), f)

    def user_recommendations(self, email, cnt=5):
        user_rated_movies = self.db.get_user_ratings(email)
        if not user_rated_movies:
            return 0, "No rated movies to create recommendations."

        # The goal is:
        # To understand which movies the user liked,
        # take the vectors of these movies (vector = numerical representation of the content of the movie),
        # and calculate the average "taste vector" of the user. This vector will be used to search for similar movies.

        # Creating dict of user's rated movies {123: 4.5, 678: 9.0}
        user_rated_movies_dict = {}
        for r in user_rated_movies:
            user_rated_movies_dict[r.movie_id] = r.rate

        # Adding high-rated movies to the list (rate >= 6.0)
        user_liked_ids = []
        for movie_id, rate in user_rated_movies_dict.items():
            if rate >= 6:
                user_liked_ids.append(movie_id)

        if not user_liked_ids:
            return 0, "No favourite movies (rate >= 6.0) to create recommendations."

        # Getting the indexes of liked movies
        liked_indexes = []
        for m_id in user_liked_ids:
            if m_id in self.movie_ids:  # checking just in case. in fact, it should always be true
                idx = self.movie_ids.index(m_id)
                liked_indexes.append(idx)

        liked_vectors = self.vectors[liked_indexes]
        avg_vector = liked_vectors.mean(axis=0)  # getting the avg vector of user's movie taste
        avg_vector = np.asarray(avg_vector)

        # Compute cosine similarity between user profile and all movie vectors
        similarities = cosine_similarity(avg_vector, self.vectors).flatten()  # flatten makes [] from [[]]

        # Sort indexes by similarity score descending
        sorted_indexes = np.argsort(similarities)[::-1]

        # Exclude movies that user has already rated
        rated_set = set(user_rated_movies_dict.keys())
        recommendations = []
        for idx in sorted_indexes:
            movie_id = self.movie_ids[idx]
            if movie_id not in rated_set:
                recommendations.append(movie_id)
            if len(recommendations) >= cnt:
                break

        # DEBUG: Weight of top-20 movies for user
        print("\nTop 20 movie recommendations by similarity:")
        for i in range(20):
            idx = sorted_indexes[i]
            sim_score = similarities[idx]
            movie_id = self.movie_ids[idx]
            title = self.titles[idx] if self.titles else "(unknown)"
            print(f"{i + 1}. ID: {movie_id} | Title: {title} | Similarity: {sim_score:.4f}")

        return 1, recommendations
