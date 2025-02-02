import logging
import unittest

from datagencars.synthetic_dataset.generator.generator_output_file.generator_item_file import GeneratorItemFile


class TestGeneratorItem(unittest.TestCase):

    def setUp(self):
        schema_path = 'resources/generate_synthetic_dataset/rating_implicit/context/data_schema/imascono/'
        # item_schema.conf
        item_schema_file_path = schema_path + 'item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()        
        # generation_config.conf
        generation_config_file_path = schema_path + 'generation_config.conf'
        with open(generation_config_file_path, 'r') as generation_config_file:
            generation_config = generation_config_file.read()  
        # Item generator:
        self.__generator = GeneratorItemFile(item_schema, generation_config, item_profile=None)
    
    def tearDown(self):
        del self.__generator

    def test_generate_item_file(self):
        '''        
        Generates the item file without correlation.        
        '''        
        item_file = self.__generator.generate_file(with_correlation=False)        
        logging.info(f'item_file: {item_file}')
        item_file.to_csv('resources/generate_synthetic_dataset/rating_implicit/context/data_schema/imascono/item.csv', index=False)
        self.assertEqual(item_file.shape[0], 25)

    
if __name__ == '__main__':
    unittest.main()