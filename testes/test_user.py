from database.ontology_manager import OntologyManager
from database.ontology_repository import OntologyRepository
from services.movie_services import MovieService


manager = OntologyManager("./ontology/movie_ontology.rdf")
repository = OntologyRepository(manager)
service = MovieService(repository)


print(service.exists("Gran Torino"))