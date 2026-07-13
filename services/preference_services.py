from database.ontology_repository import OntologyRepository
from models.preference import Preference
from constants.ontology_constants import *


class PreferenceService:
    def __init__(self, repository: OntologyRepository):
        self.repository = repository

    def _next_preference_id(self) -> str:

        preferences = self.repository.get_individuals_by_class(
            PREFERENCE
        )

        highest = 0

        for preference in preferences:

            try:

                number = int(
                    preference.name.replace(
                        "preference_",
                        ""
                    )
                )

                highest = max(
                    highest,
                    number
                )

            except ValueError:
                continue

        return f"preference_{highest + 1:03d}"

    def exists(
        self,
        preference_id: str
    ) -> bool:

        return self.repository.exists_individual(
            preference_id
        )

    def _build_preference(
        self,
        preference_individual
    ):

        preference_id = preference_individual.name

        interest_level = self.repository.get_data_property(
            preference_individual,
            INTEREST_LEVEL
        )

        preference_type = self.repository.get_data_property(
            preference_individual,
            PREFERENCE_TYPE
        )

        users = self.repository.get_object_property(
            preference_individual,
            PREFERENCE_OF
        )

        username = None

        if users:

            username = self.repository.get_data_property(
                users[0],
                USERNAME
            )

        preferred = self.repository.get_object_property(
            preference_individual,
            PREFERS
        )

        preferred_element = None

        if preferred:

            preferred = preferred[0]

            if preference_type == "Theme":

                preferred_element = self.repository.get_data_property(
                    preferred,
                    THEME_NAME
                )

            elif preference_type in ("Actor", "Director"):

                preferred_element = self.repository.get_data_property(
                    preferred,
                    NAME
                )

            elif preference_type == "CinematicWork":

                preferred_element = self.repository.get_data_property(
                    preferred,
                    ORIGINAL
                )

        return Preference(
            preference_id=preference_id,
            username=username,
            preferred_element=preferred_element,
            preference_type=preference_type,
            interest_level=interest_level
        )

    def get_preference(
        self,
        preference_id: str
    ) -> Preference:

        preference = self.repository.require_individual(
            preference_id
        )

        return self._build_preference(
            preference
        )

    def list_preferences(
        self
    ) -> list[Preference]:

        preferences = []

        individuals = self.repository.get_individuals_by_class(
            PREFERENCE
        )

        for individual in individuals:

            preferences.append(
                self._build_preference(
                    individual
                )
            )

        return preferences

    def _get_preference_type(
        self,
        individual
    ) -> str:
        for parent in individual.is_a:
            if hasattr(parent, "name"):
                if parent.name in (
                    "Theme",
                    "Actor",
                    "Director",
                    "CinematicWork"
                ):
                    return parent.name

        raise ValueError(
            "Elemento incompatível para preferência."
        )

    def create_preference(
        self,
        username: str,
        preferred_element_id: str,
        interest_level: int
    ) -> Preference:

        user = self.repository.require_individual(
            username
        )

        preferred_element = (
            self.repository.require_individual(
                preferred_element_id
            )
        )

        preference_type = (
            self._get_preference_type(
                preferred_element
            )
        )

        preference = self.repository.create_individual(
            PREFERENCE,
            self._next_preference_id()
        )

        self.repository.set_data_property(
            preference,
            INTEREST_LEVEL,
            interest_level
        )

        self.repository.set_data_property(
            preference,
            PREFERENCE_TYPE,
            preference_type
        )

        self.repository.add_object_property(
            user,
            HAS_PREFERENCE,
            preference
        )

        self.repository.add_object_property(
            preference,
            PREFERS,
            preferred_element
        )

        return self._build_preference(
            preference
        )

    def update_interest_level(
        self,
        preference_id: str,
        interest_level: int
    ) -> Preference:

        preference = self.repository.require_individual(
            preference_id
        )

        self.repository.set_data_property(
            preference,
            INTEREST_LEVEL,
            interest_level
        )

        return self._build_preference(
            preference
        )

    def delete_preference(
        self,
        preference_id: str
    ):

        preference = self.repository.require_individual(
            preference_id
        )

        self.repository.remove_individual(
            preference
        )

    def list_user_preferences(
        self,
        username: str
    ) -> list[Preference]:

        user = self.repository.require_individual(
            username
        )

        preferences = []

        for preference in self.repository.get_object_property(
            user,
            HAS_PREFERENCE
        ):

            preferences.append(
                self._build_preference(
                    preference
                )
            )

        return preferences
