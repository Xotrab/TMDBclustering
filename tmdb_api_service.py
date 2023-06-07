from typing import Type, TypeVar
from marshmallow import Schema
import requests
from config import api_url, api_key, language
from urllib.parse import urlencode, urljoin
import json

from models.movie import Movie, MovieSchema

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

    def _create_url(self, endpoint: str, params: dict) -> str:
        url = urljoin(self.api_url, endpoint)
        encoded_params = urlencode(params)

        return url + '?' + encoded_params
    
    def _deserialize_json(self, json_str: str, schema: Type[T]):
        return schema.loads(json_str)

tmdb_api_service = TmdbApiService()
result = tmdb_api_service.get_movie_details(713704)
print(result.status)
    