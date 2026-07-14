import customtkinter as ctk


class RecommendationsView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Recomendações", font=("Arial", 28, "bold")).pack(pady=40)