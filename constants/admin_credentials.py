import os


ADMIN_USERNAME = os.getenv(
    "MOVIE_ADMIN_USERNAME",
    "admin"
)

ADMIN_PASSWORD = os.getenv(
    "MOVIE_ADMIN_PASSWORD",
    "admin123"
)
