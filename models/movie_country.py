from sqlalchemy import Column, ForeignKey, Table
from models.base import Base

movie_country_table = Table(
    'movie_country',
    Base.metadata,
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
    Column('country_iso_3166_1', ForeignKey('countries.iso_3166_1'), primary_key=True),
)