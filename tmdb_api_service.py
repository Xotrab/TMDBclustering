from typing import List, Type, TypeVar
from marshmallow import Schema
import requests
from config import api_url, api_key, language
from urllib.parse import urlencode, urljoin

from models.movie import Movie, MovieSchema
from models.paginated_response import ReviewsPaginatedResponse, ReviewsPaginatedResponseSchema
from models.review import Review

T = TypeVar('T', bound=Schema)

class TmdbApiService():

    def __init__(self) -> None:
        self.api_url = api_url
        self.default_params = {
            'api_key': api_key,
            'language': language
        }
    
    def get_movie_details(self, movie_id: int) -> Movie:
        endpoint = f'movie/{movie_id}'
        
        url = self._create_url(endpoint, self.default_params)
        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        movie_schema = MovieSchema()

        return self._deserialize_json(response.text, movie_schema)
    
    def get_movie_reviews_page(self, movie_id: int, page: int) -> ReviewsPaginatedResponse:
        endpoint = f'movie/{movie_id}/reviews'

        params = self.default_params
        params['page'] = page

        url = self._create_url(endpoint, params)
        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        reviews_paginated_response_schema = ReviewsPaginatedResponseSchema()

        return self._deserialize_json(response.text, reviews_paginated_response_schema)
    
    def get_movie_reviews(self, movie_id) -> List[Review]:
        paginated_response = self.get_movie_reviews_page(movie_id, 1)
        reviews = paginated_response.results

        page = 2
        while (page <= paginated_response.total_pages):
            paginated_response = self.get_movie_reviews_page(movie_id, 2)
            reviews.append(paginated_response.results)
            page +=1

            # Maximum amount of fetched pages has been capped to 5
            if (page == 5):
                break
        
        return reviews





    def _create_url(self, endpoint: str, params: dict) -> str:
        url = urljoin(self.api_url, endpoint)
        encoded_params = urlencode(params)

        return url + '?' + encoded_params
    
    def _deserialize_json(self, json_str: str, schema: Type[T]):
        return schema.loads(json_str)

api_service = TmdbApiService()
   