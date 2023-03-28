import sys
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics import (
    make_scorer,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import (
    cross_validate,
    ShuffleSplit,
    KFold,
    LeaveOneOut,
    RepeatedKFold,
    train_test_split,
)
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
sys.path.append("src/main/python/streamlit")
import config

def create_algorithm(algo_name, params=None):
    """
    Creates an algorithm from its name and parameters
    :param algo_name: the name of the algorithm
    :param params: the parameters of the algorithm
    :return: the algorithm
    """
    if algo_name == "KNeighborsClassifier":
        return KNeighborsClassifier(**params)
    elif algo_name == "SVC":
        return SVC(**params)
    elif algo_name == "GaussianNB":
        return GaussianNB()
    elif algo_name == "RandomForestClassifier":
        return RandomForestClassifier(**params)
    elif algo_name == "KMeans":
        return KMeans(**params)
    elif algo_name == "DBSCAN":
        return DBSCAN(**params)
    elif algo_name == "HistGradientBoostingClassifier":
        return HistGradientBoostingClassifier(**params)
    else:
        raise ValueError("Invalid algorithm name")
    
def create_split_strategy(strategy, strategy_params):
    """
    Creates a split strategy from its name and parameters
    :param strategy: the name of the strategy
    :param strategy_params: the parameters of the strategy
    :return: the strategy
    """
    if strategy == "ShuffleSplit":
        return ShuffleSplit(n_splits=strategy_params['n_splits'],
                             train_size=strategy_params['train_size'],
                             random_state=strategy_params['random_state'])
    elif strategy == "KFold":
        return KFold(n_splits=strategy_params['n_splits'],
                     random_state=strategy_params['random_state'],
                     shuffle=strategy_params['shuffle'])
    elif strategy == "LeaveOneOut":
        return LeaveOneOut()
    elif strategy == "RepeatedKFold":
        return RepeatedKFold(n_splits=strategy_params['n_splits'],
                             n_repeats=strategy_params['n_repeats'],
                             random_state=strategy_params['random_state'])
    elif strategy == "train_test_split":
        return train_test_split # Note that train_test_split is a function and not a class, so it doesn't need instantiation.
    else:
        raise ValueError(f"Unsupported split strategy: {strategy}")

def get_categorical_cols(df):
    '''
    Returns a list of the column names in a pandas dataframe that are categorical.
    '''
    # Select columns with dtype 'object'
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Check if there are any columns with dtype 'category'
    categorical_cols += df.select_dtypes(include=['category']).columns.tolist()
    
    return categorical_cols

def preprocess_missing_values(df, strategy='mean'):
    '''
    Imputes missing values in a pandas dataframe.
    Replace 'mean' with 'median', 'most_frequent', or 'constant' if needed
    '''
    imputer = SimpleImputer(missing_values=np.nan, strategy=strategy)
    imputed_data = imputer.fit_transform(df)
    return pd.DataFrame(imputed_data, columns=df.columns)

def evaluate(merged_df, algo_list, strategy_instance, metrics, user_id=None):
    """
    Evaluates a list of algorithms using a given split strategy
    :param merged_df: the dataframe to use
    :param algo_list: the list of algorithms to evaluate
    :param strategy_instance: the split strategy to use
    :param metrics: the metrics to use
    :param user_id: the target user id
    :return: a dataframe with the results
    """
    categorical_columns = get_categorical_cols(merged_df)
    dummies_df = pd.get_dummies(merged_df, columns=categorical_columns)
    data = dummies_df
    # data = preprocess_missing_values(dummies_df, strategy='mean')
    # Filter the data for the target user if a target_user_id is provided
    if user_id is not None:
        data = data[data['user_id'] == user_id]

    # Prepare the input for the evaluation
    X = data.drop(columns=["user_id", "item_id", "rating"])
    y = data["rating"]

    # Prepare the dictionary for the metrics
    scoring = {}
    for metric in metrics:
        if metric == "Precision":
            scoring["precision"] = make_scorer(precision_score, average='weighted')
        elif metric == "Recall":
            scoring["recall"] = make_scorer(recall_score, average='weighted')
        elif metric == "F1 score":
            scoring["f1"] = make_scorer(f1_score, average='weighted')
        elif metric == "ROC-AUC":
            scoring["roc_auc"] = make_scorer(roc_auc_score, needs_proba=True, average='weighted', multi_class='ovr')

    results = []
    for algorithm in algo_list:
        algo_name = type(algorithm).__name__
        cv_results = cross_validate(algorithm, X, y, cv=strategy_instance, scoring=scoring, return_estimator=True)
        n_splits = strategy_instance.get_n_splits()
        for fold_idx in range(n_splits):
            fold_results = {"Fold": fold_idx + 1, "Algorithm": algo_name}
            for metric, score in cv_results.items():
                if metric.startswith("test_precision"):
                    fold_results["Precision"] = score[fold_idx]
                elif metric.startswith("test_recall"):
                    fold_results["Recall"] = score[fold_idx]
                elif metric.startswith("test_f1"):
                    fold_results["F1 score"] = score[fold_idx]
                elif metric.startswith("test_roc_auc"):
                    fold_results["ROC-AUC"] = score[fold_idx]
                elif metric.startswith("fit_time"):
                    fold_results["Time (train)"] = score[fold_idx]
                elif metric.startswith("score_time"):
                    fold_results["Time (test)"] = score[fold_idx]
            results.append(fold_results)

    results_df = pd.DataFrame(results)

    available_columns = results_df.columns.tolist()
    column_order = ['Fold', 'Algorithm']
    for metric in config.SCIKIT_LEARN_METRICS:
        if metric in available_columns:
            column_order.append(metric)
    column_order.extend(['Time (train)', 'Time (test)'])
    results_df = results_df[column_order]

    return results_df
