import logging

from datagencars.synthetic_dataset.generator.generator_instance.generator_instance import GeneratorInstance
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_gaussian import GeneratorAttributeGaussian


class GeneratorInstanceGaussian(GeneratorInstance):

    def __init__(self, generation_access, schema_access): 
        super().__init__(generation_access, schema_access)

    def generate_instance(self):
        number_attributes = self.schema_access.get_number_attributes()
        attribute_list = []
        for position in range(1, number_attributes+1):
            generator_type = self.schema_access.get_generator_type_attribute_from_pos(position)

            attribute_generator = None
            attribute_value = None
            if generator_type == 'GaussianAttributeGenerator':
                attribute_generator = GeneratorAttributeGaussian(self.schema_access)            
            attribute_value = attribute_generator.generate_attribute_value()
            attribute_list.append(attribute_value)
        return attribute_list