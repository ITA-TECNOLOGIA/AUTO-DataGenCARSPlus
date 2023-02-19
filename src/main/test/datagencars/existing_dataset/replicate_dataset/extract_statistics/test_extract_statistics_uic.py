import pandas as pd
import numpy as np
import unittest
from datagencars.existing_dataset.replicate_dataset.extract_statistics import extract_statistics_uic

"""
Usage: python -m unittest src\main\test\datagencars\existing_dataset\replicate_dataset\extract_statistics\test_extract_statistics_uic.py
"""

class TestListAttributesAndRanges(unittest.TestCase):
    def test_list_attributes_and_ranges(self):
        data = pd.DataFrame({'A': [1,2,3], 'B': [4.0, 5.0, 6.0], 'C': ['Yes', 'No', 'Yes']})
        result = extract_statistics_uic.list_attributes_and_ranges(data)
        assert type(result) == list

    def test_list_attributes_and_ranges_empty_dataframe(self):
        df = pd.DataFrame()
        expected_output = []
        actual_output = extract_statistics_uic.list_attributes_and_ranges(df)
        self.assertEqual(actual_output, expected_output)  

    def test_list_attributes_and_ranges_with_datetime(self):
        data = pd.DataFrame({'A': [1,2,3], 'B': [4.0, 5.0, 6.0], 'C': ['Yes', 'No', 'Yes'], 'D': ['01/01/2020', '02/01/2020', '03/01/2020']})
        result = extract_statistics_uic.list_attributes_and_ranges(data)
        assert type(result) == list

    def test_list_attributes_and_ranges_with_datetime_and_nan(self):
        data = pd.DataFrame({'A': [1,2,3], 'B': [4.0, 5.0, 6.0], 'C': ['Yes', 'No', 'Yes'], 'D': ['01/01/2020', '02/01/2020', '03/01/2020'], 'E': ['01/01/2020', '02/01/2020', np.nan]})
        result = extract_statistics_uic.list_attributes_and_ranges(data)
        assert type(result) == list

    def test_list_attributes_and_ranges_with_datetime_and_nan_and_empty_string(self):
        data = pd.DataFrame({'A': [1,2,3], 'B': [4.0, 5.0, 6.0], 'C': ['Yes', 'No', 'Yes'], 'D': ['01/01/2020', '02/01/2020', '03/01/2020'], 'E': ['01/01/2020', '02/01/2020', np.nan], 'F': ['01/01/2020', '02/01/2020', '']})
        result = extract_statistics_uic.list_attributes_and_ranges(data)
        assert type(result) == list

class TestColumnAttributesCount(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'column1': ['a', 'b', 'c', 'd', 'a', 'b', 'c', 'd'],
            'column2': [1, 2, 3, 4, 1, 2, 3, 4],
            'column3': [pd.Timestamp('2020-01-01'), pd.Timestamp('2020-01-01'), pd.Timestamp('2020-02-01'), pd.Timestamp('2020-02-01'), pd.Timestamp('2020-03-01'), pd.Timestamp('2020-03-01'), pd.Timestamp('2020-04-01'), pd.Timestamp('2020-04-01')]
        })

    def test_count_attributes_of_object_column(self):
        result = extract_statistics_uic.column_attributes_count(self.df, 'column1')
        expected = pd.DataFrame({'column1': ['a', 'b', 'c', 'd'], 'count': [2, 2, 2, 2]})
        pd.testing.assert_frame_equal(result, expected)

    def test_count_attributes_of_numeric_column(self):
        result = extract_statistics_uic.column_attributes_count(self.df, 'column2')
        expected = pd.DataFrame({'column2': [1, 2, 3, 4], 'count': [2, 2, 2, 2]})
        pd.testing.assert_frame_equal(result, expected)

    def test_count_attributes_of_datetime_column(self):
        result = extract_statistics_uic.column_attributes_count(self.df, 'column3')
        expected = pd.DataFrame({'column3': ['January 2020', 'February 2020', 'March 2020', 'April 2020'], 'count': [2, 2, 2, 2]})
        pd.testing.assert_frame_equal(result, expected)

class TestReplaceCountMissingValues(unittest.TestCase):
    def test_returns_dataframe_with_correct_columns(self):
        df = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})
        replace_values = {}
        result = extract_statistics_uic.replace_count_missing_values(df, replace_values)
        expected_columns = ['Attribute name', 'Count']
        self.assertEqual(list(result.columns), expected_columns)
        
    def test_correctly_replaces_single_value_and_counts_missing_values(self):
        df = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': ['a', 'b', 'c', 'd', 'e']})
        replace_values = {4: 'NaN'}
        result = extract_statistics_uic.replace_count_missing_values(df, replace_values)
        expected_counts = pd.DataFrame({'Attribute name': ['A', 'B'], 'Count': [1, 0]})
        self.assertEqual(result.to_dict(), expected_counts.to_dict())
        
    def test_correctly_replaces_multiple_values_and_counts_missing_values(self):
        df = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': ['a', 'b', 'c', 'd', 'e'], 'C': [10, 20, 30, 40, 50]})
        replace_values = {4: 'NaN', 'c': 'NaN', 50: 'NaN'}
        result = extract_statistics_uic.replace_count_missing_values(df, replace_values)
        expected_counts = pd.DataFrame({'Attribute name': ['A', 'B', 'C'], 'Count': [1, 1, 1]})
        self.assertEqual(result.to_dict(), expected_counts.to_dict())
        
    def test_handles_already_missing_values_correctly(self):
        df = pd.DataFrame({'A': [1, 2, 3, np.nan, 5], 'B': ['a', 'b', 'c', 'd', 'e']})
        replace_values = {4: 'NaN'}
        result = extract_statistics_uic.replace_count_missing_values(df, replace_values)
        expected_counts = pd.DataFrame({'Attribute name': ['A', 'B'], 'Count': [1, 0]})
        self.assertEqual(result.to_dict(), expected_counts.to_dict())
