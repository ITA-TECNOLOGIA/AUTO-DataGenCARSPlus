import pandas as pd
import numpy as np
import unittest
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_uic import ExtractStatisticsUIC as extract_statistics_uic

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

class TestCountMissingValues(unittest.TestCase):
    def test_returns_dataframe_with_correct_columns(self):
        df = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})
        replace_values = {}
        result = extract_statistics_uic.count_missing_values(df, replace_values)
        expected_columns = ['Attribute name', 'Count']
        self.assertEqual(list(result.columns), expected_columns)
        
    def test_correctly_replaces_single_value_and_counts_missing_values(self):
        df = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': ['a', 'b', 'c', 'd', 'e']})
        replace_values = {4: 'NaN'}
        result = extract_statistics_uic.count_missing_values(df, replace_values)
        expected_counts = pd.DataFrame({'Attribute name': ['A', 'B'], 'Count': [1, 0]})
        self.assertEqual(result.to_dict(), expected_counts.to_dict())
        
    def test_correctly_replaces_multiple_values_and_counts_missing_values(self):
        df = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': ['a', 'b', 'c', 'd', 'e'], 'C': [10, 20, 30, 40, 50]})
        replace_values = {4: 'NaN', 'c': 'NaN', 50: 'NaN'}
        result = extract_statistics_uic.count_missing_values(df, replace_values)
        expected_counts = pd.DataFrame({'Attribute name': ['A', 'B', 'C'], 'Count': [1, 1, 1]})
        self.assertEqual(result.to_dict(), expected_counts.to_dict())
        
    def test_handles_already_missing_values_correctly(self):
        df = pd.DataFrame({'A': [1, 2, 3, np.nan, 5], 'B': ['a', 'b', 'c', 'd', 'e']})
        replace_values = {4: 'NaN'}
        result = extract_statistics_uic.count_missing_values(df, replace_values)
        expected_counts = pd.DataFrame({'Attribute name': ['A', 'B'], 'Count': [1, 0]})
        self.assertEqual(result.to_dict(), expected_counts.to_dict())

class TestGeneralStatistics(unittest.TestCase):
    def test_empty_list(self):
        empty_df = pd.DataFrame({'user_id': [], 'time': [], 'longitude': [], 'latitude': [], 'item_id': [], 'context_id': []})
        self.assertEqual(extract_statistics_uic.general_statistics(empty_df), {'Number of userID': 0, 'Number of itemID': 0, 'Number of contextID': 0, 'Number of ratings': 0})

    def test_single_element_list(self):
        data = pd.DataFrame({'user_id': [1], 'time': [0], 'longitude': [0.0], 'latitude': [0.0], 'item_id': [1], 'context_id': [1]})
        self.assertEqual(extract_statistics_uic.general_statistics(data), {'Number of userID': 1, 'Number of itemID': 1, 'Number of contextID': 1, 'Number of ratings': 3})

    def test_even_number_of_elements(self):
        data = pd.DataFrame({'user_id': [1, 1, 2, 2], 'time': [0, 1, 2, 3], 'longitude': [0.0, 1.0, 0.0, 1.0], 'latitude': [0.0, 1.0, 0.0, 1.0], 'item_id': [1, 2, 1, 2], 'context_id': [1, 2, 1, 2]})
        self.assertEqual(extract_statistics_uic.general_statistics(data), {'Number of userID': 2, 'Number of itemID': 2, 'Number of contextID': 2, 'Number of ratings': 6})

    def test_odd_number_of_elements(self):
        data = pd.DataFrame({'user_id': [1, 2, 3], 'time': [0, 0, 0], 'longitude': [0.0, 0.0, 0.0], 'latitude': [0.0, 0.0, 0.0], 'item_id': [1, 2, 3], 'context_id': [1, 2, 3]})
        self.assertEqual(extract_statistics_uic.general_statistics(data), {'Number of userID': 3, 'Number of itemID': 3, 'Number of contextID': 3, 'Number of ratings': 9})

    def test_negative_numbers(self):
        data = pd.DataFrame({'user_id': [-1, -2, -3], 'time': [0, 0, 0], 'longitude': [0.0, 0.0, 0.0], 'latitude': [0.0, 0.0, 0.0], 'item_id': [-1, -2, -3], 'context_id': [-1, -2, -3]})
        self.assertEqual(extract_statistics_uic.general_statistics(data), {'Number of userID': 3, 'Number of itemID': 3, 'Number of contextID': 3, 'Number of ratings': 9})

