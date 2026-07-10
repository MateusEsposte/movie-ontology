
from database.ontology_manager import OntologyManager
from database.ontology_repository import OntologyRepository
from data.people import PEOPLE
from data.theme import THEMES
from data.languages import LANGUAGES
from data.countries import COUNTRIES
from data.movies import MOVIES



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
            "CountryOfOrigin",
            country
        )


def populate_people(repository):
    for person_data in PEOPLE:
        if repository.exists_individual(person_data["id"]):
            print(f"  - {person_data['name']} já existe.")
            continue

        person = repository.create_individual(
            "Person",
            person_data["id"]
        )

        repository.set_data_property(person, "fullName", person_data["name"])
        repository.set_data_property(person, "birthDate", person_data["birth_date"])
        repository.set_data_property(person, "nationality", person_data["nationality"])

        for role in person_data["roles"]:
            repository.add_class(person, role)


def populate_movies(repository):
    for movie_data in MOVIES:
        # Evita criar o mesmo filme novamente
        if repository.exists_individual(movie_data["id"]):
            print(f'  - {movie_data["originalTitle"]} já existe.')
            continue

        # Cria o indivíduo Film
        movie = repository.create_individual(
            "Film",
            movie_data["id"]
        )

        # -----------------------------
        # Data Properties
        # -----------------------------
        repository.set_data_property(
            movie,
            "originalTitle",
            movie_data["originalTitle"]
        )

        repository.set_data_property(
            movie,
            "portugueseTitle",
            movie_data["portugueseTitle"]
        )

        repository.set_data_property(
            movie,
            "releaseDate",
            movie_data["releaseDate"]
        )

        repository.set_data_property(
            movie,
            "durationMinutes",
            movie_data["durationMinutes"]
        )

        repository.set_data_property(
            movie,
            "ageRating",
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
                    "hasDirector",
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
                    "hasActor",
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
                    "hasTheme",
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
                "hasCountryOfOrigin",
                country
            )


def populate_users(repository):
    pass


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