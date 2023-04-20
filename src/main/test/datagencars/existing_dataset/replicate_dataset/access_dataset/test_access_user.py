import logging
import unittest

import pandas as pd
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_user import AccessUser


class TestAccessUser(unittest.TestCase):

    def setUp(self):             
        # user.csv
        user_file_path = 'resources/dataset_sts/user.csv'
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


if __name__ == '__main__':
    unittest.main()
