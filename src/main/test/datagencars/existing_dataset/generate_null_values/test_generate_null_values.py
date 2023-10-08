import logging
import unittest

import pandas as pd
from datagencars.existing_dataset.generate_null_values.generate_null_values import GenerateNullValues


class TestGenerateNullValues(unittest.TestCase):

    def setUp(self):        
        # item_df:
        item_file_path = 'resources/existing_dataset/context/preferencial_rating/ml_20k/item.csv'
        self.item_df = pd.read_csv(item_file_path, encoding='utf-8', index_col=False, sep=',')
        # context_df:
        context_file_path = 'resources/existing_dataset/context/preferencial_rating/ml_20k/context_categorical.csv'
        self.context_df = pd.read_csv(context_file_path, encoding='utf-8', index_col=False, sep=',')
                
        # Constructor:
        self.__generate_nulls_item = GenerateNullValues()
        self.__generate_nulls_context = GenerateNullValues()
     
    def tearDown(self):
        del self.__generate_nulls_item
        del self.__generate_nulls_context
         
    def test_generate_null_values_item_20(self):
        '''        
        Generating null values in the item file: "item.csv".
        '''               
        new_df = self.__generate_nulls_item.regenerate_file(file_df=self.item_df, percentage_null=20)
        logging.info(f'new_item: {new_df}')
        self.assertEqual(new_df.isnull().any().any(), True)                

    def test_generate_null_values_context_20(self):
        '''        
        Generating null values in the context file: "context.csv".
        '''                
        new_df = self.__generate_nulls_context.regenerate_file(file_df=self.context_df, percentage_null=20)
        logging.info(f'new_context: {new_df}')
        self.assertEqual(new_df.isnull().any().any(), True)        


if __name__ == '__main__':
    unittest.main()
