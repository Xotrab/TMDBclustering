from sqlalchemy import create_engine, text
from config import connection_string
from models.base import Base
from models.movie import Movie
from models.genre import Genre

engine = create_engine(connection_string, echo=True)

def create_tables():
    print('CREATING TABLES >>>>')
    Base.metadata.create_all(bind=engine)

# with engine.connect() as connection:
#     result = connection.execute(text('select "Hello"'))

#     print(result.all())

