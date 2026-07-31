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
            0,
            weight=1
        )

        self.movie_list_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            width=250
        )

        self.movie_list_frame.grid(
            row=0,
            column=0,
            sticky="nsw",
            padx=(10,5),
            pady=10
        )

        self.movie_buttons = []

        for movie in self.movies:
            button = ctk.CTkButton(
                self.movie_list_frame,
                text=movie.original_title,
                command=lambda m=movie: self.show_movie(m)
            )

            button.pack(
                fill="x",
                padx=5,
                pady=4
            )

            self.movie_buttons.append(button)


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

        self.watch_button.pack(
            pady=20
        )

        self.details_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5,10),
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

    def watch_movie(self):

        if self.selected_movie is None:
            return

        self.user_service.watch_movie(

            self.current_user.username,

            self.selected_movie.ontology_id

        )

        print(
            f"{self.current_user.username} assistiu {self.selected_movie.original_title}"
        )

        movies = self.user_service.get_watched_movies(
            self.current_user.username
        )

        print("\nFilmes assistidos:")

        for movie in movies:
            print(movie.original_title)

