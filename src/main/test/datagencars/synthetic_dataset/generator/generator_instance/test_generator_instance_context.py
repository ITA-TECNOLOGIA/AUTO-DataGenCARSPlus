import logging
import unittest

from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.generator.generator_instance.generator_instance import GeneratorInstance


class TestGeneratorInstanceContext(unittest.TestCase):

    def setUp(self):        
        context_schema_file_path = 'resources/data_schema/context_schema.conf'
        with open(context_schema_file_path, 'r') as context_schema_file:
            context_schema = context_schema_file.read()            
        schema_access = AccessSchema(file_str=context_schema)
        self.__generator = GeneratorInstance(schema_access)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_instance_context(self):
        attribute_list = self.__generator.generate_instance()        
        logging.info(f'attribute_list: {attribute_list}')        
        self.assertEqual(len(attribute_list), 7)                   


if __name__ == '__main__':
    unittest.main()
