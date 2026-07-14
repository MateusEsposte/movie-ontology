class NavigationManager:

    def __init__(self, app):
        self.app = app
        self.current_view = None

    def show_view(self, view_class):
        if self.current_view:
            self.current_view.destroy()

        self.current_view = view_class(self.app)
        self.current_view.pack(fill="both", expand=True)
