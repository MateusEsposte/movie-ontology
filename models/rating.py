class Rating:
    def __init__(
        self,
        rating_id: str,
        username: str,
        movie_title: str,
        score: float,
        rating_date: str
    ):
        self.rating_id = rating_id
        self.username = username
        self.movie_title = movie_title
        self.score = score
        self.rating_date = rating_date