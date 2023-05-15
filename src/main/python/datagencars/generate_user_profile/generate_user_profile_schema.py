import logging


class UserProfileSchema:

    '''
    Generates a user profile automatically from schema files. 
    For that, the LSMR method (An Iterative Algorithm for Sparse Least-Squares Problems)
    was used. [https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.lsmr.html]

    Input:
        item_schema.conf
        context.conf
        generation_config.conf.
    Output:
        user_profile.csv
    '''

    def __init__(self):
        pass