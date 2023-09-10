from flask_openapi3 import Tag, APIBlueprint

from schemas import *
from schemas import ErrorSchema

from logger import logger
from models import Session, Watchlist, AddedMovie
from sqlalchemy.exc import IntegrityError

from services import Api

api = Api()

movie_tag = Tag(
    name="Movie",
    description="Busca de filmes na base",
)

movie_bp = APIBlueprint("movie", __name__)


@movie_bp.get(
    "/movies",
    tags=[movie_tag],
    responses={
        "200": MovieSearchResponseSchema,
        "404": ErrorSchema,
    },
)
def search_movies(query: MovieSearchSchema):
    """Faz a busca por filmes na API."""
    logger.info(f"Buscando filmes ")
    # fazendo a busca
    movies = api.get_movies(dict(query))

    if movies["Response"] == "False":
        logger.error(f"Filme não encontrado")

        return movies, 404

    logger.info(f"Filme encontrado")
    return movies, 200


@movie_bp.get(
    "/movies/<string:imdb_id>",
    tags=[movie_tag],
    responses={
        "200": MovieViewSchema,
        "404": ErrorSchema,
    },
)
def search_movie(path: MovieByIdSchema):
    """Busca por um filme específico na API."""
    logger.info(f"Buscando filme ")

    imdb_id = path.imdb_id

    # fazendo a busca
    movie = api.get_movie_by_id(imdb_id)

    if movie["Response"] == "False":
        logger.error(f"Filme não encontrado")

        return movie, 404

    logger.info(f"Filme encontrado")
    return movie, 200
