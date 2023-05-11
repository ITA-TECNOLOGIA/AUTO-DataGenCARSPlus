import unittest
import pandas as pd
import unittest
from unittest.mock import MagicMock
from collections import defaultdict
from datagencars.recommenders.recommender_sidelars import RecommenderSIDELARS

class TestRecommender(unittest.TestCase):

    def setUp(self):
        self.df_item = pd.DataFrame(data={'item_id': [1, 2, 3]})
        self.df_context = pd.DataFrame(data={'context_id': [1, 2, 3]})
        self.df_rating = pd.DataFrame(data={'user_id': [1, 2, 3], 'item_id': [1, 2, 3], 'rating': [4, 5, 2]})
        self.df_behavior = pd.DataFrame(data={'user_id': [1, 2, 3], 'object_action': ['Update', 'Update', 'Update'],
                                              'timestamp': ['2023-05-11', '2023-05-12', '2023-05-13'], 
                                              'user_position': ['(1.0,2.0)', '(2.0,3.0)', '(3.0,4.0)']})

        self.recommender = RecommenderSIDELARS(self.df_item, self.df_context, self.df_rating, self.df_behavior)

    def test_get_top_n(self):
        predictions = [(1, 1, 3, 4.0, {}), (2, 2, 1, 4.5, {}), (3, 3, 2, 2.0, {})]
        n = 2
        expected = defaultdict(list, {1: [(1, 4.0)], 2: [(2, 4.5)], 3: [(3, 2.0)]})
        result = self.recommender.get_top_n(predictions, n)
        self.assertEqual(result, expected)

    def test_get_user_based_recommendation(self):
        algorithm = MagicMock()
        algorithm.test.return_value = [(1, 1, 3, 4.0, {}), (2, 2, 1, 4.5, {}), (3, 3, 2, 2.0, {})]
        algorithm.fit.return_value = None

        trainset = MagicMock()
        testset = [(1, 1, 3), (2, 2, 1), (3, 3, 2)]
        k_recommendations = 2

        expected = defaultdict(list, {1: [(1, 4.0)], 2: [(2, 4.5)], 3: [(3, 2.0)]})
        result = self.recommender.get_user_based_recommendation(algorithm, trainset, testset, k_recommendations)

        self.assertEqual(result, expected)

    def test_get_last_position_for_user(self):
        self.recommender.df_behavior = pd.DataFrame({
            "user_id": [1, 2],
            "object_action": ["Update", "Update"],
            "timestamp": ["2023-05-01", "2023-05-02"],
            "user_position": ["(1.0, 1.0, 1.0)", "(2.0, 2.0, 2.0)"]
        })

        last_position = self.recommender.get_last_position_for_user(1)
        self.assertEqual(last_position, [1.0, 1.0, 1.0])

    def test_get_npoi_recommendation(self):
        self.recommender.df_item = pd.DataFrame({
            "item_id": [1, 2, 3],
            "object_position": ["(1.0, 1.0, 1.0)", "(2.0, 2.0, 2.0)", "(3.0, 3.0, 3.0)"]
        })

        recommendations = self.recommender.get_npoi_recommendation(2, [1])
        self.assertDictEqual(recommendations, defaultdict(list))

    def test_get_trajectory(self):
        candidate_recommendations = {
            1: [(1, 5.0), (2, 4.0), (3, 4.5)],
            2: [(2, 4.0), (1, 3.0), (3, 3.5)]
        }
        self.recommender.df_item = pd.DataFrame({
            "item_id": [1, 2, 3],
            "object_position": ["(1.0, 1.0, 1.0)", "(2.0, 2.0, 2.0)", "(3.0, 3.0, 3.0)"],
            "object_type": ["chair", "table", "sofa"],
            "room_id": [1, 1, 2]
        })
        self.recommender.df_behavior = pd.DataFrame({
            "user_id": [1, 2],
            "object_action": ["Update", "Update"],
            "timestamp": ["2023-05-01", "2023-05-02"],
            "user_position": ["(1.0, 1.0, 1.0)", "(2.0, 2.0, 2.0)"]
        })

        trajectory = self.recommender.get_trajectory(candidate_recommendations)
        expected_trajectory = {
            1: [{'object_id': 1, 'object_position': [1.0, 1.0, 1.0], 'object_type': 'chair', 'distance': 0.0, 'room_id': 1},
                {'object_id': 2, 'object_position': [2.0, 2.0, 2.0], 'object_type': 'table', 'distance': 1.4142135623730951, 'room_id': 1},
                {'object_id': 3, 'object_position': [3.0, 3.0, 3.0], 'object_type': 'sofa', 'distance': 2.8284271247461903, 'room_id': 2}],
            2: [{'object_id': 2, 'object_position': [2.0, 2.0, 2.0], 'object_type': 'table', 'distance': 0.0, 'room_id': 1},
                {'object_id': 1, 'object_position': [1.0, 1.0, 1.0], 'object_type': 'chair', 'distance': 1.4142135623730951, 'room_id': 1},
                {'object_id': 3, 'object_position': [3.0, 3.0, 3.0], 'object_type': 'sofa', 'distance': 1.4142135623730951, 'room_id': 2}]
        }

        self.assertDictEqual(trajectory, expected_trajectory)

if __name__ == '__main__':
    unittest.main()
