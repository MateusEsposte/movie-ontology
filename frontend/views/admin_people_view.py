import re
import unicodedata

import customtkinter as ctk


class AdminPeopleView(ctk.CTkFrame):

    ROLE_CLASSES = {
        "Ator": "Actor",
        "Diretor": "Director",
        "Roteirista": "Screenwriter"
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
            text="Cadastro de pessoas",
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
            text="Nova pessoa",
            font=("Arial", 22, "bold")
        )

        form_title.pack(
            pady=(25, 20)
        )

        name_label = ctk.CTkLabel(
            self.form_frame,
            text="Nome completo"
        )

        name_label.pack(
            pady=(10, 5)
        )

        self.name_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Ex.: Clint Eastwood"
        )

        self.name_entry.pack(
            padx=25,
            pady=5,
            fill="x"
        )

        self.name_entry.bind(
            "<KeyRelease>",
            self.preview_identifier
        )

        self.identifier_label = ctk.CTkLabel(
            self.form_frame,
            text="Identificador: -",
            wraplength=260
        )

        self.identifier_label.pack(
            padx=20,
            pady=(10, 5)
        )

        birth_date_label = ctk.CTkLabel(
            self.form_frame,
            text="Data de nascimento"
        )

        birth_date_label.pack(
            pady=(18, 5)
        )

        self.birth_date_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="AAAA-MM-DD"
        )

        self.birth_date_entry.pack(
            padx=25,
            pady=5,
            fill="x"
        )

        nationality_label = ctk.CTkLabel(
            self.form_frame,
            text="Nacionalidade"
        )

        nationality_label.pack(
            pady=(18, 5)
        )

        self.nationality_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Ex.: American"
        )

        self.nationality_entry.pack(
            padx=25,
            pady=5,
            fill="x"
        )

        roles_label = ctk.CTkLabel(
            self.form_frame,
            text="Funções profissionais",
            font=("Arial", 16, "bold")
        )

        roles_label.pack(
            pady=(22, 8)
        )

        self.actor_checkbox = ctk.CTkCheckBox(
            self.form_frame,
            text="Ator"
        )

        self.actor_checkbox.pack(
            anchor="w",
            padx=35,
            pady=5
        )

        self.director_checkbox = ctk.CTkCheckBox(
            self.form_frame,
            text="Diretor"
        )

        self.director_checkbox.pack(
            anchor="w",
            padx=35,
            pady=5
        )

        self.screenwriter_checkbox = ctk.CTkCheckBox(
            self.form_frame,
            text="Roteirista"
        )

        self.screenwriter_checkbox.pack(
            anchor="w",
            padx=35,
            pady=5
        )

        self.save_button = ctk.CTkButton(
            self.form_frame,
            text="Cadastrar pessoa",
            command=self.save_person
        )

        self.save_button.pack(
            pady=(25, 10)
        )

        self.message_label = ctk.CTkLabel(
            self.form_frame,
            text="",
            wraplength=280
        )

        self.message_label.pack(
            padx=20,
            pady=10
        )

        # =====================================
        # Lista
        # =====================================

        self.people_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            label_text="Pessoas cadastradas"
        )

        self.people_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 10),
            pady=10
        )

        self.load_people()

    def generate_identifier(
        self,
        name: str
    ) -> str:

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

        return normalized_name.strip("_")

    def preview_identifier(
        self,
        event=None
    ):

        name = self.name_entry.get().strip()

        if not name:

            self.identifier_label.configure(
                text="Identificador: -"
            )

            return

        identifier = self.generate_identifier(
            name
        )

        self.identifier_label.configure(
            text=f"Identificador: {identifier}"
        )

    def get_selected_roles(self) -> list[str]:

        roles = []

        if self.actor_checkbox.get():
            roles.append("Actor")

        if self.director_checkbox.get():
            roles.append("Director")

        if self.screenwriter_checkbox.get():
            roles.append("Screenwriter")

        return roles

    def save_person(self):

        full_name = self.name_entry.get().strip()

        birth_date = (
            self.birth_date_entry.get().strip()
        )

        nationality = (
            self.nationality_entry.get().strip()
        )

        roles = self.get_selected_roles()

        if not full_name:

            self.message_label.configure(
                text="O nome completo é obrigatório."
            )

            return

        if not birth_date:

            self.message_label.configure(
                text=(
                    "A data de nascimento "
                    "é obrigatória."
                )
            )

            return

        if not nationality:

            self.message_label.configure(
                text="A nacionalidade é obrigatória."
            )

            return

        if not roles:

            self.message_label.configure(
                text=(
                    "Selecione pelo menos uma "
                    "função profissional."
                )
            )

            return

        identifier = self.generate_identifier(
            full_name
        )

        if self.repository.exists_individual(
            identifier
        ):

            self.message_label.configure(
                text=(
                    "Já existe uma pessoa com "
                    "esse identificador."
                )
            )

            return

        try:

            person = self.repository.create_individual(
                "Person",
                identifier
            )

            self.repository.set_data_property(
                person,
                "fullName",
                full_name
            )

            self.repository.set_data_property(
                person,
                "birthDate",
                birth_date
            )

            self.repository.set_data_property(
                person,
                "nationality",
                nationality
            )

            for role in roles:

                self.repository.add_class(
                    person,
                    role
                )

            self.repository.save()

            self.message_label.configure(
                text="Pessoa cadastrada com sucesso."
            )

            self.clear_form()

            self.load_people()

        except ValueError as error:

            self.message_label.configure(
                text=str(error)
            )

    def clear_form(self):

        self.name_entry.delete(
            0,
            "end"
        )

        self.birth_date_entry.delete(
            0,
            "end"
        )

        self.nationality_entry.delete(
            0,
            "end"
        )

        self.actor_checkbox.deselect()
        self.director_checkbox.deselect()
        self.screenwriter_checkbox.deselect()

        self.identifier_label.configure(
            text="Identificador: -"
        )

    def get_person_roles(
        self,
        person
    ) -> list[str]:

        roles = []

        if self.repository.has_class(
            person,
            "Actor"
        ):
            roles.append("Ator")

        if self.repository.has_class(
            person,
            "Director"
        ):
            roles.append("Diretor")

        if self.repository.has_class(
            person,
            "Screenwriter"
        ):
            roles.append("Roteirista")

        return roles

    def load_people(self):

        for widget in (
            self.people_frame.winfo_children()
        ):
            widget.destroy()

        people = (
            self.repository.get_individuals_by_class(
                "Person"
            )
        )

        # Usuários também são pessoas, mas não devem
        # aparecer na administração cinematográfica.
        people = [
            person
            for person in people
            if not self.repository.has_class(
                person,
                "User"
            )
        ]

        if not people:

            empty_label = ctk.CTkLabel(
                self.people_frame,
                text="Nenhuma pessoa cadastrada."
            )

            empty_label.pack(
                pady=25
            )

            return

        people.sort(
            key=lambda person: (
                self.repository.get_data_property(
                    person,
                    "fullName"
                )
                or person.name
            )
        )

        for person in people:

            full_name = (
                self.repository.get_data_property(
                    person,
                    "fullName"
                )
                or person.name
            )

            birth_date = (
                self.repository.get_data_property(
                    person,
                    "birthDate"
                )
                or "-"
            )

            nationality = (
                self.repository.get_data_property(
                    person,
                    "nationality"
                )
                or "-"
            )

            roles = self.get_person_roles(
                person
            )

            roles_text = (
                ", ".join(roles)
                if roles
                else "Sem função"
            )

            person_frame = ctk.CTkFrame(
                self.people_frame
            )

            person_frame.pack(
                fill="x",
                padx=8,
                pady=7
            )

            person_frame.grid_columnconfigure(
                0,
                weight=1
            )

            name_label = ctk.CTkLabel(
                person_frame,
                text=full_name,
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
                f"Identificador: {person.name}\n"
                f"Nascimento: {birth_date}\n"
                f"Nacionalidade: {nationality}\n"
                f"Funções: {roles_text}"
            )

            details_label = ctk.CTkLabel(
                person_frame,
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

            delete_button = ctk.CTkButton(
                person_frame,
                text="Excluir",
                width=80,
                command=lambda person_id=(
                    person.name
                ): self.delete_person(
                    person_id
                )
            )

            delete_button.grid(
                row=0,
                column=1,
                rowspan=2,
                padx=12,
                pady=12
            )

    def delete_person(
        self,
        person_id: str
    ):

        try:

            self.repository.remove_individual(
                person_id
            )

            self.message_label.configure(
                text="Pessoa excluída."
            )

            self.load_people()

        except ValueError as error:

            self.message_label.configure(
                text=str(error)
            )