from services.movie_services import MovieService
import customtkinter as ctk

class RatingsView(ctk.CTkFrame):
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
            text="Avaliações",
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

        self.current_rating_label = ctk.CTkLabel(
            self.details_frame,
            text="Nota atual: -",
            font=("Arial", 18)
        )

        self.current_rating_label.pack(
            pady=(20,10)
        )

        self.rating_combobox = ctk.CTkComboBox(
            self.details_frame,
            values=["1", "2", "3", "4", "5"]
        )

        self.rating_combobox.pack(
            pady=10
        )

        self.save_button = ctk.CTkButton(
            self.details_frame,
            text="Salvar avaliação",
            command=self.save_rating
        )

        self.save_button.pack(
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
        self.selected_movie = movie

        self.title_label.configure(
            text=movie.original_title
        )

        info = (
            f"Título Original: {movie.original_title}\n\n"
            f"Título em Português: {movie.portuguese_title}\n\n"
            f"Ano: {movie.release_date}\n\n"
            f"Duração: {movie.duration_minutes} minutos\n\n"
            f"Classificação: {movie.age_rating}\n\n"
            f"Diretor: {movie.director}\n\n"
            f"Tema: {movie.theme}\n\n"
            f"País: {movie.country}"
        )

        self.info_label.configure(
            text=info
        )

        self.load_rating()


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