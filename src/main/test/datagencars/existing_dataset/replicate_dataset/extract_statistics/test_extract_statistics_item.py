import logging
import unittest

import pandas as pd
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_uic import ExtractStatisticsUIC


class TestExtractStatisticsItem(unittest.TestCase):

    def setUp(self):             
        # item.csv
        item_file_path = 'resources/existing_dataset/context/sts/item.csv'
        item_df = pd.read_csv(item_file_path, encoding='utf-8', index_col=False, sep=';')        
        # Extract Statistics of Item:
        self.__extract = ExtractStatisticsUIC(uic_df=item_df)
    
    def tearDown(self):
        del self.__extract
    
    def test_get_number_id(self):        
        '''
        Gets the number of item_id in file item.csv.
        '''         
        number_id = self.__extract.get_number_id()
        logging.info(f'number_id: {number_id}')                
        self.assertEqual(number_id, 249)

    def test_get_number_possible_values_by_attribute(self):        
        '''
        Gets the number of possible values by attribute in a file item.csv.
        '''         
        number_possible_values_df = self.__extract.get_number_possible_values_by_attribute()        
        number_possible_values = number_possible_values_df['category1'].iloc[0]
        logging.info(f'number_possible_values: {number_possible_values}')                
        self.assertEqual(number_possible_values, 27)

    def test_get_avg_possible_values_by_attribute(self):
        '''
        Gets the average of possible values by attribute in a file item.csv.
        '''         
        avg_possible_values_df = self.__extract.get_avg_possible_values_by_attribute()        
        avg_possible_values = avg_possible_values_df['category1'].iloc[0]
        logging.info(f'avg_possible_values: {avg_possible_values}')                
        self.assertEqual(avg_possible_values, 7.94)   

    def test_get_sd_possible_values_by_attribute(self):
        '''
        Gets the standard deviation of possible values by attribute in a file item.csv.
        '''         
        sd_possible_values_df = self.__extract.get_sd_possible_values_by_attribute()    
        sd_possible_values = sd_possible_values_df['category1'].iloc[0]
        logging.info(f'sd_possible_values: {sd_possible_values}')                
        self.assertEqual(sd_possible_values, 7.27)

    def test_get_frequency_possible_values_by_attribute(self):
        '''
        Gets the frequency of possible values by attribute in a file item.csv.
        '''         
        frequency_possible_values_df = self.__extract.get_frequency_possible_values_by_attribute()            
        frequency_possible_values = frequency_possible_values_df['category1'].iloc[0]        
        logging.info(f'frequency_possible_values: {frequency_possible_values}')                
        self.assertEqual(frequency_possible_values, 76)

    def test_count_missing_values(self):
        '''
        Count missing values in the dataframe.
        '''         
        count_missing_values_df = self.__extract.count_missing_values()            
        count_missing_values = count_missing_values_df.loc[count_missing_values_df['Attribute name'] == 'category1', 'Count'].iloc[0]
        logging.info(f'count_missing_values: {count_missing_values}')                
        self.assertEqual(count_missing_values, 0)

    def test_column_attributes_count(self):
        '''
        Count each attribute of a selected column.
        '''         
        column_attributes_count_df = self.__extract.column_attributes_count(column='category1')           
        column_attributes_count = column_attributes_count_df.loc[column_attributes_count_df['category1'] == 1, 'count'].iloc[0]
        logging.info(f'column_attributes_count: {column_attributes_count}')                
        self.assertEqual(column_attributes_count, 39)


if __name__ == '__main__':
    unittest.main()
