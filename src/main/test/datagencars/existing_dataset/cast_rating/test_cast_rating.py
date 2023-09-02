import logging
import unittest

import pandas as pd
from datagencars.existing_dataset.cast_rating.cast_rating import CastRating


class TestCastRating(unittest.TestCase):

    def setUp(self):
        # CARS:
        # Rating preferencial:
        dataset_preferencial_cars_path = 'resources/existing_dataset/context/sts/rating_preferencial/'                
        rating_preferencial_cars_file_path = dataset_preferencial_cars_path + 'ratings.csv'
        rating_df_preferencial_cars = pd.read_csv(rating_preferencial_cars_file_path, encoding='utf-8', index_col=False, sep=';')        
        # Rating binary:
        dataset_binary_cars_path = 'resources/existing_dataset/context/sts/rating_binary/'                
        rating_binary_cars_file_path = dataset_binary_cars_path + 'ratings.csv'        
        rating_df_binary_cars = pd.read_csv(rating_binary_cars_file_path, encoding='utf-8', index_col=False, sep=',')        
        
        # RS:
        # Rating preferencial:
        dataset_preferencial_rs_path = 'resources/existing_dataset/without_context/sts/rating_preferencial/'        
        rating_preferencial_rs_file_path = dataset_preferencial_rs_path + 'ratings.csv'
        rating_df_preferencial_rs = pd.read_csv(rating_preferencial_rs_file_path, encoding='utf-8', index_col=False, sep=';')
        # Rating binary:
        dataset_binary_rs_path = 'resources/existing_dataset/without_context/sts/rating_binary/'                
        rating_binary_rs_file_path = dataset_binary_rs_path + 'ratings.csv'
        rating_df_binary_rs = pd.read_csv(rating_binary_rs_file_path, encoding='utf-8', index_col=False, sep=',')
       
        # Dataset replication generator:        
        self.__generator_preferencial_cars = CastRating(rating_df=rating_df_preferencial_cars)
        self.__generator_binary_cars = CastRating(rating_df=rating_df_binary_cars)
        self.__generator_preferencial_rs = CastRating(rating_df=rating_df_preferencial_rs)
        self.__generator_binary_rs = CastRating(rating_df=rating_df_binary_rs)
    
    def tearDown(self):
        del self.__generator_preferencial_cars
        del self.__generator_binary_cars
        del self.__generator_preferencial_rs
        del self.__generator_binary_rs
    
    def test_rating_preferencial_to_binary_cars(self):
        threshold = 3 
        new_rating_df = self.__generator_preferencial_cars.rating_preferencial_to_binary(threshold)            
        logging.info(f'rating_file: {new_rating_df}')
        generator = CastRating(rating_df=new_rating_df)
        self.assertEqual(generator.is_binary_rating(), True)

    def test_rating_preferencial_to_binary_rs(self):
        threshold = 3 
        new_rating_df = self.__generator_preferencial_rs.rating_preferencial_to_binary(threshold)
        logging.info(f'rating_file: {new_rating_df}')
        generator = CastRating(rating_df=new_rating_df)
        self.assertEqual(generator.is_binary_rating(), True)

    def test_rating_binary_to_preferencial_cars(self):
        scale = 5 
        threshold = 3
        new_rating_df = self.__generator_binary_cars.rating_binary_to_preferencial(scale, threshold)        
        logging.info(f'rating_file: {new_rating_df}')
        generator = CastRating(rating_df=new_rating_df)
        self.assertEqual(generator.is_preferencial_rating(), True)    

    def test_rating_binary_to_preferencial_rs(self):
        scale = 5 
        threshold = 3
        new_rating_df = self.__generator_binary_rs.rating_binary_to_preferencial(scale, threshold)
        logging.info(f'rating_file: {new_rating_df}')
        generator = CastRating(rating_df=new_rating_df)
        self.assertEqual(generator.is_preferencial_rating(), True)

    def test_set_binary_rating_label_cars(self):
        new_rating_df = self.__generator_binary_cars.set_binary_rating_label(label_1='like', label_0='dislike')
        logging.info(f'rating_file: {new_rating_df}')
        rating_label_list = new_rating_df['rating'].dropna().unique().tolist()  
        self.assertEqual(len(rating_label_list), 2)

    def test_set_binary_rating_label_rs(self):
        new_rating_df = self.__generator_binary_rs.set_binary_rating_label(label_1='like', label_0='dislike')
        logging.info(f'rating_file: {new_rating_df}')
        rating_label_list = new_rating_df['rating'].dropna().unique().tolist()  
        self.assertEqual(len(rating_label_list), 2)


if __name__ == '__main__':
    unittest.main()
