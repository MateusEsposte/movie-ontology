import customtkinter as ctk

from services.recommendation_service import (
    RecommendationService
)


class HomeView(ctk.CTkFrame):
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

        self.recommendation_service = (
            RecommendationService(
                repository,
                repository.manager
            )
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            2,
            weight=1
        )

        welcome_label = ctk.CTkLabel(
            self,
            text=(
                f"Bem-vindo, "
                f"{self.current_user.name}"
            ),
            font=("Arial", 28, "bold")
        )

        welcome_label.grid(
            row=0,
            column=0,
            pady=(25, 8)
        )

        subtitle = ctk.CTkLabel(
            self,
            text=(
                "Filmes recomendados para você"
            ),
            font=("Arial", 18)
        )

        subtitle.grid(
            row=1,
            column=0,
            pady=(0, 15)
        )

        self.results_frame = (
            ctk.CTkScrollableFrame(
                self,
                label_text=(
                    "Recomendações por preferências"
                )
            )
        )

        self.results_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(0, 20)
        )

        self.load_recommendations()

    def load_recommendations(self):

        for widget in (
            self.results_frame.winfo_children()
        ):
            widget.destroy()

        recommendations = (
            self.recommendation_service
            .recommend_by_preferences(
                self.current_user.username
            )
        )

        if not recommendations:

            message = ctk.CTkLabel(
                self.results_frame,
                text=(
                    "Ainda não há recomendações.\n\n"
                    "Cadastre preferências ou avalie "
                    "filmes para personalizar o sistema."
                ),
                font=("Arial", 16),
                justify="center"
            )

            message.pack(
                pady=40
            )

            return

        # Mostra no máximo cinco filmes na Home.
        for position, item in enumerate(
            recommendations[:5],
            start=1
        ):

            movie, score = item

            card = ctk.CTkFrame(
                self.results_frame
            )

            card.pack(
                fill="x",
                padx=10,
                pady=8
            )

            title = ctk.CTkLabel(
                card,
                text=(
                    f"{position}. "
                    f"{movie.original_title}"
                ),
                font=("Arial", 19, "bold"),
                anchor="w"
            )

            title.pack(
                fill="x",
                padx=15,
                pady=(12, 5)
            )

            details = (
                f"Título em português: "
                f"{movie.portuguese_title}\n"
                f"Tema: {movie.theme}\n"
                f"Diretor: {movie.director}\n"
                f"Pontuação: {score}"
            )

            details_label = ctk.CTkLabel(
                card,
                text=details,
                justify="left",
                anchor="w"
            )

            details_label.pack(
                fill="x",
                padx=15,
                pady=(5, 12)
            )