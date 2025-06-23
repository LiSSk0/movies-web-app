# import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import orm, create_engine, MetaData, Table, Column, String, ForeignKey, Integer, Float
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from .models import User, Movie, Rate

SqlAlchemyBase = orm.declarative_base()


class DataBase:
    def __init__(self, db_name, user, password):
        # Creating connection to postgres
        connection = psycopg2.connect(user=user, password=password)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # без автокоммита нельзя создавать БД,
                                                                    # т.к. открыта одна транзакция

        # Creating DB if still not
        cursor = connection.cursor()
        try:
            cursor.execute('create database ' + db_name)
        except psycopg2.errors.DuplicateDatabase:  # db is already created
            pass
        finally:  # closing the connection
            cursor.close()
            connection.close()

        # Creating engine and connection
        # default: echo=False, pool_size=5, max_overflow=10, encoding='UTF-8'
        connection_link = "postgresql+psycopg2://" + user + ":" + password + "@localhost/" + db_name
        try:
            engine = create_engine(connection_link)
        except Exception as e:
            print("# Error: Wrong DB credentials:", e)
            raise
        metadata = MetaData()

        # Creating users table
        self.users_table = Table('users', metadata,
                                 Column('email', String, primary_key=True, nullable=False),
                                 Column('password', String, nullable=False),
                                 Column('nickname', String, nullable=False))

        # Creating movies table
        self.movies_table = Table('movies', metadata,
                                  Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
                                  Column('name', String, nullable=False),
                                  Column('year', Integer, nullable=False),
                                  Column('genre', String, nullable=False))

        # Creating rates table
        self.rates_table = Table('rates', metadata,
                                 Column('user_email', String, ForeignKey('users.email'), primary_key=True, nullable=False),
                                 Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True, nullable=False),
                                 Column('rate', Float, nullable=False))

        # Initializing tables
        metadata.create_all(engine)
        self.engine = engine

    # Adding new user to 'users'
    def add_user(self, email, password, nickname):
        new_user = User(
            email=email,
            password=password,
            nickname=nickname
        )
        with Session(self.engine) as session:
            session.add(new_user)
            session.commit()

    # Adding new rate to 'rates'
    def add_rate(self, email, movie_id, rate):
        new_rate = Rate(
            user_email=email,
            movie_id=movie_id,
            rate=rate
        )
        with Session(self.engine) as session:
            session.add(new_rate)
            session.commit()

    # Adding new movie to 'movies'
    def add_movie(self, movie_id, name, year, genre):
        new_movie = Movie(
            id=movie_id,
            name=name,
            year=year,
            genre=genre
        )
        with Session(self.engine) as session:
            session.add(new_movie)
            session.commit()