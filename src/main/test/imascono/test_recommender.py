import unittest
import pandas as pd
from pandas.testing import assert_frame_equal

from imascono.recommender import Recommender

class TestRecommender(unittest.TestCase):

    def setUp(self):
        self.recommender = Recommender()

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
        expected_recommendations = {1: [(3, None), (2, None)]}
        self.assertDictEqual(recommendations, expected_recommendations)

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
            '1': [{'object_id': 1, 'object_position': [1.0, 1.0, 1.0], 'object_type': 'chair', 'distance': 0.0, 'room_id': 1},
                  {'object_id': 2, 'object_position': [2.0, 2.0, 2.0], 'object_type': 'table', 'distance': 1.4142135623730951, 'room_id': 1},
                  {'object_id': 3, 'object_position': [3.0, 3.0, 3.0], 'object_type': 'sofa', 'distance': 2.8284271247461903, 'room_id': 2}],
            '2': [{'object_id': 2, 'object_position': [2.0, 2.0, 2.0], 'object_type': 'table', 'distance': 0.0, 'room_id': 1},
                {'object_id': 1, 'object_position': [1.0, 1.0, 1.0], 'object_type': 'chair', 'distance': 1.4142135623730951, 'room_id': 1},
                {'object_id': 3, 'object_position': [3.0, 3.0, 3.0], 'object_type': 'sofa', 'distance': 1.4142135623730951, 'room_id': 2}]
        }

        self.assertDictEqual(trajectory, expected_trajectory)

if __name__ == '__main__':
    unittest.main()
