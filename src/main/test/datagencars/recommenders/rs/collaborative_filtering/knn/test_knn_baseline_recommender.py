import logging
import unittest

import pandas as pd
from datagencars.evaluation.rs_surprise import evaluation, surprise_helpers
from datagencars.evaluation.rs_surprise.accuracy import (f1_score, fcp, mae,
                                                         map, mse, ndcg,
                                                         precision, recall,
                                                         rmse)
from surprise import KNNBaseline
from surprise.model_selection import train_test_split


class TestKNNBaselineRecommender(unittest.TestCase):    
    """
    A basic collaborative filtering algorithm taking into account a baseline rating.
    """

    def setUp(self):
        # Loading a dataset:
        rating_df_path = 'resources/existing_dataset/without_context/preferencial_rating/sts/rating.csv'
        rating_df = pd.read_csv(rating_df_path, sep=';')
        self.data = surprise_helpers.convert_to_surprise_dataset(df=rating_df) 

        # Split the data into a training set and a test set:
        self.trainset, self.testset = train_test_split(self.data, test_size=0.20, random_state=42)
        
        # Parameters:
        k = 40
        min_k = 1
        sim_options = {'name': 'pearson', 'user_based': True, 'min_support': 1}
        bsl_options = {'method': "als", "reg_i": 10, "reg_u": 15, "n_epochs": 10, "learning_rate": 0.005}
        # Create a recommender instance:
        self.__rs = KNNBaseline(k=k, min_k=min_k, sim_options=sim_options, bsl_options=bsl_options)
    
    def tearDown(self):
        del self.__rs
    
    def test_knn_baseline_recommender_metrics(self):
        # Train the model on the training set:
        self.__rs.fit(self.trainset)
        
        # Make predictions on the test set
        predictions = self.__rs.test(self.testset)
        
        # Calculate and print multiple evaluation metrics:
        mae_value = mae(predictions)    
        rmse_value = rmse(predictions)        
        mse_value = mse(predictions)  
        fcp_value = fcp(predictions)  
        map_value = map(predictions)  
        ndcg_value = ndcg(predictions)
        precision_value = precision(predictions)
        recall_value = recall(predictions)
        f1_score_value = f1_score(predictions)

        logging.info(f'mae: {mae_value}')   
        logging.info(f'rmse: {rmse_value}')   
        logging.info(f'mse: {mse_value}')   
        logging.info(f'fcp: {fcp_value}')   
        logging.info(f'map: {map_value}')   
        logging.info(f'ndcg: {ndcg_value}')   
        logging.info(f'precision: {precision_value}')   
        logging.info(f'recall: {recall}')   
        logging.info(f'f1_score: {f1_score_value}')   

        # Assertions based on specific use cases:
        self.assertLessEqual(mae_value, 5.0)      
        self.assertLessEqual(rmse_value, 5.0)
        self.assertLessEqual(mse_value, 5.0)
        self.assertGreaterEqual(fcp_value, 0.0)
        self.assertGreaterEqual(map_value, 0.0) 
        self.assertGreaterEqual(ndcg_value, 0.0)
        self.assertGreaterEqual(precision_value, 0.0)
        self.assertGreaterEqual(recall_value, 0.0)
        self.assertGreaterEqual(f1_score_value, 0.0)

    def test_knn_baseline_recommender_cross_validation(self):
        metric_result_map = evaluation.cross_validate(algo=self.__rs, data=self.data, measures=['RMSE', 'MAE'], cv=5, return_train_measures=True, verbose=True)
        for metric_name, metric_value_list in metric_result_map.items():
            logging.info(f'{metric_name}: {metric_value_list}')       
            for metric_value in metric_value_list:
                self.assertTrue(0 <= metric_value <= 2.0, f"Metric value {metric_name} is out of range")


if __name__ == '__main__':
    unittest.main()
