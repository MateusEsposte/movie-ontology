from models.user import User
from constants.ontology_constants import *
from models.movie import Movie

import hashlib
import hmac
import os

from constants.ontology_constants import PASSWORD_HASH

class UserService:
    def __init__(self, repository, manager):
        self.repository = repository
        self.manager = manager

    def create_user(
        self,
        username: str,
        full_name: str,
        email: str,
        age: int,
        password: str
    ) -> User:

        username = username.strip().lower()
        full_name = full_name.strip()
        email = email.strip().lower()

        self._validate_user(
            username,
            full_name,
            email,
            age
        )

        if not username:
            raise ValueError(
                "O nome de usuário é obrigatório."
            )

        if " " in username:
            raise ValueError(
                "O nome de usuário não pode conter espaços."
            )

        if len(password) < 6:
            raise ValueError(
                "A senha deve possuir pelo menos 6 caracteres."
            )

        if age <= 0:
            raise ValueError(
                "A idade deve ser maior que zero."
            )

        if self.repository.exists_individual(
            username
        ):
            raise ValueError(
                "Esse nome de usuário já está em uso."
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
                AGE: age,
                PASSWORD_HASH: self._hash_password(
                    password
                )
            }
        )

        return User(
            username=username,
            name=full_name,
            email=email,
            age=age
        )
    
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

    def rate_movie(
        self,
        username: str,
        movie_id: str,
        rating: int
    ):

        user = self.repository.require_individual(
            username
        )

        movie = self.repository.require_individual(
            movie_id
        )

        self.repository.add_or_update_rating(
            user,
            movie,
            rating
        )

        self.repository.save()

    def get_movie_rating(
        self,
        username: str,
        movie_id: str
    ):

        user = self.repository.require_individual(
            username
        )

        movie = self.repository.require_individual(
            movie_id
        )

        return self.repository.get_rating(
            user,
            movie
        )

    def list_friends(
        self,
        username: str
    ) -> list[User]:

        user = self.repository.require_individual(
            username
        )

        friend_individuals = (
            self.repository.get_object_property(
                user,
                FRIEND_OF
            )
        )

        friends = []

        for friend in friend_individuals:

            friends.append(
                self.get_user(
                    friend.name
                )
            )

        return friends

    def add_friend(
        self,
        username: str,
        friend_username: str
    ):

        if username == friend_username:
            raise ValueError(
                "Um usuário não pode adicionar a si mesmo."
            )

        user = self.repository.require_individual(
            username
        )

        friend = self.repository.require_individual(
            friend_username
        )

        user_friends = (
            self.repository.get_object_property(
                user,
                FRIEND_OF
            )
        )

        if friend in user_friends:
            raise ValueError(
                "Esse usuário já está na lista de amigos."
            )

        # Como friendOf não foi declarada simétrica,
        # criamos as duas relações explicitamente.
        self.repository.add_object_property(
            user,
            FRIEND_OF,
            friend
        )

        friend_friends = (
            self.repository.get_object_property(
                friend,
                FRIEND_OF
            )
        )

        if user not in friend_friends:

            self.repository.add_object_property(
                friend,
                FRIEND_OF,
                user
            )

        self.repository.save()

    def remove_friend(
        self,
        username: str,
        friend_username: str
    ):

        user = self.repository.require_individual(
            username
        )

        friend = self.repository.require_individual(
            friend_username
        )

        user_friends = (
            self.repository.get_object_property(
                user,
                FRIEND_OF
            )
        )

        if friend not in user_friends:
            raise ValueError(
                "Esse usuário não está na lista de amigos."
            )

        self.repository.remove_object_property(
            user,
            FRIEND_OF,
            friend
        )

        # Remove também a relação inversa criada
        # explicitamente pelo sistema.
        friend_friends = (
            self.repository.get_object_property(
                friend,
                FRIEND_OF
            )
        )

        if user in friend_friends:

            self.repository.remove_object_property(
                friend,
                FRIEND_OF,
                user
            )

        # remove_object_property não salva sozinho
        # no Repository atual.
        self.repository.save()

    def _hash_password(
        self,
        password: str
    ) -> str:

        salt = os.urandom(16)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100_000
        )

        return (
            f"{salt.hex()}:"
            f"{password_hash.hex()}"
        )

    def _verify_password(
        self,
        password: str,
        stored_password: str
    ) -> bool:

        try:
            salt_hex, hash_hex = (
                stored_password.split(":", 1)
            )

            salt = bytes.fromhex(
                salt_hex
            )

            expected_hash = bytes.fromhex(
                hash_hex
            )

        except (ValueError, AttributeError):
            return False

        received_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100_000
        )

        return hmac.compare_digest(
            received_hash,
            expected_hash
    )

    def authenticate(
        self,
        username: str,
        password: str
    ) -> User:

        username = username.strip()

        if not username or not password:
            raise ValueError(
                "Informe o usuário e a senha."
            )

        individual = (
            self.repository.get_individual_by_name(
                username
            )
        )

        if (
            individual is None
            or not self.repository.has_class(
                individual,
                "User"
            )
        ):
            raise ValueError(
                "Usuário ou senha inválidos."
            )

        stored_password = (
            self.repository.get_data_property(
                individual,
                PASSWORD_HASH
            )
        )

        if (
            stored_password is None
            or not self._verify_password(
                password,
                stored_password
            )
        ):
            raise ValueError(
                "Usuário ou senha inválidos."
            )

        return self.get_user(
            username
        )







    