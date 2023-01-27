import logging

import numpy as np
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute import GeneratorAttribute


class GeneratorAttributeBooleanList(GeneratorAttribute):

    '''
    A generator of boolean attribute values. Specifically, generates an array of boolean values representing the presence or absence of a certain feature or
    Component (e.g., fills with true/false the opening days of a business [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday] or the types
    of foods served in a restaurant [Italian, Mexican], etc., based on the average percentage of true values desired).
 
    @author Maria del Carmen Rodriguez-Hernandez
    '''

    def __init__(self, schema_access):
        super().__init__(schema_access)

    def generate_attribute_value(self, position):
        # sourcery skip: extract-method, for-append-to-extend, list-comprehension
        '''
        XXX

        Example of item_schema.conf:
            [attribute6]
            name_attribute_6=weekday_is_open
            type_attribute_6=List
            number_maximum_component_attribute_6=7
            type_component_attribute_6=Boolean
            component_1_attribute_6=monday
            component_2_attribute_6=tuesday
            component_3_attribute_6=wednesday
            component_4_attribute_6=thursday
            component_5_attribute_6=friday
            component_6_attribute_6=saturday
            component_7_attribute_6=sunday
            generator_type_attribute_6=BooleanListAttributeGenerator
            input_parameter_attribute_6=1
        '''
        attribute_value_list = []
        attribute_name = self.schema_access.get_attribute_name_from_pos(position)
        if attribute_name == 'id_user_profile':
            print('TODO')
        else:  
            component_attribute_list = self.schema_access.get_component_attribute_list_from_pos(position)            
            input_parameter_attribute = self.schema_access.get_input_parameter_attribute_from_pos(position)            
            removed_attribute_value_list = np.random.choice(component_attribute_list, int(input_parameter_attribute))
            for component_attribute in component_attribute_list:
                if component_attribute not in removed_attribute_value_list:
                    attribute_value_list.append(component_attribute)           
        return attribute_name, attribute_value_list

# from datagencars.generator.file_access.schema_access import SchemaAccess
# schema_access = SchemaAccess(file_path='resources/data/item_schema.conf')
# bool_array_list_generator = BooleanListAttributeGenerator(schema_access)
# attribute_name, attribute_value_list = bool_array_list_generator.generate_attribute_value(position=6)
# print('attribute_name: ', attribute_name)
# print('attribute_value_list: ', attribute_value_list)
