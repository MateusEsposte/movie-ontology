from models.user import User
from constants.ontology_constants import *


class UserService:
    def __init__(self, repository, manager):
        self.repository = repository
        self.manager = manager

    def create_user(self, username, full_name, email, age) -> User:

        self._validate_user( username, full_name, email, age)

        if self.exists(username):
            raise ValueError(
                "Já existe um usuário com esse username."
            )

        user = self.repository.create_individual(
            USER,
            username
        )

        self.repository.set_data_properties(
            user,
            {
                USERNAME: username,
                NAME: full_name,
                EMAIL: email,
                AGE: age
            }
        )

        return User(username=username, name=full_name, email=email, age=age)
    
    def get_user(self, username: str) -> User:
        if not self.exists(username):
            raise ValueError(
                "Usuário não encontrado."
            )

        individual = self.repository.get_individual_by_name(
            username
        )

        return User(
            username=self.repository.get_data_property(
                individual,
                USERNAME
            ),
            name=self.repository.get_data_property(
                individual,
                NAME
            ),
            email=self.repository.get_data_property(
                individual,
                EMAIL
            ),
            age=self.repository.get_data_property(
                individual,
                AGE
            )
        )
    
    def delete_user(self, username: str):
        if not self.exists(username):
            raise ValueError(
                "Usuário não encontrado."
            )

        self.repository.remove_individual(username)
    
    def exists(self, username: str) -> bool:
        if not username:
            return False

        return self.repository.exists_individual(username)
    
    def _validate_user(self, username: str, full_name: str, email: str, age: int):
        username = username.strip()
        full_name = full_name.strip()
        email = email.strip()

        if username == "":
            raise ValueError("Username não pode ser vazio.")

        if full_name == "":
            raise ValueError("Nome não pode ser vazio.")

        if "@" not in email:
            raise ValueError("E-mail inválido.")

        if age < 0:
            raise ValueError("Idade inválida.")
         
    def list_users(self) -> list[User]:
        users = []

        individuals = self.repository.get_individuals_by_class(USER)

        for individual in individuals:
            users.append(
                self.get_user(individual.name)
            )

        return users