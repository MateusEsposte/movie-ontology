class Movie:
    def __init__(
        self,
        original_title: str,
        portuguese_title: str,
        release_date: str,
        duration_minutes: int,
        age_rating: str,
        country: str,
        languages: list[str],
        theme: str,
        director: str,
        actors: list[str]
    ):

        self.original_title = original_title
        self.portuguese_title = portuguese_title
        self.release_date = release_date
        self.duration_minutes = duration_minutes
        self.age_rating = age_rating
        self.country = country
        self.languages = languages
        self.theme = theme
        self.director = director
        self.actors = actors

    def __str__(self):
        return f"{self.original_title} ({self.release_date})"

    def __repr__(self):
        return self.__str__()