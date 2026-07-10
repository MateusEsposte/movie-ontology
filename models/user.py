class User:
    def __init__(self, username, name, email, age):
        self.username = username
        self.name = name
        self.email = email
        self.age = age
    
    
    def __str__(self):
        return f"{self.username} - {self.name}"
    
    def __repr__(self):
        return self.__str__()