import logging
import unittest

from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_random import GeneratorAttributeRandom


class TestGeneratorAttributeRandom(unittest.TestCase):

    def setUp(self):        
        item_schema_file_path = 'resources/generate_synthetic_dataset/rating_explicit/context/restaurant/data_schema/item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()         
        schema_access = AccessSchema(file_str=item_schema)
        self.__generator = GeneratorAttributeRandom(schema_access)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_attribute_value_int(self):
        ''' 
        [attribute5]
        name_attribute_5=phone
        type_attribute_5=Integer
        minimum_value_attribute_5=976000000
        maximum_value_attribute_5=976999999
        generator_type_attribute_5=RandomAttributeGenerator
        '''
        attribute_name, attribute_value = self.__generator.generate_attribute_value(position=5)
        logging.info(f'int_random_attribute_name: {attribute_name}')
        logging.info(f'int_random_attribute_value: {attribute_value}')
        self.assertEqual(attribute_name, 'phone')     

    def test_generate_attribute_value_bool(self):
        '''        
        [attribute9]
        name_attribute_9=card
        type_attribute_9=Boolean
        generator_type_attribute_9=RandomAttributeGenerator
        important_weight_attribute_9=True
        '''
        attribute_name, attribute_value = self.__generator.generate_attribute_value(position=9)
        logging.info(f'bool_random_attribute_name: {attribute_name}')
        logging.info(f'bool_random_attribute_value: {attribute_value}')
        self.assertEqual(attribute_name, 'card')     

    def test_generate_attribute_value_str(self):
        '''        
        [attribute15]
        name_attribute_15=quality_food
        type_attribute_15=String
        number_posible_values_attribute_15=5
        posible_value_1_attribute_15=excellent
        posible_value_2_attribute_15=good
        posible_value_3_attribute_15=normal
        posible_value_4_attribute_15=bad
        posible_value_5_attribute_15=dreadful
        generator_type_attribute_15=RandomAttributeGenerator
        important_profile_attribute_15=True
        ranking_order_by_attribute_15=desc
        important_weight_attribute_15=True 
        '''
        attribute_name, attribute_value = self.__generator.generate_attribute_value(position=15)
        logging.info(f'str_random_attribute_name: {attribute_name}')
        logging.info(f'str_random_attribute_value: {attribute_value}')
        self.assertEqual(attribute_name, 'quality_food')     


if __name__ == '__main__':
    unittest.main()
