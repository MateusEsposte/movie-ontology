import customtkinter as ctk
from frontend.views.admin_movies_view import AdminMoviesView
from frontend.views.admin_elements_view import AdminElementsView
from frontend.views.admin_people_view import (AdminPeopleView)

class AdminSidebar(ctk.CTkFrame):

    def __init__(
        self,
        master,
        admin_home
    ):
        super().__init__(
            master,
            width=220,
            corner_radius=0
        )

        self.admin_home = admin_home

        title = ctk.CTkLabel(
            self,
            text="Administração",
            font=("Arial", 24, "bold")
        )

        title.pack(
            padx=20,
            pady=(30, 40)
        )

        movies_button = ctk.CTkButton(
            self,
            text="Filmes",
            command=lambda: (
                self.admin_home.show_content(
                    AdminMoviesView
                )
            )
        )

        movies_button.pack(
            fill="x",
            padx=20,
            pady=8
        )

        elements_button = ctk.CTkButton(
            self,
            text="Elementos",
            command=lambda: (
                self.admin_home.show_content(
                    AdminElementsView
                )
            )
        )

        elements_button.pack(
            fill="x",
            padx=20,
            pady=8
        )

        people_button = ctk.CTkButton(
            self,
            text="Pessoas",
            command=lambda: (
                self.admin_home.show_content(
                    AdminPeopleView
                )
            )
        )

        people_button.pack(
            fill="x",
            padx=20,
            pady=8
        )