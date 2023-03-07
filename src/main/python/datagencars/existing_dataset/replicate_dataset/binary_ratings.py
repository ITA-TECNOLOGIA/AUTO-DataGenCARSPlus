import pandas as pd

def is_binary_rating(df):
    """
    Check if the 'rating' column has only two unique values
    :param df: dataframe to check
    :return: True if the 'rating' column has only two unique values, False otherwise
    """
    unique_values = df['rating'].dropna().unique()
    return len(unique_values) == 2
