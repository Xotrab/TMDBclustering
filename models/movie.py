from typing import List
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.genre import Genre
from models.movie_genre import movie_genre_table

class Movie(Base):
    __tablename__ = 'movies'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)

    genres: Mapped[List[Genre]] = relationship(secondary=movie_genre_table)
    
    def __repr__(self) -> str:
        return f'<Movie id={self.id}, title={self.title}, genres={self.genres}>'