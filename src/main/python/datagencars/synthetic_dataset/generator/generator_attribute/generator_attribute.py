from abc import ABC, abstractmethod


class GeneratorAttribute(ABC):

    def __init__(self, schema_access):
        self.schema_access = schema_access

    @abstractmethod
    def generate_attribute_value(self, position, input_parameter_content=None, input_paramenter_split=None):
        pass