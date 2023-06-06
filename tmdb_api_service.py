import requests
from config import api_url, api_key, language
from urllib.parse import urlencode, urljoin

class TmdbApiService():

    def __init__(self) -> None:
        self.api_url = api_url
        self.default_params = {
            'api_key': api_key,
            'language': language
        }
    
    def get_movie_details(self, movie_id: int):
        endpoint = f'movie/{movie_id}'
        
        url = self._create_url(endpoint, self.default_params)
        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        return response.text

    def _create_url(self, endpoint: str, params: dict) -> str:
        url = urljoin(self.api_url, endpoint)
        encoded_params = urlencode(params)

        return url + '?' + encoded_params

tmdb_api_service = TmdbApiService()

print(tmdb_api_service.get_movie_details(713704))
    