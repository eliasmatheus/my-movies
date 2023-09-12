import requests
import os


def is_docker():
    """Verifica se o container está rodando em um ambiente docker."""
    path = "/proc/self/cgroup"
    return (
        os.path.exists("/.dockerenv")
        or os.path.isfile(path)
        and any("docker" in line for line in open(path))
    )


class Top100Api:
    """API do iMBD Scraper."""

    def get_movies(self):
        """Busca todos os filmes do top 100."""
        host = "http://localhost"

        if is_docker():
            host = "http://host.docker.internal"

        return requests.get(f"{host}:5001/movies").json()
