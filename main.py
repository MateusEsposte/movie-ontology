from database.ontology_manager import OntologyManager
from database.ontology_repository import OntologyRepository


def print_separator():

    print("=" * 60)


def main():
    manager = OntologyManager("ontology/movie_ontology.rdf")
    manager.load()
    repository = OntologyRepository(manager)

    print("INDIVÍDUOS\n")
    
    individuals = repository.get_individuals()
    if len(individuals) == 0:
        print("Nenhum indivíduo cadastrado.")
    else:
        for individual in individuals:
            print(individual.name)


if __name__ == "__main__":
    main()
