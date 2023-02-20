import logging
import unittest

import pandas as pd
from datagencars.synthetic_dataset.generator.generator_output_file.generator_rating import GeneratorRatingFile


class TestGeneratorContext(unittest.TestCase):

    def setUp(self):        
        # generation_config:
        generation_config_file_path = 'resources/data_schema/generation_config.conf'
        with open(generation_config_file_path, 'r') as generation_config_file:
            generation_config = generation_config_file.read()

        # user_df:
        user_path = 'resources/data_schema/user.csv'
        user_df = pd.read_csv(user_path, encoding='utf-8', index_col=False)

        # user_profile_df:
        user_profile_path = 'resources/data_schema/user_profile.csv'
        user_profile_df = pd.read_csv(user_profile_path, encoding='utf-8', index_col=False)

        # item_df:
        item_path = 'resources/data_schema/item.csv'
        item_df = pd.read_csv(item_path, encoding='utf-8', index_col=False)

        # item_schema:
        item_schema_file_path = 'resources/data_schema/item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()

        # context_schema:
        context_schema_file_path = 'resources/data_schema/context_schema.conf'
        with open(context_schema_file_path, 'r') as context_schema_file:
            context_schema = context_schema_file.read() 

        # context_df:
        context_path = 'resources/data_schema/context.csv'
        context_df = pd.read_csv(context_path, encoding='utf-8', index_col=False)
       
        # Rating generator:        
        self.__generator = GeneratorRatingFile(generation_config, user_df, user_profile_df, item_df, item_schema, context_df, context_schema)                                                
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_rating_file(self):     
        rating_file = self.__generator.generate_file(with_context=True)         
        logging.info(f'rating_file: {rating_file}')        
        self.assertEqual(rating_file.shape[0], 2000)                


if __name__ == '__main__':
    unittest.main()
