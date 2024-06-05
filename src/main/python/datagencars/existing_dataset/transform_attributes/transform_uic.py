import numpy as np
from sklearn.preprocessing import LabelEncoder


class TransformUIC:
    """
    Transforms user, item and contexts attributes (categorical to numerical / numerical to categorical).
    """

    def __init__(self, df):
        # The input DataFrame.
        self.df = df

    def numerical_to_categorical(self, mappings):
        """
        Converts specified numerical columns in a DataFrame to categorical using provided mappings.
        :param mappings: A dictionary of column-name to mapping dict pairs.
        :return: The DataFrame with numerical columns converted to categorical.
        """
        for key, value in mappings.items():
            self.df[key] = self.df[key].map(value)
        return self.df
    
    def categorical_to_numerical(self, column_name_list, ignore_nan=True):
        """
        Converts specified categorical columns in a DataFrame to numerical using label encoding.        
        :param column_name_list: A list of column names to be converted to numerical.
        :param ignore_nan: If True, NaN values in the specified columns are ignored and not replaced with numeric values. If False, NaN values are replaced with numeric values using label encoding.
        :return: The DataFrame with categorical columns converted to numerical.  
        """
        encoder = LabelEncoder()
        # Ignores NaN values (the rest of values are replaced by numeric values):
        if ignore_nan:
            for col in column_name_list:
                if col in self.df.columns:
                    # Store NaN values in a separate mask
                    nan_mask = self.df[col].isna()                
                    # Encode non-NaN values
                    self.df.loc[~nan_mask, col] = encoder.fit_transform(self.df.loc[~nan_mask, col])                
                    # Restore NaN values
                    self.df.loc[nan_mask, col] = np.nan       
        # Replaces NaN by numeric values:
        else:        
            for col in column_name_list:
                if col in self.df.columns:
                    self.df[col] = encoder.fit_transform(self.df[col])
            return self.df         
        return self.df
