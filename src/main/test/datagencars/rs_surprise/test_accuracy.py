import unittest

import numpy as np
from datagencars.evaluation.rs_surprise import accuracy

"""
Test cases for the accuracy module
Usage: python -m unittest src\main\test\rs_surprise\test_accuracy.py
"""

class TestRMSE(unittest.TestCase):
    
    def test_rmse_with_valid_input(self):
        predictions = [
            (1, 2, 3, 4, 5),
            (6, 7, 8, 9, 10),
            (11, 12, 13, 14, 15)
        ]
        expected_rmse = np.sqrt(np.mean([(3 - 4)**2, (8 - 9)**2, (13 - 14)**2]))
        result = accuracy.rmse(predictions, verbose=False)
        self.assertAlmostEqual(result, expected_rmse, delta=1e-4)

    def test_rmse_with_empty_input(self):
        predictions = []
        with self.assertRaises(ValueError) as context:
            accuracy.rmse(predictions, verbose=False)
        self.assertIn("Prediction list is empty.", str(context.exception))

class TestMSE(unittest.TestCase):
    def test_empty_prediction_list(self):
        predictions = []
        with self.assertRaises(ValueError) as context:
            accuracy.mse(predictions)
        self.assertEqual(str(context.exception), "Prediction list is empty.")

    def test_calculate_mse(self):
        predictions = [(0, 0, 4, 3, None), (0, 0, 2, 1, None), (0, 0, 3, 2, None)]
        result = accuracy.mse(predictions, verbose=False)
        expected = (4 - 3)**2 + (2 - 1)**2 + (3 - 2)**2
        expected /= len(predictions)
        self.assertAlmostEqual(result, expected)

    def test_mse_with_verbose(self):
        predictions = [(0, 0, 4, 3, None), (0, 0, 2, 1, None), (0, 0, 3, 2, None)]
        result = accuracy.mse(predictions, verbose=True)
        expected = (4 - 3)**2 + (2 - 1)**2 + (3 - 2)**2
        expected /= len(predictions)
        self.assertAlmostEqual(result, expected)

class TestMAE(unittest.TestCase):
    def test_mae_with_valid_input(self):
        predictions = [(1, 1, 4, 4, None),
                       (1, 2, 3, 2, None),
                       (2, 1, 2, 3, None),
                       (2, 2, 1, 1, None)]
        mae_ = accuracy.mae(predictions, verbose=False)
        self.assertAlmostEqual(mae_, 0.5, delta=1e-4)

    def test_empty_prediction_list(self):
        predictions = []
        with self.assertRaises(ValueError) as context:
            accuracy.mae(predictions, verbose=False)
        self.assertEqual(str(context.exception), "Prediction list is empty.")

    def test_mae_with_empty_input(self):
        predictions = []
        with self.assertRaises(ValueError):
            accuracy.mae(predictions, verbose=False)
            
    def test_mae_with_single_input(self):
        predictions = [(1, 1, 4, 3, None)]
        mae_ = accuracy.mae(predictions, verbose=False)
        self.assertAlmostEqual(mae_, 1.0, delta=1e-4)

class TestFCP(unittest.TestCase):
    def test_fcp_with_empty_input(self):
        predictions = []

        with self.assertRaises(ValueError):
            accuracy.fcp(predictions, verbose=False)

    def test_fcp_with_only_one_prediction(self):
        predictions = [
            (1, 2, 3)
        ]
        with self.assertRaises(ValueError):
            result = accuracy.fcp(predictions, verbose=False)

class TestPrecision(unittest.TestCase):
    def test_empty_prediction_list(self):
        predictions = []
        with self.assertRaises(ValueError) as context:
            accuracy.precision(predictions)
        self.assertEqual(str(context.exception), "Prediction list is empty.")

    def test_precision_calculation(self):
        predictions = [
            (1, 1, 4, 3, None),
            (1, 2, 5, 4, None),
            (1, 3, 2, 1, None),
            (2, 1, 4, 4, None),
            (2, 2, 5, 5, None),
            (2, 3, 1, 1, None),
        ]
        expected_precision = 1
        result = accuracy.precision(predictions)
        self.assertAlmostEqual(expected_precision, result, places=2)

    def test_precision_calculation(self):
        predictions = [
            (1, 1, 1, 1, 1),
            (1, 2, 1, 1, 1),
            (1, 3, 0, 0, 1)
        ]
        expected_precision = 0
        result = accuracy.precision(predictions)
        self.assertAlmostEqual(expected_precision, result, places=2)

