from collections import defaultdict
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
    """
    df = df.drop("timestamp", axis=1) #¡IMPORTANTE!
    reader = Reader(rating_scale=(1, 5))
    return Dataset.load_from_df(df, reader)

def precision_recall_at_k(predictions, k=10, threshold=3.5):
    """
    Return precision, recall, F1-score and MAP at k metrics for each user
    Source: https://github.com/NicolasHug/Surprise/blob/master/examples/precision_recall_at_k.py
    """

    # First map the predictions to each user.
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))

    precisions = dict()
    recalls = dict()
    f1_scores = dict()
    maps = dict()
    for uid, user_ratings in user_est_true.items():

        # Sort user ratings by estimated value
        user_ratings.sort(key=lambda x: x[0], reverse=True)

        # Number of relevant items
        n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)

        # Number of recommended items in top k
        n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])

        # Number of relevant and recommended items in top k
        n_rel_and_rec_k = sum(
            ((true_r >= threshold) and (est >= threshold))
            for (est, true_r) in user_ratings[:k]
        )

        # Precision@K: Proportion of recommended items that are relevant
        # When n_rec_k is 0, Precision is undefined. We here set it to 0.
        precision = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 0
        precisions[uid] = precision

        # Recall@K: Proportion of relevant items that are recommended
        # When n_rel is 0, Recall is undefined. We here set it to 0.
        recall = n_rel_and_rec_k / n_rel if n_rel != 0 else 0
        recalls[uid] = recall

        # F1-score@K: Harmonic mean of precision and recall
        f1_score = 2 * ((precision * recall) / (precision + recall)) if precision + recall != 0 else 0
        f1_scores[uid] = f1_score

        # Mean Average Precision (MAP)
        ap_values = []
        for i, (est, true_r) in enumerate(user_ratings):
            if true_r >= threshold:
                ap_values.append(precisions[uid] * (i + 1) / (i + 1))
        map_value = sum(ap_values) / n_rel if n_rel != 0 else 0
        maps[uid] = map_value

    return precisions, recalls, f1_scores, maps
