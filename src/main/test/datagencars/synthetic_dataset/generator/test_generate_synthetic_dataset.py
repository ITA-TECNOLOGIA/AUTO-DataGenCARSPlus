import logging
import unittest

import pandas as pd
from datagencars.synthetic_dataset.rating_explicit import GenerateSyntheticDataset


class TestGeneratorSyntheticDataset(unittest.TestCase):

    def setUp(self):             
        # generation_config.conf
        generation_config_file_path = 'resources/data_schema/generation_config.conf'
        with open(generation_config_file_path, 'r') as generation_config_file:
            generation_config = generation_config_file.read()          
        # Item generator:        
        self.__generator = GenerateSyntheticDataset(generation_config)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_user_file(self):
        '''        
        Generates the user file.        
        '''
        # user_schema.conf
        user_schema_file_path = 'resources/data_schema/user_schema.conf'
        with open(user_schema_file_path, 'r') as user_schema_file:
            user_schema = user_schema_file.read()   
        user_file = self.__generator.generate_user_file(user_schema=user_schema)        
        logging.info(f'user_file: {user_file}')
        self.assertEqual(user_file.shape[0], 100)

    def test_generate_item_file_correlation(self):
        '''        
        Generates the item file with correlation.        
        '''        
        # item_schema.conf
        item_schema_file_path = 'resources/data_schema/item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()  
        # item_profile.conf
        item_profile_path = 'resources/data_schema/item_profile.conf'
        with open(item_profile_path, 'r') as item_profile_file:            
            item_profile = item_profile_file.read()
        # Correlation:
        with_correlation = True
        item_file = self.__generator.generate_item_file(item_schema, item_profile, with_correlation)
        logging.info(f'item_file: {item_file}')
        self.assertEqual(item_file.shape[0], 1000)

    def test_generate_item_file(self):
        '''        
        Generates the item file without correlation.        
        '''        
        # item_schema.conf
        item_schema_file_path = 'resources/data_schema/item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()        
        # Without correlation:        
        item_file = self.__generator.generate_item_file(item_schema)
        logging.info(f'item_file: {item_file}')
        self.assertEqual(item_file.shape[0], 1000)

    def test_generate_context_file(self):
        '''        
        Generates the context file.        
        '''
        # context_schema.conf
        context_schema_file_path = 'resources/data_schema/context_schema.conf'
        with open(context_schema_file_path, 'r') as context_schema_file:
            context_schema = context_schema_file.read()   
        context_file = self.__generator.generate_context_file(context_schema=context_schema)
        logging.info(f'context_file: {context_file}')
        self.assertEqual(context_file.shape[0], 1500)

    def test_generate_rating_file_cars(self):
        '''        
        Generates the rating file.        
        '''
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

        with_context = True
        rating_file = self.__generator.generate_rating_file(user_df, user_profile_df, item_df, item_schema, with_context, context_df, context_schema)
        logging.info(f'rating_file: {rating_file}')
        self.assertEqual(rating_file.shape[0], 2000)

    def test_generate_rating_file(self):
        '''        
        Generates the rating file.        
        '''
        # user_df:
        user_path = 'resources/data_schema/user.csv'
        user_df = pd.read_csv(user_path, encoding='utf-8', index_col=False)
        # user_profile_df:
        user_profile_path = 'resources/data_schema/user_profile_2d.csv'
        user_profile_df = pd.read_csv(user_profile_path, encoding='utf-8', index_col=False)
        # item_df:
        item_path = 'resources/data_schema/item.csv'
        item_df = pd.read_csv(item_path, encoding='utf-8', index_col=False)
        # item_schema:
        item_schema_file_path = 'resources/data_schema/item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()
        
        with_context = False
        rating_file = self.__generator.generate_rating_file(user_df, user_profile_df, item_df, item_schema, with_context)        
        logging.info(f'rating_file: {rating_file}')
        self.assertEqual(rating_file.shape[0], 2000)


if __name__ == '__main__':
    unittest.main()
