import logging
import re

import pandas as pd
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute import GeneratorAttribute


class GeneratorAttributeAddress(GeneratorAttribute):
    '''
    A generator of attribute values representing an address ("street", "number", "ZIP code", "latitude", and "longitude") 
    by collecting these values from an input file provided.
 
    @author Maria del Carmen Rodriguez-Hernandez
    '''

    def __init__(self, schema_access):
        super().__init__(schema_access)

    def generate_attribute_value(self, position):
        # sourcery skip: extract-method, for-append-to-extend
        '''
        Generates an attribute value (address) of a instance.

        Example of item_schema.conf:
            [attribute2]
            name_attribute_2=address
            type_attribute_2=AttributeComposite
            number_maximum_subattribute_attribute_2=5
            name_subattribute_1_attribute_2=street
            name_subattribute_2_attribute_2=number
            name_subattribute_3_attribute_2=zp
            name_subattribute_4_attribute_2=latitude
            name_subattribute_5_attribute_2=longitude
            type_subattribute_1_attribute_2=String
            type_subattribute_2_attribute_2=String
            type_subattribute_3_attribute_2=String
            type_subattribute_4_attribute_2=String
            type_subattribute_5_attribute_2=String
            generator_type_attribute_2=AddressAttributeGenerator
            input_parameter_attribute_2=address_restaurant.csv

        Example of item_address.csv:
            street;number;zp;latitude;longitude
            Via Alto Adige - Südtiroler Straße;60;39100;11.35465;11.364649
            Via Cassa di Risparmio - Sparkassenstraße;12;39100;11.344651;11.364649
            ...
        :param position: The position of an attribute.
        :return: The attribute value (address). 
        '''
        attribute_value = []
        attribute_name = self.schema_access.get_attribute_name_from_pos(position)
        if attribute_name == 'id_user_profile':
            print('TODO')
        else:  
            # Loading file "name_restaurant.csv":
            schema_file_path = self.schema_access.file_path
            input_parameter_attribute = self.schema_access.get_input_parameter_attribute_from_pos(position)
            input_parameter_file_path = re.sub(r'([a-z]*)_schema.conf', input_parameter_attribute, schema_file_path)
            input_parameter_df = pd.read_csv(input_parameter_file_path, encoding='utf-8', index_col=False, sep=';')              
            row_random = input_parameter_df.sample()
            # print(row_random)

            # Gets sub-attribute names and values:
            name_subattribute_list = self.schema_access.get_name_subattribute_list_from_pos(position)
            for name_subattribute in name_subattribute_list:
                if name_subattribute in row_random:
                    attribute_value.append(str(row_random[name_subattribute].iloc[0]))
        return attribute_name, attribute_value

# from datagencars.generator.file_access.schema_access import SchemaAccess
# schema_access = SchemaAccess(file_path='resources/data/item_schema.conf')
# address_attribute_generator = AddressAttributeGenerator(schema_access)
# attribute_name, attribute_value_list = address_attribute_generator.generate_attribute_value(position=2)
# print('attribute_name: ', attribute_name)
# print('attribute_value_list: ', attribute_value_list)