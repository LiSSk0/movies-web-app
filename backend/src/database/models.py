from sqlalchemy import Column, String, Integer, Date, Float, ForeignKey
from sqlalchemy.orm import declarative_base

# Base class for models
Base = declarative_base()


# Model for users table
class User(Base):
    __tablename__ = 'users'

    email = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False)
    nickname = Column(String, nullable=False)

    def __init__(self, email, password, nickname):
        self.email = email
        self.password = password
        self.nickname = nickname


# Model for movies table
class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    description = Column(String, nullable=False)

    def __init__(self, id, name, year, genre, description):
        self.id = id
        self.name = name
        self.year = year
        self.genre = genre
        self.description = description


# Model for rates table
class Rate(Base):
    __tablename__ = 'rates'

    user_email = Column(String, ForeignKey('users.email'), primary_key=True, nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True, nullable=False)
    rate = Column(Float, nullable=False)

    def __init__(self, user_email, movie_id, rate):
        self.user_email = user_email
        self.movie_id = movie_id
        self.rate = rate
