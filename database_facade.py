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

class DatabaseFacade():

    def __init__(self) -> None:
        self.engine = create_engine(connection_string, echo=False)
        self.session = Session(bind=self.engine)

    def create_tables(self) -> None:
        Base.metadata.create_all(bind=self.engine)

    def add_many(self, movies: List[Movie]) -> None:
        self.session.add_all(movies)
        self.session.commit()

    def select_movies(self) -> List[Movie]:
        # statement = select(Movie)
        # return session.scalars(statement).all()
        return self.session.query(Movie).all()
