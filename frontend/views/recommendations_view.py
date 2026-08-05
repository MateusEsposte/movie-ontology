import customtkinter as ctk

from services.recommendation_service import (
    RecommendationService
)


class RecommendationsView(ctk.CTkFrame):
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

        title = ctk.CTkLabel(
            self,
            text="Recomendações",
            font=("Arial", 28, "bold")
        )

        title.grid(
            row=0,
            column=0,
            pady=(20, 10)
        )

        self.description_label = ctk.CTkLabel(
            self,
            text=(
                "Escolha um método para gerar "
                "as recomendações."
            ),
            font=("Arial", 16)
        )

        self.description_label.grid(
            row=1,
            column=0,
            pady=(0, 15)
        )

        self.main_frame = ctk.CTkFrame(
            self
        )

        self.main_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(0, 20)
        )

        self.main_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.main_frame.grid_rowconfigure(
            0,
            weight=1
        )

        # ==============================
        # Painel de métodos
        # ==============================

        self.methods_frame = ctk.CTkFrame(
            self.main_frame,
            width=230
        )

        self.methods_frame.grid(
            row=0,
            column=0,
            sticky="ns",
            padx=(10, 5),
            pady=10
        )

        methods_title = ctk.CTkLabel(
            self.methods_frame,
            text="Método",
            font=("Arial", 21, "bold")
        )

        methods_title.pack(
            padx=20,
            pady=(25, 20)
        )

        self.preferences_button = ctk.CTkButton(
            self.methods_frame,
            text="Por preferências",
            command=self.recommend_by_preferences
        )

        self.preferences_button.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.friends_button = ctk.CTkButton(
            self.methods_frame,
            text="Por amigos",
            command=self.recommend_by_friends
        )

        self.friends_button.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.community_button = ctk.CTkButton(
            self.methods_frame,
            text="Pela comunidade",
            command=self.recommend_by_community
        )

        self.community_button.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.status_label = ctk.CTkLabel(
            self.methods_frame,
            text="",
            wraplength=180
        )

        self.status_label.pack(
            padx=20,
            pady=20
        )

        # ==============================
        # Painel de resultados
        # ==============================

        self.results_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            label_text="Filmes recomendados"
        )

        self.results_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 10),
            pady=10
        )

        self.show_empty_message(
            "Escolha um método de recomendação."
        )

    def clear_results(self):

        for widget in (
            self.results_frame.winfo_children()
        ):
            widget.destroy()

    def show_empty_message(
        self,
        message: str
    ):

        self.clear_results()

        label = ctk.CTkLabel(
            self.results_frame,
            text=message,
            font=("Arial", 16)
        )

        label.pack(
            pady=30
        )

    def show_recommendations(
        self,
        recommendations,
        method_name: str
    ):

        self.clear_results()

        if not recommendations:

            self.show_empty_message(
                "Nenhuma recomendação encontrada."
            )

            self.status_label.configure(
                text=(
                    "Não há dados suficientes para "
                    f"recomendações por {method_name.lower()}."
                )
            )

            return

        self.status_label.configure(
            text=(
                f"{len(recommendations)} "
                "recomendação(ões) encontrada(s)."
            )
        )

        for position, item in enumerate(
            recommendations,
            start=1
        ):
            movie, score = item

            recommendation_frame = ctk.CTkFrame(
                self.results_frame
            )

            recommendation_frame.pack(
                fill="x",
                padx=8,
                pady=7
            )

            recommendation_frame.grid_columnconfigure(
                0,
                weight=1
            )

            title = ctk.CTkLabel(
                recommendation_frame,
                text=(
                    f"{position}. "
                    f"{movie.original_title}"
                ),
                font=("Arial", 19, "bold"),
                anchor="w"
            )

            title.grid(
                row=0,
                column=0,
                sticky="ew",
                padx=15,
                pady=(12, 5)
            )

            score_text = self.format_score(
                score
            )

            details = (
                f"Título em português: "
                f"{movie.portuguese_title}\n"
                f"Ano: {movie.release_date}\n"
                f"Tema: {movie.theme}\n"
                f"Diretor: {movie.director}\n"
                f"Pontuação: {score_text}\n"
                f"Método: {method_name}"
            )

            details_label = ctk.CTkLabel(
                recommendation_frame,
                text=details,
                justify="left",
                anchor="w"
            )

            details_label.grid(
                row=1,
                column=0,
                sticky="ew",
                padx=15,
                pady=(5, 12)
            )

    def format_score(
        self,
        score
    ) -> str:

        if isinstance(score, float):
            return f"{score:.2f}"

        return str(score)

    def recommend_by_preferences(self):

        try:

            recommendations = (
                self.recommendation_service
                .recommend_by_preferences(
                    self.current_user.username
                )
            )

            self.show_recommendations(
                recommendations,
                "Preferências"
            )

        except ValueError as error:

            self.show_empty_message(
                str(error)
            )

    def recommend_by_friends(self):

        try:

            recommendations = (
                self.recommendation_service
                .recommend_by_friends(
                    self.current_user.username
                )
            )

            self.show_recommendations(
                recommendations,
                "Amigos"
            )

        except ValueError as error:

            self.show_empty_message(
                str(error)
            )

    def recommend_by_community(self):

        try:

            recommendations = (
                self.recommendation_service
                .recommend_by_community(
                    self.current_user.username
                )
            )

            self.show_recommendations(
                recommendations,
                "Comunidade"
            )

        except ValueError as error:

            self.show_empty_message(
                str(error)
            )