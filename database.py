from typing import List
from sqlalchemy import create_engine, select
from config import connection_string
from models.base import Base
from models.movie import Movie
from models.genre import Genre
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

genre1 = Genre(id = 1, name = 'Thriller')
genre2 = Genre(id = 2, name = 'Documentary')
genre3 = Genre(id = 3, name = 'Action')

movie1 = Movie(
    id = 1,
    title = 'Wieloryb',
    genres = [
       genre1,
       genre2
    ]
)

movie2 = Movie(
    id = 2,
    title = 'Terminator',
    genres = [
        genre1,
        genre3
    ]
)

movie3 = Movie(
    id = 3,
    title = 'King Kong',
    genres = [
        genre3
    ]
)

# add_many(movies=[movie1, movie2, movie3])
movies = select_movies()
print(movies)
