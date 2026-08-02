import hmac

from constants.admin_credentials import (
    ADMIN_PASSWORD,
    ADMIN_USERNAME
)


class AuthService:

    def authenticate_admin(
        self,
        username: str,
        password: str
    ) -> bool:

        username_matches = hmac.compare_digest(
            username.strip(),
            ADMIN_USERNAME
        )

        password_matches = hmac.compare_digest(
            password,
            ADMIN_PASSWORD
        )

        return (
            username_matches
            and password_matches
        )