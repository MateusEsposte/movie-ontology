import customtkinter as ctk


class FriendsView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Amigos", font=("Arial", 28, "bold")).pack(pady=40)