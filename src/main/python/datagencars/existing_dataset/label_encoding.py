from sklearn.preprocessing import LabelEncoder

def apply_label_encoder(df, columns):
    encoder = LabelEncoder()
    for col in columns:
        if col in df.columns:
            df[col] = encoder.fit_transform(df[col])
    return df