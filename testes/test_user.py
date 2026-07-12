from database.ontology_manager import OntologyManager
from database.ontology_repository import OntologyRepository
from services.preference_services import PreferenceService


manager = OntologyManager("./ontology/movie_ontology.rdf")
repository = OntologyRepository(manager)
service = PreferenceService(repository)


service.delete_preference(
    "preference_001"
)

print(
    service.exists(
        "preference_001"
    )
)