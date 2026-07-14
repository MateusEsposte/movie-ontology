import customtkinter as ctk


class PreferencesView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Preferencias", font=("Arial", 28, "bold")).pack(pady=40)