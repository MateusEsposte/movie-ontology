from database.ontology_manager import OntologyManager
from database.ontology_repository import OntologyRepository
from services.user_service import UserService


manager = OntologyManager("./ontology/movie_ontology.rdf")
repository = OntologyRepository(manager)
service = UserService(repository, manager)

users = service.list_users()

for user in users:
    print(user)