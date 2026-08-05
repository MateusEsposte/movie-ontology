from services.movie_services import MovieService
import customtkinter as ctk


class MoviesView(ctk.CTkFrame):
    def __init__(self, master, repository, current_user, user_service):
        super().__init__(master)

        self.repository = repository
        self.current_user = current_user
        self.user_service = user_service

        self.movie_service = MovieService(
            repository
        )

        self.movies = self.movie_service.list_movies()

        self.filtered_movies = list(
            self.movies
        )

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
            text="Filmes",
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
            pady=(0,20)
        )

        self.main_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.main_frame.grid_columnconfigure(
            1,
            weight=3
        )

        self.main_frame.grid_rowconfigure(
            1,
            weight=1
        )

        self.filters_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.filters_frame.grid(
            row=0,
            column=0,
            sticky="new",
            padx=(10, 5),
            pady=10
        )

        self.search_entry = ctk.CTkEntry(
            self.filters_frame,
            placeholder_text="Buscar por título"
        )

        self.search_entry.pack(
            fill="x",
            padx=10,
            pady=(10, 5)
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.apply_filters
        )

        themes = sorted({
            movie.theme
            for movie in self.movies
            if movie.theme
        })

        self.theme_filter = ctk.CTkComboBox(
            self.filters_frame,
            values=["Todos"] + themes,
            command=self.apply_filters
        )

        self.theme_filter.set(
            "Todos"
        )

        self.theme_filter.pack(
            fill="x",
            padx=10,
            pady=5
        )

        countries = sorted({
            movie.country
            for movie in self.movies
            if movie.country
        })

        self.country_filter = ctk.CTkComboBox(
            self.filters_frame,
            values=["Todos"] + countries,
            command=self.apply_filters
        )

        self.country_filter.set(
            "Todos"
        )

        self.country_filter.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.movie_list_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            width=250
        )

        self.movie_list_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(10, 5),
            pady=(0, 10)
        )

        self.movie_buttons = []

        self.render_movie_list(
            self.movies
        )

        self.details_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.title_label = ctk.CTkLabel(
            self.details_frame,
            text="",
            font=("Arial", 24, "bold")
        )

        self.title_label.pack(
            pady=(20,10)
        )

        self.info_label = ctk.CTkLabel(
            self.details_frame,
            text="",
            justify="left",
            anchor="w"
        )

        self.info_label.pack(
            padx=20,
            pady=10,
            anchor="w"
        )

        self.watch_button = ctk.CTkButton(
            self.details_frame,
            text="Marcar como assistido",
            command=self.watch_movie
        )

        self.current_rating_label = ctk.CTkLabel(
            self.details_frame,
            text="Nota atual: -",
            font=("Arial", 16)
        )

        self.current_rating_label.pack(
            pady=(10, 5)
        )

        self.rating_combobox = ctk.CTkComboBox(
            self.details_frame,
            values=["1", "2", "3", "4", "5"]
        )

        self.rating_combobox.pack(
            pady=5
        )

        self.save_rating_button = ctk.CTkButton(
            self.details_frame,
            text="Salvar avaliação",
            command=self.save_rating
        )

        self.save_rating_button.pack(
            pady=(5, 20)
        )

        self.watch_button.pack(
            pady=20
        )

        self.details_frame.grid(
            row=0,
            column=1,
            rowspan=2,
            sticky="nsew",
            padx=(5, 10),
            pady=10
        )

        if self.movies:
            self.show_movie(
                self.movies[0]
            )

    def show_movie(self, movie):
        info = (
            f"Título Original: {movie.original_title}\n\n"
            f"Título em Português: {movie.portuguese_title}\n\n"
            f"Ano: {movie.release_date}\n\n"
            f"Duração: {movie.duration_minutes} minutos\n\n"
            f"Classificação: {movie.age_rating}\n\n"
            f"Tema: {movie.theme}\n\n"
            f"Diretor: {movie.director}\n\n"
            f"País: {movie.country}\n\n"
            f"Idiomas: {', '.join(movie.languages)}\n\n"
            f"Atores: {', '.join(movie.actors)}"
        )

        self.selected_movie = movie

        self.title_label.configure(
            text=movie.original_title
        )

        self.info_label.configure(
            text=info
        )

        self.update_watch_button()
        self.load_rating()

    def watch_movie(self):
        if self.selected_movie is None:
            return

        self.user_service.watch_movie(

            self.current_user.username,

            self.selected_movie.ontology_id

        )

        self.update_watch_button()
        self.load_rating()

    def update_watch_button(self):
        if self.selected_movie is None:
            return

        watched_movies = self.user_service.get_watched_movies(
            self.current_user.username
        )

        watched_ids = [
            movie.ontology_id
            for movie in watched_movies
        ]

        if self.selected_movie.ontology_id in watched_ids:
            self.watch_button.configure(
                text="Assistido ✓",
                state="disabled"
            )
            self.rating_combobox.configure(
                state="readonly"
            )

            self.save_rating_button.configure(
                state="normal"
            )

        else:
            self.watch_button.configure(
                text="Marcar como assistido",
                state="normal"
            )

            self.current_rating_label.configure(
                text="Assista ao filme para avaliá-lo."
            )

            self.rating_combobox.set("5")

            self.rating_combobox.configure(
                state="disabled"
            )

            self.save_rating_button.configure(
                state="disabled"
            )

    def render_movie_list(
        self,
        movies
    ):

        for widget in (
            self.movie_list_frame.winfo_children()
        ):
            widget.destroy()

        self.movie_buttons = []

        if not movies:

            empty_label = ctk.CTkLabel(
                self.movie_list_frame,
                text="Nenhum filme encontrado."
            )

            empty_label.pack(
                pady=20
            )

            return

        for movie in movies:

            button = ctk.CTkButton(
                self.movie_list_frame,
                text=movie.original_title,
                command=lambda m=movie: (
                    self.show_movie(m)
                )
            )

            button.pack(
                fill="x",
                padx=5,
                pady=4
            )

            self.movie_buttons.append(
                button
            )

    def apply_filters(
        self,
        event=None
    ):

        search_text = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )

        selected_theme = (
            self.theme_filter.get()
        )

        selected_country = (
            self.country_filter.get()
        )

        filtered = []

        for movie in self.movies:

            titles = (
                f"{movie.original_title} "
                f"{movie.portuguese_title}"
            ).lower()

            if (
                search_text
                and search_text not in titles
            ):
                continue

            if (
                selected_theme != "Todos"
                and movie.theme != selected_theme
            ):
                continue

            if (
                selected_country != "Todos"
                and movie.country != selected_country
            ):
                continue

            filtered.append(
                movie
            )

        self.filtered_movies = filtered

        self.render_movie_list(
            filtered
        )

        if filtered:
            self.show_movie(
                filtered[0]
            )
        else:
            self.selected_movie = None

            self.title_label.configure(
                text=""
            )

            self.info_label.configure(
                text=""
            )

            self.watch_button.configure(
                text="Marcar como assistido",
                state="disabled"
            )

    def load_rating(self):
        if self.selected_movie is None:
            return

        rating = self.user_service.get_movie_rating(
            self.current_user.username,
            self.selected_movie.ontology_id
        )

        if rating is None:
            self.current_rating_label.configure(
                text="Nota atual: -"
            )
            self.rating_combobox.set("5")
        else:
            self.current_rating_label.configure(
                text=f"Nota atual: {rating}"
            )
            self.rating_combobox.set(
                str(rating)
            )

    def save_rating(self):
        if self.selected_movie is None:
            return

        rating = int(
            self.rating_combobox.get()
        )

        self.user_service.rate_movie(
            self.current_user.username,
            self.selected_movie.ontology_id,
            rating
        )

        self.load_rating()

