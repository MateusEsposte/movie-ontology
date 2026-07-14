import customtkinter as ctk


class RatingsView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Avaliações", font=("Arial", 28, "bold")).pack(pady=40)