from pydantic import BaseModel, Field
from typing import Optional, List


class MovieViewSchema(BaseModel):
    """Define como um filme será representado."""

    Title: str = "The Avengers"
    Year: int = "2012"
    Rated: str = "PG-13"
    Released: str = "04 May 2012"
    Runtime: str = "143 min"
    Genre: str = "Action, Adventure, Sci-Fi"
    Director: str = "Joss Whedon"
    Writer: str = (
        "Joss Whedon (screenplay), Zak Penn (story), Joss Whedon (story)"
    )
    Actors: str = "Robert Downey Jr., Chris Evans, Scarlett Johansson"
    Plot: str = (
        "Earth's mightiest heroes must come together and learn to"
        "fight as a team if they are going to stop the mischievous Loki and"
        "his alien army from enslaving humanity."
    )
    Language: str
    Country: str = "United States"
    Awards: str = "Nominated for 1 Oscar. 38 wins & 80 nominations total"
    Poster: str = (
        "https://m.media-amazon.com/images/M/"
        "MV5BNDYxNjQyMjAtNTdiOS00NGYwLWFmNTAtNThmY"
        "jU5ZGI2YTI1XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg"
    )
    Rated: str = "PG-13"
    Ratings: List[dict] = [
        {"Source": "Internet Movie Database", "Value": "8.0/10"},
        {"Source": "Rotten Tomatoes", "Value": "91%"},
        {"Source": "Metacritic", "Value": "69/100"},
    ]
    Metascore: str = "69"
    imdbRating: str = "8.0"
    imdbVotes: str = "1,285,614"
    imdbID: str = "tt0848228"
    Type: str = "movie"
    DVD: str = "22 Jun 2014"
    BoxOffice: str = "$623,279,547"
    Production: str = "N/A"
    Website: str = "N/A"
    Response: str = "True"


class MoviePreview(BaseModel):
    """Define como uma versão preview do filme será representado."""

    Title: str = "The Avengers"
    Year: int = "2012"
    imdbID: str = "tt0848228"
    Type: str = "movie"
    Poster: str = (
        "https://m.media-amazon.com/images/M/"
        "MV5BNDYxNjQyMjAtNTdiOS00NGYwLWFmNTAtNThmY"
        "jU5ZGI2YTI1XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg"
    )


class MovieSearchSchema(BaseModel):
    """Define como uma busca por um filme será representada."""

    s: str = Field(
        default="Avengers",
        description="Título do filme a ser pesquisado.",
    )
    tipo: Optional[str] = Field(
        description="Tipo de resultado a ser retornado. \
        Opções válidas: movie, show, episode",
    )
    y: Optional[str] = Field(
        description="Ano de lançamento. Exemplo: 2015",
    )
    page: Optional[str] = Field(
        description="Número da página a ser retornada. Opções válidas: 1-100",
    )
    callback: Optional[str] = Field(
        description="Nome do callback JSONP.",
    )


class MovieSearchResponseSchema(BaseModel):
    """Define como uma resposta de busca na API será representada."""

    Search: List[MoviePreview]
    totalResults: str
    Response: str
    Error: Optional[str]


class MovieByIdSchema(BaseModel):
    """Define como uma busca por um filme será representada."""

    imdb_id: str = Field(
        default="tt0848228",
        description="ID do filme a ser pesquisado.",
    )
