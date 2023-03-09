import logging
import unittest

from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_boolean_list import GeneratorAttributeBooleanList


class TestGeneratorAttributeBooleanList(unittest.TestCase):

    def setUp(self):        
        item_schema_file_path = 'resources/data_schema/item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()            
        schema_access = AccessSchema(file_str=item_schema)
        self.__generator = GeneratorAttributeBooleanList(schema_access)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_attribute_value(self):
        '''
        [attribute6]
        name_attribute_6=weekday_is_open
        type_attribute_6=List
        number_maximum_component_attribute_6=7
        type_component_attribute_6=Boolean
        component_1_attribute_6=monday
        component_2_attribute_6=tuesday
        component_3_attribute_6=wednesday
        component_4_attribute_6=thursday
        component_5_attribute_6=friday
        component_6_attribute_6=saturday
        component_7_attribute_6=sunday
        generator_type_attribute_6=BooleanListAttributeGenerator
        input_parameter_attribute_6=1
        '''
        attribute_name, attribute_value = self.__generator.generate_attribute_value(position=6)
        logging.info(f'boolean_list_attribute_name: {attribute_name}')
        logging.info(f'boolean_list_attribute_value: {attribute_value}')
        self.assertEqual(attribute_name, 'weekday_is_open')                   


if __name__ == '__main__':
    unittest.main()
