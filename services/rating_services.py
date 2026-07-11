from database.ontology_repository import OntologyRepository
from models.rating import Rating
from services.movie_services import MovieService
from constants.ontology_constants import *


class RatingService:
    def __init__(self, repository: OntologyRepository):
        self.repository = repository

    def _next_rating_id(self) -> str:
        ratings = self.repository.get_individuals_by_class(
            RATING
        )

        highest = 0

        for rating in ratings:
            try:
                number = int(
                    rating.name.replace("rating_", "")
                )

                if number > highest:
                    highest = number

            except ValueError:
                continue

        return f"rating_{highest + 1:03d}"

    def exists(self, rating_id: str) -> bool:
        return self.repository.exists_individual(
            rating_id
        )

    def _build_rating(self, rating_individual):
        rating_id = rating_individual.name

        score = self.repository.get_data_property(
            rating_individual,
            SCORE
        )

        rating_date = self.repository.get_data_property(
            rating_individual,
            RATING_DATE
        )

        users = self.repository.get_object_property(
            rating_individual,
            RATING_OF
        )

        username = None

        if users:
            username = self.repository.get_data_property(
                users[0],
                USERNAME
            )

        movies = self.repository.get_object_property(
            rating_individual,
            RATING_ABOUT
        )

        movie_title = None

        if movies:
            movie_title = self.repository.get_data_property(
                movies[0],
                ORIGINAL
            )

        return Rating(
            rating_id=rating_id,
            username=username,
            movie_title=movie_title,
            score=score,
            rating_date=rating_date
        )

    def get_rating(self, rating_id: str) -> Rating:
        rating = self.repository.require_individual(
            rating_id
        )

        return self._build_rating(rating)

    def list_ratings(self) -> list[Rating]:
        ratings = []

        individuals = self.repository.get_individuals_by_class(
            RATING
        )

        for individual in individuals:
            ratings.append(
                self._build_rating(individual)
            )

        return ratings

    def create_rating(
        self,
        username: str,
        movie_title: str,
        score: float,
        rating_date: str
    ):

        user = self.repository.require_individual(username)

        movie_id = (
            FILM_PREFIX +
            movie_title.strip().lower().replace(" ", "_")
        )

        movie = self.repository.require_individual(movie_id)

        rating = self.repository.create_individual(
            RATING,
            self._next_rating_id()
        )

        self.repository.set_data_property(
            rating,
            SCORE,
            score
        )

        self.repository.set_data_property(
            rating,
            RATING_DATE,
            rating_date
        )

        self.repository.add_object_property(
            user,
            HAS_RATING,
            rating
        )

        self.repository.add_object_property(
            rating,
            RATING_ABOUT,
            movie
        )

        return self._build_rating(rating)

    def update_rating(
        self,
        rating_id: str,
        score: float,
        rating_date: str
    ):

        rating = self.repository.require_individual(
            rating_id
        )

        self.repository.set_data_property(
            rating,
            SCORE,
            score
        )

        self.repository.set_data_property(
            rating,
            RATING_DATE,
            rating_date
        )

        return self._build_rating(rating)

    def delete_rating(
        self,
        rating_id: str
    ):

        rating = self.repository.require_individual(
            rating_id
        )

        self.repository.remove_individual(
            rating
        )

    def list_user_ratings(
        self,
        username: str
    ) -> list[Rating]:

        ratings = []

        user = self.repository.require_individual(
            username
        )

        user_ratings = self.repository.get_object_property(
            user,
            HAS_RATING
        )

        for rating in user_ratings:
            ratings.append(
                self._build_rating(rating)
            )

        return ratings

    def list_movie_ratings(
        self,
        movie_title: str
    ) -> list[Rating]:

        ratings = []

        for rating in self.list_ratings():

            if rating.movie_title == movie_title:
                ratings.append(rating)

        return ratings

    def update_rating(
        self,
        rating_id: str,
        score: float,
        rating_date: str
    ) -> Rating:

        rating = self.repository.require_individual(
            rating_id
        )

        self.repository.set_data_property(
            rating,
            SCORE,
            score
        )

        self.repository.set_data_property(
            rating,
            RATING_DATE,
            rating_date
        )

        return self._build_rating(rating)
    
    def delete_rating(
        self,
        rating_id: str
    ):

        rating = self.repository.require_individual(
            rating_id
        )

        self.repository.remove_individual(
            rating
        )

    def list_user_ratings(
        self,
        username: str
    ) -> list[Rating]:

        user = self.repository.require_individual(
            username
        )

        ratings = []

        for rating in self.repository.get_object_property(
            user,
            HAS_RATING
        ):

            ratings.append(
                self._build_rating(rating)
            )

        return ratings

    def list_movie_ratings(
        self,
        movie_title: str
    ) -> list[Rating]:

        ratings = []

        for rating in self.list_ratings():

            if rating.movie_title == movie_title:
                ratings.append(rating)

        return ratings

    def calculate_average(
        self,
        movie_title: str
    ) -> float:

        ratings = self.list_movie_ratings(
            movie_title
        )

        if not ratings:
            return 0.0

        total = 0

        for rating in ratings:
            total += rating.score

        return total / len(ratings)

    def top_rated_movies(self):

        movie_service = MovieService(
            self.repository
        )

        movies = movie_service.list_movies()

        ranking = []

        for movie in movies:

            average = self.calculate_average(
                movie.original_title
            )

            ranking.append(
                (
                    movie,
                    average
                )
            )

        ranking.sort(
            key=lambda item: item[1],
            reverse=True
        )

        return ranking







