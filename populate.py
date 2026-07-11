
from database.ontology_manager import OntologyManager
from database.ontology_repository import OntologyRepository
from data.people import DATA_PEOPLE
from data.theme import DATA_THEMES
from data.languages import DATA_LANGUAGES
from data.countries import DATA_COUNTRIES
from data.movies import DATA_MOVIES
from data.users import DATA_USERS
from constants.ontology_constants import *

def populate_themes(repository):
    for theme in DATA_THEMES:
        create_entity(
            repository,
            THEME,
            theme
        )


def populate_languages(repository):
    for language in DATA_LANGUAGES:
        create_entity(
            repository,
            LANGUAGE,
            language
        )


def populate_countries(repository):
    for country in DATA_COUNTRIES:
        create_entity(
            repository,
            COUNTRY,
            country
        )


def populate_people(repository):
    for person_data in DATA_PEOPLE:
        if repository.exists_individual(person_data["id"]):
            print(f"  - {person_data['name']} já existe.")
            continue

        person = repository.create_individual(
            PERSON,
            person_data["id"]
        )

        repository.set_data_property(person, "fullName", person_data["name"])
        repository.set_data_property(person, "birthDate", person_data["birth_date"])
        repository.set_data_property(person, "nationality", person_data["nationality"])

        for role in person_data["roles"]:
            repository.add_class(person, role)


def populate_movies(repository):
    for movie_data in DATA_MOVIES:
        # Evita criar o mesmo filme novamente
        if repository.exists_individual(movie_data["id"]):
            print(f'  - {movie_data["originalTitle"]} já existe.')
            continue

        # Cria o indivíduo Film
        movie = repository.create_individual(
            FILM,
            movie_data["id"]
        )

        # -----------------------------
        # Data Properties
        # -----------------------------
        repository.set_data_property(
            movie,
            ORIGINAL,
            movie_data["originalTitle"]
        )

        repository.set_data_property(
            movie,
            PORTUGUESE,
            movie_data["portugueseTitle"]
        )

        repository.set_data_property(
            movie,
            RELEASE,
            movie_data["releaseDate"]
        )

        repository.set_data_property(
            movie,
            DURATION_MINUTES,
            movie_data["durationMinutes"]
        )

        repository.set_data_property(
            movie,
            AGE_RATING,
            movie_data["ageRating"]
        )

        # -----------------------------
        # Director (opcional)
        # -----------------------------
        if movie_data.get("director"):
            director = repository.get_individual_by_name(
                movie_data["director"]
            )

            if director is not None:
                repository.add_object_property(
                    movie,
                    HAS_DIRECTOR,
                    director
                )

        # -----------------------------
        # Actors
        # -----------------------------
        for actor_id in movie_data["actors"]:
            actor = repository.get_individual_by_name(actor_id)

            if actor is not None:
                repository.add_object_property(
                    movie,
                    HAS_ACTOR,
                    actor
                )

        # -----------------------------
        # Themes
        # -----------------------------
        for theme_id in movie_data["themes"]:
            theme = repository.get_individual_by_name(theme_id)

            if theme is not None:
                repository.add_object_property(
                    movie,
                    HAS_THEME,
                    theme
                )

        # -----------------------------
        # Country
        # -----------------------------
        country = repository.get_individual_by_name(
            movie_data["country"]
        )

        if country is not None:

            repository.add_object_property(
                movie,
                HAS_COUNTRY_OF_ORIGIN,
                country
            )


def populate_users(repository):
    for user in DATA_USERS:
        create_entity(
            repository,
            USER,
            {
                "id": user["id"],
                NAME: user["full_name"],
                EMAIL: user["email"],
                AGE: user["age"],
                REGISTRATION: user["registration_date"]
            }
        )


def populate_preferences(repository):
    pass


def populate_ratings(repository):
    pass


def create_entity(repository, class_name, entity_data):
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