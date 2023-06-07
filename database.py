from typing import List
from sqlalchemy import create_engine, select
from config import connection_string
from models.base import Base
from models.movie import Movie
from models.genre import Genre
from models.company import Company
from models.country import Country
from models.language import Language
from sqlalchemy.orm import Session

engine = create_engine(connection_string, echo=False)
session = Session(bind=engine)

def create_tables() -> None:
    print('CREATING TABLES >>>>')
    Base.metadata.create_all(bind=engine)

def add_many(movies: List[Movie]) -> None:
    session.add_all(movies)
    session.commit()

def select_movies() -> List[Movie]:
    # statement = select(Movie)
    # return session.scalars(statement).all()
    return session.query(Movie).all()
