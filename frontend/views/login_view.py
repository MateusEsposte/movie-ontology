import customtkinter as ctk
from views.user_home_view import UserHomeView


class LoginView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            self,
            text="Movie Recommendation System",
            font=("Arial", 30, "bold")
        )

        title.pack(pady=80)

        button = ctk.CTkButton(
            self, 
            text="Entrar",
            command=lambda:
                self.master.navigation.show_view(
                    UserHomeView
                )
        )

        button.pack(pady=30)