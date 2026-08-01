import customtkinter as ctk
from frontend.components.admin_sidebar import AdminSidebar
from frontend.views.admin_movies_view import AdminMoviesView


class AdminHomeView(ctk.CTkFrame):

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

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        self.sidebar = AdminSidebar(
            self,
            self
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        self.content = ctk.CTkFrame(
            self,
            corner_radius=0
        )

        self.content.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.content.grid_columnconfigure(
            0,
            weight=1
        )

        self.content.grid_rowconfigure(
            0,
            weight=1
        )

        self.current_view = None

        self.show_content(
            AdminMoviesView
        )

    def show_content(
        self,
        view_class
    ):

        if self.current_view:
            self.current_view.destroy()

        self.current_view = view_class(
            self.content,
            self.repository
        )

        self.current_view.pack(
            fill="both",
            expand=True
        )