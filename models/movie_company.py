from sqlalchemy import Column, ForeignKey, Table
from models.base import Base

movie_company_table = Table(
    'movie_company',
    Base.metadata,
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
    Column('company_id', ForeignKey('companies.id'), primary_key=True),
)