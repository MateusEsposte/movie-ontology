class Preference:
    def __init__(
        self,
        preference_id: str,
        username: str,
        preference_type: str,
        preferred_element: str,
        interest_level: int
    ):

        self.preference_id = preference_id
        self.username = username
        self.preference_type = preference_type
        self.preferred_element = preferred_element
        self.interest_level = interest_level