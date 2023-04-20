import logging
import unittest

import pandas as pd
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_uic import ExtractStatisticsUIC


class TestExtractStatisticsUser(unittest.TestCase):

    def setUp(self):             
        # user.csv
        user_file_path = 'resources/dataset_sts/user.csv'
        user_df = pd.read_csv(user_file_path, encoding='utf-8', index_col=False, sep=';')        
        # Extract Statistics of User:
        self.__extract = ExtractStatisticsUIC(uic_df=user_df)
    
    def tearDown(self):
        del self.__extract
    
    def test_get_number_id(self):        
        '''
        Gets the number of user_id in file user.csv.
        '''         
        number_id = self.__extract.get_number_id()
        logging.info(f'number_id: {number_id}')                
        self.assertEqual(number_id, 325)

    def test_get_number_possible_values_by_attribute(self):        
        '''
        Gets the number of possible values by attribute in a file user.csv.
        '''         
        number_possible_values_df = self.__extract.get_number_possible_values_by_attribute()
        number_possible_values = number_possible_values_df['birthDate'].iloc[0]
        logging.info(f'number_possible_values: {number_possible_values}')                
        self.assertEqual(number_possible_values, 172)

    def test_get_avg_possible_values_by_attribute(self):
        '''
        Gets the average of possible values by attribute in a file user.csv.
        '''         
        avg_possible_values_df = self.__extract.get_avg_possible_values_by_attribute()        
        avg_possible_values = avg_possible_values_df['conscientiousness'].iloc[0]
        logging.info(f'avg_possible_values: {avg_possible_values}')                
        self.assertEqual(avg_possible_values, 5.2)   

    def test_get_sd_possible_values_by_attribute(self):
        '''
        Gets the standard deviation of possible values by attribute in a file user.csv.
        '''         
        sd_possible_values_df = self.__extract.get_sd_possible_values_by_attribute()    
        sd_possible_values = sd_possible_values_df['conscientiousness'].iloc[0]
        logging.info(f'sd_possible_values: {sd_possible_values}')                
        self.assertEqual(sd_possible_values, 1.15)

    def test_get_frequency_possible_values_by_attribute(self):
        '''
        Gets the frequency of possible values by attribute in a file user.csv.
        '''         
        frequency_possible_values_df = self.__extract.get_frequency_possible_values_by_attribute()            
        frequency_possible_values = frequency_possible_values_df['conscientiousness'].iloc[0]        
        logging.info(f'frequency_possible_values: {frequency_possible_values}')                
        self.assertEqual(frequency_possible_values, 109)

    def test_count_missing_values(self):
        '''
        Count missing values in the dataframe.
        '''         
        count_missing_values_df = self.__extract.count_missing_values()            
        count_missing_values = count_missing_values_df.loc[count_missing_values_df['Attribute name'] == 'birthDate', 'Count'].iloc[0]
        logging.info(f'count_missing_values: {count_missing_values}')                
        self.assertEqual(count_missing_values, 130)

    def test_column_attributes_count(self):
        '''
        Count each attribute of a selected column.
        '''         
        column_attributes_count_df = self.__extract.column_attributes_count(column='gender')                   
        column_attributes_count = column_attributes_count_df.loc[column_attributes_count_df['gender'] == 'f', 'count'].iloc[0]
        logging.info(f'column_attributes_count: {column_attributes_count}')                
        self.assertEqual(column_attributes_count, 63)

    def test_empty_dataframe(self):
        data = pd.DataFrame({'user_id': [], 'time': [], 'longitude': [], 'latitude': [], 'item_id': [], 'context_id': []})
        result = self.__extract.statistics_by_user(data, 1, 'word')
        self.assertEqual(result, {'Average of word by user': 0, 'Variance of word by user': 0, 'Standard deviation of word by user': 0, 'Number of word not repeated by user': 0, 'Percent of word not repeated by user': 0, 'Number of word repeated by user': 0, 'Percent of word repeated by user': 0})

    def test_multiple_user_dataframe(self):
        data = pd.DataFrame({'user_id': [1, 1, 1, 2, 2, 3], 'time': [1, 2, 3, 4, 5, 6], 'longitude': [1, 2, 3, 4, 5, 6], 'latitude': [1, 2, 3, 4, 5, 6], 'item_id': ['A', 'B', 'C', 'A', 'B', 'D'], 'context_id': [1, 2, 3, 4, 5, 6]})
        result = self.__extract.statistics_by_user(data, 1, 'item_id')
        self.assertEqual(result, {'Average of item_id by user': 2.0, 'Variance of item_id by user': 1.0, 'Standard deviation of item_id by user': 1.0, 'Number of item_id not repeated by user': 3, 'Percent of item_id not repeated by user': 100.0, 'Number of item_id repeated by user': 0, 'Percent of item_id repeated by user': 0.0})

    def test_nonexistent_user(self):
        data = pd.DataFrame({'user_id': [1, 1, 1, 2, 2, 3], 'time': [1, 2, 3, 4, 5, 6], 'longitude': [1, 2, 3, 4, 5, 6], 'latitude': [1, 2, 3, 4, 5, 6], 'item_id': ['A', 'B', 'C', 'A', 'B', 'D'], 'context_id': [1, 2, 3, 4, 5, 6]})
        result = self.__extract.statistics_by_user(data, 4, 'item_id')
        self.assertEqual(result, {'Average of item_id by user': 0, 'Variance of item_id by user': 0, 'Standard deviation of item_id by user': 0, 'Number of item_id not repeated by user': 0, 'Percent of item_id not repeated by user': 0, 'Number of item_id repeated by user': 0, 'Percent of item_id repeated by user': 0})


if __name__ == '__main__':
    unittest.main()
