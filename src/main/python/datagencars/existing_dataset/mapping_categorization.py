def apply_mappings(df, mappings):
    for key, value in mappings.items():
        df[key] = df[key].map(value)
    return df
