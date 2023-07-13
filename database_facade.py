from typing import List
from sqlalchemy import create_engine, select
from config import connection_string
from models.base import Base
from models.movie import Movie
from models.genre import Genre
from models.company import Company
from models.country import Country
from models.language import Language
from models.person import Person
from sqlalchemy.orm import Session, joinedload, subqueryload
from sqlalchemy import and_

class DatabaseFacade():

    def __init__(self) -> None:
        self.engine = create_engine(connection_string, echo=False)
        self.session = Session(bind=self.engine)

    def create_tables(self) -> None:
        Base.metadata.create_all(bind=self.engine)

    def add_many(self, movies: List[Movie]) -> None:
        for movie in movies:
            self.session.merge(movie)
        self.session.commit()

    def select_movies(self) -> List[Movie]:
        # statement = select(Movie)
        # return session.scalars(statement).all()
        return self.session.query(Movie).filter(
            and_(
                Movie.poster_path.isnot(None),
                Movie.genres.any(),
                Movie.production_companies.any(),
                Movie.production_countries.any(),
                Movie.spoken_languages.any(),
                Movie.reviews.any(),
                Movie.cast.any(),
                Movie.directors.any()
            )
        ).options(
            joinedload(Movie.genres),
            joinedload(Movie.production_companies),
            joinedload(Movie.production_countries),
            joinedload(Movie.spoken_languages),
            subqueryload(Movie.reviews),
            subqueryload(Movie.cast),
            joinedload(Movie.directors),
        ).all()

db_facade = DatabaseFacade()
