import logging
import unittest

import pandas as pd
from datagencars.existing_dataset.generate_user_profile.generate_user_profile_dataset import GenerateUserProfileDataset


class TestGenerateUserProfileDataset(unittest.TestCase):

    def setUp(self):
        # item.csv:
        item_file_path = 'resources/existing_dataset/context/sts/item.csv'
        item_df = pd.read_csv(item_file_path, encoding='utf-8', index_col=False, sep=';')

        # context.csv:
        context_file_path = 'resources/existing_dataset/context/sts/context.csv'
        context_df = pd.read_csv(context_file_path, encoding='utf-8', index_col=False, sep=';')

        # rating.csv:
        rating_file_path = 'resources/existing_dataset/context/sts/ratings.csv'
        rating_df = pd.read_csv(rating_file_path, encoding='utf-8', index_col=False, sep=';')
                          
        # Generate User Profile, including context:
        self.__generate_cars = GenerateUserProfileDataset(rating_df, item_df, context_df)
        # Generate User Profile, without context:
        self.__generate_rs = GenerateUserProfileDataset(rating_df, item_df)
    
    def tearDown(self):
        del self.__generate_cars
        del self.__generate_rs
    
    def test_generate_user_profile_all_attribute_cars(self):
        '''
        Gets the value of the weights (or unknown variables) by using LSMR method to generate the user profile. For CARS.
        '''         
        # All attributes:        
        item_attribute_list = ['category1', 'category2', 'category3']
        context_attribute_list = ['distance', 'timeAvailable', 'temperature', 'crowdedness', 'knowledgeOfSurroundings', 'season', 'budget', 'daytime', 'weather', 'companion', 'mood', 'weekday', 'travelGoal', 'transport']        
        # Generate user profile:
        user_profile_df = self.__generate_cars.generate_user_profile(item_attribute_list, context_attribute_list)
        logging.info(f'user_profile_df: {user_profile_df.shape[0]}')                
        self.assertEqual(user_profile_df.shape[0], 325)

    def test_generate_user_profile_relevant_attribute_cars(self):
        '''
        Gets the value of the weights (or unknown variables) by using LSMR method to generate the user profile. For CARS.
        ''' 
        # Relevant attributes:
        relevant_item_attribute_list = ['category1']
        relevant_context_attribute_list = ['distance']
        # Generate user profile:
        user_profile_df = self.__generate_cars.generate_user_profile(item_attribute_list=relevant_item_attribute_list, context_attribute_list=relevant_context_attribute_list)
        logging.info(f'user_profile_df: {user_profile_df.shape[0]}')                
        self.assertEqual(user_profile_df.shape[0], 325)

    def test_generate_user_profile_all_attribute_rs(self):
        '''
        Gets the value of the weights (or unknown variables) by using LSMR method to generate the user profile. For RS.
        '''         
        # All attributes:
        item_attribute_list = ['category1', 'category2', 'category3']        
        # Generate user profile:
        user_profile_df = self.__generate_rs.generate_user_profile(item_attribute_list)        
        logging.info(f'user_profile_df: {user_profile_df.shape[0]}')         
        self.assertEqual(user_profile_df.shape[0], 325)

    def test_generate_user_profile_relevant_attribute_rs(self):
        '''
        Gets the value of the weights (or unknown variables) by using LSMR method to generate the user profile. For RS.
        '''   
        # Relevant attributes:
        relevant_item_attribute_list = ['category1', 'category2']
        # Generate user profile:
        user_profile_df = self.__generate_rs.generate_user_profile(item_attribute_list=relevant_item_attribute_list)        
        logging.info(f'user_profile_df: {user_profile_df.shape[0]}')         
        self.assertEqual(user_profile_df.shape[0], 325)

if __name__ == '__main__':
    unittest.main()
