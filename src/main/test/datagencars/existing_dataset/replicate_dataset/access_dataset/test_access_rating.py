import logging
import unittest

import pandas as pd

from datagencars.existing_dataset.replicate_dataset.access_dataset.access_rating import AccessRating


class TestAccessRating(unittest.TestCase):

    def setUp(self):             
        # rating.csv
        rating_file_path = 'resources/existing_dataset/context/preferencial_rating/sts/rating.csv'
        rating_df = pd.read_csv(rating_file_path, encoding='utf-8', index_col=False, sep=';')
        # Access rating:
        self.__access = AccessRating(rating_df)
    
    def tearDown(self):
        del self.__access
    
    def test_get_min_rating(self):        
        '''
        Gets the minimum rating value.
        '''         
        min_rating = self.__access.get_min_rating()
        logging.info(f'min_rating: {min_rating}')                
        self.assertEqual(min_rating, 1)

    def test_get_max_rating(self):        
        '''
        Gets the minimum rating value.
        '''         
        max_rating = self.__access.get_max_rating()
        logging.info(f'max_rating: {max_rating}')                
        self.assertEqual(max_rating, 5)

    def test_get_user_id_list(self):        
        '''
        Gets a list with unique values of user_id.
        '''         
        user_id_list = self.__access.get_user_id_list()
        logging.info(f'user_id_list: {user_id_list}')                
        self.assertEqual(len(user_id_list), 325)

    def test_get_item_id_list_from_user_false(self):        
        '''
        Gets a list of item_id from a specific user.
        unique_values=False
        '''         
        item_id_list = self.__access.get_item_id_list_from_user(user_id=1)
        logging.info(f'item_id_list: {item_id_list}')                
        self.assertEqual(len(item_id_list), 175)

    def test_get_item_id_list_from_user_true(self):        
        '''
        Gets a list of item_id from a specific user.
        unique_values=True        
        '''         
        item_id_list = self.__access.get_item_id_list_from_user(user_id=1, unique_values=True)
        logging.info(f'item_id_list: {item_id_list}')                
        self.assertEqual(len(item_id_list), 8)

    def test_get_context_id_list_from_user_false(self):        
        '''
        Gets a list of context_id from a specific user.
        unique_values=False
        '''         
        context_id_list = self.__access.get_context_id_list_from_user(user_id=1)
        logging.info(f'context_id_list: {context_id_list}')                
        self.assertEqual(len(context_id_list), 175)

    def test_get_context_id_list_from_user_true(self):        
        '''
        Gets a list of context_id from a specific user.
        unique_values=True        
        '''         
        context_id_list = self.__access.get_context_id_list_from_user(user_id=1, unique_values=True)
        logging.info(f'context_id_list: {context_id_list}')                
        self.assertEqual(len(context_id_list), 175)

    def test_get_rating_list_from_user(self):        
        '''
        Gets a list of ratings from a specific user.
        '''         
        rating_list = self.__access.get_rating_list_from_user(user_id=1)
        logging.info(f'rating_list: {rating_list}')
        self.assertEqual(len(rating_list), 175)

    def test_get_rating_list_from_user_item(self):        
        '''
        Gets a list of ratings from a specific user and item.
        '''         
        rating_list = self.__access.get_rating_list_from_user_item(user_id=1, item_id=1)
        logging.info(f'rating_list: {rating_list}')
        self.assertEqual(len(rating_list), 43)

    def test_get_rating_list_from_user_item_context(self):        
        '''
        Gets a list of ratings from a specific user, item and context.
        '''         
        rating_list = self.__access.get_rating_list_from_user_item_context(user_id=1, item_id=1, context_id=1)
        logging.info(f'rating_list: {rating_list}')
        self.assertEqual(len(rating_list), 1)
            

if __name__ == '__main__':
    unittest.main()
