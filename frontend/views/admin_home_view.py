import customtkinter as ctk

class AdminHomeView(ctk.CTkFrame):
    def __init__(self, master):

        super().__init__(master)

        label = ctk.CTkLabel(self, text="Área Administrativa")
        label.pack(pady=50)