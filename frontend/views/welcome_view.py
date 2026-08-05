import customtkinter as ctk


class WelcomeView(ctk.CTkFrame):
    def __init__(
        self,
        master,
        repository
    ):
        super().__init__(master)

        self.repository = repository

        self.pack(
            fill="both",
            expand=True
        )

        title = ctk.CTkLabel(
            self,
            text="Movie Recommendation System",
            font=("Arial", 30, "bold")
        )

        title.pack(
            pady=(100, 20)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Escolha uma opção",
            font=("Arial", 18)
        )

        subtitle.pack(
            pady=(0, 35)
        )

        login_button = ctk.CTkButton(
            self,
            text="Entrar",
            width=240,
            command=self.open_login
        )

        login_button.pack(
            pady=10
        )

        register_button = ctk.CTkButton(
            self,
            text="Criar nova conta",
            width=240,
            command=self.open_register
        )

        register_button.pack(
            pady=10
        )

    def open_login(self):

        from frontend.views.login_view import LoginView

        self.master.navigation.show_view(
            LoginView
        )

    def open_register(self):

        from frontend.views.register_view import RegisterView

        self.master.navigation.show_view(
            RegisterView
        )
