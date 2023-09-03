import logging
import unittest

import numpy as np
import pandas as pd
from datagencars.existing_dataset.data_converter.data_converter import DataConverter


class TestCastRating(unittest.TestCase):

    
    def setUp(self):
        # user.csv:
        user_file_path = 'resources/existing_dataset/context/sts/rating_preferencial/user.csv'
        user_df = pd.read_csv(user_file_path, encoding='utf-8', index_col=False, sep=';')
               
        # Dataset converting data generator:        
        self.__generator = DataConverter(df=user_df)       
    
    def tearDown(self):
        del self.__generator
    
    def test_categorical_to_numerical_ignore_nan(self):
        """
        Ignores NaN values (the rest of values are replaced by numeric values):
        """
        column_name_list = ['gender']
        new_user_df = self.__generator.categorical_to_numerical(column_name_list, ignore_nan=True)        
        logging.info(f'user_file: {new_user_df}')  
        output_attribute_list = new_user_df['gender'].unique().tolist()
        real_attribute_list = [np.nan, 1, 0]
        self.assertListEqual(output_attribute_list, real_attribute_list)

    def test_categorical_to_numerical_replace_nan(self):
        """
        Replaces NaN by numeric values.
        """
        column_name_list = ['gender']
        new_user_df = self.__generator.categorical_to_numerical(column_name_list, ignore_nan=False)
        logging.info(f'user_file: {new_user_df}')  
        output_attribute_list = new_user_df['gender'].unique().tolist()        
        real_attribute_list = [2, 1, 0]
        self.assertListEqual(output_attribute_list, real_attribute_list)

    def test_numerical_to_categorical_ignore_nan(self):
        mappings = {"opennessToExperience": {2.0: "Low", 3.0: "Moderate", 4.0: "Moderate-High", 5.0: "High", 6.0: "Very High", 7.0: "Exceptional"}, # nan: nan, 
                    "conscientiousness": {1.0: "Very Low", 2.0: "Low", 3.0: "Moderate", 4.0: "Moderate-High", 5.0: "High", 6.0: "Very High", 7.0: "Exceptional"}, 
                    "extraversion": {1.0: "Very Low", 2.0: "Low", 3.0: "Moderate", 4.0: "Moderate-High", 5.0: "High", 6.0: "Very High", 7.0: "Exceptional"}, 
                    "agreeableness": {2.0: "Low", 3.0: "Moderate", 4.0: "Moderate-High", 5.0: "High", 6.0: "Very High", 7.0: "Exceptional"}, 
                    "emotionalStability": {2.0: "Low", 3.0: "Moderate", 4.0: "Moderate-High", 5.0: "High", 6.0: "Very High", 7.0: "Exceptional"}}        
        new_user_df = self.__generator.numerical_to_categorical(mappings)        
        logging.info(f'user_file: {new_user_df}')
        output_attribute_list = new_user_df['opennessToExperience'].unique().tolist()
        real_attribute_list = [np.nan, 'Very High', 'High', 'Moderate-High', 'Moderate', 'Exceptional', 'Low']
        self.assertListEqual(output_attribute_list, real_attribute_list)

    def test_numerical_to_categorical_replace_nan(self):
        mappings = {"opennessToExperience": {np.nan: "Unknown", 2.0: "Low", 3.0: "Moderate", 4.0: "Moderate-High", 5.0: "High", 6.0: "Very High", 7.0: "Exceptional"}, # nan: nan, 
                        "conscientiousness": {np.nan: "Unknown", 1.0: "Very Low", 2.0: "Low", 3.0: "Moderate", 4.0: "Moderate-High", 5.0: "High", 6.0: "Very High", 7.0: "Exceptional"}, 
                        "extraversion": {np.nan: "Unknown", 1.0: "Very Low", 2.0: "Low", 3.0: "Moderate", 4.0: "Moderate-High", 5.0: "High", 6.0: "Very High", 7.0: "Exceptional"}, 
                        "agreeableness": {np.nan: "Unknown", 2.0: "Low", 3.0: "Moderate", 4.0: "Moderate-High", 5.0: "High", 6.0: "Very High", 7.0: "Exceptional"}, 
                        "emotionalStability": {np.nan: "Unknown", 2.0: "Low", 3.0: "Moderate", 4.0: "Moderate-High", 5.0: "High", 6.0: "Very High", 7.0: "Exceptional"}}
        new_user_df = self.__generator.numerical_to_categorical(mappings)
        logging.info(f'user_file: {new_user_df}')        
        output_attribute_list = new_user_df['opennessToExperience'].unique().tolist()        
        real_attribute_list = ['Unknown', 'Very High', 'High', 'Moderate-High', 'Moderate', 'Exceptional', 'Low']
        self.assertListEqual(output_attribute_list, real_attribute_list)


if __name__ == '__main__':
    unittest.main()
