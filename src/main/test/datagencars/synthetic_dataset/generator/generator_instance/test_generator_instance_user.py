import logging
import unittest

from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.generator.generator_instance.generator_instance import GeneratorInstance


class TestGeneratorInstanceUser(unittest.TestCase):

    def setUp(self):        
        user_schema_file_path = 'resources/generate_synthetic_dataset/rating_explicit/context/restaurant/data_schema/user_schema.conf'
        with open(user_schema_file_path, 'r') as user_schema_file:
            user_schema = user_schema_file.read()            
        schema_access = AccessSchema(file_str=user_schema)
        self.__generator = GeneratorInstance(schema_access)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_instance_user(self):
        attribute_list = self.__generator.generate_instance()        
        logging.info(f'attribute_list: {attribute_list}')        
        self.assertEqual(len(attribute_list), 5)                   


if __name__ == '__main__':
    unittest.main()
