from database.ontology_manager import OntologyManager
from database.ontology_repository import OntologyRepository
from services.movie_services import MovieService


manager = OntologyManager("./ontology/movie_ontology.rdf")
repository = OntologyRepository(manager)
service = MovieService(repository)


movies = service.search_by_theme("Drama")

for movie in movies:
    print(movie.original_title)