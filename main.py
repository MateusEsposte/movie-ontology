from database.ontology_manager import OntologyManager
from database.ontology_repository import OntologyRepository
from frontend.app import App
import customtkinter as ctk


def main():
    manager = OntologyManager("ontology/movie_ontology.rdf")

    manager.load()

    repository = OntologyRepository(manager)
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = App(
        repository,
        manager
    )

    app.mainloop()



if __name__ == "__main__":
    main()
