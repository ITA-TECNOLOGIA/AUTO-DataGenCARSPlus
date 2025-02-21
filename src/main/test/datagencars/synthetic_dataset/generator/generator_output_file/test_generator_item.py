import logging
import unittest

from datagencars.synthetic_dataset.generator.generator_output_file.generator_item_file import GeneratorItemFile


class TestGeneratorItem(unittest.TestCase):

    def setUp(self):
        data_schema_path = "resources/generate_synthetic_dataset/rating_explicit/context/data_schema/restaurant/"
        # item_schema.conf
        item_schema_file_path = data_schema_path + 'item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()        
        # generation_config.conf
        generation_config_file_path = data_schema_path + 'generation_config.conf'
        with open(generation_config_file_path, 'r') as generation_config_file:
            generation_config = generation_config_file.read()  
        # item_profile.conf
        item_profile_path = data_schema_path + 'item_profile.conf'
        with open(item_profile_path, 'r') as item_profile_file:            
            item_profile = item_profile_file.read()  
        # Item generator:
        self.__generator_with_correlation = GeneratorItemFile(generation_config=generation_config, item_schema=item_schema, item_profile=item_profile)
        self.__generator_without_correlation = GeneratorItemFile(generation_config=generation_config, item_schema=item_schema)
    
    def tearDown(self):
        del self.__generator_with_correlation
        del self.__generator_without_correlation
    
    def test_generate_item_file_correlation(self):
        '''        
        Generates the item file with correlation.        
        '''        
        item_file = self.__generator_with_correlation.generate_file()        
        logging.info(f'item_file: {item_file}')
        self.assertEqual(item_file.shape[0], 1000)

    def test_generate_item_file(self):
        '''        
        Generates the item file without correlation.        
        '''        
        item_file = self.__generator_without_correlation.generate_file()        
        logging.info(f'item_file: {item_file}')
        self.assertEqual(item_file.shape[0], 1000)

    
if __name__ == '__main__':
    unittest.main()