import unittest
import pandas as pd
from streamlit_app.preprocess_dataset import wf_util
from datagencars.existing_dataset.extend_dataset.increase_rating import IncreaseRating

class TestIncreaseRating(unittest.TestCase):

    def setUp(self):
        # Mock data for testing
        
        self.user_df = pd.DataFrame({
            'user_id': [1, 2, 3, 4, 5],
        })

        self.item_df = pd.DataFrame({
            'item_id': [1, 2, 3, 4, 5],
            'category1': [6, 7, 8, 9, 10],
            'category2': [11, 12, 13, 14, 15],
            'category3': [16, 17, 18, 19, 20],
        })

        self.context_df = pd.DataFrame({
            'context_id': [1, 2, 3, 4],
        })

        self.ratings_df = pd.DataFrame({
            'user_id': [1, 2, 3, 4, 5],
            'item_id': [1, 2, 3, 4, 5],
            'context_id': [1, 2, 3, 4, 2],
            'rating': [4, 4, 3, 2, 2]
        })

    def test_incremental_rating_random(self):
        # Generate user profile
        user_profile = wf_util.generate_user_profile_automatic(self.ratings_df, self.item_df, self.context_df)
        inc_rating = IncreaseRating(rating_df=self.ratings_df, item_df=self.item_df, user_df=self.user_df, context_df=self.context_df, user_profile=user_profile)
        result_df = inc_rating.incremental_rating_random(percentage_rating_variation=25, number_ratings=10, k=10)
        self.assertIsNotNone(result_df)
        self.assertTrue(len(result_df) > 0)

    # def test_incremental_rating_by_user(self):
    #     inc_rating = IncreaseRating(rating_df=self.ratings_df, item_df=self.item_df, user_df=self.user_df, context_df=self.context_df)
    #     user_ids = [1, 2]
    #     result_df = inc_rating.incremental_rating_by_user(user_ids, percentage_rating_variation=25, number_ratings=10, k=10)
    #     self.assertIsNotNone(result_df)
    #     self.assertTrue(len(result_df) > 0)

if __name__ == '__main__':
    unittest.main()
