from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from models import Base, AddedMovie


class Watchlist(Base):
    """Classe que representa a tabela watchlist no banco de dados."""

    # O name da tabela no banco de dados
    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True)
    name = Column(String(140), unique=True)
    description = Column(String(2000))

    # A data de inserção será o instante de inserção caso não tenha
    # um valor definido pelo usuário
    created_at = Column(DateTime, default=datetime.now())

    movies = relationship(
        "AddedMovie",
        back_populates="watchlist",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __init__(
        self,
        name,
        description,
        id: int = None,
        created_at: Union[DateTime, None] = None,
    ):
        """
        Cria uma lista de filmes.

        Arguments:
            name: name da lista.
            description (optional): descrição da lista.
            created_at (optional): data da criação da lista.
        """
        if id:
            self.id = id

        self.name = name
        self.description = description

        # se não for informada, será o data exata da inserção no banco
        if created_at:
            self.created_at = created_at

    def to_dict(self):
        """Retorna a representação em dicionário do Objeto Watchlist."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "movies": [m.to_dict() for m in self.movies],
        }

    def __repr__(self):
        """Retorna uma representação do Produto em forma de texto."""
        return f"Watchlist(id={self.id}, name='{self.name}',\
            description='{self.description}', created_at='{self.created_at}')"

    def add_movie(self, movie: AddedMovie):
        """Adiciona um novo filme à lista."""
        self.movies.append(movie)

    def remove_movie(self, movie: AddedMovie):
        """Remove um filme da lista."""
        self.movies.remove(movie)
