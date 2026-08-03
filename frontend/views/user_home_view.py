import customtkinter as ctk
from frontend.components.sidebar import Sidebar
from frontend.views.home_view import HomeView

class UserHomeView(ctk.CTkFrame):

    def __init__(self, master, repository):

        super().__init__(master)

        self.repository = repository
        self.current_user = master.current_user
        self.user_service = master.user_service

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
            self,
            repository
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

        self.show_content(
            HomeView
        )

    def show_content(self, view_class):

        if hasattr(self, "current_view") and self.current_view:
            self.current_view.destroy()

        self.current_view = view_class(
            self.content,
            self.repository,
            self.current_user,
            self.user_service
        )

        self.current_view.pack(
            fill="both",
            expand=True
        )