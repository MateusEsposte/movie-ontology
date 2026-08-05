import re
import unicodedata

import customtkinter as ctk
from services.movie_services import MovieService
import csv
from tkinter import filedialog


class AdminMoviesView(ctk.CTkFrame):

    def __init__(
        self,
        master,
        repository
    ):
        super().__init__(master)

        self.repository = repository

        self.movie_service = MovieService(
            repository
        )

        self.actor_variables = {}
        self.language_variables = {}

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
            text="Cadastro de filmes",
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

        self.form_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            label_text="Novo filme"
        )

        self.form_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(10, 5),
            pady=10
        )

        self.original_title_entry = (
            self.create_entry(
                "Título original",
                "Ex.: The Shawshank Redemption"
            )
        )

        self.original_title_entry.bind(
            "<KeyRelease>",
            self.preview_identifier
        )

        self.identifier_label = ctk.CTkLabel(
            self.form_frame,
            text="Identificador: -",
            wraplength=300
        )

        self.identifier_label.pack(
            padx=20,
            pady=(5, 10)
        )

        self.portuguese_title_entry = (
            self.create_entry(
                "Título em português",
                "Ex.: Um Sonho de Liberdade"
            )
        )

        self.release_date_entry = (
            self.create_entry(
                "Ano de lançamento",
                "Ex.: 1994"
            )
        )

        self.duration_entry = (
            self.create_entry(
                "Duração em minutos",
                "Ex.: 142"
            )
        )

        self.age_rating_entry = (
            self.create_entry(
                "Classificação indicativa",
                "Ex.: 14"
            )
        )

        self.create_field_label(
            "Tema"
        )

        self.theme_combobox = ctk.CTkComboBox(
            self.form_frame,
            values=[]
        )

        self.theme_combobox.pack(
            fill="x",
            padx=25,
            pady=5
        )

        self.create_field_label(
            "Diretor"
        )

        self.director_combobox = ctk.CTkComboBox(
            self.form_frame,
            values=[]
        )

        self.director_combobox.pack(
            fill="x",
            padx=25,
            pady=5
        )

        self.create_field_label(
            "País de origem"
        )

        self.country_combobox = ctk.CTkComboBox(
            self.form_frame,
            values=[]
        )

        self.country_combobox.pack(
            fill="x",
            padx=25,
            pady=5
        )

        # =====================================
        # Atores
        # =====================================

        actors_label = ctk.CTkLabel(
            self.form_frame,
            text="Atores",
            font=("Arial", 16, "bold")
        )

        actors_label.pack(
            pady=(25, 8)
        )

        self.actors_frame = ctk.CTkScrollableFrame(
            self.form_frame,
            height=150
        )

        self.actors_frame.pack(
            fill="x",
            padx=25,
            pady=5
        )

        # =====================================
        # Idiomas
        # =====================================

        languages_label = ctk.CTkLabel(
            self.form_frame,
            text="Idiomas",
            font=("Arial", 16, "bold")
        )

        languages_label.pack(
            pady=(25, 8)
        )

        self.languages_frame = (
            ctk.CTkScrollableFrame(
                self.form_frame,
                height=120
            )
        )

        self.languages_frame.pack(
            fill="x",
            padx=25,
            pady=5
        )

        self.save_button = ctk.CTkButton(
            self.form_frame,
            text="Cadastrar filme",
            command=self.save_movie
        )

        self.save_button.pack(
            pady=(30, 10)
        )

        self.import_button = ctk.CTkButton(
            self.form_frame,
            text="Importar filmes de CSV",
            command=self.import_movies_from_csv
        )

        self.import_button.pack(
            pady=(5, 10)
        )

        self.message_label = ctk.CTkLabel(
            self.form_frame,
            text="",
            wraplength=320
        )

        self.message_label.pack(
            padx=20,
            pady=(5, 20)
        )

        # =====================================
        # Filmes cadastrados
        # =====================================

        self.movies_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            label_text="Filmes cadastrados"
        )

        self.movies_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 10),
            pady=10
        )

        self.load_selection_data()
        self.load_movies()

    def create_field_label(
        self,
        text: str
    ):

        label = ctk.CTkLabel(
            self.form_frame,
            text=text
        )

        label.pack(
            pady=(18, 5)
        )

    def create_entry(
        self,
        label_text: str,
        placeholder: str
    ):

        self.create_field_label(
            label_text
        )

        entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text=placeholder
        )

        entry.pack(
            fill="x",
            padx=25,
            pady=5
        )

        return entry

    def generate_identifier(
        self,
        title: str
    ) -> str:

        normalized = (
            unicodedata.normalize(
                "NFKD",
                title
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

        normalized = re.sub(
            r"[^a-z0-9]+",
            "_",
            normalized
        )

        normalized = normalized.strip("_")

        return f"film_{normalized}"

    def preview_identifier(
        self,
        event=None
    ):

        title = (
            self.original_title_entry
            .get()
            .strip()
        )

        if not title:

            self.identifier_label.configure(
                text="Identificador: -"
            )

            return

        identifier = self.generate_identifier(
            title
        )

        self.identifier_label.configure(
            text=f"Identificador: {identifier}"
        )

    def load_selection_data(self):

        self.load_themes()
        self.load_directors()
        self.load_countries()
        self.load_actors()
        self.load_languages()

    def get_display_name(
        self,
        individual,
        property_name: str
    ) -> str:

        value = self.repository.get_data_property(
            individual,
            property_name
        )

        if value:
            return str(value)

        return (
            individual.name
            .replace("_", " ")
            .title()
        )

    def configure_combobox(
        self,
        combobox,
        mapping: dict
    ):

        values = list(
            mapping.keys()
        )

        combobox.configure(
            values=values
        )

        if values:

            combobox.set(
                values[0]
            )

        else:

            combobox.set(
                ""
            )

    def load_themes(self):

        self.theme_mapping = {}

        themes = (
            self.repository
            .get_individuals_by_class(
                "Theme"
            )
        )

        for theme in themes:

            display_name = self.get_display_name(
                theme,
                "themeName"
            )

            self.theme_mapping[
                display_name
            ] = theme.name

        self.configure_combobox(
            self.theme_combobox,
            self.theme_mapping
        )

    def load_directors(self):

        self.director_mapping = {}

        directors = (
            self.repository
            .get_individuals_by_class(
                "Director"
            )
        )

        for director in directors:

            display_name = self.get_display_name(
                director,
                "fullName"
            )

            self.director_mapping[
                display_name
            ] = director.name

        self.configure_combobox(
            self.director_combobox,
            self.director_mapping
        )

    def load_countries(self):

        self.country_mapping = {}

        countries = (
            self.repository
            .get_individuals_by_class(
                "CountryOfOrigin"
            )
        )

        for country in countries:

            display_name = self.get_display_name(
                country,
                "countryName"
            )

            self.country_mapping[
                display_name
            ] = country.name

        self.configure_combobox(
            self.country_combobox,
            self.country_mapping
        )

    def load_actors(self):

        for widget in (
            self.actors_frame.winfo_children()
        ):
            widget.destroy()

        self.actor_variables = {}

        actors = (
            self.repository
            .get_individuals_by_class(
                "Actor"
            )
        )

        actors.sort(
            key=lambda actor: (
                self.get_display_name(
                    actor,
                    "fullName"
                )
            )
        )

        if not actors:

            label = ctk.CTkLabel(
                self.actors_frame,
                text="Nenhum ator cadastrado."
            )

            label.pack(
                pady=15
            )

            return

        for actor in actors:

            variable = ctk.BooleanVar(
                value=False
            )

            display_name = self.get_display_name(
                actor,
                "fullName"
            )

            checkbox = ctk.CTkCheckBox(
                self.actors_frame,
                text=display_name,
                variable=variable
            )

            checkbox.pack(
                anchor="w",
                padx=10,
                pady=4
            )

            self.actor_variables[
                actor.name
            ] = variable

    def load_languages(self):

        for widget in (
            self.languages_frame
            .winfo_children()
        ):
            widget.destroy()

        self.language_variables = {}

        languages = (
            self.repository
            .get_individuals_by_class(
                "Language"
            )
        )

        languages.sort(
            key=lambda language: (
                self.get_display_name(
                    language,
                    "languageName"
                )
            )
        )

        if not languages:

            label = ctk.CTkLabel(
                self.languages_frame,
                text="Nenhum idioma cadastrado."
            )

            label.pack(
                pady=15
            )

            return

        for language in languages:

            variable = ctk.BooleanVar(
                value=False
            )

            display_name = self.get_display_name(
                language,
                "languageName"
            )

            checkbox = ctk.CTkCheckBox(
                self.languages_frame,
                text=display_name,
                variable=variable
            )

            checkbox.pack(
                anchor="w",
                padx=10,
                pady=4
            )

            self.language_variables[
                language.name
            ] = variable

    def get_selected_ids(
        self,
        variables: dict
    ) -> list[str]:

        return [
            individual_id
            for individual_id, variable
            in variables.items()
            if variable.get()
        ]

    def validate_form(
        self
    ) -> str | None:

        original_title = (
            self.original_title_entry
            .get()
            .strip()
        )

        portuguese_title = (
            self.portuguese_title_entry
            .get()
            .strip()
        )

        release_date = (
            self.release_date_entry
            .get()
            .strip()
        )

        duration = (
            self.duration_entry
            .get()
            .strip()
        )

        age_rating = (
            self.age_rating_entry
            .get()
            .strip()
        )

        if not original_title:
            return "O título original é obrigatório."

        if not portuguese_title:
            return "O título em português é obrigatório."

        if not release_date:
            return "O ano de lançamento é obrigatório."

        if not duration.isdigit():
            return "A duração deve ser um número inteiro."

        if int(duration) <= 0:
            return "A duração deve ser maior que zero."

        if not age_rating:
            return (
                "A classificação indicativa "
                "é obrigatória."
            )

        if not self.theme_combobox.get():
            return "Cadastre e selecione um tema."

        if not self.director_combobox.get():
            return "Cadastre e selecione um diretor."

        if not self.country_combobox.get():
            return "Cadastre e selecione um país."

        if not self.get_selected_ids(
            self.actor_variables
        ):
            return "Selecione pelo menos um ator."

        return None

    def save_movie(self):

        validation_error = self.validate_form()

        if validation_error:

            self.message_label.configure(
                text=validation_error
            )

            return

        original_title = (
            self.original_title_entry
            .get()
            .strip()
        )

        portuguese_title = (
            self.portuguese_title_entry
            .get()
            .strip()
        )

        release_date = (
            self.release_date_entry
            .get()
            .strip()
        )

        duration = int(
            self.duration_entry.get()
        )

        age_rating = (
            self.age_rating_entry
            .get()
            .strip()
        )

        movie_id = self.generate_identifier(
            original_title
        )

        if self.repository.exists_individual(
            movie_id
        ):

            self.message_label.configure(
                text=(
                    "Já existe um filme com "
                    "esse identificador."
                )
            )

            return

        theme_id = self.theme_mapping.get(
            self.theme_combobox.get()
        )

        director_id = self.director_mapping.get(
            self.director_combobox.get()
        )

        country_id = self.country_mapping.get(
            self.country_combobox.get()
        )

        actor_ids = self.get_selected_ids(
            self.actor_variables
        )

        language_ids = self.get_selected_ids(
            self.language_variables
        )

        try:

            self.movie_service.create_movie(
                    original_title=original_title,
                    portuguese_title=portuguese_title,
                    release_date=release_date,
                    duration_minutes=duration,
                    age_rating=age_rating,
                    country=country_id,
                    languages=language_ids,
                    theme=theme_id,
                    director=director_id,
                    actors=actor_ids
                )

            self.message_label.configure(
                text="Filme cadastrado com sucesso."
            )

            self.clear_form()
            self.load_movies()

        except ValueError as error:

            self.message_label.configure(
                text=str(error)
            )

    def clear_form(self):

        entries = [
            self.original_title_entry,
            self.portuguese_title_entry,
            self.release_date_entry,
            self.duration_entry,
            self.age_rating_entry
        ]

        for entry in entries:

            entry.delete(
                0,
                "end"
            )

        for variable in (
            self.actor_variables.values()
        ):
            variable.set(False)

        for variable in (
            self.language_variables.values()
        ):
            variable.set(False)

        self.identifier_label.configure(
            text="Identificador: -"
        )

    def load_movies(self):

        for widget in self.movies_frame.winfo_children():
            widget.destroy()

        try:
            movies = self.movie_service.list_movies()

        except ValueError as error:
            error_label = ctk.CTkLabel(
                self.movies_frame,
                text=str(error)
            )

            error_label.pack(
                pady=25
            )

            return

        if not movies:
            empty_label = ctk.CTkLabel(
                self.movies_frame,
                text="Nenhum filme cadastrado."
            )

            empty_label.pack(
                pady=25
            )

            return

        movies.sort(
            key=lambda movie: (
                movie.original_title or ""
            ).casefold()
        )

        for movie in movies:

            movie_frame = ctk.CTkFrame(
                self.movies_frame
            )

            movie_frame.pack(
                fill="x",
                padx=8,
                pady=7
            )

            movie_frame.grid_columnconfigure(
                0,
                weight=1
            )

            title_label = ctk.CTkLabel(
                movie_frame,
                text=movie.original_title or movie.ontology_id,
                font=("Arial", 18, "bold"),
                anchor="w"
            )

            title_label.grid(
                row=0,
                column=0,
                sticky="ew",
                padx=15,
                pady=(12, 4)
            )

            actors_text = (
                ", ".join(
                    str(actor)
                    for actor in movie.actors
                    if actor
                )
                if movie.actors
                else "-"
            )

            languages_text = (
                ", ".join(
                    str(language)
                    for language in movie.languages
                    if language
                )
                if movie.languages
                else "-"
            )

            details = (
                f"Título em português: "
                f"{movie.portuguese_title or '-'}\n"
                f"Ano: {movie.release_date or '-'}\n"
                f"Duração: "
                f"{movie.duration_minutes or '-'} minutos\n"
                f"Classificação: {movie.age_rating or '-'}\n"
                f"Tema: {movie.theme or '-'}\n"
                f"Diretor: {movie.director or '-'}\n"
                f"Atores: {actors_text}\n"
                f"País: {movie.country or '-'}\n"
                f"Idiomas: {languages_text}\n"
                f"Identificador: {movie.ontology_id}"
            )

            details_label = ctk.CTkLabel(
                movie_frame,
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
                movie_frame,
                text="Excluir",
                width=80,
                command=lambda movie_id=movie.ontology_id: (
                    self.delete_movie(movie_id)
                )
            )

            delete_button.grid(
                row=0,
                column=1,
                rowspan=2,
                padx=12,
                pady=12
            )

    def delete_movie(
        self,
        movie_id: str
    ):

        try:

            self.repository.remove_individual(
                movie_id
            )

            self.message_label.configure(
                text="Filme excluído com sucesso."
            )

            self.load_movies()

        except ValueError as error:

            self.message_label.configure(
                text=str(error)
            )

    def normalize_csv_value(
        self,
        value
    ) -> str:

        if value is None:
            return ""

        return str(value).strip()

    def find_mapping_id(
        self,
        mapping: dict,
        display_name: str,
        field_name: str
    ) -> str:

        normalized_name = (
            self.normalize_csv_value(
                display_name
            )
        )

        if not normalized_name:
            raise ValueError(
                f"O campo '{field_name}' está vazio."
            )

        # Primeiro tenta localizar exatamente
        # como o nome aparece na interface.
        individual_id = mapping.get(
            normalized_name
        )

        if individual_id is not None:
            return individual_id

        # Depois tenta ignorando diferenças
        # entre maiúsculas e minúsculas.
        normalized_comparison = (
            normalized_name.casefold()
        )

        for displayed_value, mapped_id in (
            mapping.items()
        ):

            if (
                str(displayed_value)
                .strip()
                .casefold()
                == normalized_comparison
            ):
                return mapped_id

        raise ValueError(
            f"{field_name} '{normalized_name}' "
            "não encontrado na ontologia."
        )

    def find_actor_ids(
        self,
        actors_text: str
    ) -> list[str]:

        actor_names = [
            actor.strip()
            for actor in actors_text.split("|")
            if actor.strip()
        ]

        if not actor_names:
            raise ValueError(
                "O filme deve possuir pelo menos um ator."
            )

        actor_mapping = {}

        actors = (
            self.repository
            .get_individuals_by_class(
                "Actor"
            )
        )

        for actor in actors:

            display_name = self.get_display_name(
                actor,
                "fullName"
            )

            actor_mapping[
                display_name
            ] = actor.name

        actor_ids = []

        for actor_name in actor_names:

            actor_id = self.find_mapping_id(
                actor_mapping,
                actor_name,
                "Ator"
            )

            actor_ids.append(
                actor_id
            )

        return actor_ids

    def find_language_ids(
        self,
        languages_text: str
    ) -> list[str]:

        language_names = [
            language.strip()
            for language in languages_text.split("|")
            if language.strip()
        ]

        if not language_names:
            raise ValueError(
                "O filme deve possuir pelo menos um idioma."
            )

        language_mapping = {}

        languages = (
            self.repository
            .get_individuals_by_class(
                "Language"
            )
        )

        for language in languages:

            display_name = self.get_display_name(
                language,
                "languageName"
            )

            language_mapping[
                display_name
            ] = language.name

        language_ids = []

        for language_name in language_names:

            language_id = self.find_mapping_id(
                language_mapping,
                language_name,
                "Idioma"
            )

            language_ids.append(
                language_id
            )

        return language_ids

    def import_movies_from_csv(self):

        csv_path = filedialog.askopenfilename(
            title="Selecionar arquivo de filmes",
            filetypes=[
                (
                    "Arquivos CSV",
                    "*.csv"
                ),
                (
                    "Todos os arquivos",
                    "*.*"
                )
            ]
        )

        if not csv_path:
            return

        imported_count = 0
        skipped_count = 0
        errors = []

        required_columns = {
            "original_title",
            "portuguese_title",
            "release_date",
            "duration_minutes",
            "age_rating",
            "theme",
            "director",
            "country",
            "actors",
            "languages"
        }

        try:

            with open(
                csv_path,
                mode="r",
                encoding="utf-8-sig",
                newline=""
            ) as csv_file:

                reader = csv.DictReader(
                    csv_file
                )

                if reader.fieldnames is None:

                    self.message_label.configure(
                        text=(
                            "O arquivo CSV não possui "
                            "cabeçalho."
                        )
                    )

                    return

                available_columns = {
                    column.strip()
                    for column in reader.fieldnames
                    if column is not None
                }

                missing_columns = (
                    required_columns
                    - available_columns
                )

                if missing_columns:

                    missing_text = ", ".join(
                        sorted(missing_columns)
                    )

                    self.message_label.configure(
                        text=(
                            "Colunas ausentes no CSV: "
                            f"{missing_text}"
                        )
                    )

                    return

                for line_number, row in enumerate(
                    reader,
                    start=2
                ):

                    try:

                        original_title = (
                            self.normalize_csv_value(
                                row.get(
                                    "original_title"
                                )
                            )
                        )

                        portuguese_title = (
                            self.normalize_csv_value(
                                row.get(
                                    "portuguese_title"
                                )
                            )
                        )

                        release_date = (
                            self.normalize_csv_value(
                                row.get(
                                    "release_date"
                                )
                            )
                        )

                        duration_text = (
                            self.normalize_csv_value(
                                row.get(
                                    "duration_minutes"
                                )
                            )
                        )

                        age_rating = (
                            self.normalize_csv_value(
                                row.get(
                                    "age_rating"
                                )
                            )
                        )

                        theme_name = (
                            self.normalize_csv_value(
                                row.get(
                                    "theme"
                                )
                            )
                        )

                        director_name = (
                            self.normalize_csv_value(
                                row.get(
                                    "director"
                                )
                            )
                        )

                        country_name = (
                            self.normalize_csv_value(
                                row.get(
                                    "country"
                                )
                            )
                        )

                        actors_text = (
                            self.normalize_csv_value(
                                row.get(
                                    "actors"
                                )
                            )
                        )

                        languages_text = (
                            self.normalize_csv_value(
                                row.get(
                                    "languages"
                                )
                            )
                        )

                        if not original_title:
                            raise ValueError(
                                "Título original vazio."
                            )

                        try:

                            duration_minutes = int(
                                duration_text
                            )

                        except ValueError as error:

                            raise ValueError(
                                "A duração deve ser "
                                "um número inteiro."
                            ) from error

                        movie_id = (
                            self.generate_identifier(
                                original_title
                            )
                        )

                        if (
                            self.repository
                            .exists_individual(
                                movie_id
                            )
                        ):
                            skipped_count += 1
                            continue

                        theme_id = self.find_mapping_id(
                            self.theme_mapping,
                            theme_name,
                            "Tema"
                        )

                        director_id = (
                            self.find_mapping_id(
                                self.director_mapping,
                                director_name,
                                "Diretor"
                            )
                        )

                        country_id = (
                            self.find_mapping_id(
                                self.country_mapping,
                                country_name,
                                "País"
                            )
                        )

                        actor_ids = (
                            self.find_actor_ids(
                                actors_text
                            )
                        )

                        language_ids = (
                            self.find_language_ids(
                                languages_text
                            )
                        )

                        self.movie_service.create_movie(
                            original_title=original_title,
                            portuguese_title=(
                                portuguese_title
                            ),
                            release_date=release_date,
                            duration_minutes=(
                                duration_minutes
                            ),
                            age_rating=age_rating,
                            country=country_id,
                            languages=language_ids,
                            theme=theme_id,
                            director=director_id,
                            actors=actor_ids
                        )

                        imported_count += 1

                    except (
                        ValueError,
                        TypeError
                    ) as error:

                        errors.append(
                            (
                                line_number,
                                original_title
                                if "original_title"
                                in locals()
                                else "",
                                str(error)
                            )
                        )

        except (
            OSError,
            csv.Error
        ) as error:

            self.message_label.configure(
                text=(
                    "Não foi possível ler o CSV: "
                    f"{error}"
                )
            )

            return

        self.load_movies()

        summary = (
            f"Importados: {imported_count}\n"
            f"Ignorados: {skipped_count}\n"
            f"Erros: {len(errors)}"
        )

        if errors:

            print(
                "\n=== ERROS NA IMPORTAÇÃO ==="
            )

            for (
                line_number,
                movie_title,
                error_message
            ) in errors:

                print(
                    f"Linha {line_number} | "
                    f"{movie_title or 'Sem título'} | "
                    f"{error_message}"
                )

            summary += (
                "\n\nConsulte o terminal para "
                "ver os erros."
            )

        self.message_label.configure(
            text=summary
        )


