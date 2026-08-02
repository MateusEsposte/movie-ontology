import customtkinter as ctk
from frontend.controllers.navigation import NavigationManager
from frontend.views.welcome_view import WelcomeView
from services.user_service import UserService


class App(ctk.CTk):
    def __init__(self, repository, manager):

        super().__init__()

        self.repository = repository
        self.manager = manager
        self.current_user = None
        self.user_service = UserService(repository, manager)
        self.title("Movie Recommendation System")
        self.geometry("1100x700")
        self.minsize(1000, 650)
        self.navigation = NavigationManager(self, repository)
        self.navigation.show_view(WelcomeView)        
