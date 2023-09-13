import unittest
import numpy as np
from surprise import Dataset
from surprise import KNNBasic, SVD
from surprise.model_selection.split import train_test_split
from datagencars.evaluation.rs_surprise import evaluation

"""
Test cases for the evaluation module
Usage: python -m unittest src\main\test\rs_surprise\test_evaluation.py
"""
class TestCrossValidate(unittest.TestCase):
    
    def test_cross_validate(self):
        results = evaluation.cross_validate(KNNBasic(), Dataset.load_builtin('ml-100k'), measures=['RMSE', 'MAE'], cv=5)
        results_array = np.array(results['fit_time'])
        self.assertEqual(results_array.shape, (5,))

    def test_cross_validate_return_train_measures(self):
        data = Dataset.load_builtin('ml-100k')
        algo = KNNBasic()
        results = evaluation.cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, return_train_measures=True)

        # Test if the results have the correct keys and if the arrays have the correct shape
        self.assertIn('test_rmse', results)
        self.assertEqual(results['test_rmse'].shape, (5,))
        self.assertIn('train_rmse', results)
        self.assertEqual(results['train_rmse'].shape, (5,))
        self.assertIn('test_mae', results)
        self.assertEqual(results['test_mae'].shape, (5,))
        self.assertIn('train_mae', results)
        self.assertEqual(results['train_mae'].shape, (5,))

class TestFitAndScore(unittest.TestCase):
    def setUp(self):
        self.data = Dataset.load_builtin('ml-100k')
        self.algo = SVD()
        self.trainset, self.testset = train_test_split(self.data)

    def test_fit_and_score_returns_correct_output(self):
        measures = ['rmse', 'mae']
        ret = evaluation.fit_and_score(self.algo, self.trainset, self.testset, measures, False)

        self.assertIsInstance(ret, tuple)
        self.assertEqual(len(ret), 4)
        self.assertIsInstance(ret[0], dict)
        self.assertIsInstance(ret[1], dict)
        self.assertIsInstance(ret[2], float)
        self.assertIsInstance(ret[3], float)

        for measure in measures:
            self.assertIn(measure, ret[0])
            self.assertIsInstance(ret[0][measure], float)

    def test_fit_and_score_handles_train_measures_flag(self):
        measures = ['rmse', 'mae']
        ret = evaluation.fit_and_score(self.algo, self.trainset, self.testset, measures, True)

        self.assertIsInstance(ret, tuple)
        self.assertEqual(len(ret), 4)
        self.assertIsInstance(ret[0], dict)
        self.assertIsInstance(ret[1], dict)
        self.assertIsInstance(ret[2], float)
        self.assertIsInstance(ret[3], float)

        for measure in measures:
            self.assertIn(measure, ret[0])
            self.assertIsInstance(ret[0][measure], float)
            self.assertIn(measure, ret[1])
            self.assertIsInstance(ret[1][measure], float)
