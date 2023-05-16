from sqlalchemy import create_engine, text
from config import connection_string

engine = create_engine(connection_string, echo=True)

with engine.connect() as connection:
    result = connection.execute(text('select "Hello"'))

    print(result.all())

