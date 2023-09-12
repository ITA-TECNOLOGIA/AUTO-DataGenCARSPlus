import logging
import unittest

from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_address import GeneratorAttributeAddress


class TestGeneratorAttributeAddress(unittest.TestCase):

    def setUp(self):        
        item_schema_file_path = 'resources/generate_synthetic_dataset/rating_explicit/context/data_schema/restaurant/item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()            
        schema_access = AccessSchema(file_str=item_schema)
        self.__generator = GeneratorAttributeAddress(schema_access)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_attribute_value(self):
        '''
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
        '''        
        attribute_position=2        
        attribute_name, attribute_value = self.__generator.generate_attribute_value(position=attribute_position)
        logging.info(f'address_attribute_name: {attribute_name}')
        logging.info(f'address_attribute_value: {attribute_value}')
        self.assertEqual(attribute_name, 'address')        
        self.assertEqual(len(attribute_value), 5)            
   

if __name__ == '__main__':
    unittest.main()
