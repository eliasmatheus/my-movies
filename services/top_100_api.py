import requests


class Top100Api:
    """API do iMBD Scraper."""

    def get_movies(self):
        """Busca todos os filmes do top 100."""
        return requests.get(f"http://127.0.0.1:5001/movies").json()
