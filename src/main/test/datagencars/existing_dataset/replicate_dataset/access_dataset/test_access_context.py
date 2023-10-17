import logging
import unittest

import pandas as pd

from datagencars.existing_dataset.replicate_dataset.access_dataset.access_context import AccessContext


class TestAccessContext(unittest.TestCase):

    def setUp(self):             
        # context.csv
        context_file_path = 'resources/existing_dataset/context/preferencial_rating/sts/context.csv'
        context_df = pd.read_csv(context_file_path, encoding='utf-8', index_col=False, sep=';')
        # Access context:
        self.__access = AccessContext(context_df)
    
    def tearDown(self):
        del self.__access
    
    def test_get_context_id_list(self):        
        '''
        Gets a list with unique values of context_id.
        '''         
        context_id_list = self.__access.get_context_id_list()
        logging.info(f'context_id_list: {context_id_list}')                
        self.assertEqual(len(context_id_list), 2534)

    def test_get_context_attribute_list(self):               
        '''
        Gets a list of context attributes.
        '''
        context_attribute_list = self.__access.get_context_attribute_list()
        logging.info(f'context_attribute_list: {context_attribute_list}')                
        self.assertEqual(len(context_attribute_list), 14)   

    def test_get_context_value_from_context_attributte(self):               
        '''
        Gets an context value from context_id and attribute name.
        '''
        context_value = self.__access.get_context_value_from_context_attributte(context_id=1, attribute_name='temperature')
        logging.info(f'context_value: {context_value}')                
        self.assertEqual(context_value, 5)  

    def test_get_context_possible_value_list_from_attributte(self):               
        '''
        Gets a list of context possible values from a specific attribute.
        '''
        context_possible_value_list = self.__access.get_context_possible_value_list_from_attributte(attribute_name='temperature')
        logging.info(f'context_possible_value_list: {context_possible_value_list}')                
        self.assertEqual(len(context_possible_value_list), 6)
    

if __name__ == '__main__':
    unittest.main()
