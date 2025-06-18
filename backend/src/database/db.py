# import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import orm, create_engine, MetaData, Table, Column, String, Date, Integer, Float
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
        engine = create_engine(connection_link)
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
                                 Column('user_id', Integer, foreign_key=True, nullable=False),
                                 Column('movie_id', Integer, foreign_key=True, nullable=False),
                                 Column('rate', Float, nullable=False))

        # Initializing tables
        metadata.create_all(engine)
        self.engine = engine