import customtkinter as ctk
from components.sidebar import Sidebar
from views.movies_view import MoviesView


class UserHomeView(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.pack(fill="both", expand=True)

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        self.sidebar = Sidebar(
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

        title = ctk.CTkLabel(
            self.content,
            text="Bem-vindo ao Movie Recommendation System",
            font=("Arial", 28, "bold")
        )

        title.pack(
            pady=(80, 20)
        )

        subtitle = ctk.CTkLabel(
            self.content,
            text="Selecione uma opção no menu lateral.",
            font=("Arial", 18)
        )

        self.show_content(
            MoviesView
        )

        subtitle.pack()

    def show_content(self, view_class):

        if hasattr(self, "current_view") and self.current_view:

            self.current_view.destroy()

        self.current_view = view_class(
            self.content
        )

        self.current_view.pack(
            fill="both",
            expand=True
        )