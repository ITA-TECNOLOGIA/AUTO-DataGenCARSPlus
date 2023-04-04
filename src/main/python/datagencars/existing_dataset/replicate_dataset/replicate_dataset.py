import logging


class ReplicateDataset:
    '''
    Replicate an existing dataset.

    Input:
        [U]  user.csv
        [I]  item.csv
        [C]  context.csv <optional>
        [R]  rating.csv

    Algorithm:
        Precondition: If the dataset is a single file, it is expected to be divided into user.csv, item.csv, context.csv <optional> and ratings.csv.
        1- extract_statistics (extract_statistics_rating, extract_statistics_uic): 
        2- generate_user_profile:
        3- replicate_dataset:

    Ouput:
        [R]  rating.csv <replicated>        
    '''

    def __init__(self):
        pass

    def replicate_dataset(self):
        pass
