import customtkinter as ctk


class MoviesView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        title = ctk.CTkLabel(self, text="Filmes", font=("Arial", 28, "bold"))
        title.pack(pady=40)
        label = ctk.CTkLabel(self, text="Tela de filmes")
        label.pack()