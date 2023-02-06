import surprise
from surprise import rs_surprise
import unittest
import logging

"""
Test cases for the surprise module
Usage: python -m unittest src\main\test\datagencars\surprise\test_surprise.py
"""

class TestCreateAlgorithm(unittest.TestCase):
    def test_valid_algorithm_name(self):
        algo_name = "SVD"
        params = {"n_factors": 100, "n_epochs": 20, "lr_all": 0.005, "reg_all": 0.02}
        result = rs_surprise.create_algorithm(algo_name, params)
        self.assertIsInstance(result, surprise.SVD)

    def test_invalid_algorithm_name(self):
        algo_name = "InvalidAlgorithm"
        params = None
        with self.assertRaises(ValueError) as context:
            rs_surprise.create_algorithm(algo_name, params)
        self.assertEqual(str(context.exception), "Invalid algorithm name")

class TestCreateSplitStrategy(unittest.TestCase):
    def test_valid_split_strategy(self):
        strategy = "KFold"
        params = {"n_splits": 5, "shuffle": True}
        result = rs_surprise.create_split_strategy(strategy, params)
        self.assertIsInstance(result, surprise.model_selection.KFold)

    def test_invalid_split_strategy(self):
        strategy = "InvalidStrategy"
        params = None
        with self.assertRaises(ValueError) as context:
            rs_surprise.create_split_strategy(strategy, params)
        self.assertEqual(str(context.exception), 'Invalid split strategy')

