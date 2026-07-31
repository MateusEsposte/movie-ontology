from frontend.views.login_view import LoginView

class NavigationManager:

    def __init__(self, app, repository):
        self.app = app
        self.repository = repository
        self.current_view = None

    def show_view(self, view_class):
        if self.current_view:
            self.current_view.destroy()

        self.current_view = view_class(self.app, self.repository)
        self.current_view.pack(fill="both", expand=True)
