
from database_facade import db_facade
from tmdb_api_service import api_service
from config import movie_ids_json_path, json_encoding
import json

num_lines = 5

with open(movie_ids_json_path, "r", encoding=json_encoding) as file:
    line_count = 0
    for line in file:
        line_count += 1
        json_data = json.loads(line)
        movie_id = json_data.get("id")
        if movie_id is not None:
            print(f'FETCHING TMDB DATA FOR MOVIE ID={movie_id} >>>>')
            movie = api_service.get_movie_details(movie_id)

            reviews = api_service.get_movie_reviews(movie_id)

            movie.reviews = reviews

            print('ADDING DATA TO THE DATABASE >>>>')
            db_facade.add_many([movie])

            if (movie.poster_path):
                print('FETCHING TMDB MOVIE POSTER >>>>')
                api_service.save_image(movie.poster_path)

            print('FINISHED >>>>')

        if line_count == num_lines:
            break
