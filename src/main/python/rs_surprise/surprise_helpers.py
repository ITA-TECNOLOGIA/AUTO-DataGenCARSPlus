from collections import defaultdict
import math
from surprise import (
    BaselineOnly,
    CoClustering,
    KNNBaseline,
    KNNBasic,
    KNNWithMeans,
    NMF,
    NormalPredictor,
    SlopeOne,
    SVD,
    SVDpp,
    model_selection as ms,
    Reader,
    Dataset
)

def create_algorithm(algo_name, params=None):
    """
    Creates an algorithm from its name and parameters
    :param algo_name: the name of the algorithm
    :param params: the parameters of the algorithm
    :return: the algorithm
    """
    if algo_name == "SVD":
        return SVD(**params)
    elif algo_name == "SVDpp":
        return SVDpp(**params)
    elif algo_name == "NMF":
        return NMF(**params)
    elif algo_name == "SlopeOne":
        return SlopeOne()
    elif algo_name == "KNNBasic":
        return KNNBasic()
    elif algo_name == "KNNWithMeans":
        return KNNWithMeans()
    elif algo_name == "KNNBaseline":
        return KNNBaseline()
    elif algo_name == "CoClustering":
        return CoClustering(**params)
    elif algo_name == "BaselineOnly":
        return BaselineOnly()
    elif algo_name == "NormalPredictor":
        return NormalPredictor()
    else:
        raise ValueError("Invalid algorithm name")

def create_split_strategy(strategy, params):
    """
    Creates a split strategy for cross-validation
    :param strategy: the name of the strategy
    :param params: the parameters of the strategy
    :return: the split strategy
    """
    if strategy == "KFold":
        return ms.KFold(n_splits=params["n_splits"], shuffle=params["shuffle"])
    elif strategy == "RepeatedKFold":
        return ms.RepeatedKFold(n_splits=params["n_splits"], n_repeats=params["n_repeats"], shuffle=params["shuffle"])
    elif strategy == "ShuffleSplit":
        return ms.ShuffleSplit(n_splits=params["n_splits"], test_size=params["test_size"], random_state=params["random_state"])
    elif strategy == "LeaveOneOut":
        return ms.LeaveOneOut()
    elif strategy == "PredefinedKFold":
        folds = []
        with open(params["folds_file"]) as f:
            for line in f:
                folds.append(list(map(int, line.split())))
        return ms.PredefinedKFold(folds)
    elif strategy == "train_test_split":
        return ms.train_test_split(test_size=params["test_size"], random_state=params["random_state"])
    else:
        raise ValueError('Invalid split strategy')

def convert_to_surprise_dataset(df):
    """
    Converts a pandas dataframe to a surprise dataset
    :param df: the dataframe to convert
    :return: the surprise dataset
    """
    if "timestamp" in df.columns:
        df = df.drop("timestamp", axis=1)
    elif "context_id" in df.columns:
        df = df.drop("context_id", axis=1)    
    reader = Reader(rating_scale=(df["rating"].min(), df["rating"].max()))
    return Dataset.load_from_df(df, reader)
