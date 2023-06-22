from sqlalchemy import Column, ForeignKey, Table
from models.base import Base

movie_director_table = Table(
    'movie_director',
    Base.metadata,
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
    Column('person_id', ForeignKey('people.id'), primary_key=True),
)