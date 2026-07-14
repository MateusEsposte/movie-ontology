from database.ontology_repository import OntologyRepository
from database.ontology_manager import OntologyManager

from services.user_service import UserService
from services.movie_services import MovieService
from services.rating_services import RatingService
from services.preference_services import PreferenceService
from constants.ontology_constants import *

from models.movie import Movie
from models.preference import Preference
from models.rating import Rating

import math


class RecommendationService:
    def __init__(self, repository: OntologyRepository, manager: OntologyManager):
        self.repository = repository
        self.user_service = UserService(repository, manager)
        self.movie_service = MovieService(repository)
        self.rating_service = RatingService(repository)
        self.preference_service = PreferenceService(repository)

    def _get_watched_movies(self, username: str) -> set[str]:
        ratings = self.rating_service.list_user_ratings(username)
        watched = set()

        for rating in ratings:
            watched.add(rating.movie_title)

        return watched

    def _get_unwatched_movies(self, username: str) -> list[Movie]:
        watched = self._get_watched_movies(username)
        unwatched = []

        for movie in self.movie_service.list_movies():
            if movie.original_title not in watched:
                unwatched.append(movie)

        return unwatched

    def _get_user_preferences(self, username: str) -> list[Preference]:
        return self.preference_service.list_user_preferences(
            username
        )

    def _get_user_ratings(self, username: str) -> list[Rating]:
        return self.rating_service.list_user_ratings(
            username
        )

    def _get_user_friends(
        self,
        username: str
    ):

        user = self.repository.require_individual(
            username
        )

        friends = []

        for friend in self.repository.get_object_property(
            user,
            FRIEND_OF
        ):

            friends.append(
                self.user_service.get_user(
                    friend.name
                )
            )

        return friends

    def _get_all_users(self):
        return self.user_service.list_users()

    def _calculate_preference_score(
        self,
        movie: Movie,
        preferences: list[Preference]
    ) -> int:

        score = 0
        for preference in preferences:
            print(
                preference.preference_type,
                preference.preferred_element,
                preference.interest_level
            )

            if (
                preference.preference_type == "Theme"
                and preference.preferred_element == movie.theme
            ):
                score += preference.interest_level

            elif (
                preference.preference_type == "Actor"
                and preference.preferred_element in movie.actors
            ):
                score += preference.interest_level

            elif (
                preference.preference_type == "Director"
                and preference.preferred_element == movie.director
            ):
                score += preference.interest_level

            elif (
                preference.preference_type == "CinematicWork"
                and preference.preferred_element == movie.original_title
            ):
                score += preference.interest_level

        return score

    def recommend_by_preferences(
        self,
        username: str
    ) -> list[tuple[Movie, int]]:

        preferences = self._get_user_preferences(
            username
        )

        movies = self._get_unwatched_movies(
            username
        )

        scored_movies = []

        for movie in movies:

            score = self._calculate_preference_score(
                movie,
                preferences
            )

            if score > 0:

                scored_movies.append(
                    (movie, score)
                )

        scored_movies.sort(
            key=lambda item: item[1],
            reverse=True
        )

        return scored_movies

    def _common_ratings(
        self,
        username1: str,
        username2: str
    ):

        ratings1 = self.rating_service.list_user_ratings(
            username1
        )

        ratings2 = self.rating_service.list_user_ratings(
            username2
        )

        movies2 = {}

        for rating in ratings2:

            movies2[
                rating.movie_title
            ] = rating.score

        common = []

        for rating in ratings1:

            if rating.movie_title in movies2:

                common.append(
                    (
                        rating.score,
                        movies2[
                            rating.movie_title
                        ]
                    )
                )

        return common

    def _cosine_similarity(self, common_ratings: list[tuple[int, int]]) -> float:
        if not common_ratings:
            return 0.0

        numerator = 0
        sum_user1 = 0
        sum_user2 = 0

        for rating1, rating2 in common_ratings:
            numerator += rating1 * rating2
            sum_user1 += rating1 ** 2
            sum_user2 += rating2 ** 2

        denominator = (math.sqrt(sum_user1) * math.sqrt(sum_user2))

        if denominator == 0:
            return 0.0

        return numerator / denominator

    def _get_similar_users(
        self,
        username: str,
        candidates
    ):

        similarities = []

        for candidate in candidates:

            if candidate.username == username:
                continue

            common = self._common_ratings(
                username,
                candidate.username
            )

            similarity = self._cosine_similarity(
                common
            )

            if similarity > 0:

                similarities.append(
                    (
                        candidate,
                        similarity
                    )
                )

        similarities.sort(
            key=lambda item: item[1],
            reverse=True
        )

        return similarities

    def _generate_collaborative_recommendations(
        self,
        username: str,
        similar_users
    ) -> list[tuple[Movie, float]]:

        watched_movies = self._get_watched_movies(
            username
        )

        movie_scores = {}

        for user, similarity in similar_users:

            ratings = self.rating_service.list_user_ratings(
                user.username
            )

            for rating in ratings:

                if rating.movie_title in watched_movies:
                    continue

                if rating.movie_title not in movie_scores:

                    movie_scores[
                        rating.movie_title
                    ] = 0

                movie_scores[
                    rating.movie_title
                ] += rating.score * similarity

        recommendations = []

        for movie_title, score in movie_scores.items():

            movie = self.movie_service.get_movie(
                movie_title
            )

            recommendations.append(
                (
                    movie,
                    score
                )
            )

        recommendations.sort(

            key=lambda item: item[1],

            reverse=True
        )

        return recommendations

    def recommend_by_friends(
        self,
        username: str
    ):

        friends = self._get_user_friends(
            username
        )

        similar_users = self._get_similar_users(
            username,
            friends
        )

        return self._generate_collaborative_recommendations(
            username,
            similar_users
        )

    def recommend_by_community(
        self,
        username: str
    ):

        users = self._get_all_users()

        similar_users = self._get_similar_users(
            username,
            users
        )

        return self._generate_collaborative_recommendations(
            username,
            similar_users
        )

