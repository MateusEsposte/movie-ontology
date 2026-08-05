import customtkinter as ctk

from frontend.views.admin_movies_view import AdminMoviesView
from frontend.views.admin_elements_view import AdminElementsView
from frontend.views.admin_people_view import AdminPeopleView


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

        self.pack_propagate(False)

        self.menu_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.menu_frame.pack(
            fill="x"
        )

        title = ctk.CTkLabel(
            self.menu_frame,
            text="Administração",
            font=("Arial", 24, "bold")
        )

        title.pack(
            padx=20,
            pady=(30, 40)
        )

        self.movies_button = ctk.CTkButton(
            self.menu_frame,
            text="Filmes",
            command=lambda: (
                self.admin_home.show_content(
                    AdminMoviesView
                )
            )
        )

        self.movies_button.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.elements_button = ctk.CTkButton(
            self.menu_frame,
            text="Elementos",
            command=lambda: (
                self.admin_home.show_content(
                    AdminElementsView
                )
            )
        )

        self.elements_button.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.people_button = ctk.CTkButton(
            self.menu_frame,
            text="Pessoas",
            command=lambda: (
                self.admin_home.show_content(
                    AdminPeopleView
                )
            )
        )

        self.people_button.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.logout_button = ctk.CTkButton(
            self,
            text="Sair da conta",
            command=self.logout
        )

        self.logout_button.pack(
            fill="x",
            padx=20,
            pady=(8, 25),
            side="bottom"
        )

    def logout(self):
        from frontend.views.welcome_view import WelcomeView
        app = self.winfo_toplevel()
        app.current_user = None
        app.navigation.show_view(WelcomeView)