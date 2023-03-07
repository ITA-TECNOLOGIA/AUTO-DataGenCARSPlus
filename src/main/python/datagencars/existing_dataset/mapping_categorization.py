def apply_mappings(df, mappings):
    """
    Apply mappings to a dataframe
    :param df: dataframe to apply mappings to
    :param mappings: dictionary of mappings
    :return: dataframe with mappings applied
    """
    for key, value in mappings.items():
        df[key] = df[key].map(value)
    return df
