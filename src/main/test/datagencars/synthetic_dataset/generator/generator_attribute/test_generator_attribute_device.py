import logging
import unittest
from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_device import GeneratorAttributeDevice

class TestGeneratorAttributeDevice(unittest.TestCase):
    def setUp(self):        
        item_schema_file_path = 'resources\data_schema_imascono\context_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()            
        schema_access = AccessSchema(file_str=item_schema)
        self.__generator = GeneratorAttributeDevice(schema_access)
    def tearDown(self):
        del self.__generator
    def test_generate_attribute_value(self):
        '''
        [attribute1]
        name_attribute_1=device_data
        type_attribute_1=AttributeComposite
        generator_type_attribute_1=FixedAttributeGenerator
        number_maximum_subattribute_attribute_1=7
        name_subattribute_1_attribute_1=browserName
        name_subattribute_2_attribute_1=browserVersion
        name_subattribute_3_attribute_1=deviceName
        name_subattribute_4_attribute_1=deviceType
        name_subattribute_5_attribute_1=deviceVendor
        name_subattribute_6_attribute_1=osName
        name_subattribute_7_attribute_1=osVersion
        type_subattribute_1_attribute_1=String
        type_subattribute_2_attribute_1=String
        type_subattribute_3_attribute_1=String
        type_subattribute_4_attribute_1=String
        type_subattribute_5_attribute_1=String
        type_subattribute_6_attribute_1=String
        type_subattribute_7_attribute_1=String
        input_parameter_subattribute_1_attribute_1=["Chrome", "Safari", "Firefox", "Mobile Safari", "GSA", "Edge", "Samsung Browser", "Opera", "MIUI Browser"]
        input_parameter_subattribute_3_attribute_1=["Android", "Windows", "Mac OS", "iOS", "Linux", "Chromium OS"]
        generator_type_attribute_2=DeviceAttributeGenerator
        '''
        attribute_position=1
        attribute_name, attribute_value = self.__generator.generate_attribute_value(position=attribute_position)
        logging.info(f'device_attribute_name: {attribute_name}')
        logging.info(f'device_attribute_value: {attribute_value}')
        self.assertEqual(attribute_name, 'device_data')
        # self.assertEqual(len(attribute_value), 5)

if __name__ == '__main__':
    unittest.main()
