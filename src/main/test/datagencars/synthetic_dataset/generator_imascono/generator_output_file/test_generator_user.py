import logging
import unittest

from datagencars.synthetic_dataset.generator.generator_output_file.generator_user import GeneratorUserFile


class TestGeneratorUser(unittest.TestCase):

    def setUp(self):        
        # generation_config.conf
        generation_config_file_path = 'resources/data_schema_imascono/generation_config.conf'
        with open(generation_config_file_path, 'r') as generation_config_file:
            generation_config = generation_config_file.read()

        self.__generator = GeneratorUserFile(generation_config, user_schema=None)

    def tearDown(self):
        del self.__generator
    
    def test_generate_user_file(self):     
        user_file = self.__generator.generate_file()
        logging.info(f'user_file: {user_file}')
        user_file.to_csv('user.csv', index=False)
        self.assertEqual(user_file.shape[0], 100)


if __name__ == '__main__':
    unittest.main()
