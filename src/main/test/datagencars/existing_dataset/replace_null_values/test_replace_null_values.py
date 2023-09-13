import logging
import unittest

import pandas as pd
from datagencars.existing_dataset.replace_null_values.replace_null_values import ReplaceNullValues
from streamlit_app.preprocess_dataset import wf_replace_null_values


class TestGeneratorSyntheticDataset(unittest.TestCase):

    def setUp(self):        
        # item_df:
        item_file_path = 'resources/existing_dataset/context/preferencial_rating/sts/item.csv'
        self.item_df = pd.read_csv(item_file_path, encoding='utf-8', index_col=False, sep=';')
        # context_df:
        context_file_path = 'resources/existing_dataset/context/preferencial_rating/sts/context.csv'
        self.context_df = pd.read_csv(context_file_path, encoding='utf-8', index_col=False, sep=';')

        # Constructor:
        self.__replace_nulls_item = ReplaceNullValues(file_df=self.item_df)
        self.__replace_nulls_context = ReplaceNullValues(file_df=self.context_df)
     
    def tearDown(self):
        del self.__replace_nulls_item
        del self.__replace_nulls_context
    
    def test_replace_null_values_item(self):
        '''        
        Replacing null values in the schema file: "item.csv".
        '''       
        schema = wf_replace_null_values.infer_schema(df=self.item_df)
        new_df = self.__replace_nulls_item.regenerate_item_file(schema)
        logging.info(f'new_item: {new_df}')
        self.assertEqual(new_df.isnull().any().any(), False)

    def test_replace_null_values_context(self):
        '''        
        Replacing null values in the schema file: "context.csv".
        '''        
        schema = wf_replace_null_values.infer_schema(df=self.item_df)
        new_df = self.__replace_nulls_item.regenerate_item_file(schema)
        logging.info(f'new_item: {new_df}')
        self.assertEqual(new_df.isnull().any().any(), False)


if __name__ == '__main__':
    unittest.main()
