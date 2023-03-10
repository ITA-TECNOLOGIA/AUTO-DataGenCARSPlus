import ast
import logging
import random

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
            input_parameter_attribute_2=[['Via Alto Adige - Südtiroler Straße', '60', '39100', '11.35465', '11.364649'], ['Via Cassa di Risparmio - Sparkassenstraße', '12', '39100', '11.344651', '11.364649'], ['Via Museo - Museumstraße', '19', '39100', '11.34651', '11.364649'], ['Viale Druso - Drususallee', '50', '39100', '11.33465', '11.354649'], ['Via Andreas Hofer - Andreas-Hofer-Straße', '8', '39100', '11.354651', '11.374649'], ['Via dei Conciapelli - Gerbergasse', '25', '39100', '11.354651', '11.374649'], ['Via Portici - Laubengasse', '51', '39100', '11.344651', '11.364649'], ['Via Andreas Hofer - Andreas-Hofer-Straße', '30', '39100', '11.354651', '11.374649'], ['Via Cavour - Cavourstraße', '8', '39100', '11.354651', '11.37465'], ['Piazza Dogana - Zollstangenplatz', '3', '39100', '11.354651', '11.374649'], ['Piazza delle Erbe - Obstmarkt', '17', '39100', '11.344651', '11.364649']]
        :param position: The position of an attribute.
        :return: The attribute value (address). 
        '''
        attribute_value = []
        attribute_name = self.schema_access.get_attribute_name_from_pos(position)       
        if attribute_name == 'user_profile_id':
            print('TODO')
        else:
            # Gets sub-attribute names and values:
            name_subattribute_list = self.schema_access.get_name_subattribute_list_from_pos(position)
            address_input_list = ast.literal_eval(self.schema_access.get_input_parameter_attribute_from_pos(position))
            attribute_value = random.choice(address_input_list)      
        return attribute_name, attribute_value
