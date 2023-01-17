import logging

from datagencars.generator.attribute_generator.address_attribute_generator import AddressAttributeGenerator
from datagencars.generator.attribute_generator.boolean_array_list_attribute_generator import BooleanArrayListAttributeGenerator
from datagencars.generator.attribute_generator.correlation_attribute_generator import CorrelationAttributeGenerator
from datagencars.generator.attribute_generator.date_attribute_generator import DateAttributeGenerator
from datagencars.generator.attribute_generator.fixed_attribute_generator import FixedAttributeGenerator
from datagencars.generator.attribute_generator.random_attribute_generator import RandomAttributeGenerator
from datagencars.generator.attribute_generator.url_attribute_generator import URLAttributeGenerator
from datagencars.generator.instance_generator.instance_generator import InstanceGenerator


class InstanceCorrelationGeneration(InstanceGenerator):

    def __init__(self, generation_access, schema_access, item_profile_access):
        super().__init__(generation_access, schema_access)
        self.item_profile_access = item_profile_access

    def generate_instance(self, position_item_profile=None, with_noise=None):
        number_attributes = self.schema_access.get_number_attributes()
        attribute_list = []
        for position in range(1, number_attributes+1):
            generator_type = self.schema_access.get_generator_type_attribute_from_pos(position)

            attribute_generator = None
            attribute_value = None
            if generator_type == 'CorrelationAttributeGenerator':
                attribute_generator = CorrelationAttributeGenerator(schema_access=self.schema_access, item_profile_access=self.item_profile_access, generation_access=self.generation_access)
                _,attribute_value = attribute_generator.generate_attribute_value(position_attribute=position, position_item_profile=position_item_profile, with_noise=with_noise)
            else:                
                if generator_type == 'RandomAttributeGenerator':
                    attribute_generator = RandomAttributeGenerator(schema_access=self.schema_access)
                elif generator_type == 'BooleanArrayListAttributeGenerator':
                    attribute_generator = BooleanArrayListAttributeGenerator(schema_access=self.schema_access)
                elif generator_type == 'DateAttributeGenerator':
                    attribute_generator = DateAttributeGenerator(schema_access=self.schema_access)
                elif generator_type == 'FixedAttributeGenerator':
                    attribute_generator = FixedAttributeGenerator(schema_access=self.schema_access)
                elif generator_type == 'AddressAttributeGenerator':
                    attribute_generator = AddressAttributeGenerator(schema_access=self.schema_access)
                elif generator_type == 'URLAttributeGenerator':
                    attribute_generator = URLAttributeGenerator(schema_access=self.schema_access)
                _, attribute_value = attribute_generator.generate_attribute_value(position)                
            attribute_list.append(attribute_value)
        return attribute_list
