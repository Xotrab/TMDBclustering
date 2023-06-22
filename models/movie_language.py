from sqlalchemy import Column, ForeignKey, Table
from models.base import Base

movie_language_table = Table(
    'movie_language',
    Base.metadata,
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
    Column('language_iso_639_1', ForeignKey('languages.iso_639_1'), primary_key=True),
)