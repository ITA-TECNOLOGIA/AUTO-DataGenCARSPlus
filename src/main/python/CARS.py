import datetime
import random
import time
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
from tabulate import tabulate

import datetime
import random
import time
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
from tabulate import tabulate

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
random.seed(0)

df = pd.read_csv(r'resources\dataset_ml_100k\ratings.csv')
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[["userId", "movieId", "rating"]], reader)
kf = KFold(random_state=0)  # folds will be the same for all algorithms.

table = []
for algo in ALGORITHMS:
    out = cross_validate(algo, data, ["rmse", "mae"], kf)
    link = LINK[algo.__class__.__name__]
    mean_rmse = "{:.3f}".format(np.mean(out["test_rmse"]))
    mean_mae = "{:.3f}".format(np.mean(out["test_mae"]))
    table.append([link, mean_rmse, mean_mae])

header = ["Movielens 100k", "RMSE", "MAE"]
print(tabulate(table, header, tablefmt="pipe"))
