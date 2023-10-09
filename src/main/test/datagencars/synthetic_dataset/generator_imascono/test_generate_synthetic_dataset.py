import logging
import unittest

import pandas as pd
from datagencars.synthetic_dataset.generate_synthetic_implicit_dataset import RatingImplicit


class TestGeneratorSyntheticDataset(unittest.TestCase):

    def setUp(self):     
        schema_path = 'resources/generate_synthetic_dataset/rating_implicit/context/data_schema/imascono/'        
        # generation_config.conf
        generation_config_file_path = schema_path + 'generation_config.conf'
        with open(generation_config_file_path, 'r') as generation_config_file:
            generation_config = generation_config_file.read()          
        # Item generator:        
        self.__generator = RatingImplicit(generation_config)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_user_file(self):
        '''        
        Generates the user file.        
        '''
        schema_path = 'resources/generate_synthetic_dataset/rating_implicit/context/data_schema/imascono/'   
        # user_schema.conf
        user_schema_file_path = schema_path + 'user_schema.conf'
        with open(user_schema_file_path, 'r') as user_schema_file:
            user_schema = user_schema_file.read()   
        user_file = self.__generator.generate_user_file(user_schema=user_schema)        
        logging.info(f'user_file: {user_file}')
        user_file.to_csv(schema_path + 'user.csv', index=False)
        self.assertEqual(user_file.shape[0], 13820)

    def test_generate_item_file(self):
        '''        
        Generates the item file without correlation.        
        '''        
        schema_path = 'resources/generate_synthetic_dataset/rating_implicit/context/data_schema/imascono/'  
        # item_schema.conf
        item_schema_file_path = schema_path + 'item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()        
        # Without correlation:        
        item_file = self.__generator.generate_item_file(item_schema)
        logging.info(f'item_file: {item_file}')
        item_file.to_csv(schema_path + 'item.csv', index=False)
        self.assertEqual(item_file.shape[0], 25)

    def test_generate_context_file(self):
        '''
        Generates the context file.
        '''
        schema_path = 'resources/generate_synthetic_dataset/rating_implicit/context/data_schema/imascono/' 
        # context_schema.conf
        context_schema_file_path = schema_path + 'context_schema.conf'
        with open(context_schema_file_path, 'r') as context_schema_file:
            context_schema = context_schema_file.read()   
        context_file = self.__generator.generate_context_file(context_schema=context_schema)
        logging.info(f'context_file: {context_file}')
        context_file.to_csv(schema_path + 'context.csv', index=False)
        self.assertEqual(context_file.shape[0], 142)

    def test_generate_behavior_file(self):
        '''        
        Generates the behavior file.        
        '''
        schema_path = 'resources/generate_synthetic_dataset/rating_implicit/context/data_schema/imascono/' 
        # behavior_schema.conf
        behavior_schema_file_path = schema_path + 'behavior_schema.conf'
        with open(behavior_schema_file_path, 'r') as behavior_schema_file:
            behavior_schema = behavior_schema_file.read()
        # item_schema.conf
        item_schema_file_path = schema_path + 'item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()
        # item_df:
        item_path = 'resources/data_schema_imascono/item.csv'
        item_df = pd.read_csv(item_path, encoding='utf-8', index_col=False)

        behavior_file = self.__generator.generate_behavior_file(behavior_schema, item_df, item_schema)
        logging.info(f'behavior_file: {behavior_file}')
        behavior_file.to_csv('resources/data_schema_imascono/behavior.csv', index=False)
        self.assertAlmostEqual(behavior_file.shape[0], 55867, delta=1)

    def test_generate_rating_file_cars(self):
        '''        
        Generates the rating file.        
        '''
        dataset_path = 'resources/generate_synthetic_dataset/rating_implicit/context/data_schema/imascono/' 
        # user_df:
        user_path = dataset_path + 'user.csv'
        user_df = pd.read_csv(user_path, encoding='utf-8', index_col=False)
        # item_df:
        item_path = dataset_path + 'item.csv'
        item_df = pd.read_csv(item_path, encoding='utf-8', index_col=False)
        # context_df:
        context_path = dataset_path + 'context.csv'
        context_df = pd.read_csv(context_path, encoding='utf-8', index_col=False)
        with_context = True
        # behavior_df:
        behavior_path = dataset_path + 'behavior.csv'
        behavior_df = pd.read_csv(behavior_path, encoding='utf-8', index_col=False)

        rating_file = self.__generator.generate_rating_file(item_df, behavior_df, with_context, context_df)
        logging.info(f'rating_file: {rating_file}')
        rating_file.to_csv('resources/data_schema_imascono/rating.csv', index=False)
        self.assertFalse(rating_file.empty)


if __name__ == '__main__':
    unittest.main()
