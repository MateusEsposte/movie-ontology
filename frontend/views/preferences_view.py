import customtkinter as ctk
from services.preference_services import PreferenceService
from services.movie_services import MovieService


class PreferencesView(ctk.CTkFrame):
    PREFERENCE_CLASSES = {
        "Filme": "CinematicWork",
        "Tema": "Theme",
        "Ator": "Actor",
        "Diretor": "Director"
    }

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

        self.preference_service = PreferenceService(
            repository
        )

        self.movie_service = MovieService(
            repository
        )

        self.available_elements = {}

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
            text="Preferências",
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
            text="Adicionar preferência",
            font=("Arial", 22, "bold")
        )

        form_title.pack(
            pady=(25, 20)
        )

        type_label = ctk.CTkLabel(
            self.form_frame,
            text="Tipo da preferência"
        )

        type_label.pack(
            pady=(10, 5)
        )

        self.type_combobox = ctk.CTkComboBox(
            self.form_frame,
            values=list(
                self.PREFERENCE_CLASSES.keys()
            ),
            command=self.on_type_changed
        )

        self.type_combobox.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        self.type_combobox.set(
            "Filme"
        )

        element_label = ctk.CTkLabel(
            self.form_frame,
            text="Elemento preferido"
        )

        element_label.pack(
            pady=(20, 5)
        )

        self.element_combobox = ctk.CTkComboBox(
            self.form_frame,
            values=[]
        )

        self.element_combobox.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        interest_label = ctk.CTkLabel(
            self.form_frame,
            text="Nível de interesse"
        )

        interest_label.pack(
            pady=(20, 5)
        )

        self.interest_combobox = ctk.CTkComboBox(
            self.form_frame,
            values=[
                "1",
                "2",
                "3",
                "4",
                "5"
            ]
        )

        self.interest_combobox.set(
            "5"
        )

        self.interest_combobox.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        self.save_button = ctk.CTkButton(
            self.form_frame,
            text="Salvar preferência",
            command=self.save_preference
        )

        self.save_button.pack(
            pady=25
        )

        self.message_label = ctk.CTkLabel(
            self.form_frame,
            text=""
        )

        self.message_label.pack(
            padx=20,
            pady=10
        )

        self.preferences_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            label_text="Minhas preferências"
        )

        self.preferences_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 10),
            pady=10
        )

        self.load_available_elements(
            "Filme"
        )

        self.load_user_preferences()

    def on_type_changed(self, selected_type):

        self.load_available_elements(
            selected_type
        )

    def load_available_elements(
        self,
        selected_type
    ):

        self.available_elements = {}

        if selected_type == "Filme":

            movies = self.movie_service.list_movies()

            for movie in movies:

                self.available_elements[
                    movie.original_title
                ] = movie.ontology_id

        else:

            class_name = self.PREFERENCE_CLASSES[
                selected_type
            ]

            individuals = (
                self.repository
                .get_individuals_by_class(
                    class_name
                )
            )

            for individual in individuals:

                display_name = self.format_element_name(
                    individual.name
                )

                self.available_elements[
                    display_name
                ] = individual.name

        values = list(
            self.available_elements.keys()
        )

        self.element_combobox.configure(
            values=values
        )

        if values:

            self.element_combobox.set(
                values[0]
            )

        else:

            self.element_combobox.set(
                ""
            )

    def save_preference(self):

        selected_element = (
            self.element_combobox.get()
        )

        if not selected_element:

            self.message_label.configure(
                text="Nenhum elemento disponível."
            )

            return

        element_id = self.available_elements.get(
            selected_element
        )

        if element_id is None:

            self.message_label.configure(
                text="Elemento inválido."
            )

            return

        interest_level = int(
            self.interest_combobox.get()
        )

        try:

            self.preference_service.create_preference(
                username=self.current_user.username,
                preferred_element_id=element_id,
                interest_level=interest_level
            )

            self.message_label.configure(
                text="Preferência salva."
            )

            self.load_user_preferences()

        except ValueError as error:

            self.message_label.configure(
                text=str(error)
            )

    def load_user_preferences(self):

        for widget in (
            self.preferences_frame.winfo_children()
        ):

            widget.destroy()

        preferences = (
            self.preference_service
            .list_user_preferences(
                self.current_user.username
            )
        )

        if not preferences:

            empty_label = ctk.CTkLabel(
                self.preferences_frame,
                text="Nenhuma preferência cadastrada."
            )

            empty_label.pack(
                pady=20
            )

            return

        for preference in preferences:

            preference_frame = ctk.CTkFrame(
                self.preferences_frame
            )

            preference_frame.pack(
                fill="x",
                padx=8,
                pady=6
            )

            preference_frame.grid_columnconfigure(
                0,
                weight=1
            )

            description = (
                f"Tipo: {preference.preference_type}\n"
                f"Elemento: {preference.preferred_element}\n"
                f"Interesse: {preference.interest_level}"
            )

            preference_label = ctk.CTkLabel(
                preference_frame,
                text=description,
                justify="left",
                anchor="w"
            )

            preference_label.grid(
                row=0,
                column=0,
                sticky="ew",
                padx=15,
                pady=12
            )

            delete_button = ctk.CTkButton(
                preference_frame,
                text="Excluir",
                width=80,
                command=lambda preference_id=(
                    preference.preference_id
                ): self.delete_preference(
                    preference_id
                )
            )

            delete_button.grid(
                row=0,
                column=1,
                padx=10,
                pady=12
            )

    def format_element_name(
        self,
        individual_name: str
    ) -> str:

        prefixes = [
            "theme_",
            "actor_",
            "director_",
            "film_"
        ]

        formatted_name = individual_name

        for prefix in prefixes:

            if formatted_name.startswith(prefix):

                formatted_name = formatted_name[
                    len(prefix):
                ]

                break

        return (
            formatted_name
            .replace("_", " ")
            .title()
        )
    
    def delete_preference(
        self,
        preference_id: str
    ):

        try:

            self.preference_service.delete_preference(
                username=self.current_user.username,
                preference_id=preference_id
            )

            self.message_label.configure(
                text="Preferência excluída."
            )

            self.load_user_preferences()

        except ValueError as error:

            self.message_label.configure(
                text=str(error)
            )









