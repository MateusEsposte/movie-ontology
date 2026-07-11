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
        
    def _link_director(self, movie, director_name: str):
        director = self.repository.require_individual(director_name)

        self.repository.add_object_property(
            movie,
            HAS_DIRECTOR,
            director
        )
    
    def _link_actors(self, movie, actors: list[str]):
        for actor_name in actors:

            actor = self.repository.require_individual(actor_name)

            self.repository.add_object_property(
                movie,
                HAS_ACTOR,
                actor
            )

    def _link_theme(self, movie, theme_name: str):
        theme = self.repository.require_individual(theme_name)

        self.repository.add_object_property(
            movie,
            HAS_THEME,
            theme
        )

    def _link_country(self, movie, country_name: str):
        country = self.repository.require_individual(country_name)

        self.repository.add_object_property(
            movie,
            HAS_COUNTRY_OF_ORIGIN,
            country
        )

    def _link_languages(self, movie, languages: list[str]):
        for language_name in languages:
            language = self.repository.require_individual(language_name)

            self.repository.add_object_property(
                movie,
                DUBBED_IN,
                language
            )

    def create_movie(
        self,
        original_title: str,
        portuguese_title: str,
        release_date: str,
        duration_minutes: int,
        age_rating: str,
        country: str,
        languages: list[str],
        theme: str,
        director: str,
        actors: list[str]
    ) -> Movie:
        
        self._validate_movie(
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
        )

        if self.exists(original_title):
            raise ValueError(
                "Já existe um filme com esse título."
            )

        movie_id = (
            original_title
                .lower()
                .replace(" ", "_")
        )

        movie = self.repository.create_individual(FILM, movie_id)

        self.repository.set_data_properties(
            movie,
            {
                ORIGINAL: original_title,
                PORTUGUESE: portuguese_title,
                RELEASE: release_date,
                DURATION_MINUTES: duration_minutes,
                AGE_RATING: age_rating
            }
        )

        self._link_director(movie, director)
        self._link_actors(movie, actors)
        self._link_theme(movie, theme)
        self._link_country(movie, country)
        self._link_languages(movie, languages)

        return Movie(
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
        )

    def _build_movie(self, movie_individual):

        original_title = self.repository.get_data_property(
            movie_individual,
            ORIGINAL
        )

        portuguese_title = self.repository.get_data_property(
            movie_individual,
            PORTUGUESE
        )

        release_date = self.repository.get_data_property(
            movie_individual,
            RELEASE
        )

        duration_minutes = self.repository.get_data_property(
            movie_individual,
            DURATION_MINUTES
        )

        age_rating = self.repository.get_data_property(
            movie_individual,
            AGE_RATING
        )


        directors = self.repository.get_object_property(
            movie_individual,
            HAS_DIRECTOR
        )

        director = None
        if directors:
            director = self.repository.get_data_property(
                directors[0],
                NAME
            )


        actors = self.repository.get_object_property(
            movie_individual,
            HAS_ACTOR
        )

        actor_names = []

        for actor in actors:
            actor_names.append(
                self.repository.get_data_property(
                    actor,
                    NAME
                )
            )


        themes = self.repository.get_object_property(
            movie_individual,
            HAS_THEME
        )

        theme = None
        if themes:
            theme = self.repository.get_data_property(
                themes[0],
                THEME_NAME
            )


        countries = self.repository.get_object_property(
            movie_individual,
            HAS_COUNTRY_OF_ORIGIN
        )

        country = None
        if countries:
            country = self.repository.get_data_property(
                countries[0],
                COUNTRY_NAME
            )


        languages = self.repository.get_object_property(
            movie_individual,
            DUBBED_IN
        )

        language_names = []

        for language in languages:
            language_names.append(
                self.repository.get_data_property(
                    language,
                    LANGUAGE_NAME
                )
            )


        return Movie(
            original_title=original_title,
            portuguese_title=portuguese_title,
            release_date=release_date,
            duration_minutes=duration_minutes,
            age_rating=age_rating,
            country=country,
            languages=language_names,
            theme=theme,
            director=director,
            actors=actor_names
        )

    def get_movie(self, original_title: str) -> Movie:
        movie_id = (
            FILM_PREFIX +
            original_title
                .strip()
                .lower()
                .replace(" ", "_")
        )

        movie_individual = self.repository.require_individual(
            movie_id
        )

        return self._build_movie(movie_individual)

    def list_movies(self) -> list[Movie]:

        movies = []

        movie_individuals = self.repository.get_individuals_by_class(
            FILM
        )

        for movie_individual in movie_individuals:
            movies.append(
                self._build_movie(movie_individual)
            )

        return movies

    def delete_movie(self, original_title: str):

        movie_id = (
            FILM_PREFIX +
            original_title
                .strip()
                .lower()
                .replace(" ", "_")
        )

        movie = self.repository.require_individual(
            movie_id
        )

        self.repository.remove_individual(movie)

    def search_by_actor(self, actor_name: str) -> list[Movie]:
        movies = self.list_movies()

        result = []

        for movie in movies:
            if actor_name in movie.actors:
                result.append(movie)

        return result

    def search_by_director(self, director_name: str) -> list[Movie]:

        movies = self.list_movies()

        result = []

        for movie in movies:
            if movie.director == director_name:
                result.append(movie)

        return result

    def search_by_theme(self, theme_name: str) -> list[Movie]:

        movies = self.list_movies()

        result = []

        for movie in movies:
            if movie.theme == theme_name:
                result.append(movie)

        return result

    def search_by_country(self, country_name: str) -> list[Movie]:

        movies = self.list_movies()

        result = []

        for movie in movies:
            if movie.country == country_name:
                result.append(movie)

        return result

    def search_by_language(self, language_name: str) -> list[Movie]:

        movies = self.list_movies()

        result = []

        for movie in movies:
            if language_name in movie.languages:
                result.append(movie)

        return result
