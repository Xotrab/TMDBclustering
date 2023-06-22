from sqlalchemy import Column, ForeignKey, Table
from models.base import Base

movie_actor_table = Table(
    'movie_actor',
    Base.metadata,
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
    Column('person_id', ForeignKey('people.id'), primary_key=True),
)