from database.ontology_repository import OntologyRepository
from models.movie import Movie
from constants.ontology_constants import *


class MovieService:
    def __init__(self, repository: OntologyRepository):
        self.repository = repository

    def exists(self, original_title: str) -> bool:
        """
        Verifica se um filme existe.
        """
        return self.repository.exists_individual(original_title)
    
    def _validate_movie(
        self,
        original_title,
        portuguese_title,
        release_date,
        duration_minutes,
        age_rating,
        country,
        languages,
        theme,
        director,
        actors
    ):

        if original_title.strip() == "":
            raise ValueError("Título original inválido.")

        if portuguese_title.strip() == "":
            raise ValueError("Título em português inválido.")

        if duration_minutes <= 0:
            raise ValueError("Duração inválida.")

        if len(languages) == 0:
            raise ValueError("O filme deve possuir pelo menos um idioma.")

        if len(actors) == 0:
            raise ValueError("O filme deve possuir pelo menos um ator.")