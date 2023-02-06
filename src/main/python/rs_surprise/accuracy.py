"""
The :mod:`surprise.accuracy` module provides tools for computing accuracy
metrics on a set of predictions.

Available accuracy metrics:

.. autosummary::
    :nosignatures:

    rmse
    mse
    mae
    fcp
    accuracy
    precision
    recall
    f1score
    map
    ndcg
"""

from collections import defaultdict
import math
import numpy as np


def rmse(predictions, verbose=True):
    """Compute RMSE (Root Mean Squared Error).

    .. math::
        \\text{RMSE} = \\sqrt{\\frac{1}{|\\hat{R}|} \\sum_{\\hat{r}_{ui} \\in
        \\hat{R}}(r_{ui} - \\hat{r}_{ui})^2}.

    Args:
        predictions (:obj:`list` of :obj:`Prediction\
            <surprise.prediction_algorithms.predictions.Prediction>`):
            A list of predictions, as returned by the :meth:`test()
            <surprise.prediction_algorithms.algo_base.AlgoBase.test>` method.
        verbose: If True, will print computed value. Default is ``True``.


    Returns:
        The Root Mean Squared Error of predictions.

    Raises:
        ValueError: When ``predictions`` is empty.
    """

    if not predictions:
        raise ValueError("Prediction list is empty.")

    mse = np.mean(
        [float((true_r - est) ** 2) for (_, _, true_r, est, _) in predictions]
    )
    rmse_ = np.sqrt(mse)

    if verbose:
        print(f"RMSE: {rmse_:1.4f}")

    return rmse_


def mse(predictions, verbose=True):
    """Compute MSE (Mean Squared Error).

    .. math::
        \\text{MSE} = \\frac{1}{|\\hat{R}|} \\sum_{\\hat{r}_{ui} \\in
        \\hat{R}}(r_{ui} - \\hat{r}_{ui})^2.

    Args:
        predictions (:obj:`list` of :obj:`Prediction\
            <surprise.prediction_algorithms.predictions.Prediction>`):
            A list of predictions, as returned by the :meth:`test()
            <surprise.prediction_algorithms.algo_base.AlgoBase.test>` method.
        verbose: If True, will print computed value. Default is ``True``.


    Returns:
        The Mean Squared Error of predictions.

    Raises:
        ValueError: When ``predictions`` is empty.
    """

    if not predictions:
        raise ValueError("Prediction list is empty.")

    mse_ = np.mean(
        [float((true_r - est) ** 2) for (_, _, true_r, est, _) in predictions]
    )

    if verbose:
        print(f"MSE: {mse_:1.4f}")

    return mse_


def mae(predictions, verbose=True):
    """Compute MAE (Mean Absolute Error).

    .. math::
        \\text{MAE} = \\frac{1}{|\\hat{R}|} \\sum_{\\hat{r}_{ui} \\in
        \\hat{R}}|r_{ui} - \\hat{r}_{ui}|

    Args:
        predictions (:obj:`list` of :obj:`Prediction\
            <surprise.prediction_algorithms.predictions.Prediction>`):
            A list of predictions, as returned by the :meth:`test()
            <surprise.prediction_algorithms.algo_base.AlgoBase.test>` method.
        verbose: If True, will print computed value. Default is ``True``.


    Returns:
        The Mean Absolute Error of predictions.

    Raises:
        ValueError: When ``predictions`` is empty.
    """

    if not predictions:
        raise ValueError("Prediction list is empty.")

    mae_ = np.mean([float(abs(true_r - est)) for (_, _, true_r, est, _) in predictions])

    if verbose:
        print(f"MAE:  {mae_:1.4f}")

    return mae_


