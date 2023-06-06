from sqlalchemy import Column, ForeignKey, Table
from models.base import Base

movie_production_company_table = Table(
    'movie_production_company',
    Base.metadata,
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
    Column('production_company_id', ForeignKey('production_companies.id'), primary_key=True),
)