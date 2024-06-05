import logging
import unittest

import pandas as pd
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_uic import ExtractStatisticsUIC


class TestExtractStatisticsItem(unittest.TestCase):

    def setUp(self):             
        # context.csv
        context_file_path = 'resources/existing_dataset/context/preferencial_rating/sts/context.csv'
        context_df = pd.read_csv(context_file_path, encoding='utf-8', index_col=False, sep=';')        
        # Extract Statistics of Context:
        self.__extract = ExtractStatisticsUIC(uic_df=context_df)
    
    def tearDown(self):
        del self.__extract
    
    def test_get_number_id(self):        
        '''
        Gets the number of context_id in file context.csv.
        '''         
        number_id = self.__extract.get_number_id()
        logging.info(f'number_id: {number_id}')                
        self.assertEqual(number_id, 2534)

    def test_get_number_possible_values_by_attribute(self):        
        '''
        Gets the number of possible values by attribute in a file context.csv.
        '''         
        number_possible_values_df = self.__extract.get_number_possible_values_by_attribute()             
        number_possible_values = number_possible_values_df['temperature'].iloc[0]
        logging.info(f'number_possible_values: {number_possible_values}')                
        self.assertEqual(number_possible_values, 6)

    def test_get_avg_possible_values_by_attribute(self):
        '''
        Gets the average of possible values by attribute in a file context.csv.
        '''         
        avg_possible_values_df = self.__extract.get_avg_possible_values_by_attribute()        
        avg_possible_values = avg_possible_values_df['temperature'].iloc[0]
        logging.info(f'avg_possible_values: {avg_possible_values}')                
        self.assertEqual(avg_possible_values, 3.43)   

    def test_get_sd_possible_values_by_attribute(self):
        '''
        Gets the standard deviation of possible values by attribute in a file context.csv.
        '''         
        sd_possible_values_df = self.__extract.get_sd_possible_values_by_attribute()    
        sd_possible_values = sd_possible_values_df['temperature'].iloc[0]
        logging.info(f'sd_possible_values: {sd_possible_values}')                
        self.assertEqual(sd_possible_values, 0.98)

    def test_get_frequency_possible_values_by_attribute(self):
        '''
        Gets the frequency of possible values by attribute in a file context.csv.
        '''         
        frequency_possible_values_df = self.__extract.get_frequency_possible_values_by_attribute()            
        frequency_possible_values = frequency_possible_values_df['temperature'].iloc[0]        
        logging.info(f'frequency_possible_values: {frequency_possible_values}')                
        self.assertEqual(frequency_possible_values, 198)

    def test_count_missing_values(self):
        '''
        Count missing values in the dataframe.
        '''         
        count_missing_values_df = self.__extract.count_missing_values()            
        count_missing_values = count_missing_values_df.loc[count_missing_values_df['Attribute name'] == 'temperature', 'Count'].iloc[0]
        logging.info(f'count_missing_values: {count_missing_values}')                
        self.assertEqual(count_missing_values, 2139)

    def test_column_attributes_count(self):
        '''
        Count each attribute of a selected column.
        '''         
        column_attributes_count_df = self.__extract.column_attributes_count(column='temperature')           
        column_attributes_count = column_attributes_count_df.loc[column_attributes_count_df['temperature'] == 1, 'count'].iloc[0]
        logging.info(f'column_attributes_count: {column_attributes_count}')                
        self.assertEqual(column_attributes_count, 4)


if __name__ == '__main__':
    unittest.main()
