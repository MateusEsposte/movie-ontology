from database.ontology_manager import OntologyManager
from database.ontology_repository import OntologyRepository
from services.user_service import UserService


manager = OntologyManager("./ontology/movie_ontology.rdf")
repository = OntologyRepository(manager)
service = UserService(repository, manager)

service.create_user(
    username="mateus",
    name="Mateus Esposte",
    email="mateus@email.com",
    age=24
)

print(service.exists("mateus"))