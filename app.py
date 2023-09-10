from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect


from schemas import *
from flask_cors import CORS

from routes import watchlist_bp, movie_bp

info = Info(title="My Movies API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)
watchlist_tag = Tag(
    name="Produto",
    description="Adição, visualização e remoção de listas à base",
)


@app.get("/", tags=[home_tag])
def home():
    """Redireciona para /openapi.

    Esta tela permite a escolha do estilo de documentação
    """
    return redirect("/openapi")


# Registra rotas
app.register_api(watchlist_bp)
app.register_api(movie_bp)
