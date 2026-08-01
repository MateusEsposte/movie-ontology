import customtkinter as ctk


class FriendsView(ctk.CTkFrame):

    def __init__(
        self,
        master,
        repository,
        current_user,
        user_service
    ):
        super().__init__(master)

        self.repository = repository
        self.current_user = current_user
        self.user_service = user_service

        self.available_users = {}

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

        title = ctk.CTkLabel(
            self,
            text="Amigos",
            font=("Arial", 28, "bold")
        )

        title.grid(
            row=0,
            column=0,
            pady=20
        )

        self.main_frame = ctk.CTkFrame(
            self
        )

        self.main_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(0, 20)
        )

        self.main_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.main_frame.grid_columnconfigure(
            1,
            weight=2
        )

        self.main_frame.grid_rowconfigure(
            0,
            weight=1
        )

        # =====================================
        # Painel para adicionar amigos
        # =====================================

        self.form_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.form_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(10, 5),
            pady=10
        )

        form_title = ctk.CTkLabel(
            self.form_frame,
            text="Adicionar amigo",
            font=("Arial", 22, "bold")
        )

        form_title.pack(
            pady=(30, 25)
        )

        user_label = ctk.CTkLabel(
            self.form_frame,
            text="Usuário"
        )

        user_label.pack(
            pady=(10, 5)
        )

        self.user_combobox = ctk.CTkComboBox(
            self.form_frame,
            values=[]
        )

        self.user_combobox.pack(
            fill="x",
            padx=25,
            pady=5
        )

        self.add_button = ctk.CTkButton(
            self.form_frame,
            text="Adicionar amigo",
            command=self.add_friend
        )

        self.add_button.pack(
            pady=(25, 10)
        )

        self.message_label = ctk.CTkLabel(
            self.form_frame,
            text="",
            wraplength=260
        )

        self.message_label.pack(
            padx=20,
            pady=10
        )

        information_label = ctk.CTkLabel(
            self.form_frame,
            text=(
                "As amizades são utilizadas nas "
                "recomendações por filtragem colaborativa."
            ),
            wraplength=260,
            justify="left"
        )

        information_label.pack(
            padx=25,
            pady=(25, 10)
        )

        # =====================================
        # Lista de amigos
        # =====================================

        self.friends_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            label_text="Meus amigos"
        )

        self.friends_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 10),
            pady=10
        )

        self.refresh_view()

    def refresh_view(self):

        self.load_available_users()
        self.load_friends()

    def load_available_users(self):

        all_users = self.user_service.list_users()

        friends = self.user_service.list_friends(
            self.current_user.username
        )

        friend_usernames = {
            friend.username
            for friend in friends
        }

        self.available_users = {}

        for user in all_users:

            if (
                user.username
                == self.current_user.username
            ):
                continue

            if user.username in friend_usernames:
                continue

            display_name = (
                f"{user.name} ({user.username})"
            )

            self.available_users[
                display_name
            ] = user.username

        values = list(
            self.available_users.keys()
        )

        self.user_combobox.configure(
            values=values
        )

        if values:

            self.user_combobox.set(
                values[0]
            )

            self.add_button.configure(
                state="normal"
            )

        else:

            self.user_combobox.set(
                ""
            )

            self.add_button.configure(
                state="disabled"
            )

    def load_friends(self):

        for widget in (
            self.friends_frame.winfo_children()
        ):
            widget.destroy()

        friends = self.user_service.list_friends(
            self.current_user.username
        )

        if not friends:

            empty_label = ctk.CTkLabel(
                self.friends_frame,
                text="Nenhum amigo adicionado."
            )

            empty_label.pack(
                pady=30
            )

            return

        friends.sort(
            key=lambda friend: (
                friend.name or friend.username
            )
        )

        for friend in friends:

            friend_frame = ctk.CTkFrame(
                self.friends_frame
            )

            friend_frame.pack(
                fill="x",
                padx=8,
                pady=7
            )

            friend_frame.grid_columnconfigure(
                0,
                weight=1
            )

            name_label = ctk.CTkLabel(
                friend_frame,
                text=friend.name,
                font=("Arial", 18, "bold"),
                anchor="w"
            )

            name_label.grid(
                row=0,
                column=0,
                sticky="ew",
                padx=15,
                pady=(12, 4)
            )

            details = (
                f"Usuário: {friend.username}\n"
                f"E-mail: {friend.email}\n"
                f"Idade: {friend.age}"
            )

            details_label = ctk.CTkLabel(
                friend_frame,
                text=details,
                justify="left",
                anchor="w"
            )

            details_label.grid(
                row=1,
                column=0,
                sticky="ew",
                padx=15,
                pady=(4, 12)
            )

            remove_button = ctk.CTkButton(
                friend_frame,
                text="Remover",
                width=90,
                command=lambda friend_username=(
                    friend.username
                ): self.remove_friend(
                    friend_username
                )
            )

            remove_button.grid(
                row=0,
                column=1,
                rowspan=2,
                padx=12,
                pady=12
            )

    def add_friend(self):

        selected_user = (
            self.user_combobox.get()
        )

        friend_username = (
            self.available_users.get(
                selected_user
            )
        )

        if friend_username is None:

            self.message_label.configure(
                text="Selecione um usuário válido."
            )

            return

        try:

            self.user_service.add_friend(
                username=self.current_user.username,
                friend_username=friend_username
            )

            self.message_label.configure(
                text="Amigo adicionado."
            )

            self.refresh_view()

        except ValueError as error:

            self.message_label.configure(
                text=str(error)
            )

    def remove_friend(
        self,
        friend_username: str
    ):

        try:

            self.user_service.remove_friend(
                username=self.current_user.username,
                friend_username=friend_username
            )

            self.message_label.configure(
                text="Amigo removido."
            )

            self.refresh_view()

        except ValueError as error:

            self.message_label.configure(
                text=str(error)
            )