from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from .models import User, Movie, Rate, Base


class DataBase:
    def __init__(self, db_file):
        connection_link = f"sqlite:///{db_file}"
        self.engine = create_engine(connection_link, echo=True)

    # Adding a new user to the DB
    def add_user(self, email):
        new_user = User(email=email)
        with Session(self.engine) as session:
            session.add(new_user)
            session.commit()

    # Adding new movie to the DB
    def add_movie(self, name, year, genre, description):
        new_movie = Movie(name=name, year=year, genre=genre, description=description)  # "id" is autoincrement
        with Session(self.engine) as session:
            session.add(new_movie)
            session.commit()

    # Adding new rate to the DB
    def add_rate(self, email, movie_id, rate):
        new_rate = Rate(user_email=email, movie_id=movie_id, rate=rate)
        with Session(self.engine) as session:
            session.add(new_rate)
            session.commit()

    # Getting the user by email
    def get_user_by_email(self, email):
        with Session(self.engine) as session:
            return session.query(User).filter_by(email=email).first()

    # Getting (100) movies for (1) page
    def get_movies_page(self, page=1, per_page=100):
        offset = (page - 1) * per_page
        with Session(self.engine) as session:
            movies = session.query(Movie).order_by(Movie.id).offset(offset).limit(per_page).all()
            return movies

    # Adding new movies using the csv-file
    # NOTE: there is no check for genre and description validity
    def insert_movies_csv(self, csv_file_path):
        import csv
        from datetime import datetime
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = row['title'].strip()
                overview = row['overview'].strip()
                genre = row['genres'].strip()
                date_str = row['release_date'].strip()

                # Trying to get the year
                try:
                    year = datetime.strptime(date_str, '%Y-%m-%d').year
                except Exception as e:
                    print(f'Error adding the "{title}": {e}')
                    continue

                # Inserting to the DB
                self.add_movie(
                    name=title,
                    year=int(year),
                    genre=genre,
                    description=overview
                )

    # Adding new movies using the txt-file
    def insert_movies_txt(self, filepath):
        with open(filepath, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',', 3)  # split by first 3 commas (to 4 parts)
                if len(parts) != 4:
                    continue  # skipping if bad data

                name, year, genre, description = parts
                try:
                    self.add_movie(
                        name=name,
                        year=int(year),
                        genre=genre,
                        description=description
                    )
                except Exception as e:
                    print(f'Error adding the "{name}": {e}')