def fcp(predictions, verbose=True):
    """Compute FCP (Fraction of Concordant Pairs).

    Computed as described in paper `Collaborative Filtering on Ordinal User
    Feedback <https://www.ijcai.org/Proceedings/13/Papers/449.pdf>`_ by Koren
    and Sill, section 5.2.

    Args:
        predictions (:obj:`list` of :obj:`Prediction\
            <surprise.prediction_algorithms.predictions.Prediction>`):
            A list of predictions, as returned by the :meth:`test()
            <surprise.prediction_algorithms.algo_base.AlgoBase.test>` method.
        verbose: If True, will print computed value. Default is ``True``.


    Returns:
        The Fraction of Concordant Pairs.

    Raises:
        ValueError: When ``predictions`` is empty.
    """

    if not predictions:
        raise ValueError("Prediction list is empty.")

    predictions_u = defaultdict(list)
    nc_u = defaultdict(int)
    nd_u = defaultdict(int)

    for u0, _, r0, est, _ in predictions:
        predictions_u[u0].append((r0, est))

    for u0, preds in predictions_u.items():
        for r0i, esti in preds:
            for r0j, estj in preds:
                if esti > estj and r0i > r0j:
                    nc_u[u0] += 1
                if esti >= estj and r0i < r0j:
                    nd_u[u0] += 1

    nc = np.mean(list(nc_u.values())) if nc_u else 0
    nd = np.mean(list(nd_u.values())) if nd_u else 0

    try:
        fcp = nc / (nc + nd)
    except ZeroDivisionError:
        raise ValueError(
            "cannot compute fcp on this list of prediction. "
            + "Does every user have at least two predictions?"
        )

    if verbose:
        print(f"FCP:  {fcp:1.4f}")
    return fcp

def precision(predictions, verbose=True):
    k = 10
    threshold = 3.5

    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))

    precisions = []
    for uid, user_ratings in user_est_true.items():
        user_ratings.sort(key=lambda x: x[0], reverse=True)
        n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])
        n_rel_and_rec_k = sum(
            ((true_r >= threshold) and (est >= threshold))
            for (est, true_r) in user_ratings[:k]
        )
        precision = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 0
        precisions.append(precision)
    
    precision = np.mean(precisions)

    if verbose:
        print(f"Precision: {precision:1.4f}")
    return precision

def recall(predictions, verbose=True):
    """
    Compute Recall at k metric for each user
    """
    k = 10
    threshold = 3.5
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))
    recalls = []
    for uid, user_ratings in user_est_true.items():
        n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)
        n_rel_and_rec_k = sum(
            ((true_r >= threshold) and (est >= threshold))
            for (est, true_r) in user_ratings[:k]
        )
        recall = n_rel_and_rec_k / n_rel if n_rel != 0 else 0
        recalls.append(recall)
    if verbose:
        print(f"Recalls: {recalls:1.4f}")
    return np.mean(recalls)

def f1_score(predictions, verbose=True):
    """
    Compute F1 Score at k metric for each user
    """
    k = 10
    threshold = 3.5
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))
    f1_scores = dict()
    for uid, user_ratings in user_est_true.items():
        user_ratings.sort(key=lambda x: x[0], reverse=True)
        n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)
        n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])
        n_rel_and_rec_k = sum(
            ((true_r >= threshold) and (est >= threshold))
            for (est, true_r) in user_ratings[:k]
        )
        precision = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 0
        recall = n_rel_and_rec_k / n_rel if n_rel != 0 else 0
        f1_score = 2 * ((precision * recall) / (precision + recall)) if precision + recall != 0 else 0
        f1_scores[uid] = f1_score
    result = np.mean(list(f1_scores.values()))
    if verbose:
        print(f"F1-score: {result:1.4f}")
    return result

