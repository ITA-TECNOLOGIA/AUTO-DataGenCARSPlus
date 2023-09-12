import logging
import unittest

from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_fixed import GeneratorAttributeFixed


class TestGeneratorAttributeFixed(unittest.TestCase):

    def setUp(self):        
        item_schema_file_path = 'resources/generate_synthetic_dataset/rating_explicit/context/restaurant/data_schema/item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()            
        schema_access = AccessSchema(file_str=item_schema)
        self.__generator = GeneratorAttributeFixed(schema_access)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_attribute_value(self):
        '''
        [attribute3]
        name_attribute_3=province
        type_attribute_3=String
        generator_type_attribute_3=FixedAttributeGenerator
        input_parameter_attribute_3=California
        '''
        attribute_name, attribute_value = self.__generator.generate_attribute_value(position=3)
        logging.info(f'date_attribute_name: {attribute_name}')
        logging.info(f'date_attribute_value: {attribute_value}')
        self.assertEqual(attribute_name, 'province')                   


if __name__ == '__main__':
    unittest.main()
