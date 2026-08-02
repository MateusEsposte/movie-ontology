import customtkinter as ctk

from frontend.views.user_home_view import UserHomeView
from frontend.views.admin_home_view import AdminHomeView
from frontend.views.welcome_view import WelcomeView

from services.auth_service import AuthService


class LoginView(ctk.CTkFrame):

    def __init__(
        self,
        master,
        repository
    ):
        super().__init__(master)

        self.repository = repository
        self.user_service = master.user_service
        self.auth_service = AuthService()

        self.pack(
            fill="both",
            expand=True
        )

        title = ctk.CTkLabel(
            self,
            text="Entrar",
            font=("Arial", 30, "bold")
        )

        title.pack(
            pady=(80, 35)
        )

        self.username_entry = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Nome de usuário"
        )

        self.username_entry.pack(
            pady=10
        )

        self.password_entry = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Senha",
            show="*"
        )

        self.password_entry.pack(
            pady=10
        )

        login_button = ctk.CTkButton(
            self,
            text="Entrar",
            width=220,
            command=self.login
        )

        login_button.pack(
            pady=(25, 10)
        )

        back_button = ctk.CTkButton(
            self,
            text="Voltar",
            width=220,
            command=lambda: (
                self.master.navigation.show_view(
                    WelcomeView
                )
            )
        )

        back_button.pack(
            pady=10
        )

        self.message_label = ctk.CTkLabel(
            self,
            text=""
        )

        self.message_label.pack(
            pady=15
        )

    def login(self):

        username = (
            self.username_entry
            .get()
            .strip()
        )

        password = self.password_entry.get()

        if not username or not password:

            self.message_label.configure(
                text="Informe o usuário e a senha."
            )

            return

        # Primeiro verifica a conta administrativa.
        if self.auth_service.authenticate_admin(
            username,
            password
        ):

            self.master.current_user = None

            self.master.navigation.show_view(
                AdminHomeView
            )

            return

        # Caso não seja administrador,
        # tenta autenticar como usuário comum.
        try:

            user = self.user_service.authenticate(
                username,
                password
            )

            self.master.current_user = user

            self.master.navigation.show_view(
                UserHomeView
            )

        except ValueError as error:

            self.message_label.configure(
                text=str(error)
            )