import logging
import unittest

import pandas as pd
from datagencars.existing_dataset.extend_dataset.increase_rating import IncreaseRating


class TestIncreaseRating(unittest.TestCase):

    def setUp(self):
        # CARS:
        dataset_cars_path = 'resources/existing_dataset/context/preferencial_rating/sts/'        
        # rating_df:
        rating_file_path = dataset_cars_path + 'rating.csv'
        self.rating_df = pd.read_csv(rating_file_path, encoding='utf-8', index_col=False, sep=';')
        # user_profile_df:
        user_profile_file_path = dataset_cars_path + 'user_profile.csv'
        user_profile_df = pd.read_csv(user_profile_file_path, encoding='utf-8', index_col=False, sep=',')
        # user_df:
        user_file_path = dataset_cars_path + 'user.csv'
        user_df = pd.read_csv(user_file_path, encoding='utf-8', index_col=False, sep=';')
        # item_df:
        item_file_path = dataset_cars_path + 'item.csv'
        item_df = pd.read_csv(item_file_path, encoding='utf-8', index_col=False, sep=';')
        # context_df:
        context_file_path = dataset_cars_path + 'context.csv'
        context_df = pd.read_csv(context_file_path, encoding='utf-8', index_col=False, sep=';')

        # RS:
        dataset_rs_path = 'resources/existing_dataset/without_context/preferencial_rating/sts/'
        # rating_df:
        rating_file_path = dataset_rs_path + 'rating.csv'
        self.rating_df_rs = pd.read_csv(rating_file_path, encoding='utf-8', index_col=False, sep=';')
        # user_profile_df (RS):
        user_profile_file_path = dataset_rs_path + 'user_profile.csv'
        user_profile_df_rs = pd.read_csv(user_profile_file_path, encoding='utf-8', index_col=False, sep=',')
        # user_df:
        user_file_path = dataset_cars_path + 'user.csv'
        user_df_rs = pd.read_csv(user_file_path, encoding='utf-8', index_col=False, sep=';')
        # item_df:
        item_file_path = dataset_rs_path + 'item.csv'
        item_df_rs = pd.read_csv(item_file_path, encoding='utf-8', index_col=False, sep=';')        

        # Dataset extension generator:        
        self.__generator_cars = IncreaseRating(rating_df=self.rating_df, user_profile_df=user_profile_df, user_df=user_df, item_df=item_df, context_df=context_df)
        self.__generator_rs = IncreaseRating(rating_df=self.rating_df_rs, user_profile_df=user_profile_df_rs, user_df=user_df_rs, item_df=item_df_rs)
    
    def tearDown(self):
        del self.__generator_cars
        del self.__generator_rs

    def test_extend_rating_random_cars(self):        
        number_rating=1
        percentage_rating_variation=25
        k=10
        new_rating_df = self.__generator_cars.extend_rating_random(number_rating, percentage_rating_variation, k)           
        logging.info(f'Shape of rating_df: {self.rating_df.shape[0]}')
        logging.info(f'Shape of extended rating_df: {new_rating_df.shape[0]}') 
        self.assertEqual(self.rating_df.shape[0] + number_rating, new_rating_df.shape[0])
    
    def test_extend_rating_random_rs(self):        
        number_rating=1
        percentage_rating_variation=25
        k=10
        new_rating_df = self.__generator_rs.extend_rating_random(number_rating, percentage_rating_variation, k)           
        logging.info(f'Shape of rating_df: {self.rating_df.shape[0]}')
        logging.info(f'Shape of extended rating_df: {new_rating_df.shape[0]}') 
        self.assertEqual(self.rating_df.shape[0] + number_rating, new_rating_df.shape[0])
        
    def test_extend_rating_by_user_cars(self):        
        number_rating=1
        percentage_rating_variation=25
        k=10
        new_rating_df = self.__generator_cars.extend_rating_by_user(number_rating, percentage_rating_variation, k)
        logging.info(f'Shape of rating_df: {self.rating_df.shape[0]}')
        logging.info(f'Shape of extended rating_df: {new_rating_df.shape[0]}') 
        self.assertEqual(new_rating_df.shape[0], 2859)
    
    def test_extend_rating_by_user_rs(self):        
        number_rating=1
        percentage_rating_variation=25
        k=10
        new_rating_df = self.__generator_rs.extend_rating_by_user(number_rating, percentage_rating_variation, k)
        logging.info(f'Shape of rating_df: {self.rating_df.shape[0]}')
        logging.info(f'Shape of extended rating_df: {new_rating_df.shape[0]}') 
        self.assertEqual(new_rating_df.shape[0], 2859)


if __name__ == '__main__':
    unittest.main()
