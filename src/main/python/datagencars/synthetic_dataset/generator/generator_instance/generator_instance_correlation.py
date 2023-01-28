import logging

from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_address import GeneratorAttributeAddress
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_boolean_array_list import GeneratorAttributeBooleanList
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_correlation import GeneratorAttributeCorrelation
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_date import GeneratorAttributeDate
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_fixed import GeneratorAttributeFixed
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_random import GeneratorAttributeRandom
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_url import GeneratorAttributeURL
from datagencars.synthetic_dataset.generator.generator_instance.generator_instance import GeneratorInstance


class GenerationInstanceCorrelation(GeneratorInstance):

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
                attribute_generator = GeneratorAttributeCorrelation(schema_access=self.schema_access, item_profile_access=self.item_profile_access, generation_access=self.generation_access)
                _,attribute_value = attribute_generator.generate_attribute_value(position_attribute=position, position_item_profile=position_item_profile, with_noise=with_noise)
            else:                
                if generator_type == 'RandomAttributeGenerator':
                    attribute_generator = GeneratorAttributeRandom(schema_access=self.schema_access)
                elif generator_type == 'BooleanListAttributeGenerator':
                    attribute_generator = GeneratorAttributeBooleanList(schema_access=self.schema_access)
                elif generator_type == 'DateAttributeGenerator':
                    attribute_generator = GeneratorAttributeDate(schema_access=self.schema_access)
                elif generator_type == 'FixedAttributeGenerator':
                    attribute_generator = GeneratorAttributeFixed(schema_access=self.schema_access)
                elif generator_type == 'AddressAttributeGenerator':
                    attribute_generator = GeneratorAttributeAddress(schema_access=self.schema_access)
                elif generator_type == 'URLAttributeGenerator':
                    attribute_generator = GeneratorAttributeURL(schema_access=self.schema_access)
                _, attribute_value = attribute_generator.generate_attribute_value(position)                
            attribute_list.append(attribute_value)
        return attribute_list
