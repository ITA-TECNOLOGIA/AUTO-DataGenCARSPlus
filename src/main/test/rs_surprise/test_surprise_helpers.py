import surprise
from rs_surprise import surprise_helpers
import unittest
import logging
import pandas as pd
import numpy as np

"""
Test cases for the surprise helpers module
Usage: python -m unittest src\main\test\datagencars\rs_surprise\test_surprise_helpers.py
"""

class TestCreateAlgorithm(unittest.TestCase):
    def test_valid_algorithm_name(self):
        algo_name = "SVD"
        params = {"n_factors": 100, "n_epochs": 20, "lr_all": 0.005, "reg_all": 0.02}
        result = surprise_helpers.create_algorithm(algo_name, params)
        self.assertIsInstance(result, surprise.SVD)

    def test_invalid_algorithm_name(self):
        algo_name = "InvalidAlgorithm"
        params = None
        with self.assertRaises(ValueError) as context:
            surprise_helpers.create_algorithm(algo_name, params)
        self.assertEqual(str(context.exception), "Invalid algorithm name")

class TestCreateSplitStrategy(unittest.TestCase):
    def test_create_split_strategy_kfold(self):
        strategy = "KFold"
        params = {"n_splits": 5, "shuffle": True}
        result = surprise_helpers.create_split_strategy(strategy, params)
        self.assertIsInstance(result, surprise.model_selection.KFold)

    def test_create_split_strategy_leaveoneout(self):
        split_strategy = surprise_helpers.create_split_strategy("LeaveOneOut", {})
        self.assertIsInstance(split_strategy, surprise.model_selection.LeaveOneOut)

    def test_create_split_strategy_invalid(self):
        strategy = "InvalidStrategy"
        params = None
        with self.assertRaises(ValueError) as context:
            surprise_helpers.create_split_strategy(strategy, params)
        self.assertEqual(str(context.exception), 'Invalid split strategy')

class TestConvertToSurpriseDataset(unittest.TestCase):
    def test_convert_to_surprise_dataset(self):
        df = pd.DataFrame({
            "user_id": [1, 2, 3, 4, 5],
            "item_id": [6, 7, 8, 9, 10],
            "rating": [4, 3, 5, 2, 1],
            "timestamp": [100, 200, 300, 400, 500]
        })
        surprise_dataset = surprise_helpers.convert_to_surprise_dataset(df)
        self.assertIsInstance(surprise_dataset, surprise.Dataset)
        self.assertEqual(len(surprise_dataset.raw_ratings), 5)