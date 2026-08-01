import re
import unicodedata
import customtkinter as ctk


class AdminElementsView(ctk.CTkFrame):

    ELEMENT_CONFIG = {
        "Tema": {
            "class_name": "Theme",
            "prefix": "theme",
            "data_property": "themeName"
        },
        "Ator": {
            "class_name": "Actor",
            "prefix": "actor",
            "data_property": "fullName"
        },
        "Diretor": {
            "class_name": "Director",
            "prefix": "director",
            "data_property": "fullName"
        },
        "País": {
            "class_name": "CountryOfOrigin",
            "prefix": "country",
            "data_property": "countryName"
        },
        "Idioma": {
            "class_name": "Language",
            "prefix": "language",
            "data_property": "languageName"
        }
    }

    def __init__(
        self,
        master,
        repository
    ):
        super().__init__(master)

        self.repository = repository

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
            text="Cadastro de elementos",
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
        # Formulário
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
            text="Novo elemento",
            font=("Arial", 22, "bold")
        )

        form_title.pack(
            pady=(30, 25)
        )

        type_label = ctk.CTkLabel(
            self.form_frame,
            text="Tipo do elemento"
        )

        type_label.pack(
            pady=(10, 5)
        )

        self.type_combobox = ctk.CTkComboBox(
            self.form_frame,
            values=list(
                self.ELEMENT_CONFIG.keys()
            ),
            command=self.on_type_changed
        )

        self.type_combobox.set(
            "Tema"
        )

        self.type_combobox.pack(
            padx=25,
            pady=5,
            fill="x"
        )

        name_label = ctk.CTkLabel(
            self.form_frame,
            text="Nome"
        )

        name_label.pack(
            pady=(25, 5)
        )

        self.name_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Digite o nome"
        )

        self.name_entry.pack(
            padx=25,
            pady=5,
            fill="x"
        )

        self.identifier_label = ctk.CTkLabel(
            self.form_frame,
            text="Identificador: -",
            wraplength=250
        )

        self.identifier_label.pack(
            padx=20,
            pady=(15, 5)
        )

        self.name_entry.bind(
            "<KeyRelease>",
            self.preview_identifier
        )

        self.save_button = ctk.CTkButton(
            self.form_frame,
            text="Cadastrar",
            command=self.save_element
        )

        self.save_button.pack(
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

        # =====================================
        # Lista de elementos
        # =====================================

        self.elements_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            label_text="Elementos cadastrados"
        )

        self.elements_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 10),
            pady=10
        )

        self.load_elements()

    def on_type_changed(
        self,
        selected_type
    ):

        self.name_entry.delete(
            0,
            "end"
        )

        self.identifier_label.configure(
            text="Identificador: -"
        )

        self.message_label.configure(
            text=""
        )

        self.load_elements()

    def preview_identifier(
        self,
        event=None
    ):

        selected_type = (
            self.type_combobox.get()
        )

        name = self.name_entry.get()

        if not name.strip():

            self.identifier_label.configure(
                text="Identificador: -"
            )

            return

        identifier = self.generate_identifier(
            selected_type,
            name
        )

        self.identifier_label.configure(
            text=f"Identificador: {identifier}"
        )

    def generate_identifier(
        self,
        element_type: str,
        name: str
    ) -> str:

        config = self.ELEMENT_CONFIG[
            element_type
        ]

        normalized_name = (
            unicodedata.normalize(
                "NFKD",
                name
            )
            .encode(
                "ascii",
                "ignore"
            )
            .decode(
                "ascii"
            )
            .lower()
        )

        normalized_name = re.sub(
            r"[^a-z0-9]+",
            "_",
            normalized_name
        )

        normalized_name = (
            normalized_name.strip("_")
        )

        return (
            f"{config['prefix']}_"
            f"{normalized_name}"
        )

    def save_element(self):

        element_type = (
            self.type_combobox.get()
        )

        name = self.name_entry.get().strip()

        if element_type not in self.ELEMENT_CONFIG:

            self.message_label.configure(
                text="Selecione um tipo válido."
            )

            return

        if not name:

            self.message_label.configure(
                text="O nome não pode ficar vazio."
            )

            return

        config = self.ELEMENT_CONFIG[
            element_type
        ]

        identifier = self.generate_identifier(
            element_type,
            name
        )

        if self.repository.exists_individual(
            identifier
        ):

            self.message_label.configure(
                text=(
                    "Já existe um elemento com "
                    "esse identificador."
                )
            )

            return

        try:

            individual = (
                self.repository.create_individual(
                    config["class_name"],
                    identifier
                )
            )

            self.repository.set_data_property(
                individual,
                config["data_property"],
                name
            )

            self.message_label.configure(
                text=(
                    f"{element_type} cadastrado "
                    "com sucesso."
                )
            )

            self.name_entry.delete(
                0,
                "end"
            )

            self.identifier_label.configure(
                text="Identificador: -"
            )

            self.load_elements()

        except ValueError as error:

            self.message_label.configure(
                text=str(error)
            )

    def load_elements(self):

        for widget in (
            self.elements_frame.winfo_children()
        ):
            widget.destroy()

        element_type = (
            self.type_combobox.get()
        )

        if element_type not in self.ELEMENT_CONFIG:
            return

        config = self.ELEMENT_CONFIG[
            element_type
        ]

        try:

            individuals = (
                self.repository
                .get_individuals_by_class(
                    config["class_name"]
                )
            )

        except ValueError as error:

            error_label = ctk.CTkLabel(
                self.elements_frame,
                text=str(error)
            )

            error_label.pack(
                pady=20
            )

            return

        if not individuals:

            empty_label = ctk.CTkLabel(
                self.elements_frame,
                text=(
                    "Nenhum elemento desse "
                    "tipo foi cadastrado."
                )
            )

            empty_label.pack(
                pady=20
            )

            return

        for individual in sorted(
            individuals,
            key=lambda item: item.name
        ):

            stored_name = (
                self.repository.get_data_property(
                    individual,
                    config["data_property"]
                )
            )

            if stored_name is None:
                stored_name = self.format_identifier(
                    individual.name
                )

        element_frame = ctk.CTkFrame(
            self.elements_frame
        )

        element_frame.pack(
            fill="x",
            padx=8,
            pady=6
        )

        element_frame.grid_columnconfigure(
            0,
            weight=1
        )

        name_label = ctk.CTkLabel(
            element_frame,
            text=stored_name,
            font=("Arial",17,"bold"),
            anchor="w"
        )

        name_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(10,0)
        )

        identifier_label = ctk.CTkLabel(
            element_frame,
            text=individual.name,
            anchor="w"
        )

        identifier_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=15,
            pady=(0,10)
        )

        delete_button = ctk.CTkButton(
            element_frame,
            text="Excluir",
            width=80,
            fg_color="firebrick",
            hover_color="darkred",
            command=lambda ind=individual.name:
                self.delete_element(ind)
        )

        delete_button.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=15,
            pady=10
        )

    def format_identifier(
        self,
        identifier: str
    ) -> str:

        prefixes = [
            "theme_",
            "actor_",
            "director_",
            "country_",
            "language_"
        ]

        formatted = identifier

        for prefix in prefixes:

            if formatted.startswith(prefix):

                formatted = formatted[
                    len(prefix):
                ]

                break

        return (
            formatted
            .replace("_", " ")
            .title()
        )

    def delete_element(
        self,
        individual_name
    ):

        try:

            self.repository.delete_individual(
                individual_name
            )

            self.message_label.configure(
                text="Elemento removido."
            )

            self.load_elements()

        except ValueError as error:

            self.message_label.configure(
                text=str(error)
            )