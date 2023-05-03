import logging
import unittest

from datagencars.synthetic_dataset.generator.generator_output_file.generator_context import GeneratorContextFile


class TestGeneratorContext(unittest.TestCase):

    def setUp(self):        
        # context_schema.conf
        context_schema_file_path = 'resources/data_schema/context_schema.conf'
        with open(context_schema_file_path, 'r') as context_schema_file:
            context_schema = context_schema_file.read()        
        # generation_config.conf
        generation_config_file_path = 'resources/data_schema/generation_config.conf'
        with open(generation_config_file_path, 'r') as generation_config_file:
            generation_config = generation_config_file.read()      
        # Context generator:        
        self.__generator = GeneratorContextFile(generation_config, context_schema)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_context_file(self):
        context_file = self.__generator.generate_file()        
        logging.info(f'context_file: {context_file}')        
        self.assertEqual(context_file.shape[0], 1500)                


if __name__ == '__main__':
    unittest.main()
