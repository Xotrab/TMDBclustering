
from database_facade import db_facade
from tmdb_api_service import api_service
from config import movie_ids_json_path, json_encoding
import json
import argparse
import collections

def remove_duplicates(obj_list):
    seen = collections.OrderedDict()

    for obj in obj_list:
        if obj.id not in seen:
            seen[obj.id] = obj

    return list(seen.values())

parser = argparse.ArgumentParser()
parser.add_argument("start_line", type=int, help="Line number to start reading from (starting from 1)")
parser.add_argument("num_lines", type=int, help="Number of lines to read")
args = parser.parse_args()

with open(movie_ids_json_path, "r", encoding=json_encoding) as file:
    line_count = 0
    for line in file:
        line_count += 1

        if line_count < args.start_line:
            continue

        json_data = json.loads(line)
        movie_id = json_data.get("id")

        if movie_id is not None:
            print(f'FETCHING TMDB DATA FOR MOVIE ID={movie_id}, LINE={line_count}>>>>')
            movie = api_service.get_movie_details(movie_id)
            movie.production_companies = remove_duplicates(movie.production_companies)

            if not movie.poster_path or not movie.overview or not movie.genres:
                print('SKIPPING - MOVIE IS MISSING POSTER PATH, OVERVIEW OR GENRES>>>>')

                if line_count >= args.start_line + args.num_lines - 1:
                    break
                else:
                    continue

            reviews = api_service.get_movie_reviews(movie_id)

            if not reviews:
                print('SKIPPING - MOVIE IS MISSING REVIEWS>>>>')

                if line_count >= args.start_line + args.num_lines - 1:
                    break
                else:
                    continue

            movie.reviews = reviews

            credits = api_service.get_movie_credits(movie_id)

            movie.cast = remove_duplicates(credits.cast)
            movie.directors = credits.crew

            if not movie.cast or not movie.directors:
                print('SKIPPING - MOVIE IS MISSING CREDITS>>>>')

                if line_count >= args.start_line + args.num_lines - 1:
                    break
                else:
                    continue

            print('ADDING DATA TO THE DATABASE >>>>')
            db_facade.add_many([movie])

            print('FETCHING TMDB MOVIE POSTER >>>>')
            api_service.save_image(movie.poster_path)

            print('FINISHED >>>>')

        if line_count >= args.start_line + args.num_lines - 1:
            break
