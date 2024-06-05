

def sort_rating_df(rating_df):
    """
    Sort the rating dataframe by column.
    :param rating_df: The rating dataframe.
    :return: The sorted rating dataframe.
    """
    # Sorting and resetting index
    sort_columns = ['user_id', 'item_id', 'rating']
    if 'context_id' in rating_df.columns:
        sort_columns.insert(2, 'context_id')
    sorted_rating_df = rating_df.sort_values(by=sort_columns, ascending=True, na_position='first')
    sorted_rating_df.reset_index(drop=True, inplace=True) 
    return sorted_rating_df
