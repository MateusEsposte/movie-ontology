from owlready2 import get_ontology


class OntologyManager:
    def __init__(self, ontology_path):
        self.ontology_path = ontology_path
        self.ontology = None


    def load(self):
        """Carrega a ontologia."""
        self.ontology = get_ontology(self.ontology_path).load()


    def save(self):
        """Salva a ontologia."""
        self.ontology.save(file=self.ontology_path)


    @property
    def ontology(self):
        return self._ontology

    @ontology.setter
    def ontology(self, value):
        self._ontology = value
    
