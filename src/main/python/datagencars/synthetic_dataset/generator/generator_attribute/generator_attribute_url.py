import io
import logging
import random
import ast

import pandas as pd
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute import GeneratorAttribute


class GeneratorAttributeURL(GeneratorAttribute):
    '''
    A generator of URL attribute values. The URL has the structure "http://www."+value+".com", where the value is the item name. 
    For example, http://www.restaurantalley.com for a restaurant named\Restaurant Alley".

    @author Maria del Carmen Rodriguez-Hernandez
    '''

    def __init__(self, schema_access):
        super().__init__(schema_access)

    def generate_attribute_value(self, position):
        # sourcery skip: extract-method, inline-immediately-returned-variable, use-named-expression
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
            input_parameter_attribute_1=['Umami Burger', 'Restaurant Aoi', 'Drago Centro', 'Restaurant Alley', 'Daily Grill', 'Pete', 'Clifton Cafeteria', 'Lili Ya', 'Wurstkuche', 'San Sui Tei', 'Hope Street', 'Jack in the Box', 'Denny', 'First and Hope Restaurant', 'Catch 21 Seafood', 'Chop Suey Cafe Lounge', 'Wokano', 'Blue Cow', 'Sushi Toshi', 'Traxx', 'Puertos Del Pacifico', 'Taco House', 'Olvera Street', 'Little Joe', 'Les Noces de Figaro', 'Mr Ramen', 'Daikokuya', 'Izakaya Fuga', 'The Blue Cube', 'Purgatory Pizza', 'Suehiro Cafe', 'Cafe Pinot', 'Pitfire Pizza', 'Kazu Nori', 'Bottega Louie', 'Food Court', 'Subway', 'Nickel Diner', 'Cole', 'Blossom', 'Wurstkuche', 'McDonalds', 'Phillipe French Dip Deli', 'First Cup Cafe', 'Sugarfish Downtown', 'The Parish', 'Ocho Mexican Grill', 'Badmaash', 'West 7th Street', 'Korean BBQ House']
            unique_value_attribute_1=true
        :param position: The position of an attribute.
        :return: The attribute value (URL).        
        '''
        attribute_value = None
        attribute_name = self.schema_access.get_attribute_name_from_pos(position)
        if attribute_name == 'user_profile_id':
            print('TODO')
        else:
            input_parameter_list = ast.literal_eval(self.schema_access.get_input_parameter_attribute_from_pos(position))
            if_unique_value = self.schema_access.get_unique_value_attribute_from_pos(position)
            if if_unique_value:
                # True: If the attribute to be generated will have a unique value.
                place = input_parameter_list[0]
            else:
                # False: If the attribute to be generated will have a random value.
                place = str(random.choice(input_parameter_list))                        
            # Preprocessing the place value:
            place = place.lower()
            place = place.replace(' ', '_')
            place = place.strip()
            # Generating URL:
            attribute_value = f"http://www.{place}.com"
        return attribute_name, attribute_value
