import customtkinter as ctk

from frontend.views.login_view import LoginView
from frontend.views.welcome_view import WelcomeView


class RegisterView(ctk.CTkFrame):

    def __init__(
        self,
        master,
        repository
    ):
        super().__init__(master)

        self.repository = repository
        self.user_service = master.user_service

        self.pack(
            fill="both",
            expand=True
        )

        title = ctk.CTkLabel(
            self,
            text="Criar conta",
            font=("Arial", 30, "bold")
        )

        title.pack(
            pady=(45, 25)
        )

        self.username_entry = self.create_entry(
            "Nome de usuário"
        )

        self.name_entry = self.create_entry(
            "Nome completo"
        )

        self.email_entry = self.create_entry(
            "E-mail"
        )

        self.age_entry = self.create_entry(
            "Idade"
        )

        self.password_entry = ctk.CTkEntry(
            self,
            width=320,
            placeholder_text="Senha",
            show="*"
        )

        self.password_entry.pack(
            pady=8
        )

        self.confirm_password_entry = ctk.CTkEntry(
            self,
            width=320,
            placeholder_text="Confirmar senha",
            show="*"
        )

        self.confirm_password_entry.pack(
            pady=8
        )

        register_button = ctk.CTkButton(
            self,
            text="Cadastrar",
            width=220,
            command=self.register
        )

        register_button.pack(
            pady=(22, 8)
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
            pady=8
        )

        self.message_label = ctk.CTkLabel(
            self,
            text="",
            wraplength=350
        )

        self.message_label.pack(
            pady=12
        )

    def create_entry(
        self,
        placeholder: str
    ):

        entry = ctk.CTkEntry(
            self,
            width=320,
            placeholder_text=placeholder
        )

        entry.pack(
            pady=8
        )

        return entry

    def register(self):
        username = (
            self.username_entry
            .get()
            .strip()
        )

        full_name = (
            self.name_entry
            .get()
            .strip()
        )

        email = (
            self.email_entry
            .get()
            .strip()
        )

        age_text = (
            self.age_entry
            .get()
            .strip()
        )

        password = self.password_entry.get()

        confirmation = (
            self.confirm_password_entry.get()
        )

        if password != confirmation:

            self.message_label.configure(
                text="As senhas não coincidem."
            )

            return

        try:

            age = int(age_text)

        except ValueError:

            self.message_label.configure(
                text="A idade deve ser um número inteiro."
            )

            return

        try:

            self.user_service.create_user(
                username=username,
                full_name=full_name,
                email=email,
                age=age,
                password=password
            )

            self.message_label.configure(
                text="Conta criada com sucesso."
            )

            self.after(
                700,
                lambda: (
                    self.master.navigation.show_view(
                        LoginView
                    )
                )
            )

        except ValueError as error:

            self.message_label.configure(
                text=str(error)
            )