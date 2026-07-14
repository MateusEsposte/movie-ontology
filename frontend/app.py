import customtkinter as ctk
from controllers.navigation import NavigationManager
from views.login_view import LoginView


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Movie Recommendation System")
        self.geometry("1100x700")
        self.minsize(1000, 650)
        self.navigation = NavigationManager(self)
        self.navigation.show_view(LoginView)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = App() 
    app.mainloop()
