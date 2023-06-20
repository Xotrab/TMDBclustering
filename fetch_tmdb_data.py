
from database_facade import db_facade
from tmdb_api_service import api_service

print('FETCHING TMDB DATA >>>>')
movie = api_service.get_movie_details(1098160)

reviews = api_service.get_movie_reviews(1098160)

movie.reviews = reviews

print('ADDING DATA TO THE DATABASE >>>>')
db_facade.add_many([movie])

if (movie.poster_path):
    print('FETCHING TMDB MOVIE POSTER >>>>')
    api_service.save_image(movie.poster_path)

print('FINISHED >>>>')
