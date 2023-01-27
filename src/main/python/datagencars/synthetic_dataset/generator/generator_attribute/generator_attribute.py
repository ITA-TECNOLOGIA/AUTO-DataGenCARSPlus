from abc import ABC, abstractmethod


class GeneratorAttribute(ABC):

    def __init__(self, schema_access):
        self.schema_access = schema_access

    @abstractmethod
    def generate_attribute_value(self, position):
        pass