def map(predictions, verbose=True):
    k=10
    threshold=3.5
    # First map the predictions to each user.
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))
    maps = dict()
    for uid, user_ratings in user_est_true.items():
        # Sort user ratings by estimated value
        user_ratings.sort(key=lambda x: x[0], reverse=True)
        # Number of relevant items
        n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)
        # Number of relevant and recommended items in top k
        n_rel_and_rec_k = sum(
            ((true_r >= threshold) and (est >= threshold))
            for (est, true_r) in user_ratings[:k]
        )
        # Mean Average Precision (MAP)
        ap_values = []
        for i, (est, true_r) in enumerate(user_ratings):
            if true_r >= threshold:
                precision = n_rel_and_rec_k / (i + 1) if (i + 1) != 0 else 0
                ap_values.append(precision)
        map_value = sum(ap_values) / n_rel if n_rel != 0 else 0
        maps[uid] = map_value
        if verbose:
            print(f"MAP: {maps:1.4f}")
    return np.mean(list(maps.values()))

def ndcg(predictions, verbose=True):
    """
    Return Normalized Discounted Cumulative Gain (NDCG) at k for each user
    """
    k=10
    threshold=3.5
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))

    ndcgs = dict()
    for uid, user_ratings in user_est_true.items():
        # Sort user ratings by estimated value
        user_ratings.sort(key=lambda x: x[0], reverse=True)
        true_r = [x[1] for x in user_ratings]
        discount_gain = [((2**x[1])-1)/math.log2(x[0]+1) for x in enumerate(true_r, start=1)]
        ideal_dcg = sorted(discount_gain, reverse=True)
        ndcg = sum(discount_gain[:k])/sum(ideal_dcg[:k]) if sum(ideal_dcg[:k]) != 0 else 0
        ndcgs[uid] = ndcg

    if verbose:
        print(f"NDCG: {ndcgs:1.4f}")
    return np.mean(list(ndcgs.values()))

"""
Precision and Recall at k metrics for each user functions are inspired by the link´s source.
Furthermore, the function was modified to include the F1-score and MAP metrics.
"""
# def precision_recall_at_k(predictions, verbose=True):
#     """
#     Return precision, recall, F1-score and MAP at k metrics for each user
#     Source: https://github.com/NicolasHug/Surprise/blob/master/examples/precision_recall_at_k.py
#     """
#     k=10
#     threshold=3.5

#     # First map the predictions to each user.
#     user_est_true = defaultdict(list)
#     for uid, _, true_r, est, _ in predictions:
#         user_est_true[uid].append((est, true_r))

#     precisions = dict()
#     recalls = dict()
#     f1_scores = dict()
#     maps = dict()
#     for uid, user_ratings in user_est_true.items():

#         # Sort user ratings by estimated value
#         user_ratings.sort(key=lambda x: x[0], reverse=True)

#         # Number of relevant items
#         n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)

#         # Number of recommended items in top k
#         n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])

#         # Number of relevant and recommended items in top k
#         n_rel_and_rec_k = sum(
#             ((true_r >= threshold) and (est >= threshold))
#             for (est, true_r) in user_ratings[:k]
#         )

#         # Precision@K: Proportion of recommended items that are relevant
#         # When n_rec_k is 0, Precision is undefined. We here set it to 0.
#         precision = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 0
#         precisions[uid] = precision

#         # Recall@K: Proportion of relevant items that are recommended
#         # When n_rel is 0, Recall is undefined. We here set it to 0.
#         recall = n_rel_and_rec_k / n_rel if n_rel != 0 else 0
#         recalls[uid] = recall

#         # F1-score@K: Harmonic mean of precision and recall
#         f1_score = 2 * ((precision * recall) / (precision + recall)) if precision + recall != 0 else 0
#         f1_scores[uid] = f1_score

#         # Mean Average Precision (MAP)
#         ap_values = []
#         for i, (est, true_r) in enumerate(user_ratings):
#             if true_r >= threshold:
#                 ap_values.append(precisions[uid] * (i + 1) / (i + 1))
#         map_value = sum(ap_values) / n_rel if n_rel != 0 else 0
#         maps[uid] = map_value

#         if verbose:
#             print(f"Precissions: {precisions:1.4f}")
#             print(f"Recalls: {recalls:1.4f}")
#             print(f"F1-score: {f1_scores:1.4f}")
#             print(f"MAP: {maps:1.4f}")

#     return precisions, recalls, f1_scores, maps
