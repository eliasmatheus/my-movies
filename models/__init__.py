from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
import os

# importando os elementos definidos no modelo
from models.base import Base
from models.added_movie import AddedMovie
from models.watchlist import Watchlist


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Ativa o suporte a foreign keys no sqlite3."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
    # então cria o diretorio
    os.makedirs(db_path)
# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = "sqlite:///%s/db.sqlite3" % db_path

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# cria o banco se ele não existir
if not database_exists(engine.url):
    create_database(engine.url)

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)
