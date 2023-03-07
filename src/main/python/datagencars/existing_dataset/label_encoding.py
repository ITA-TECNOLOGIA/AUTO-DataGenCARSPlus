from sklearn.preprocessing import LabelEncoder

def apply_label_encoder(df, columns):
    """
    Apply label encoder to a dataframe
    :param df: dataframe to apply label encoder to
    :param columns: columns to apply label encoder to
    :return: dataframe with label encoder applied
    """
    encoder = LabelEncoder()
    for col in columns:
        if col in df.columns:
            df[col] = encoder.fit_transform(df[col])
    return df