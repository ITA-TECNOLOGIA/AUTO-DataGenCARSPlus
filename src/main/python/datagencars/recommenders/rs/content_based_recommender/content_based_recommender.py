from surprise import AlgoBase


class ContentBasedRecommender(AlgoBase):
    """
    A basic content-based recommendation algorithm, by using Vector Space Model.
    """

    def __init__(self):
        AlgoBase.__init__(self)

    def fit(self, trainset):
        AlgoBase.fit(self, trainset)
        # self.sim = self.compute_similarities()

        return self

    def estimate(self, u, i):
        est = None
        
        return est
