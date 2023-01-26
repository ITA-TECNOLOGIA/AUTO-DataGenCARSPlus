import numpy as np
import pandas as pd
from surprise import (
    BaselineOnly,
    CoClustering,
    Dataset,
    KNNBaseline,
    KNNBasic,
    KNNWithMeans,
    NMF,
    NormalPredictor,
    SlopeOne,
    SVD,
    SVDpp,
    Reader
)
from surprise.model_selection import cross_validate, KFold

# The algorithms to cross-validate
ALGORITHMS = (
    SVD(random_state=0),
    SVDpp(random_state=0, cache_ratings=False),
    SVDpp(random_state=0, cache_ratings=True),
    NMF(random_state=0),
    SlopeOne(),
    KNNBasic(),
    KNNWithMeans(),
    KNNBaseline(),
    CoClustering(random_state=0),
    BaselineOnly(),
    NormalPredictor(),
)

# ugly dict to map algo names and datasets to their markdown links in the table
LINK = {
    "SVD": "SVD",
    "SVDpp": "SVD++",
    "NMF": "NMF",
    "SlopeOne": "Slope One",
    "KNNBasic": "k-NN",
    "KNNWithMeans": "Centered k-NN",
    "KNNBaseline": "k-NN Baseline",
    "CoClustering": "Co-Clustering",
    "BaselineOnly": "Baseline",
    "NormalPredictor": "Random"
}

np.random.seed(0)

df = pd.read_csv(r'resources\dataset_ml_100k\ratings.csv')
data = Dataset.load_from_df(df[["userId", "movieId", "rating"]], reader=Reader(rating_scale=(1, 5)))
kf = KFold(random_state=0)  # folds will be the same for all algorithms.

table = []
for algo in ALGORITHMS:
    out = cross_validate(algo, data, ["rmse", "mae"], kf)
    link = LINK[algo.__class__.__name__]
    mean_rmse = np.mean(out["test_rmse"])
    mean_mae = np.mean(out["test_mae"])
    print(f"{link}: RMSE={mean_rmse:.3f}, MAE={mean_mae:.3f}")
    table.append([link, mean_rmse, mean_mae])

# print(tabulate(table, headers=["Movielens 100k", "RMSE", "MAE"], floatfmt=".3f", tablefmt="pipe"))
results = pd.DataFrame(table, columns=["Movielens 100k", "RMSE", "MAE"])
results.to_csv(r'results_ml100k.csv', index=False)
print(results)
