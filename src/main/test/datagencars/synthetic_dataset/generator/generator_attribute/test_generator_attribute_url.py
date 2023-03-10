import logging
import unittest

from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_url import GeneratorAttributeURL


class TestGeneratorAttributeURL(unittest.TestCase):

    def setUp(self):        
        item_schema_file_path = 'resources/data_schema/item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()            
        schema_access = AccessSchema(file_str=item_schema)
        self.__generator = GeneratorAttributeURL(schema_access)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_attribute_value(self):
        '''
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
        '''                
        attribute_name, attribute_value = self.__generator.generate_attribute_value(position=1)
        logging.info(f'url_attribute_name: {attribute_name}')
        logging.info(f'url_attribute_value: {attribute_value}')
        self.assertEqual(attribute_name, 'web_name')                   


if __name__ == '__main__':
    unittest.main()
