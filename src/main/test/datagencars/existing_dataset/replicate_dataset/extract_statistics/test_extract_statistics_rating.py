import pandas as pd
import numpy as np
import unittest
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_rating import ExtractStatisticsRating as extract_statistics_rating

"""
Usage: python -m unittest src\main\test\datagencars\existing_dataset\replicate_dataset\extract_statistics\test_extract_statistics_rating.py
"""

class TestReplaceMissingValues(unittest.TestCase):
    def setUp(self):
        self.df1 = pd.DataFrame({'A': ['1', '2', '3', '4', '5'], 
                                'B': [-1, 0, 1, 2, 3], 
                                'C': ['NULL', 'a', 'b', 'c', 'NULL']})
        self.df2 = pd.DataFrame({'A': ['1', '2', '3', '4', '5'], 
                                'B': [-1, 0, 1, 2, 3], 
                                'C': [None, 'a', 'b', 'c', None]})
        self.df3 = pd.DataFrame({'A': ['1', '2', '3', '4', '5'], 
                                'B': [-1, 0, 1, 2, 3], 
                                'C': ['NULL', 'a', 'b', 'c', 'NULL']})

    def test_replace_null(self):
        df = extract_statistics_rating.replace_missing_values(self.df1)
        self.assertTrue(pd.isna(df.loc[0, 'C']) and pd.isna(df.loc[4, 'C']))
        
    def test_replace_minus_1(self):
        df = extract_statistics_rating.replace_missing_values(self.df1)
        self.assertTrue(pd.isna(df.loc[0, 'B']))
        
    def test_replace_both(self):
        df = extract_statistics_rating.replace_missing_values(self.df1)
        self.assertTrue(pd.isna(df.loc[0, 'C']) and pd.isna(df.loc[4, 'C']) and pd.isna(df.loc[0, 'B']))
        
    def test_no_missing_values(self):
        df = extract_statistics_rating.replace_missing_values(self.df2)
        self.assertTrue(df.equals(self.df2))

class TestCountUnique(unittest.TestCase):
    def test_count_unique(self):
        df = pd.DataFrame({
            "user_id": [1, 2, 3, 4, 5],
            "item_id": [101, 102, 103, 104, 105],
            "context_id": [201, 202, 203, 204, 205],
            "timestamp": [1, 2, 3, 4, 5],
            "rating": [1, 2, 3, 4, 5]
        })
        unique_counts_df = extract_statistics_rating.count_unique(df)
        self.assertTrue(unique_counts_df.shape == (5, 2))

    def test_count_unique_counts_ratings(self):
        df = pd.DataFrame({'user_id': [1, 2, 3], 'item_id': [101, 102, 103], 'rating': [4, 3, 5]})
        result = extract_statistics_rating.count_unique(df)
        assert result[result['Attribute name'] == 'Ratings']['Count'].values[0] == 3

    def test_count_unique_handles_missing_data(self):
        df = pd.DataFrame({'user_id': [1, 2, 3], 'item_id': [101, np.nan, 103], 'rating': [4, 3, 5]})
        result = extract_statistics_rating.count_unique(df)
        assert result[result['Attribute name'] == 'Users']['Count'].values[0] == 3
        assert result[result['Attribute name'] == 'Items']['Count'].values[0] == 2
        assert result[result['Attribute name'] == 'Ratings']['Count'].values[0] == 3

