from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from .models import User, Movie, Rate, Base


class DataBase:
    def __init__(self, db_file):
        connection_link = f"sqlite:///{db_file}"
        self.engine = create_engine(connection_link, echo=True)

    # Adding a new user to the DB
    def add_user(self, email, password, nickname):
        new_user = User(email=email, password=password, nickname=nickname)
        with Session(self.engine) as session:
            session.add(new_user)
            session.commit()

    # Adding new movie to the DB
    def add_movie(self, movie_id, name, year, genre, description):
        new_movie = Movie(id=movie_id, name=name, year=year, genre=genre, description=description)
        with Session(self.engine) as session:
            session.add(new_movie)
            session.commit()

    # Adding new rate to the DB
    def add_rate(self, email, movie_id, rate):
        new_rate = Rate(user_email=email, movie_id=movie_id, rate=rate)
        with Session(self.engine) as session:
            session.add(new_rate)
            session.commit()

    # Adding new movies through the CSV (Excel)
    def insert_movies(self, filepath):
        import csv
        with open(filepath, encoding='utf-8') as f:
            reader = csv.DictReader(f)  # file contains the heading
            with Session(self.engine) as session:
                for row in reader:
                    movie = Movie(
                        id=int(row['id']),
                        name=row['name'],
                        year=int(row['year']),
                        genre=row['genre'],
                        description=row.get('description', '')  # if no description
                    )
                    session.add(movie)
                session.commit()
