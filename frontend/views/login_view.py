import customtkinter as ctk
from frontend.views.admin_home_view import AdminHomeView
from frontend.views.user_home_view import UserHomeView


class LoginView(ctk.CTkFrame):

    def __init__(self, master, repository):

        super().__init__(master)

        self.repository = repository
        self.user_service = master.user_service
        self.users = self.user_service.list_users()

        self.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            self,
            text="Movie Recommendation System",
            font=("Arial", 30, "bold")
        )

        title.pack(pady=(80, 40))

        values = []

        for user in self.users:
            values.append(user.username)

        self.user_combobox = ctk.CTkComboBox(
            self,
            values=values
        )

        self.user_combobox.pack(pady=20)

        if values:
            self.user_combobox.set(values[0])

        button = ctk.CTkButton(
            self,
            text="Entrar",
            command=self.login
        )

        button.pack(pady=30)

        admin_button = ctk.CTkButton(
            self,
            text="Entrar como administrador",
            command=self.open_admin
        )

        admin_button.pack(
            pady=10
        )


    def login(self):
        username = self.user_combobox.get()

        user = self.user_service.get_user(
            username
        )

        self.master.current_user = user

        self.master.navigation.show_view(
            UserHomeView
        )

    def open_admin(self):
        self.master.current_user = None

        self.master.navigation.show_view(
            AdminHomeView
        )