from database.ontology_manager import OntologyManager
from database.ontology_repository import OntologyRepository


def print_separator():

    print("=" * 60)


def main():
    print_separator()
    print("MOVIE RECOMMENDATION SYSTEM")
    print_separator()

    manager = OntologyManager("ontology/movie_ontology.rdf")
    manager.load()
    repository = OntologyRepository(manager)

    print_separator()
    print("CLASSES\n")
    for cls in repository.get_classes():
        print(cls.name)


    print_separator()
    print("OBJECT PROPERTIES\n")
    for prop in repository.get_object_properties():
        print(prop.name)


    print_separator()
    print("DATA PROPERTIES\n")
    for prop in repository.get_data_properties():
        print(prop.name)


    print_separator()
    print("INDIVÍDUOS\n")
    individuals = repository.get_individuals()
    if len(individuals) == 0:
        print("Nenhum indivíduo cadastrado.")
    else:
        for individual in individuals:
            print(individual.name)


if __name__ == "__main__":
    main()
