import logging
import random

from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute import GeneratorAttribute


class GeneratorAttributeRandom(GeneratorAttribute):
    '''
    A generator of random attribute values: an integer or float value in a given range, a string value from an enumerated list, or a boolean value.

    @author Maria del Carmen Rodriguez-Hernandez
    '''

    def __init__(self, schema_access):
        super().__init__(schema_access)

    def generate_attribute_value(self, position):
        '''
        Generates an attribute value (random) of a instance.

        Example of context_schema.conf:
            [attribute1]
            name_attribute_1=transport_way
            type_attribute_1=String
            number_posible_values_attribute_1=4
            posible_value_1_attribute_1=walking
            posible_value_2_attribute_1=bicycle
            posible_value_3_attribute_1=car
            posible_value_4_attribute_1=public
            generator_type_attribute_1=RandomAttributeGenerator
            important_weight_attribute_1=true
        :param position: The position of an attribute.
        :return: The attribute value (random). 
        '''
        attribute_value = None
        attribute_name = self.schema_access.get_attribute_name_from_pos(position)       
        type_attribute = self.schema_access.get_type_attribute_from_pos(position)            
        if type_attribute == 'Integer':     
            minimum_value = int(self.schema_access.get_minimum_value_attribute_from_pos(position))
            maximum_value = int(self.schema_access.get_maximum_value_attribute_from_pos(position))
            attribute_value = int(random.randint(int(minimum_value), int(maximum_value)))
        elif type_attribute == 'Float':
            minimum_value = float(self.schema_access.get_minimum_value_attribute_from_pos(position))
            maximum_value = float(self.schema_access.get_maximum_value_attribute_from_pos(position))
            attribute_value = float(round(random.uniform(float(minimum_value), float(maximum_value)),1))
        elif type_attribute == 'String' or type_attribute == 'List':
            possible_values_attribute_list = self.schema_access.get_possible_values_attribute_list_from_pos(position)
            attribute_value = str(random.choice(possible_values_attribute_list))
        elif type_attribute == 'Boolean':
            attribute_value = bool(random.choice([True, False]))  
        return attribute_name, attribute_value
