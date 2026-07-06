from database.ontology_manager import OntologyManager


def main():
    print("=" * 40)
    print(" Movie Recommendation System")
    print("=" * 40)

    manager = OntologyManager("ontology/movie_ontology.rdf")
    manager.load()

    print("Classes encontradas:\n")

    for classe in manager.list_classes():
        print(f"- {classe.name}")


if __name__ == "__main__":
    main()
