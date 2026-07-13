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
from services.recommendation_service import RecommendationService


manager = OntologyManager("./ontology/movie_ontology.rdf")
repository = OntologyRepository(manager)
preference_service = PreferenceService(repository)
movie_service = MovieService(repository)
recommendation_service = RecommendationService(repository, manager)





common = [
    (5,1),
    (1,5)
]

print(
    recommendation_service._cosine_similarity(
        common
    )
)