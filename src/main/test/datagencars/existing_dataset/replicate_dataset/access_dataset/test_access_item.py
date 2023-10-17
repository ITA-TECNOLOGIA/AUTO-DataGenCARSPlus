import logging
import unittest

import pandas as pd
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_item import AccessItem


class TestAccessItem(unittest.TestCase):

    def setUp(self):             
        # item.csv
        item_file_path = 'resources/existing_dataset/context/preferencial_rating/sts/item.csv'
        item_df = pd.read_csv(item_file_path, encoding='utf-8', index_col=False, sep=';')
        # Access item:
        self.__access = AccessItem(item_df)
    
    def tearDown(self):
        del self.__access
    
    def test_get_item_list(self):        
        '''
        Gets a list with unique values of user_id.
        '''         
        item_id_list = self.__access.get_item_list()
        logging.info(f'item_id_list: {item_id_list}')                
        self.assertEqual(len(item_id_list), 249)

    def test_get_item_attribute_list(self):               
        '''
        Gets a list of item attributes.
        '''
        item_attribute_list = self.__access.get_item_attribute_list()
        logging.info(f'item_attribute_list: {item_attribute_list}')                
        self.assertEqual(len(item_attribute_list), 3)   

    def test_get_item_value_from_item_attributte(self):               
        '''
        Gets an item value from item_id and attribute name.
        '''
        item_value = self.__access.get_item_value_from_item_attributte(item_id=1, attribute_name='category1')
        logging.info(f'item_value: {item_value}')                
        self.assertEqual(item_value, 1)  

    def test_get_item_possible_value_list_from_attributte(self):               
        '''
        Gets a list of item possible values from a specific attribute.
        '''
        item_possible_value_list = self.__access.get_item_possible_value_list_from_attributte(attribute_name='category1')
        logging.info(f'item_possible_value_list: {item_possible_value_list}')                
        self.assertEqual(len(item_possible_value_list), 27)  
    

if __name__ == '__main__':
    unittest.main()