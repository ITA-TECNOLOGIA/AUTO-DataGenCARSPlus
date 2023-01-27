from abc import ABC, abstractmethod


class GeneratorInstance(ABC):

    def __init__(self, generation_access, schema_access):      
        self.generation_access = generation_access
        self.schema_access = schema_access            

    @abstractmethod
    def generate_instance(self):
        pass