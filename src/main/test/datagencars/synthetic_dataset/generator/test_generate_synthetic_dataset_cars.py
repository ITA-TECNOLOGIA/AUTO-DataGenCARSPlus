import logging
import unittest

import pandas as pd
from datagencars.synthetic_dataset.rating_explicit import RatingExplicit


class TestGeneratorSyntheticDatasetCARS(unittest.TestCase):

    def setUp(self):      
        self.data_schema_cars_path = 'resources/generate_synthetic_dataset/rating_explicit/context/restaurant/data_schema/'
        self.data_schema_rs_path = 'resources/generate_synthetic_dataset/rating_explicit/withput_context/restaurant/data_schema/'
        # generation_config.conf
        generation_config_file_path = self.data_schema_path + 'generation_config.conf'
        with open(generation_config_file_path, 'r') as generation_config_file:
            generation_config = generation_config_file.read()          
        # Item generator:        
        self.__generator = RatingExplicit(generation_config)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_user_file(self):
        '''        
        Generates the user file.        
        '''
        # user_schema.conf
        user_schema_file_path = self.data_schema_path + 'user_schema.conf'
        with open(user_schema_file_path, 'r') as user_schema_file:
            user_schema = user_schema_file.read()   
        self.user_file = self.__generator.generate_user_file(user_schema=user_schema)        
        logging.info(f'user_file: {self.user_file}')
        self.assertEqual(self.user_file.shape[0], 100)

    def test_generate_item_file_correlation(self):
        '''        
        Generates the item file with correlation.        
        '''        
        # item_schema.conf
        item_schema_file_path = self.data_schema_path + 'item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()  
        # item_profile.conf
        item_profile_path = self.data_schema_path + 'item_profile.conf'
        with open(item_profile_path, 'r') as item_profile_file:            
            item_profile = item_profile_file.read()
        # Correlation:
        with_correlation = True
        self.item_file = self.__generator.generate_item_file(item_schema, item_profile, with_correlation)
        logging.info(f'item_file: {self.item_file}')
        self.assertEqual(self.item_file.shape[0], 1000)

    def test_generate_item_file(self):
        '''        
        Generates the item file without correlation.        
        '''        
        # item_schema.conf
        item_schema_file_path = self.data_schema_path + 'item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()        
        # Without correlation:        
        self.item_file = self.__generator.generate_item_file(item_schema)
        logging.info(f'item_file: {self.item_file}')
        self.assertEqual(self.item_file.shape[0], 1000)

    def test_generate_context_file(self):
        '''        
        Generates the context file.        
        '''
        # context_schema.conf
        context_schema_file_path = self.data_schema_path + 'context_schema.conf'
        with open(context_schema_file_path, 'r') as context_schema_file:
            context_schema = context_schema_file.read()   
        self.context_file = self.__generator.generate_context_file(context_schema=context_schema)
        logging.info(f'context_file: {self.context_file}')
        self.assertEqual(self.context_file.shape[0], 1500)

    def test_generate_rating_file_cars(self):
        '''        
        Generates the rating file.        
        '''       
        # user_profile_df:
        user_profile_path = self.data_schema_path + 'user_profile.csv'
        user_profile_df = pd.read_csv(user_profile_path, encoding='utf-8', index_col=False)        
        # item_schema:
        item_schema_file_path = self.data_schema_path + 'item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()
        # context_schema:
        context_schema_file_path = self.data_schema_path + 'context_schema.conf'
        with open(context_schema_file_path, 'r') as context_schema_file:
            context_schema = context_schema_file.read()        
        with_context = True
        rating_file = self.__generator.generate_rating_file(user_df=self.user_file, user_profile_df=user_profile_df, item_df=self.item_file, item_schema=item_schema, with_context=with_context, context_df=self.context_file, context_schema=context_schema)
        logging.info(f'rating_file: {rating_file}')
        self.assertEqual(rating_file.shape[0], 2000)

    def test_generate_rating_file_rs(self):
        '''
        Generates the rating file.        
        '''       
        data_schema_path = 'resources/generate_synthetic_dataset/rating_explicit/without_context/restaurant/data_schema'
        # user_profile_df:
        user_profile_path = data_schema_path + 'user_profile.csv'
        user_profile_df = pd.read_csv(user_profile_path, encoding='utf-8', index_col=False)       
        # item_schema:
        item_schema_file_path = data_schema_path + 'item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()        
        with_context = False
        rating_file = self.__generator.generate_rating_file(user_df=self.user_file, user_profile_df=user_profile_df, item_df=self.item_file, item_schema=item_schema, with_context=with_context)
        logging.info(f'rating_file: {rating_file}')
        self.assertEqual(rating_file.shape[0], 2000)


if __name__ == '__main__':
    unittest.main()
