import logging
import unittest

import pandas as pd

from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_rating import ExtractStatisticsRating


class TestExtractStatisticsRating(unittest.TestCase):

    def setUp(self):             
        # rating.csv
        rating_file_path = 'resources/existing_dataset/context/preferencial_rating/sts/rating.csv'
        rating_df = pd.read_csv(rating_file_path, encoding='utf-8', index_col=False, sep=';')        
        # Extract Statistics of Ratings:
        self.__extract = ExtractStatisticsRating(rating_df)
    
    def tearDown(self):
        del self.__extract
    
    def test_get_number_ratings(self):
        '''
        Gets the number of ratings.
        '''         
        number_ratings = self.__extract.get_number_ratings()
        logging.info(f'number_ratings: {number_ratings}')                
        self.assertEqual(number_ratings, 2534) 

    def test_get_number_users(self):
        '''
        Gets the number total of users.
        '''         
        number_users = self.__extract.get_number_users()
        logging.info(f'number_users: {number_users}')                
        self.assertEqual(number_users, 325)

    def test_get_number_items(self):
        '''
        Gets the number total of items.
        '''         
        number_items = self.__extract.get_number_items()
        logging.info(f'number_items: {number_items}')                
        self.assertEqual(number_items, 249)

    def test_get_number_contexts(self):
        '''
        Gets the number total of contexts.
        '''         
        number_contexts = self.__extract.get_number_contexts()
        logging.info(f'number_contexts: {number_contexts}')                
        self.assertEqual(number_contexts, 2534)

    def test_get_number_ratings_by_user(self):
        '''
        Gets the number ratings by user.
        '''         
        number_ratings_df = self.__extract.get_number_ratings_by_user()        
        number_ratings = number_ratings_df.loc[number_ratings_df['user_id'] == 1, 'count_ratings'].iloc[0]
        logging.info(f'number_ratings: {number_ratings}')                
        self.assertEqual(number_ratings, 175)

    def test_get_percentage_ratings_by_user(self):
        '''
        Gets percentage of ratings by user.
        '''         
        percentage_ratings_df = self.__extract.get_percentage_ratings_by_user()                
        percentage_ratings = percentage_ratings_df.loc[percentage_ratings_df['user_id'] == 1, 'percentage_ratings'].iloc[0]
        logging.info(f'percentage_ratings: {percentage_ratings}')                
        self.assertEqual(percentage_ratings, 6.91)

    def test_get_avg_ratings_by_user(self):
        '''
        Gets the average of ratings by user.
        '''         
        avg_ratings_df = self.__extract.get_avg_ratings_by_user()             
        avg_ratings = avg_ratings_df.loc[avg_ratings_df['user_id'] == 1, 'avg_ratings'].iloc[0]
        logging.info(f'avg_ratings: {avg_ratings}')                
        self.assertEqual(avg_ratings, 3.39)

    def test_get_variance_ratings_by_user(self):
        '''
        Gets the variance of ratings by user.
        '''         
        variance_ratings_df = self.__extract.get_variance_ratings_by_user()                
        variance_ratings = variance_ratings_df.loc[variance_ratings_df['user_id'] == 1, 'variance_ratings'].iloc[0]
        logging.info(f'variance_ratings: {variance_ratings}')                
        self.assertEqual(variance_ratings, 1.13)

    def test_get_sd_ratings_by_user(self):
        '''
        Gets the standard deviation of ratings by user.
        '''         
        sd_ratings_df = self.__extract.get_sd_ratings_by_user()               
        sd_ratings = sd_ratings_df.loc[sd_ratings_df['user_id'] == 1, 'sd_ratings'].iloc[0]
        logging.info(f'sd_ratings: {sd_ratings}')                
        self.assertEqual(sd_ratings, 1.06)

    def test_get_number_items_from_user(self):
        '''
        Gets the number of items rated by a user.
        '''         
        counts_items, unique_items, total_count = self.__extract.get_number_items_from_user(selected_user=1)        
        logging.info(f'counts_items: {counts_items}')  
        logging.info(f'unique_items: {unique_items}')  
        logging.info(f'number_items_from_user: {total_count}')                
        self.assertEqual(total_count, 175)

    def test_get_avg_items_by_user(self):
        '''
        Gets the average of items by user.
        '''         
        avg_items_df = self.__extract.get_avg_items_by_user()                  
        avg_items = avg_items_df.loc[avg_items_df['user_id'] == 1, 'avg_items'].iloc[0]
        logging.info(f'avg_items: {avg_items}')                
        self.assertEqual(avg_items, 2.64)

    def test_get_variance_items_by_user(self):
        '''
        Gets the variance of items by user.
        '''         
        variance_items_df = self.__extract.get_variance_items_by_user()                   
        variance_items = variance_items_df.loc[variance_items_df['user_id'] == 1, 'variance_items'].iloc[0]
        logging.info(f'variance_items: {variance_items}')                
        self.assertEqual(variance_items, 5.82)

    def test_get_sd_items_by_user(self):
        '''
        Gets the standard deviation of items by user.
        '''         
        sd_items_df = self.__extract.get_sd_items_by_user()                   
        sd_items = sd_items_df.loc[sd_items_df['user_id'] == 1, 'sd_items'].iloc[0]
        logging.info(f'sd_items: {sd_items}')                
        self.assertEqual(sd_items, 2.4)

    def test_get_number_not_repeated_items_by_user(self):
        '''
        Gets the number of items not repeated by user.
        '''         
        number_not_repeated_items_df = self.__extract.get_number_not_repeated_items_by_user()                   
        number_not_repeated_items = number_not_repeated_items_df.loc[number_not_repeated_items_df['user_id'] == 1, 'not_repeated_items'].iloc[0]
        logging.info(f'number_not_repeated_items: {number_not_repeated_items}')                
        self.assertEqual(number_not_repeated_items, 0)

    def test_get_percentage_not_repeated_items_by_user(self):
        '''
        Gets the porcentage of items not repeated by user.
        '''         
        percentage_not_repeated_items_df = self.__extract.get_percentage_not_repeated_items_by_user()                   
        percentage_not_repeated_items = percentage_not_repeated_items_df.loc[percentage_not_repeated_items_df['user_id'] == 1, 'percentage_not_repeated_items'].iloc[0]
        logging.info(f'percentage_not_repeated_items: {percentage_not_repeated_items}')                
        self.assertEqual(percentage_not_repeated_items, 0)
    
    def test_get_percentage_repeated_items_by_user(self):
        '''
        Gets the porcentage of items repeated by user.
        '''
        percentage_repeated_items_df = self.__extract.get_percentage_repeated_items_by_user()                   
        percentage_repeated_items = percentage_repeated_items_df.loc[percentage_repeated_items_df['user_id'] == 1, 'porcentage_repeated_items'].iloc[0]
        logging.info(f'percentage_repeated_items: {percentage_repeated_items}')                
        self.assertEqual(percentage_repeated_items, 100)
        
    def test_get_avg_contexts_by_user(self):
        '''
        Gets the average of contexts by user.
        '''
        avg_contexts_df = self.__extract.get_avg_contexts_by_user()                   
        avg_contexts = avg_contexts_df.loc[avg_contexts_df['user_id'] == 1, 'avg_contexts'].iloc[0]
        logging.info(f'avg_contexts: {avg_contexts}')                
        self.assertEqual(avg_contexts, 12.53)

    def test_get_variance_contexts_by_user(self):
        '''
        Gets the average of contexts by user.
        '''
        variance_contexts_df = self.__extract.get_variance_contexts_by_user()                   
        variance_contexts = variance_contexts_df.loc[variance_contexts_df['user_id'] == 1, 'variance_contexts'].iloc[0]
        logging.info(f'variance_contexts: {variance_contexts}')
        self.assertEqual(variance_contexts, 2711.16)

    def test_get_sd_contexts_by_user(self):
        '''
        Gets the standard deviation of contexts by user.
        '''
        sd_contexts_df = self.__extract.get_sd_contexts_by_user()                   
        sd_contexts = sd_contexts_df.loc[sd_contexts_df['user_id'] == 1, 'sd_contexts'].iloc[0]
        logging.info(f'sd_contexts: {sd_contexts}')
        self.assertEqual(sd_contexts, 51.92)

    def test_get_number_not_repeated_contexts_by_user(self):
        '''
        Gets the number of contexts not repeated by user.
        '''
        number_not_repeated_contexts_df = self.__extract.get_number_not_repeated_contexts_by_user()                   
        number_not_repeated_contexts = number_not_repeated_contexts_df.loc[number_not_repeated_contexts_df['user_id'] == 1, 'not_repeated_contexts'].iloc[0]
        logging.info(f'number_not_repeated_contexts: {number_not_repeated_contexts}')
        self.assertEqual(number_not_repeated_contexts, 175)

    def test_get_percentage_not_repeated_contexts_by_user(self):
        '''
        Gets the porcentage of contexts not repeated by user.
        '''
        percentage_not_repeated_contexts_df = self.__extract.get_percentage_not_repeated_contexts_by_user()                   
        percentage_not_repeated_contexts = percentage_not_repeated_contexts_df.loc[percentage_not_repeated_contexts_df['user_id'] == 1, 'percentage_not_repeated_contexts'].iloc[0]
        logging.info(f'percentage_not_repeated_contexts: {percentage_not_repeated_contexts}')
        self.assertEqual(percentage_not_repeated_contexts, 100)

    def test_get_percentage_repeated_contexts_by_user(self):
        '''
        Gets the porcentage of contexts repeated by user.
        '''
        percentage_repeated_contexts_df = self.__extract.get_percentage_repeated_contexts_by_user()                   
        percentage_repeated_contexts = percentage_repeated_contexts_df.loc[percentage_repeated_contexts_df['user_id'] == 1, 'porcentage_repeated_contexts'].iloc[0]
        logging.info(f'percentage_repeated_contexts: {percentage_repeated_contexts}')
        self.assertEqual(percentage_repeated_contexts, 0)
        

if __name__ == '__main__':
    unittest.main()
