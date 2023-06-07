
from database_facade import db_facade
from tmdb_api_service import api_service

print('FETCHING TMDB DATA >>>>')
movie = api_service.get_movie_details(713704)

print('ADDING DATA TO THE DATABASE >>>>')
db_facade.add_many([movie])

print('FINISHED >>>>')
