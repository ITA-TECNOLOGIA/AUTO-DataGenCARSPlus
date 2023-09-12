import logging
import unittest

import pandas as pd
from datagencars.synthetic_dataset.rating_explicit import RatingExplicit


class TestGeneratorSyntheticDatasetCARS(unittest.TestCase):

    def setUp(self):              
        self.data_schema_cars_path = 'resources/generate_synthetic_dataset/rating_explicit/context/data_schema/restaurant/'
        # generation_config.conf
        generation_config_file_path = self.data_schema_cars_path + 'generation_config.conf'
        with open(generation_config_file_path, 'r') as generation_config_file:
            generation_config = generation_config_file.read()          
        # Rating generator:        
        self.__generator = RatingExplicit(generation_config)

        # user_schema.conf
        user_schema_file_path = self.data_schema_cars_path + 'user_schema.conf'
        with open(user_schema_file_path, 'r') as user_schema_file:
            user_schema = user_schema_file.read()   
        self.user_file = self.__generator.generate_user_file(user_schema=user_schema) 

        # context_schema.conf
        context_schema_file_path = self.data_schema_cars_path + 'context_schema.conf'
        with open(context_schema_file_path, 'r') as context_schema_file:
            self.context_schema = context_schema_file.read()   
        self.context_file = self.__generator.generate_context_file(context_schema=self.context_schema)

        # user_profile_df:
        user_profile_path = self.data_schema_cars_path + 'user_profile.csv'
        self.user_profile_df = pd.read_csv(user_profile_path, encoding='utf-8', index_col=False)  
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_rating_file_cars_correlation(self):
        '''
        Generates the rating file.        
        '''    
        # item_schema.conf
        item_schema_file_path = self.data_schema_cars_path + 'item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()  
        # item_profile.conf
        item_profile_path = self.data_schema_cars_path + 'item_profile.conf'
        with open(item_profile_path, 'r') as item_profile_file:            
            item_profile = item_profile_file.read()
        # Correlation:
        with_correlation = True
        item_file = self.__generator.generate_item_file(item_schema, item_profile, with_correlation)

        # Generating rating file:      
        with_context = True        
        rating_file = self.__generator.generate_rating_file(user_df=self.user_file, user_profile_df=self.user_profile_df, item_df=item_file, item_schema=item_schema, with_context=with_context, context_df=self.context_file, context_schema=self.context_schema)
        logging.info(f'rating_file: {rating_file}')
        self.assertEqual(rating_file.shape[0], 2000)

    def test_generate_rating_file_cars_without_correlation(self):
        '''
        Generates the rating file.        
        '''    
        # item_schema.conf
        item_schema_file_path = self.data_schema_cars_path + 'item_schema.conf'
        with open(item_schema_file_path, 'r') as item_schema_file:
            item_schema = item_schema_file.read()  
        # item_profile.conf
        item_profile_path = self.data_schema_cars_path + 'item_profile.conf'
        with open(item_profile_path, 'r') as item_profile_file:            
            item_profile = item_profile_file.read()    
        # Without correlation:        
        item_file = self.__generator.generate_item_file(item_schema)

        # user_profile_df:
        user_profile_path = self.data_schema_cars_path + 'user_profile.csv'
        user_profile_df = pd.read_csv(user_profile_path, encoding='utf-8', index_col=False)       
             
        with_context = True
        rating_file = self.__generator.generate_rating_file(user_df=self.user_file, user_profile_df=self.user_profile_df, item_df=item_file, item_schema=item_schema, with_context=with_context, context_df=self.context_file, context_schema=self.context_schema)
        logging.info(f'rating_file: {rating_file}')
        self.assertEqual(rating_file.shape[0], 2000)


if __name__ == '__main__':
    unittest.main()
