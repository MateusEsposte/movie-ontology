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