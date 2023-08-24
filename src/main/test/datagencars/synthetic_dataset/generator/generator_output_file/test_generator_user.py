import logging
import unittest

from datagencars.synthetic_dataset.generator.generator_output_file.generator_user import GeneratorUserFile


class TestGeneratorUser(unittest.TestCase):

    def setUp(self):      
        data_schema_path = 'resources/generate_synthetic_dataset/rating_explicit/context/restaurant/data_schema/'
        # user_schema.conf
        user_schema_file_path = data_schema_path + 'user_schema.conf'
        with open(user_schema_file_path, 'r') as user_schema_file:
            user_schema = user_schema_file.read()        
        # generation_config.conf
        generation_config_file_path = data_schema_path + 'generation_config.conf'
        with open(generation_config_file_path, 'r') as generation_config_file:
            generation_config = generation_config_file.read()      
        # User generator:
        self.__generator = GeneratorUserFile(generation_config=generation_config, user_schema=user_schema)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_user_file(self):     
        user_file = self.__generator.generate_file()        
        logging.info(f'user_file: {user_file}')        
        self.assertEqual(user_file.shape[0], 100)                   


if __name__ == '__main__':
    unittest.main()
