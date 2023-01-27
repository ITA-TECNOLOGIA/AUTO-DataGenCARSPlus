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
    Reader,
    Dataset
)

def create_algorithm(algo_name, params=None):
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
