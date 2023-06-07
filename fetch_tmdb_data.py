from database import add_many
from tmdb_api_service import TmdbApiService

tmdb_api_service = TmdbApiService()
movie = tmdb_api_service.get_movie_details(713704)

add_many([movie])