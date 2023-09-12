import logging
import unittest

import pandas as pd
from datagencars.synthetic_dataset.generator.generator_output_file.generator_context import GeneratorContextFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_item import GeneratorItemFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_rating_explicit import GeneratorExplicitRatingFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_user import GeneratorUserFile


class TestGeneratorContext(unittest.TestCase):

    def setUp(self):    
        data_schema_path = 'resources/generate_synthetic_dataset/rating_explicit/context/data_schema/restaurant/'
        # generation_config:
        generation_config_file_path = data_schema_path + 'generation_config.conf'
        with open(generation_config_file_path, 'r') as generation_config_file:
            generation_config = generation_config_file.read()

        # user_schema.conf
        user_schema_file_path = data_schema_path + 'user_schema.conf'
        with open(user_schema_file_path, 'r') as user_schema_file:
            user_schema = user_schema_file.read()
        # user_df:
        user_generator = GeneratorUserFile(generation_config=generation_config, user_schema=user_schema)
        user_df = user_generator.generate_file()  

        # user_profile_df:
        user_profile_path = data_schema_path + 'user_profile.csv'
        user_profile_df = pd.read_csv(user_profile_path, encoding='utf-8', index_col=False)

        # item_schema:
        item_schema_file_path =data_schema_path + 'item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()       
        # item_df:
        item_generator = GeneratorItemFile(generation_config=generation_config, item_schema=item_schema)
        item_df = item_generator.generate_file(with_correlation=False)

        # context_schema:
        context_schema_file_path = data_schema_path + 'context_schema.conf'
        with open(context_schema_file_path, 'r') as context_schema_file:
            context_schema = context_schema_file.read() 
        # context_df:
        context_generator = GeneratorContextFile(generation_config=generation_config, context_schema=context_schema)
        context_df = context_generator.generate_file()

        # Rating generator:        
        self.__generator = GeneratorExplicitRatingFile(generation_config, user_df, user_profile_df, item_df, item_schema, context_df, context_schema)                                                
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_rating_file(self):     
        rating_file = self.__generator.generate_file(with_context=True)         
        logging.info(f'rating_file: {rating_file}')        
        self.assertEqual(rating_file.shape[0], 2000)                


if __name__ == '__main__':
    unittest.main()
