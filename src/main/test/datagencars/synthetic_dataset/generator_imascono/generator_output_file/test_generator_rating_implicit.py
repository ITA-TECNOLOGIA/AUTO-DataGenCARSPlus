import logging
import unittest

import pandas as pd
from datagencars.synthetic_dataset.generator.generator_output_file.generator_rating_implicit import GeneratorImplicitRatingFile


class TestGeneratorContext(unittest.TestCase):

    def setUp(self):
        schema_path = 'resources/generate_synthetic_dataset/rating_implicit/context/data_schema/imascono/'
        # generation_config:
        generation_config_file_path = schema_path + 'generation_config.conf'
        with open(generation_config_file_path, 'r') as generation_config_file:
            generation_config = generation_config_file.read()

        # item_df:
        item_path = schema_path + 'item.csv'
        item_df = pd.read_csv(item_path, encoding='utf-8', index_col=False)

        # behavior_df:
        behavior_path = schema_path + 'behavior.csv'
        behavior_df = pd.read_csv(behavior_path, encoding='utf-8', index_col=False)

        # context_df:
        context_path = schema_path + 'context.csv'
        context_df = pd.read_csv(context_path, encoding='utf-8', index_col=False)
       
        # Rating generator:
        self.__generator = GeneratorImplicitRatingFile(generation_config, item_df, behavior_df, context_df=context_df)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_rating_file(self):
        rating_file = self.__generator.generate_file(with_context=True)
        logging.info(f'rating_file: {rating_file}')
        rating_file.to_csv('resources/generate_synthetic_dataset/rating_implicit/context/data_schema/imascono/rating.csv', index=False)
        self.assertFalse(rating_file.empty)

if __name__ == '__main__':
    unittest.main()
