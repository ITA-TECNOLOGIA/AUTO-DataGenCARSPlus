import logging
import unittest
from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_object_position import GeneratorAttributeObjectPosition


class TestGeneratorAttributeLocation(unittest.TestCase):

    def setUp(self):        
        item_schema_file_path = 'resources/generate_synthetic_dataset/rating_implicit/context/data_schema/imascono/item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()            
        schema_access = AccessSchema(file_str=item_schema)
        self.__generator = GeneratorAttributeObjectPosition(schema_access)

    def tearDown(self):
        del self.__generator

    def test_generate_attribute_value(self):
        '''
        [attribute8]
        name_attribute_8=object_position
        type_attribute_8=AttributeComposite
        number_maximum_subattribute_attribute_8=3
        name_subattribute_1_attribute_8=longitude
        name_subattribute_2_attribute_8=lattitude
        name_subattribute_3_attribute_8=altitude
        type_subattribute_1_attribute_8=float
        type_subattribute_2_attribute_8=float
        type_subattribute_3_attribute_8=float
        generator_type_attribute_8=ObjectPositionAttributeGenerator
        '''        
        attribute_position=3
        attribute_name, attribute_value = self.__generator.generate_attribute_value(position=attribute_position)
        logging.info(f'location_attribute_name: {attribute_name}')
        logging.info(f'location_attribute_value: {attribute_value}')
        self.assertEqual(attribute_name, 'object_position')        
        # self.assertEqual(len(attribute_value), 5)            

if __name__ == '__main__':
    unittest.main()
