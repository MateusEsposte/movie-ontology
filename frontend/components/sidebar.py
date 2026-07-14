import customtkinter as ctk
from views.movies_view import MoviesView
from views.preferences_view import PreferencesView
from views.ratings_view import RatingsView
from views.friends_view import FriendsView
from views.recommendations_view import RecommendationsView


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, home_view):
        super().__init__(
            master,
            width=220,
            corner_radius=0
        )

        self.grid_rowconfigure(7, weight=1)
        self.home_view = home_view

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
            text="Home"
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

        self.ratings_button = ctk.CTkButton(
            self,
            text="Avaliações",
            command=lambda:
            self.home_view.show_content(
                RatingsView
            )
        )

        self.ratings_button.grid(
            row=4,
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
            command=lambda:
            self.home_view.show_content(
                RecommendationsView
            )
        )

        self.recommendations_button.grid(
            row=6,
            column=0,
            padx=20,
            pady=8,
            sticky="ew"
        )