import unittest
import logging

from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_address import GeneratorAttributeAddress


class TestGeneratorAttributeAddress(unittest.TestCase):

    def setUp(self):        
        item_schema_file_path = 'resources/data_schema/item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()            
        schema_access = AccessSchema(file_str=item_schema)
        self.__generator = GeneratorAttributeAddress(schema_access)
    
    def tearDown(self):
        del self.__access
    
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
        input_parameter_attribute_2=address_restaurant.csv
        '''
        attribute_name, attribute_value = self.__generator.generate_attribute_value(position=2)
        logging.info(f'address_attribute_name: {attribute_name}')   
        logging.info(f'address_attribute_value: {attribute_value}')   
        print(f'address_attribute_name: {attribute_name}')  
        print(f'address_attribute_value: {attribute_value}')         
        self.assertEqual(attribute_name, 'address')            
   

if __name__ == '__main__':
    unittest.main()
