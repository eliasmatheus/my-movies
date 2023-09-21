from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from models import Base


class AddedMovie(Base):
    """Classe que representa a tabela auxiliar de filmes adicionados."""

    # O name da tabela no banco de dados
    __tablename__ = "added_movie"

    id = Column(Integer, primary_key=True)
    imdb_id = Column(String(12))
    created_at = Column(DateTime, default=datetime.now())

    watchlist_id = Column(
        Integer, ForeignKey("watchlist.id", ondelete="CASCADE")
    )
    watchlist = relationship(
        "Watchlist",
        foreign_keys="AddedMovie.watchlist_id",
        back_populates="movies",
    )

    # Criando um requisito de unicidade envolvendo uma par de informações
    __table_args__ = (
        UniqueConstraint(
            "imdb_id", "watchlist_id", name="added_movie_unique_id"
        ),
    )

    def __init__(self, imdb_id: str, created_at: Union[DateTime, None] = None):
        """Criar uma relação entre filmes e listas.

        Arguments:
            imdb_id: id do filme no imdb.
            watchlist_id: id da lista de filmes.
        """
        self.imdb_id = imdb_id

        if created_at:
            self.created_at = created_at

    def to_dict(self):
        """Retorna a representação em dicionário do Objeto Comentario."""
        return {
            "id": self.id,
            "imdb_id": self.imdb_id,
            "created_at": self.created_at,
            "watchlist_id": self.watchlist_id,
        }

    def __repr__(self):
        """Retorna uma representação do Produto em forma de texto."""
        return f"Added(id={self.id}, imdb_id='{self.imdb_id}',\
            created_at='{self.created_at}', watchlist_id='{self.watchlist_id}')"
