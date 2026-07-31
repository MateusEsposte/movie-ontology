from models.user import User
from constants.ontology_constants import *
from models.movie import Movie

class UserService:
    def __init__(self, repository, manager):
        self.repository = repository
        self.manager = manager

    def create_user(self, username, full_name, email, age) -> User:

        self._validate_user( username, full_name, email, age)

        if self.exists(username):
            raise ValueError(
                "Já existe um usuário com esse username."
            )

        user = self.repository.create_individual(
            USER,
            username
        )

        self.repository.set_data_properties(
            user,
            {
                USERNAME: username,
                NAME: full_name,
                EMAIL: email,
                AGE: age
            }
        )

        return User(username=username, name=full_name, email=email, age=age)
    
    def get_user(self, username: str) -> User:
        if not self.exists(username):
            raise ValueError(
                "Usuário não encontrado."
            )

        individual = self.repository.get_individual_by_name(
            username
        )

        return User(
            username=individual.name,
            name=self.repository.get_data_property(
                individual,
                NAME
            ),
            email=self.repository.get_data_property(
                individual,
                EMAIL
            ),
            age=self.repository.get_data_property(
                individual,
                AGE
            )
        )
    
    def delete_user(self, username: str):
        if not self.exists(username):
            raise ValueError(
                "Usuário não encontrado."
            )

        self.repository.remove_individual(username)
    
    def exists(self, username: str) -> bool:
        if not username:
            return False

        return self.repository.exists_individual(username)
    
    def _validate_user(self, username: str, full_name: str, email: str, age: int):
        username = username.strip()
        full_name = full_name.strip()
        email = email.strip()

        if username == "":
            raise ValueError("Username não pode ser vazio.")

        if full_name == "":
            raise ValueError("Nome não pode ser vazio.")

        if "@" not in email:
            raise ValueError("E-mail inválido.")

        if age < 0:
            raise ValueError("Idade inválida.")
         
    def list_users(self) -> list[User]:
        users = []

        individuals = self.repository.get_individuals_by_class(USER)

        for individual in individuals:
            users.append(
                self.get_user(individual.name)
            )

        return users

    def watch_movie(
        self,
        username: str,
        movie_title: str
    ):

        user = self.repository.require_individual(
            username
        )

        movie = self.repository.require_individual(
            movie_title
        )

        watched = self.repository.get_object_property(
            user,
            WATCHED
        )

        if movie not in watched:

            self.repository.add_object_property(
                user,
                WATCHED,
                movie
            )

    def get_watched_movies(
        self,
        username: str
    ) -> list[Movie]:

        user = self.repository.require_individual(
            username
        )

        watched_movies = self.repository.get_object_property(
            user,
            WATCHED
        )

        movies = []

        for movie in watched_movies:

            movies.append(
                self._build_movie(
                    movie
                )
            )

        return movies

    def get_unwatched_movies(self, username: str):
        pass

    def unwatch_movie(self, username: str, movie_title: str):
        pass

    def _build_movie(
        self,
        movie_individual
    ):

        ontology_id = movie_individual.name

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
            ontology_id=ontology_id,
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















    