
from database.ontology_manager import OntologyManager
from database.ontology_repository import OntologyRepository
from data.people import PEOPLE
from data.theme import THEMES
from data.languages import LANGUAGES
from data.countries import COUNTRIES



def populate_themes(repository):
    for theme in THEMES:

        create_entity(
            repository,
            "Theme",
            theme
        )


def populate_languages(repository):
    for language in LANGUAGES:

        create_entity(
            repository,
            "Language",
            language
        )


def populate_countries(repository):
    for country in COUNTRIES:

        create_entity(
            repository,
            "Country",
            country
        )


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


def create_entity(
    repository,
    class_name,
    entity_data
):
    """Cria um indivíduo e preenche automaticamente todas as Data Properties informadas."""

    entity_id = entity_data["id"]

    if repository.exists_individual(entity_id):
        return repository.get_individual_by_name(entity_id)

    entity = repository.create_individual(
        class_name,
        entity_id
    )

    for property_name, value in entity_data.items():

        if property_name == "id":
            continue

        repository.set_data_property(
            entity,
            property_name,
            value
        )

    return entity


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