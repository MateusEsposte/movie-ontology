
from database.ontology_manager import OntologyManager
from database.ontology_repository import OntologyRepository
from data.people import PEOPLE


def populate_themes(repository):
    pass


def populate_languages(repository):
    pass


def populate_countries(repository):
    pass


def populate_people(repository):
    for person_data in PEOPLE:
        # Evita criar indivíduos duplicados
        if repository.exists_individual(person_data["id"]):
            print(f"  - {person_data['name']} já existe.")
            continue

        # Cria o indivíduo como Person
        person = repository.create_individual(
            "Person",
            person_data["id"]
        )

        # Data Properties
        repository.set_data_property(person, "fullName", person_data["name"])
        repository.set_data_property(person, "birthDate", person_data["birth_date"])
        repository.set_data_property(person, "nationality", person_data["nationality"])

        # Papéis
        for role in person_data["roles"]:
            repository.add_class(person, role)


def populate_movies(repository):
    pass


def populate_users(repository):
    pass


def populate_preferences(repository):
    pass


def populate_ratings(repository):
    pass


def main():
    manager = OntologyManager("ontology/movie_ontology.rdf")
    manager.load()

    repository = OntologyRepository(manager)

    populate_themes(repository)
    populate_languages(repository)
    populate_countries(repository)
    populate_people(repository)
    populate_movies(repository)
    populate_users(repository)
    populate_preferences(repository)
    populate_ratings(repository)

    manager.save()

if __name__ == "__main__":
    main()