import logging
import unittest

from datagencars.synthetic_dataset.generator.generator_output_file.generator_context_file import GeneratorContextFile


class TestGeneratorContext(unittest.TestCase):

    def setUp(self):        
        schema_path = 'resources/generate_synthetic_dataset/rating_implicit/context/data_schema/imascono/'
        # context_schema.conf
        context_schema_file_path = schema_path +'context_schema.conf'
        with open(context_schema_file_path, 'r') as context_schema_file:
            context_schema = context_schema_file.read()
        # generation_config.conf
        generation_config_file_path = schema_path +'generation_config.conf'
        with open(generation_config_file_path, 'r') as generation_config_file:
            generation_config = generation_config_file.read()
        # Context generator:        
        self.__generator = GeneratorContextFile(context_schema, generation_config)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_context_file(self):
        context_file = self.__generator.generate_file()
        logging.info(f'context_file: {context_file}')
        context_file.to_csv('context.csv', index=False)
        self.assertEqual(context_file.shape[0], 10)


if __name__ == '__main__':
    unittest.main()
