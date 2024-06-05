import logging
import unittest

from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_gaussian import GeneratorAttributeGaussian


class TestGeneratorAttributeGaussian(unittest.TestCase):

    def setUp(self):        
        user_schema_file_path = 'resources/generate_synthetic_dataset/rating_explicit/context/data_schema/restaurant/user_schema.conf'
        with open(user_schema_file_path, 'r') as user_schema_file:
            user_schema = user_schema_file.read()         
        schema_access = AccessSchema(file_str=user_schema)
        self.__generator = GeneratorAttributeGaussian(schema_access)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_attribute_value_int(self):
        ''' 
        [attribute1]
        name_attribute_1=age
        type_attribute_1=Integer
        minimum_value_attribute_1=18
        maximum_value_attribute_1=80
        generator_type_attribute_1=GaussianAttributeGenerator
        '''
        attribute_name, attribute_value = self.__generator.generate_attribute_value(position=1)
        logging.info(f'int_random_attribute_name: {attribute_name}')
        logging.info(f'int_random_attribute_value: {attribute_value}')
        self.assertEqual(attribute_name, 'age')        

    def test_generate_attribute_value_str(self):
        '''        
        [attribute2]
        name_attribute_2=gender
        type_attribute_2=String
        number_posible_values_attribute_2=2
        posible_value_1_attribute_2=female
        posible_value_2_attribute_2=male
        generator_type_attribute_2=GaussianAttributeGenerator
        '''
        attribute_name, attribute_value = self.__generator.generate_attribute_value(position=2)
        logging.info(f'str_random_attribute_name: {attribute_name}')
        logging.info(f'str_random_attribute_value: {attribute_value}')
        self.assertEqual(attribute_name, 'gender')     


if __name__ == '__main__':
    unittest.main()
