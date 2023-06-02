from sqlalchemy import Column, ForeignKey, Table
from models.base import Base

movie_genre_table = Table(
    'movie_genre',
    Base.metadata,
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
    Column('genre_id', ForeignKey('genres.id'), primary_key=True),
)