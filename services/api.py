import requests
from dotenv import dotenv_values


class Api:
    # carrega a chave da API
    api_key = dotenv_values(".env")["API_KEY"]

    def get_movies(self, query: dict):
        """Faz uma busca na API do OMDb."""

        # adiciona a chave da API
        query["apikey"] = self.api_key

        return requests.get(f"https://www.omdbapi.com", params=query).json()

    def get_movie_by_id(self, imdb_id: str):
        """Faz uma busca na API do OMDb."""

        # adiciona a chave da API
        query = {"apikey": self.api_key, "i": imdb_id}

        return requests.get(f"https://www.omdbapi.com", params=query).json()
