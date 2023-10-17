import logging
import unittest

import pandas as pd
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_user import AccessUser


class TestAccessUser(unittest.TestCase):

    def setUp(self):             
        # user.csv
        user_file_path = 'resources/existing_dataset/context/preferencial_rating/sts/user.csv'
        user_df = pd.read_csv(user_file_path, encoding='utf-8', index_col=False, sep=';')        
        # Access user:
        self.__access = AccessUser(user_df)
    
    def tearDown(self):
        del self.__access
    
    def test_get_user_id_list(self):        
        '''
        Gets a list with unique values of user_id.
        '''         
        user_id_list = self.__access.get_user_id_list()
        logging.info(f'user_id_list: {user_id_list}')
        self.assertEqual(len(user_id_list), 325)

    def test_get_user_attribute_list(self):
        '''
        Gets a list of user attributes.
        '''
        user_attribute_list = self.__access.get_user_attribute_list()
        logging.info(f'user_attribute_list: {user_attribute_list}')
        self.assertEqual(len(user_attribute_list), 7)

    def test_is_user_profile_id(self):
        '''
        Check if the 'user_df' dataframe has a column named 'user_profile_id'.
        '''
        if_user_profile_id = self.__access.is_user_profile_id()
        logging.info(f'if_user_profile_id: {if_user_profile_id}')
        self.assertEqual(if_user_profile_id, False)

    def test_get_count_user_profile_id(self):
        '''
        Get the count of unique values in the 'user_profile_id' column of the 'user_df' dataframe.
        '''
        count_user_profile_id = self.__access.get_count_user_profile_id()
        logging.info(f'count_user_profile_id: {count_user_profile_id}')
        self.assertEqual(count_user_profile_id, 0)

    def test_get_count_user_profile_id(self):
        '''
        Get the count of unique values in the 'user_profile_id' column of the 'user_df' dataframe.
        '''
        user_profile_id = self.__access.get_user_profile_id_from_user_id(user_id=4)        
        logging.info(f'user_profile_id: {user_profile_id}')
        self.assertEqual(user_profile_id, 0)        


if __name__ == '__main__':
    unittest.main()
