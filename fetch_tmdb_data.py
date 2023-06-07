
from database_facade import DatabaseFacade
from tmdb_api_service import TmdbApiService

tmdb_api_service = TmdbApiService()
database_facade = DatabaseFacade()

print('FETCHING TMDB DATA >>>>')
movie = tmdb_api_service.get_movie_details(713704)

print('ADDING DATA TO THE DATABASE >>>>')
database_facade.add_many([movie])

print('FINISHED >>>>')
