import logging
import unittest
import pandas as pd
from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.generator.generator_output_file.generator_behavior import GeneratorBehaviorFile


class TestGeneratorBehavior(unittest.TestCase):

    def setUp(self):
        schema_path = 'resources/generate_synthetic_dataset/rating_implicit/context/data_schema/imascono/'
        # generation_config.conf
        generation_config_file_path = schema_path + 'generation_config.conf'
        with open(generation_config_file_path, 'r') as generation_config_file:
            generation_config = generation_config_file.read()

        # behavior_schema.conf
        behavior_schema_file_path = schema_path + 'behavior_schema.conf'
        with open(behavior_schema_file_path, 'r') as behavior_schema_file:
            behavior_schema = behavior_schema_file.read()

        # item_df:
        item_path = schema_path + 'item.csv'
        item_df = pd.read_csv(item_path, encoding='utf-8', index_col=False)

        item_schema_file_path = schema_path + 'item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()
        
        # Behavior generator:
        self.__generator = GeneratorBehaviorFile(generation_config, behavior_schema, item_df, item_schema)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_behavior_file(self):
        behavior_file = self.__generator.generate_file()
        logging.info(f'behavior_file: {behavior_file}')
        behavior_file.to_csv('resources/generate_synthetic_dataset/rating_implicit/context/data_schema/imascono/behavior.csv', index=False)
        # If, for instance, the last action generated is Play, a Pause action will be generated
        self.assertAlmostEqual(behavior_file.shape[0], 55867, delta=1)

if __name__ == '__main__':
    unittest.main()
