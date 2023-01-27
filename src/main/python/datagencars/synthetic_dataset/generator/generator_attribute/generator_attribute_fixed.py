import logging

from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute import GeneratorAttribute


class GeneratorAttributeFixed(GeneratorAttribute):
    '''
    A generator of fixed attribute values specified as input parameter (e.g., the value "Chicago" for an attribute "city" of the type of item "hotel").

    @author Maria del Carmen Rodriguez-Hernandez
    '''

    def __init__(self, schema_access):
        super().__init__(schema_access)

    def generate_attribute_value(self, position):
        '''
        XXX

        Example of item_schema.conf:
            [attribute1]
            name_attribute_1=province
            type_attribute_1=String
            generator_type_attribute_1=FixedAttributeGenerator
            input_parameter_attribute_1=California
        
        '''
        attribute_value = None
        attribute_name = self.schema_access.get_attribute_name_from_pos(position)
        if attribute_name == 'id_user_profile':
            print('TODO')
        else:   
            attribute_value = self.schema_access.get_input_parameter_attribute_from_pos(position)
        return attribute_name, attribute_value


# from datagencars.generator.file_access.schema_access import SchemaAccess
# schema_access = SchemaAccess(file_path='resources/data/item_schema.conf')
# fixed_attribute_generator = FixedAttributeGenerator(schema_access)
# attribute_name, attribute_value_list = fixed_attribute_generator.generate_attribute_value(position=3)
# print('attribute_name: ', attribute_name)
# print('attribute_value_list: ', attribute_value_list)