from surprise import (NMF, SVD, BaselineOnly, CoClustering, Dataset,
                      KNNBaseline, KNNBasic, KNNWithMeans, KNNWithZScore,
                      NormalPredictor, Reader, SlopeOne, SVDpp)
from surprise import model_selection as ms


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
    elif algo_name == "CoClustering":
        return CoClustering(**params)
    elif algo_name == "BaselineOnly":
        return BaselineOnly()
    elif algo_name == "NormalPredictor":
        return NormalPredictor()
    elif algo_name == "KNNBasic":
        return KNNBasic(**params)
    elif algo_name == "KNNWithMeans":
        return KNNWithMeans(**params)
    elif algo_name == "KNNWithZScore":
        return KNNWithZScore(**params)
    elif algo_name == "KNNBaseline":
        return KNNBaseline(**params)
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
        return ms.RepeatedKFold(n_splits=params["n_splits"], n_repeats=params["n_repeats"])
    elif strategy == "ShuffleSplit":
        return ms.ShuffleSplit(n_splits=params["n_splits"], test_size=params["test_size"], shuffle=params["shuffle"])
    elif strategy == "LeaveOneOut":
        return ms.LeaveOneOut(n_splits=params["n_splits"], min_n_ratings=params["min_n_ratings"])
    # elif strategy == "PredefinedKFold":
    #     folds = []
    #     with open(params["folds_file"]) as f:
    #         for line in f:
    #             folds.append(list(map(int, line.split())))
    #     return ms.PredefinedKFold(folds)
    # elif strategy == "train_test_split":
    #     return ms.train_test_split(test_size=params["test_size"], random_state=params["random_state"])
    else:
        raise ValueError('Invalid split strategy')

def convert_to_surprise_dataset(df):
    """
    Converts a pandas dataframe to a surprise dataset
    :param df: the dataframe to convert
    :return: the surprise dataset
    """
    # A reader is still needed but only the rating_scale param is required.
    reader = Reader(rating_scale=(df["rating"].min(), df["rating"].max()))
    # The columns must correspond to user id, item id and ratings (in that order).
    return Dataset.load_from_df(df[["user_id", "item_id", "rating"]], reader)  
