from datagencars.generator.attribute_generator.gaussian_attribute_generator import GaussianAttributeGenerator
from datagencars.generator.instance_generator.instance_generator import InstanceGenerator
import logging


class InstanceGaussianGenerator(InstanceGenerator):

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
                attribute_generator = GaussianAttributeGenerator(self.schema_access)            
            attribute_value = attribute_generator.generate_attribute_value()
            attribute_list.append(attribute_value)
        return attribute_list