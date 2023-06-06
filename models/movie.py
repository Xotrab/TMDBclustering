from sqlalchemy.types import Enum
from typing import List
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.genre import Genre
from models.movie_genre import movie_genre_table
from models.movie_company import movie_company_table
from models.company import Company
from models.status_enum import StatusEnum

class Movie(Base):
    __tablename__ = 'movies'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    original_title: Mapped[str] = mapped_column(nullable=False)
    original_language: Mapped[str] = mapped_column(nullable=False)
    overview: Mapped[str] = mapped_column(nullable=True)
    tagline: Mapped[str] = mapped_column(nullable=True)
    release_date: Mapped[str] = mapped_column(nullable=False)
    budget: Mapped[int] = mapped_column(nullable=False)
    popularity: Mapped[float] = mapped_column(nullable=False)
    revenue: Mapped[int] = mapped_column(nullable=False)
    vote_average: Mapped[float] = mapped_column(nullable=False)
    vote_count: Mapped[int] = mapped_column(nullable=False)
    runtime: Mapped[int] = mapped_column(nullable=True)
    adult: Mapped[bool] = mapped_column(nullable=False)
    video: Mapped[bool] = mapped_column(nullable=False)
    status = mapped_column(Enum(StatusEnum), nullable=False)
    poster_path: Mapped[str] = mapped_column(nullable=True)
    backdrop_path: Mapped[str] = mapped_column(nullable=True)

    genres: Mapped[List[Genre]] = relationship(secondary=movie_genre_table)
    production_companies: Mapped[List[Company]] = relationship(secondary=movie_company_table)
    
    def __repr__(self) -> str:
        return f'<Movie id={self.id}, title={self.title}, genres={self.genres}>'