class TestRecall(unittest.TestCase):
    def test_empty_predictions(self):
        predictions = []
        with self.assertRaises(ValueError) as context:
            accuracy.recall(predictions)
        self.assertEqual(str(context.exception), "Prediction list is empty.")

    def test_single_prediction(self):
        predictions = [(1, 2, 4, 3, 5)]
        result = accuracy.recall(predictions, verbose=False)
        self.assertEqual(result, 0.0)

    def test_multiple_predictions(self):
        predictions = [(1, 2, 4, 3, None), (3, 2, 5, 4, None), (2, 1, 3, 2, None)]
        result = accuracy.recall(predictions, verbose=False)
        self.assertEqual(result, 1/3)

    def test_verbose(self):
        predictions = [(1, 2, 4, 3, None)]
        result = accuracy.recall(predictions)
        self.assertEqual(result, 0.0)

class TestF1Score(unittest.TestCase):
    def test_f1_score_with_correct_predictions(self):
        predictions = [
            (0, 1, 4, 4, None),
            (0, 2, 5, 5, None),
            (0, 3, 3, 3, None),
            (1, 0, 5, 5, None),
            (1, 2, 4, 4, None),
            (1, 3, 2, 2, None),
            (2, 0, 3, 3, None),
            (2, 1, 2, 2, None),
            (2, 3, 4, 4, None),
            (3, 0, 2, 2, None),
            (3, 1, 4, 4, None),
            (3, 2, 3, 3, None),
        ]
        f1 = accuracy.f1_score(predictions)
        self.assertAlmostEqual(f1, 1.0, delta=1e-7)
        
    def test_f1_score_with_incorrect_predictions(self):
        predictions = [
            (0, 1, 4, 5, None),
            (0, 2, 5, 4, None),
            (0, 3, 3, 2, None),
            (1, 0, 5, 3, None),
            (1, 2, 4, 3, None),
            (1, 3, 2, 1, None),
            (2, 0, 3, 2, None),
            (2, 1, 2, 1, None),
            (2, 3, 4, 5, None),
            (3, 0, 2, 1, None),
            (3, 1, 4, 5, None),
            (3, 2, 3, 2, None),
        ]
        f1 = accuracy.f1_score(predictions)
        self.assertAlmostEqual(f1, 0.75, delta=1e-7)

import unittest

import numpy as np


class TestMAP(unittest.TestCase):
    def test_map_with_empty_predictions_list(self):
        predictions = []
        with self.assertRaises(ValueError) as context:
            accuracy.map(predictions)
        self.assertEqual(str(context.exception), "Prediction list is empty.")

    def test_map_with_verbose_False(self):
        predictions = [
            (1, 1, 4, 4.5, ""),
            (1, 2, 3, 3.5, ""),
            (2, 1, 4, 4.5, ""),
            (2, 2, 2, 2.5, ""),
        ]
        result = accuracy.map(predictions, verbose=False)
        self.assertEqual(result, 1.0)

    def test_map_with_multiple_users(self):
        predictions = [
            (1, 1, 4, 4.5, ""),
            (1, 2, 3, 3.5, ""),
            (2, 1, 4, 4.5, ""),
            (2, 2, 2, 2.5, ""),
        ]
        result = accuracy.map(predictions)
        self.assertEqual(result, 1.0)

    def test_map_with_threshold_of_3_5(self):
        predictions = [
            (1, 1, 4, 4.5, ""),
            (1, 2, 3, 3.5, ""),
            (2, 1, 4, 4.5, ""),
            (2, 2, 2, 2.5, ""),
        ]
        result = accuracy.map(predictions)
        self.assertEqual(result, 1.0)

    def test_map_with_k_of_10(self):
        predictions = [
            (1, 1, 4, 4.5, ""),
            (1, 2, 3, 3.5, ""),
            (2, 1, 4, 4.5, ""),
            (2, 2, 2, 2.5, ""),
        ]
        result = accuracy.map(predictions)
        self.assertEqual(result, 1.0)

    def test_map_with_predictions_list(self):
        predictions = [
            (1, 1, 4, 4.5, ""),
            (1, 2, 3, 3.5, ""),
            (2, 1, 4, 4.5, ""),
            (2, 2, 2, 2.5, ""),
        ]
        result = accuracy.map(predictions)
        self.assertEqual(result, 1.0)

class TestNDCG(unittest.TestCase):
    def test_ndcg_empty_input(self):
        predictions = []
        with self.assertRaises(ValueError) as context:
            accuracy.ndcg(predictions)
        self.assertEqual("Prediction list is empty.", str(context.exception))

    def test_ndcg_correct_calculation(self):
        predictions = [
            (1, 2, 4, 5, None),
            (2, 1, 4, 4, None),
            (1, 3, 5, 4, None),
            (3, 2, 4, 4, None),
        ]
        result = accuracy.ndcg(predictions, verbose=False)
        self.assertAlmostEqual(1, result, places=3)

    def test_ndcg_top_n(self):
        predictions = [
            (1, 2, 4, 5, None),
            (2, 1, 4, 4, None),
            (1, 3, 5, 4, None),
            (3, 2, 4, 4, None),
        ]
        result = accuracy.ndcg(predictions, verbose=True)
        self.assertAlmostEqual(1, result, places=3)
