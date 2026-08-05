import customtkinter as ctk
from frontend.views.movies_view import MoviesView
from frontend.views.preferences_view import PreferencesView
from frontend.views.friends_view import FriendsView
from frontend.views.recommendations_view import RecommendationsView
from frontend.views.home_view import HomeView


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, home_view, repository):
        super().__init__(
            master,
            width=220,
            corner_radius=0
        )

        self.app = master.winfo_toplevel()
        self.home_view = home_view
        self.repository = repository

        title = ctk.CTkLabel(
            self,
            text="Movie\nOntology",
            font=("Arial", 24, "bold")
        )

        title.grid(
            row=0,
            column=0,
            padx=20,
            pady=(30, 40)
        )

        self.home_button = ctk.CTkButton(
            self,
            text="Home",
            command=lambda: (
                self.home_view.show_content(
                    HomeView
                )
            )
        )

        self.home_button.grid(
            row=1,
            column=0,
            padx=20,
            pady=8,
            sticky="ew"
        )

        self.movies_button = ctk.CTkButton(
            self,
            text="Filmes",
            command=lambda:
            self.home_view.show_content(
                MoviesView
            )
        )

        self.movies_button.grid(
            row=2,
            column=0,
            padx=20,
            pady=8,
            sticky="ew"
        )

        self.preferences_button = ctk.CTkButton(
            self,
            text="Preferências",
            command=lambda:
            self.home_view.show_content(
                PreferencesView
            )
        )

        self.preferences_button.grid(
            row=3,
            column=0,
            padx=20,
            pady=8,
            sticky="ew"
        )

        self.friends_button = ctk.CTkButton(
            self,
            text="Amigos",
            command=lambda:
            self.home_view.show_content(
                FriendsView
            )
        )

        self.friends_button.grid(
            row=5,
            column=0,
            padx=20,
            pady=8,
            sticky="ew"
        )

        self.recommendations_button = ctk.CTkButton(
            self,
            text="Recomendações",
            command=lambda: (
                self.home_view.show_content(
                    RecommendationsView
                )
            )
        )

        self.recommendations_button.grid(
            row=6,
            column=0,
            padx=20,
            pady=8,
            sticky="ew"
        )

        self.grid_rowconfigure(
            7,
            weight=1
        )

        self.logout_button = ctk.CTkButton(
            self,
            text="Sair da conta",
            command=self.logout
        )

        self.logout_button.grid(
            row=8,
            column=0,
            padx=20,
            pady=(8, 25),
            sticky="ew"
        )

    def logout(self):
        from frontend.views.welcome_view import WelcomeView
        app = self.winfo_toplevel()
        app.current_user = None
        app.navigation.show_view(WelcomeView)
        