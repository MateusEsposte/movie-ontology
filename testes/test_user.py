from database.ontology_manager import OntologyManager
from database.ontology_repository import OntologyRepository
from services.rating_services import RatingService


manager = OntologyManager("./ontology/movie_ontology.rdf")
repository = OntologyRepository(manager)
service = RatingService(repository)


ratings = service.list_user_ratings("mateus")

for rating in ratings:
    print(
        rating.movie_title,
        rating.score
    )