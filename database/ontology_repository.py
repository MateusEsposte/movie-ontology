from owlready2 import destroy_entity

class OntologyRepository:
    def __init__(self, manager):
        self.manager = manager
        self.ontology = manager.ontology

    
    def get_classes(self):
        return list(self.ontology.classes())
    

    def get_object_properties(self):
        return list(self.ontology.object_properties())


    def get_data_properties(self):
        return list(self.ontology.data_properties())
    

    def get_individuals(self):
        return list(self.ontology.individuals())
    

    def get_class_by_name(self, class_name: str):
        """Retorna uma classe da ontologia pelo nome."""
        for cls in self.ontology.classes():
            if cls.name == class_name:
                return cls

        return None
    

    def get_object_property_by_name(self, property_name: str):
        """Retorna uma Object Property pelo nome."""
        for prop in self.ontology.object_properties():
            if prop.name == property_name:
                return prop

        return None
    

    def get_data_property_by_name(self, property_name: str):
        """Retorna uma Data Property pelo nome."""
        for prop in self.ontology.data_properties():
            if prop.name == property_name:
                return prop

        return None
    

    def get_individual_by_name(self, individual_name: str):
        """Retorna um indivíduo pelo nome."""
        for individual in self.ontology.individuals():
            if individual.name == individual_name:
                return individual

        return None
    

    def exists_individual(self, individual_name: str):
        """Verifica se um indivíduo existe."""
        return self.get_individual_by_name(individual_name) is not None
    

    def create_individual(self, class_name: str, individual_name: str):
        """Cria um novo indivíduo em uma classe da ontologia."""
        ontology_class = self.get_class_by_name(class_name)

        if ontology_class is None:
            raise ValueError(f"Classe '{class_name}' não encontrada.")

        if self.exists_individual(individual_name):
            raise ValueError(
                f"O indivíduo '{individual_name}' já existe."
            )

        return ontology_class(individual_name)
    

    def list_individuals_by_class(self, class_name: str):
        """Lista todos os indivíduos de uma determinada classe."""
        ontology_class = self.get_class_by_name(class_name)

        if ontology_class is None:
            raise ValueError(f"Classe '{class_name}' não encontrada.")

        return list(ontology_class.instances())
    

    def create_individual(self, class_name: str, individual_name: str):
        ontology_class = self.get_class_by_name(class_name)

        if ontology_class is None:
            raise ValueError(f"Classe '{class_name}' não encontrada.")

        if self.exists_individual(individual_name):
            raise ValueError(f"O indivíduo '{individual_name}' já existe.")

        individual = ontology_class(individual_name)

        self.save()

        return individual
    

    def list_individuals_by_class(self, class_name: str):
        ontology_class = self.get_class_by_name(class_name)

        if ontology_class is None:
            raise ValueError(f"Classe '{class_name}' não encontrada.")

        return list(ontology_class.instances())
    

    def set_data_property(self, individual, property_name: str, value):
        data_property = self.get_data_property_by_name(property_name)
        if data_property is None:
            raise ValueError(
                f"Data Property '{property_name}' não encontrada."
            )

        setattr(individual, property_name, [value])

        self.save()


    def get_data_property(self, individual, property_name: str):
        data_property = self.get_data_property_by_name(
            property_name
        )

        if data_property is None:
            raise ValueError(
                f"Data Property '{property_name}' não encontrada."
            )

        values = data_property[individual]

        if len(values) == 0:
            return None

        return values[0]
    

    def add_object_property(self, source, property_name: str, target):

        if not hasattr(source, property_name):
            raise ValueError(
                f"Object Property '{property_name}' não encontrada."
            )
        getattr(source, property_name).append(target)
        self.save()


    def remove_object_property(self, source, property_name: str, target):
        relation = getattr(source, property_name)

        if target in relation:
            relation.remove(target)

    
    def add_class(self, individual, class_name: str):
        """Adiciona uma classe a um indivíduo existente."""
        ontology_class = self.get_class_by_name(class_name)

        if ontology_class is None:
            raise ValueError(f"Classe '{class_name}' não encontrada.")

        if ontology_class not in individual.is_a:
            individual.is_a.append(ontology_class)

    
    def has_class(self, individual, class_name: str):
        ontology_class = self.get_class_by_name(class_name)

        if ontology_class is None:
            return False

        return ontology_class in individual.is_a
    

    def list_individuals_by_class(self, class_name: str):
        ontology_class = self.find_class(class_name)

        if ontology_class is None:
            raise ValueError(f"Classe '{class_name}' não encontrada.")

        return list(ontology_class.instances())
    

    def connect_individuals(self, source_individual, property_name: str, target_individual_name: str):
        """Cria uma Object Property entre dois indivíduos."""

        target = self.get_individual_by_name(target_individual_name)

        if target is None:
            raise ValueError(
                f"Indivíduo '{target_individual_name}' não encontrado."
            )

        self.add_object_property(
            source_individual,
            property_name,
            target
        )


    def save(self):
        self.manager.save()


    def get_individuals_by_class(self, class_name: str):
        ontology_class = self.get_class_by_name(class_name)

        if ontology_class is None:
            raise ValueError(
                f"Classe '{class_name}' não encontrada."
            )

        return list(ontology_class.instances())
    
    
    def remove_individual(self, individual_name: str):
        individual = self.get_individual_by_name(
            individual_name
        )

        if individual is None:
            raise ValueError(
                f"Indivíduo '{individual_name}' não encontrado."
            )

        destroy_entity(individual)

        self.save()


    def get_object_property(self, individual, property_name: str):
        object_property = self.get_object_property_by_name(
            property_name
        )

        if object_property is None:
            raise ValueError(
                f"Object Property '{property_name}' não encontrada."
            )

        return list(object_property[individual])