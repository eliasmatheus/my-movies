from flask_openapi3 import Tag, APIBlueprint

from schemas import *
from schemas import ErrorSchema

from logger import logger
from models import Session, Watchlist, AddedMovie
from sqlalchemy.exc import IntegrityError

watchlist_tag = Tag(
    name="Watchlist",
    description="Adição, edição, visualização e remoção de listas à base",
)

watchlist_bp = APIBlueprint("watchlist", __name__)


@watchlist_bp.post(
    "/watchlist",
    tags=[watchlist_tag],
    responses={
        "200": WatchlistViewSchema,
        "409": ErrorSchema,
        "400": ErrorSchema,
    },
)
def add_watchlist(form: WatchlistSchema):
    """Adiciona uma nova lista de filmes à base.

    Retorna uma representação das listas e filmes associados.
    """
    watchlist = Watchlist(
        name=form.name,
        description=form.description,
    )
    logger.info(f"Adicionando nova lista de name: '{watchlist.name}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando watchlist
        session.add(watchlist)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.info("Adicionado lista: %s" % watchlist)
        return render_watchlist(watchlist), 200

    except IntegrityError as e:
        # como a duplicidade do name é a provável razão do IntegrityError
        error_msg = "Lista de mesmo name já salva na base :/"
        logger.warning(
            f"Erro ao adicionar lista '{watchlist.name}', {error_msg}"
        )
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar nova lista :/"
        logger.warning(
            f"Erro ao adicionar lista '{watchlist.name}', {error_msg}"
        )
        return {"message": error_msg}, 400


@watchlist_bp.get(
    "/watchlist",
    tags=[watchlist_tag],
    responses={"200": WatchlistListSchema, "404": ErrorSchema},
)
def get_watchlists():
    """Faz a busca por todas as listas de filmes cadastradas.

    Retorna uma representação das listas de filmes cadastradas.
    """
    logger.info(f"Coletando listas de filmes cadastradas")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    watchlists = session.query(Watchlist).all()

    if not watchlists:
        # se não há watchlists cadastradas
        return {"watchlist": []}, 200
    else:
        logger.info(f"%d watchlist econtrados" % len(watchlists))
        # retorna a representação das listas
        return render_watchlists(watchlists), 200


@watchlist_bp.get(
    "/watchlist/<int:id>",
    tags=[watchlist_tag],
    responses={"200": WatchlistDetailsSchema, "404": ErrorSchema},
)
def get_watchlist(path: WatchlistByIDSchema):
    """Busca uma lista específica à partir do id.

    Retorna uma representação da lista.
    """
    watchlist_id = path.id

    logger.debug(f"Coletando lista com ID: {watchlist_id} ")

    # criando conexão com a base
    session = Session()

    # fazendo a busca
    watchlist = (
        session.query(Watchlist)
        .filter(Watchlist.id == watchlist_id)
        .one_or_none()
    )

    if not watchlist:
        # se a lista não foi encontrado
        error_msg = "Lista não encontrada na base :/"
        log_error_msg = (
            f"Erro ao buscar lista com ID: #'{watchlist_id}', {error_msg}"
        )

        logger.warning(log_error_msg)
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Lista com ID: #{watchlist_id} encontrado com sucesso")
        # retorna a representação da lista
        return render_watchlist(watchlist), 200


@watchlist_bp.put(
    "/watchlist",
    tags=[watchlist_tag],
    responses={
        "200": WatchlistViewSchema,
        "409": ErrorSchema,
        "400": ErrorSchema,
    },
)
def put_watchlist(form: WatchlistUpdateSchema):
    """Edita uma lista já existente na base de dados.

    Retorna uma representação da lista.
    """
    watchlist = Watchlist(**form.dict())

    # criando conexão com a base
    session = Session()

    # fazendo a busca
    watchlist_id = form.id

    old_watchlist = (
        session.query(Watchlist).filter(Watchlist.id == watchlist_id).first()
    )

    logger.debug(f"Editando lista de ID: '{old_watchlist.id}'")

    try:
        # edita os valores do lista
        old_watchlist.name = watchlist.name
        old_watchlist.description = watchlist.description

        # efetivando o comando de edição do lista na tabela
        session.commit()
        logger.debug(f"Editado lista de ID: '{watchlist.name}'")

        # fazendo a busca
        watchlist = (
            session.query(Watchlist)
            .filter(Watchlist.id == watchlist_id)
            .one_or_none()
        )

        return render_watchlist(watchlist), 200

    except IntegrityError as e:
        # como a duplicidade do título é a provável razão do IntegrityError
        error_msg = "Artigo de mesmo título já salvo na base :/"
        log_error_msg = (
            f"Erro ao adicionar lista '{watchlist.name}', {error_msg}"
        )
        logger.warning(log_error_msg)

        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo lista :/"
        log_error_msg = (
            f"Erro ao adicionar lista '{watchlist.name}', {error_msg}"
        )
        logger.warning(log_error_msg)

        return {"message": error_msg}, 400


@watchlist_bp.delete(
    "/watchlist/<int:id>",
    tags=[watchlist_tag],
    responses={"200": WatchlistDeleteSchema, "404": ErrorSchema},
)
def delete_watchlist(path: WatchlistByIDSchema):
    """Remove uma lista à partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    watchlist_id = path.id

    logger.debug(f"Removendo lista com ID: #{watchlist_id}")

    # criando conexão com a base
    session = Session()

    # fazendo a remoção
    count = (
        session.query(Watchlist).filter(Watchlist.id == watchlist_id).delete()
    )

    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Lista com ID: #{watchlist_id} excluída com sucesso")
        return {"message": "Lista removida", "id": watchlist_id}
    else:
        # se o lista não foi encontrado
        error_msg = "Lista não encontrada na base :/"
        log_error_msg = (
            f"Erro ao remover lista com ID: '{watchlist_id}', {error_msg}"
        )
        logger.warning(log_error_msg)

        return {"message": error_msg}, 404


@watchlist_bp.post(
    "/watchlist/movie",
    tags=[watchlist_tag],
    responses={
        "200": WatchlistDetailsSchema,
        "409": ErrorSchema,
        "400": ErrorSchema,
    },
)
def add_movie_to_watchlists(form: WatchlistAddMovieSchema):
    """Adiciona um novo filme à lista.

    Retorna uma representação da lista e seus filmes.
    """
    watchlist_ids = form.watchlist_ids

    # criando conexão com a base
    session = Session()

    # fazendo a busca pelas listas
    watchlists = (
        session.query(Watchlist).filter(Watchlist.id.in_(watchlist_ids)).all()
    )

    if not watchlists:
        # se a lista não foi encontrado
        error_msg = "Lista não encontrada na base :/"
        log_error_msg = f"Erro ao buscar lista com IDS, {error_msg}"
        logger.warning(log_error_msg)
        return {"message": error_msg}, 404

    logger.info(f"Adicionando filme às listas")

    try:
        # adicionando filme às listas
        for watchlist in watchlists:
            # checando se o filme já foi adicionado à lista
            for movie in watchlist.movies:
                if movie.imdb_id == form.imdb_id:
                    error_msg = "Filme já adicionado à lista :/"
                    logger.warning(
                        f"Erro ao adicionar lista '{watchlist.name}', {error_msg}"
                    )

                    break

            else:
                # criando filme
                movie = AddedMovie(form.imdb_id)
                watchlist.add_movie(movie)

                # efetivando o comando de adição de novo item na tabela
                session.commit()

        logger.info(f"Adicionado filme às listas")

        # retorna a representação da lista
        return render_watchlists(watchlists), 200

    except IntegrityError as e:
        # como a duplicidade do name é a provável razão do IntegrityError
        error_msg2 = "Filme já adicionado à lista :/"
        logger.warning(
            f"Erro ao adicionar lista '{watchlist.name}', {error_msg2}"
        )
        return {"message": error_msg2}, 409


@watchlist_bp.get(
    "/watchlist/movie/<string:imdb_id>",
    tags=[watchlist_tag],
    responses={
        "200": WatchlistDetailsSchema,
        "409": ErrorSchema,
        "400": ErrorSchema,
    },
)
def get_movie_watchlists(path: MovieWatchlistGetSchema):
    """Busca pelas listas que um filme pertence.

    Retorna uma representação da lista e seus filmes.
    """
    imdb_id = path.imdb_id

    # Criando conexão com a base de dados
    session = Session()

    # Buscando todas as vezes que o filme foi adicionado à lista
    movies = (
        session.query(AddedMovie).filter(AddedMovie.imdb_id == imdb_id).all()
    )

    if not movies:
        # Se o filme não foi encontrado
        # retorna a representação da lista
        render_movie_watchlists(imdb_id, []), 204

    watchlists = []

    for movie in movies:
        watchlists.append(movie.watchlist)

    # retorna a representação da lista
    return render_movie_watchlists(imdb_id, watchlists), 200


@watchlist_bp.delete(
    "/watchlist/<int:watchlist_id>/movie/<string:imdb_id>",
    tags=[watchlist_tag],
    responses={
        "200": WatchlistDetailsSchema,
        "409": ErrorSchema,
        "400": ErrorSchema,
    },
)
def remove_movie_from_watchlist(path: WatchlistRemoveMovieSchema):
    """Remove um filme da lista.

    Retorna uma representação da lista e seus filmes.
    """
    watchlist_id = path.watchlist_id
    imdb_id = path.imdb_id

    # Criando conexão com a base de dados
    session = Session()

    # Buscando a lista de reprodução pelo ID
    watchlist = (
        session.query(Watchlist)
        .filter(Watchlist.id == watchlist_id)
        .one_or_none()
    )

    if not watchlist:
        # Se a lista de reprodução não foi encontrada
        error_msg = "Lista não encontrada na base :/"
        log_error_msg = (
            f"Erro ao buscar lista com ID: '{watchlist_id}', {error_msg}"
        )
        logger.warning(log_error_msg)
        return {"message": error_msg}, 404

    logger.info(f"Removendo filme da lista #{watchlist_id}")

    movie_query = session.query(AddedMovie).filter(
        AddedMovie.imdb_id == imdb_id
        and AddedMovie.watchlist_id == watchlist_id
    )

    movie = movie_query.one_or_none()

    if not movie:
        # Se o filme não foi encontrado
        error_msg = "Filme não encontrado na lista :/"
        log_error_msg = (
            f"Erro ao buscar filme com ID: '{imdb_id}', {error_msg}"
        )
        logger.warning(log_error_msg)
        return {"message": error_msg}, 404

    # Removendo o filme da lista
    movie_query.delete()
    session.commit()

    logger.info(f"Removido filme da lista #{watchlist_id}")

    # retorna a representação da lista
    return render_watchlist(watchlist), 200
