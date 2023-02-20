import logging
import unittest

from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.generator.access_schema.access_generation_config import AccessGenerationConfig
from datagencars.synthetic_dataset.generator.access_schema.access_item_profile import AccessItemProfile
from datagencars.synthetic_dataset.generator.generator_instance.generator_instance import GeneratorInstance


class TestGeneratorInstanceItem(unittest.TestCase):

    def setUp(self):       
        # item_schema.conf 
        item_schema_file_path = 'resources/data_schema/item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()            
        schema_access = AccessSchema(file_str=item_schema)
        # generation_config.conf
        generation_config_file_path = 'resources/data_schema/generation_config.conf'
        with open(generation_config_file_path, 'r') as generation_config_file:
            generation_config = generation_config_file.read()                
        generation_access = AccessGenerationConfig(file_str=generation_config)
        # item_profile.conf
        item_profile_file_path = 'resources/data_schema/item_profile.conf'
        with open(item_profile_file_path, 'r') as item_profile_file:
            item_profile = item_profile_file.read()   
        item_profile_access = AccessItemProfile(file_str=item_profile)
        # Generator.
        self.__generator = GeneratorInstance(schema_access, generation_access, item_profile_access)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_instance_item(self):
        attribute_list = self.__generator.generate_instance(position_item_profile=1, with_noise=False)        
        logging.info(f'attribute_list: {attribute_list}')        
        self.assertEqual(len(attribute_list), 18)      

    def test_generate_instance_item_noise(self):
        attribute_list = self.__generator.generate_instance(position_item_profile=1, with_noise=True)        
        logging.info(f'attribute_list: {attribute_list}')        
        self.assertEqual(len(attribute_list), 18)                  


if __name__ == '__main__':
    unittest.main()
