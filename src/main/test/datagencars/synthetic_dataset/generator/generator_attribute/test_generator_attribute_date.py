import logging
import unittest

from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_date import GeneratorAttributeDate


class TestGeneratorAttributeDate(unittest.TestCase):

    def setUp(self):        
        user_schema_file_path = 'resources/generate_synthetic_dataset/rating_explicit/context/restaurant/data_schema/user_schema.conf'
        with open(user_schema_file_path, 'r') as user_schema_file:
            user_schema = user_schema_file.read()            
        schema_access = AccessSchema(file_str=user_schema)
        self.__generator = GeneratorAttributeDate(schema_access)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_attribute_value(self):
        '''
        [attribute4]
        name_attribute_4=birthdate
        type_attribute_4=String
        minimum_value_attribute_4=1957
        maximum_value_attribute_4=2000
        generator_type_attribute_4=DateAttributeGenerator
        '''
        attribute_name, attribute_value = self.__generator.generate_attribute_value(position=4)
        logging.info(f'date_attribute_name: {attribute_name}')
        logging.info(f'date_attribute_value: {attribute_value}')
        self.assertEqual(attribute_name, 'birthdate')                   


if __name__ == '__main__':
    unittest.main()