class TestStatisticsByUser(unittest.TestCase):
    def test_empty_dataframe(self):
        data = pd.DataFrame({'user_id': [], 'time': [], 'longitude': [], 'latitude': [], 'item_id': [], 'context_id': []})
        result = extract_statistics_uic.statistics_by_user(data, 1, 'word')
        self.assertEqual(result, {'Average of word by user': 0, 'Variance of word by user': 0, 'Standard deviation of word by user': 0, 'Number of word not repeated by user': 0, 'Percent of word not repeated by user': 0, 'Number of word repeated by user': 0, 'Percent of word repeated by user': 0})

    def test_multiple_user_dataframe(self):
        data = pd.DataFrame({'user_id': [1, 1, 1, 2, 2, 3], 'time': [1, 2, 3, 4, 5, 6], 'longitude': [1, 2, 3, 4, 5, 6], 'latitude': [1, 2, 3, 4, 5, 6], 'item_id': ['A', 'B', 'C', 'A', 'B', 'D'], 'context_id': [1, 2, 3, 4, 5, 6]})
        result = extract_statistics_uic.statistics_by_user(data, 1, 'item_id')
        self.assertEqual(result, {'Average of item_id by user': 2.0, 'Variance of item_id by user': 1.0, 'Standard deviation of item_id by user': 1.0, 'Number of item_id not repeated by user': 3, 'Percent of item_id not repeated by user': 100.0, 'Number of item_id repeated by user': 0, 'Percent of item_id repeated by user': 0.0})

    def test_nonexistent_user(self):
        data = pd.DataFrame({'user_id': [1, 1, 1, 2, 2, 3], 'time': [1, 2, 3, 4, 5, 6], 'longitude': [1, 2, 3, 4, 5, 6], 'latitude': [1, 2, 3, 4, 5, 6], 'item_id': ['A', 'B', 'C', 'A', 'B', 'D'], 'context_id': [1, 2, 3, 4, 5, 6]})
        result = extract_statistics_uic.statistics_by_user(data, 4, 'item_id')
        self.assertEqual(result, {'Average of item_id by user': 0, 'Variance of item_id by user': 0, 'Standard deviation of item_id by user': 0, 'Number of item_id not repeated by user': 0, 'Percent of item_id not repeated by user': 0, 'Number of item_id repeated by user': 0, 'Percent of item_id repeated by user': 0})

class TestStatisticsByAttribute(unittest.TestCase):
    def test_continuous_single_attribute(self):
        data = pd.DataFrame({'attribute': [1, 2, 3, 4, 5]})
        result = extract_statistics_uic.statistics_by_attribute(data)
        expected_result = [['attribute', 3.0, 1.58, pd.DataFrame({'Value': [1, 2, 3, 4, 5], 'Frequency': [1, 1, 1, 1, 1]}), pd.DataFrame({'Value': [1, 2, 3, 4, 5], 'Percentage': ['20.00%', '20.00%', '20.00%', '20.00%', '20.00%']})]]
        pd.testing.assert_frame_equal(result[0][3], expected_result[0][3])
        pd.testing.assert_frame_equal(result[0][4], expected_result[0][4])
        self.assertEqual(result[0][0], expected_result[0][0])
        self.assertEqual(result[0][1], expected_result[0][1])
        self.assertEqual(result[0][2], expected_result[0][2])

    def test_continuous_single_attribute(self):
        data = pd.DataFrame({'attribute': [1, 2, 3, 4, 5]})
        result = extract_statistics_uic.statistics_by_attribute(data)
        expected_result = [['attribute', 3.0, 1.58, pd.DataFrame({'Value': [1, 2, 3, 4, 5], 'Frequency': [1, 1, 1, 1, 1]}), pd.DataFrame({'Value': [1, 2, 3, 4, 5], 'Percentage': ['20.00%', '20.00%', '20.00%', '20.00%', '20.00%']})]]
        pd.testing.assert_frame_equal(result[0][3], expected_result[0][3])
        pd.testing.assert_frame_equal(result[0][4], expected_result[0][4])
        self.assertEqual(result[0][0], expected_result[0][0])
        self.assertEqual(result[0][1], expected_result[0][1])
        self.assertEqual(result[0][2], expected_result[0][2])
    
    def test_continuous_multiple_attributes(self):
        data = pd.DataFrame({'attribute1': [1, 2, 3, 4, 5], 'attribute2': [5, 4, 3, 2, 1]})
        result = extract_statistics_uic.statistics_by_attribute(data)
        expected_result = [['attribute1', 3.0, 1.58, pd.DataFrame({'Value': [1, 2, 3, 4, 5], 'Frequency': [1, 1, 1, 1, 1]}), pd.DataFrame({'Value': [1, 2, 3, 4, 5], 'Percentage': ['20.00%', '20.00%', '20.00%', '20.00%', '20.00%']})],
                        ['attribute2', 3.0, 1.58, pd.DataFrame({'Value': [5, 4, 3, 2, 1], 'Frequency': [1, 1, 1, 1, 1]}), pd.DataFrame({'Value': [5, 4, 3, 2, 1], 'Percentage': ['20.00%', '20.00%', '20.00%', '20.00%', '20.00%']})]]
        pd.testing.assert_frame_equal(result[0][3], expected_result[0][3])
        pd.testing.assert_frame_equal(result[0][4], expected_result[0][4])
        self.assertEqual(result[0][0], expected_result[0][0])
        self.assertEqual(result[0][1], expected_result[0][1])
        self.assertEqual(result[0][2], expected_result[0][2])
        pd.testing.assert_frame_equal(result[1][3], expected_result[1][3])
        pd.testing.assert_frame_equal(result[1][4], expected_result[1][4])
        self.assertEqual(result[1][0], expected_result[1][0])
        self.assertEqual(result[1][1], expected_result[1][1])
        self.assertEqual(result[1][2], expected_result[1][2])
