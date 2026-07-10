from models.user import User


class UserService:
    def __init__(self, repository, manager):
        self.repository = repository
        self.manager = manager

    def create_user(self, username: str, name: str, email: str, age: int) -> User:
        username = username.strip()
        name = name.strip()
        email = email.strip()

        if username == "":
            raise ValueError("O username não pode ser vazio.")

        if name == "":
            raise ValueError("O nome não pode ser vazio.")

        if "@" not in email:
            raise ValueError("E-mail inválido.")

        if age < 0:
            raise ValueError("Idade inválida.")

        if self.exists(username):
            raise ValueError("Já existe um usuário com esse username.")


        user = self.repository.create_individual(
            "User",
            username
        )

        self.repository.set_data_property(
            user,
            "username",
            username
        )

        self.repository.set_data_property(
            user,
            "fullName",
            name
        )

        self.repository.set_data_property(
            user,
            "email",
            email
        )

        self.repository.set_data_property(
            user,
            "age",
            age
        )

        return User(
            username=username,
            name=name,
            email=email,
            age=age
        )
    
    def get_user():
        pass
    
    def list_users():
        pass
    
    def delete_user():
        pass
    
    def exists(self, username: str) -> bool:
        if not username:
            return False

        return self.repository.exists_individual(username)
    