class CountItemsVotedByUser(unittest.TestCase):
    def test_count_items_voted_by_user(self):
        data = pd.DataFrame({
            'user_id': [1, 1, 1, 2, 2, 2, 3, 3],
            'item_id': [10, 20, 30, 10, 20, 40, 10, 30],
            'rating': [3, 4, 2, 5, 1, 4, 2, 3]
        })
        selected_user = 1
        counts_items, unique_items, total_count = extract_statistics_rating.count_items_voted_by_user(data, selected_user)
        assert total_count == 3, f"total_count was {total_count}, but it should be 3"
        assert set(unique_items) == {10, 20, 30}, f"unique_items were {unique_items}, but they should be [10, 20, 30]"
        assert counts_items.loc[10] == 1, f"counts_items for item 10 was {counts_items.loc[10]}, but it should be 1"
        assert counts_items.loc[20] == 1, f"counts_items for item 20 was {counts_items.loc[20]}, but it should be 1"
        assert counts_items.loc[30] == 1, f"counts_items for item 30 was {counts_items.loc[30]}, but it should be 1"

    def test_count_items_voted_by_user_returns_tuple(self):
        data = pd.DataFrame({
            'user_id': ['user1', 'user1', 'user2', 'user3', 'user3'],
            'item_id': ['item1', 'item2', 'item1', 'item3', 'item4'],
            'rating': [5, 3, 4, 2, 1]
        })
        selected_user = 'user1'
        result = extract_statistics_rating.count_items_voted_by_user(data, selected_user)
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_count_items_voted_by_user_counts_items(self):
        data = pd.DataFrame({
            'user_id': ['user1', 'user1', 'user2', 'user3', 'user3'],
            'item_id': ['item1', 'item2', 'item1', 'item3', 'item4'],
            'rating': [5, 3, 4, 2, 1]
        })
        selected_user = 'user1'
        counts_items, _, _ = extract_statistics_rating.count_items_voted_by_user(data, selected_user)
        assert len(counts_items) == 2
        assert counts_items['item1'] == 1
        assert counts_items['item2'] == 1

    def test_count_items_voted_by_user_unique_items(self):
        data = pd.DataFrame({
            'user_id': ['user1', 'user1', 'user2', 'user3', 'user3'],
            'item_id': ['item1', 'item2', 'item1', 'item3', 'item4'],
            'rating': [5, 3, 4, 2, 1]
        })
        selected_user = 'user1'
        _, unique_items, _ = extract_statistics_rating.count_items_voted_by_user(data, selected_user)
        assert len(unique_items) == 2
        assert 'item1' in unique_items
        assert 'item2' in unique_items

    def test_count_items_voted_by_user_returns_zero_count(self):
        data = pd.DataFrame({
            'user_id': ['user1', 'user1', 'user2', 'user3', 'user3'],
            'item_id': ['item1', 'item2', 'item1', 'item3', 'item4'],
            'rating': [5, 3, 4, 2, 1]
        })
        selected_user = 'user4'
        _, _, total_count = extract_statistics_rating.count_items_voted_by_user(data, selected_user)
        assert total_count == 0

class CalculateVoteStats(unittest.TestCase):
    def test_calculate_vote_stats_no_ratings_for_user(self):
        data = {
            "user_id": [1, 2, 3],
            "item_id": [101, 102, 103],
            "rating": [4, 5, 2]
        }
        df = pd.DataFrame(data)
        selected_user = 4
        expected_stats = {}
        assert extract_statistics_rating.calculate_vote_stats(df, selected_user) == expected_stats

    def test_calculate_vote_stats_one_rating_for_user(self):
        data = {
            "user_id": [1, 1, 1],
            "item_id": [101, 102, 103],
            "rating": [4, 5, 2]
        }
        df = pd.DataFrame(data)
        selected_user = 1
        expected_stats = {
            "Vote standard deviation": "1.53",
            "Average vote for user 1": "3.67"
        }
        assert extract_statistics_rating.calculate_vote_stats(df, selected_user) == expected_stats

    def test_calculate_vote_stats_multiple_users(self):
        data = {
            "user_id": [1, 2, 2, 3, 3, 3],
            "item_id": [101, 102, 103, 104, 105, 106],
            "rating": [4, 5, 2, 3, 1, 4]
        }
        df = pd.DataFrame(data)
        selected_user = "All users"
        expected_stats = {
            "Vote standard deviation": "1.47",
            "Average vote for all users": "3.17"
        }
        assert extract_statistics_rating.calculate_vote_stats(df, selected_user) == expected_stats

    def test_calculate_vote_stats_same_average_for_all_users(self):
        data = {
            "user_id": [1, 2, 3],
            "item_id": [101, 102, 103],
            "rating": [3, 3, 3]
        }
        df = pd.DataFrame(data)
        selected_user = "All users"
        expected_stats = {
            "Vote standard deviation": "0.00",
            "Average vote for all users": "3.00"
        }
        assert extract_statistics_rating.calculate_vote_stats(df, selected_user) == expected_stats

    def test_calculate_vote_stats_same_rating_for_all_users(self):
        data = {
            "user_id": [1, 2, 3],
            "item_id": [101, 102, 103],
            "rating": [4, 4, 4]
        }
        df = pd.DataFrame(data)
        selected_user = "All users"
        expected_stats = {
            "Vote standard deviation": "0.00",
            "Average vote for all users": "4.00"
        }
        assert extract_statistics_rating.calculate_vote_stats(df, selected_user) == expected_stats
