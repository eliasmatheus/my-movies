from pydantic import BaseModel, Field
from typing import Optional, List
from models.watchlist import Watchlist
from schemas import MovieViewSchema
from services import MDbApi

mdb_api = MDbApi()


class WatchlistSchema(BaseModel):
    """Define como uma nova lista de filmes a ser inserida deve ser."""

    name: str = "Maratona Marvel"
    description: str = "Uma lista de filmes da Marvel"


class WatchlistUpdateSchema(BaseModel):
    """Define como uma nova lista de filmes a ser inserida deve ser."""

    id: int = Field(
        default=1, description="ID da lista de filmes a ser atualizada"
    )
    name: str = "Maratona Marvel Editada"
    description: str = "Uma lista de filmes da Marvel Editada"


class WatchlistViewSchema(BaseModel):
    """Define como uma lista de filmes será retornada."""

    id: int = 1
    name: str = "Maratona Marvel"
    description: str = "Uma lista de filmes da Marvel"
    movies: list[str] = ["tt0848228", "tt4154796"]


class WatchlistByIDSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.

    A busca será feita apenas com base no ID da lista.
    """

    id: int = 1


class WatchlistListSchema(BaseModel):
    """Define como uma listagem de lista de filmes será retornada."""

    watchlists: List[WatchlistSchema]


def render_watchlists(watchlists: List[Watchlist]):
    """Retorna uma representação da lista segundo o WatchlistListSchema."""
    result = []

    for list in watchlists:
        movies = []

        for movie in list.movies:
            movies.append(movie.imdb_id)

        result.append(
            {
                "id": list.id,
                "name": list.name,
                "description": list.description,
                "movies": movies,
            }
        )

    return {"watchlists": result}


class WatchlistDetailsSchema(BaseModel):
    """Define como uma lista de filmes será retornada."""

    id: int = 1
    name: str = "Maratona Marvel"
    description: str = "Uma lista de filmes da Marvel"
    movies: List[MovieViewSchema] = [
        {
            "Title": "Pulp Fiction",
            "Year": "1994",
            "Rated": "R",
        }
    ]


class WatchlistDeleteSchema(BaseModel):
    """Define estrutura do retorno após uma requisição de remoção."""

    id: int
    message: str


def render_watchlist(watchlist: Watchlist):
    """Retorna uma representação da lista.

    Segue o schema definido em WatchlistDetailsSchema.
    """
    movies = []

    for movie in watchlist.movies:
        movie = mdb_api.get_movie_by_id(movie.imdb_id)
        movies.append(movie)

    return {
        "id": watchlist.id,
        "name": watchlist.name,
        "description": watchlist.description,
        "movies": movies,
    }


class WatchlistAddMovieSchema(BaseModel):
    """Define como um filme a ser inserido deve ser."""

    watchlist_ids: list[int] = [1]
    imdb_id: str = Field(
        default="tt0848228", description="ID do filme no imdb"
    )


class MovieWatchlistDeleteSchema(BaseModel):
    """Define a busca de um filme dentro de uma lista."""

    watchlist_id: int = 1
    imdb_id: str = Field(
        default="tt0848228", description="ID do filme no imdb"
    )


class MovieWatchlistGetSchema(BaseModel):
    """Define a busca pelas listas que um filme pertence."""

    imdb_id: str = Field(
        default="tt0848228", description="ID do filme no imdb"
    )


class MovieWatchlistsViewSchema(BaseModel):
    """Define a lista de playlists que um filme pertence."""

    imdb_id: str = Field(
        default="tt0848228", description="ID do filme no imdb"
    )
    watchlists: List[int] = [1]


def render_movie_watchlists(imdb_id, watchlists):
    """Retorna uma representação da lista segundo o MovieWatchlistsViewSchema."""
    return {"imdb_id": imdb_id, "watchlists": watchlists}
