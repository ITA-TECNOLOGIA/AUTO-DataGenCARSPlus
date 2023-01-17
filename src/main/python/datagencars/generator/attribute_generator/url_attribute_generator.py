import logging

from datagencars.generator.attribute_generator.attribute_generator import AttributeGenerator
import pandas as pd
import re
import random


class URLAttributeGenerator(AttributeGenerator):
    '''
    A generator of URL attribute values. The URL has the structure "http://www."+value+".com", where the value is the item name. 
    For example, http://www.restaurantalley.com for a restaurant named\Restaurant Alley".

    @author Maria del Carmen Rodriguez-Hernandez
    '''

    def __init__(self, schema_access):
        super().__init__(schema_access)

    def generate_attribute_value(self, position, import_file_path=None):
        # sourcery skip: extract-method, inline-immediately-returned-variable
        '''
        Generates an attribute value (URL) of a instance.
        Example of item_schema.conf:
            [attribute1]
            name_attribute_1=web_name
            type_attribute_1=AttributeComposite
            number_maximum_subattribute_attribute_1=2
            name_subattribute_1_attribute_1=name
            name_subattribute_2_attribute_1=url
            type_subattribute_1_attribute_1=String
            type_subattribute_2_attribute_1=String
            generator_type_attribute_1=NameURLAttributeGenerator
            input_parameter_attribute_1=name_restaurant.csv
            unique_value_attribute_1=true

        Example of name_restaurant.csv:
            place
            Umami Burger
            Restaurant Aoi
            ...

        :param position: The position of an attribute.
        :return: The attribute value (URL).        
        '''
        attribute_value = None
        attribute_name = self.schema_access.get_attribute_name_from_pos(position)
        if attribute_name == 'id_user_profile':
            print('TODO')
        else:        
            # Loading file "name_restaurant.csv":
            schema_file_path = self.schema_access.file_path
            input_parameter_attribute = self.schema_access.get_input_parameter_attribute_from_pos(position)
            input_parameter_file_path = re.sub(r'([a-z]*)_schema.conf', input_parameter_attribute, schema_file_path)
            input_parameter_df = pd.read_csv(input_parameter_file_path, encoding='utf-8', index_col=False)
            input_parameter_list = input_parameter_df['place'].unique().tolist()
            place = str(random.choice(input_parameter_list))
            # Preprocessing the place value:
            place = place.lower()
            place = place.replace(' ', '_')
            place = place.strip()
            # Generating URL:
            attribute_value = f"http://www.{place}.com"
        return attribute_name, attribute_value


# from datagencars.generator.file_access.schema_access import SchemaAccess
# schema_access = SchemaAccess(file_path='resources/data/item_schema.conf')
# url_generator = URLAttributeGenerator(schema_access)
# attribute_name, attribute_value_list = url_generator.generate_attribute_value(position=1)
# print('attribute_name: ', attribute_name)
# print('attribute_value_list: ', attribute_value_list)
