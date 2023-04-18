import numpy as np
import pandas as pd
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics import ExtractStatistics


class ExtractStatisticsUIC(ExtractStatistics):

    def __init__(self, uic_df):
        super().__init__(uic_df)

    def get_number_id(self):
        """
        Gets the number of IDs (user_id, item_id and context_id) in a file (user.csv, item.csv and context.csv).
        :return: The number of IDs in a file.
        """        
        return self.df.shape[0]
    
    def get_number_possible_values_by_attribute(self):
        """
        Gets the number of possible values by attribute in a file (user.csv, item.csv and context.csv).
        :return: The number of possible values by attribute in a file.
        """
        # Get the number of possible values by column:
        number_possible_values_serie = self.df.apply(lambda x: len(x.value_counts()))        
        # Convert the Series to a DataFrame and reset the index:
        number_possible_values_df = number_possible_values_serie.to_frame().reset_index(drop=True)
        df = number_possible_values_df.T.reset_index(drop=True)        
        # Rename the columns:
        df.columns = number_possible_values_serie.index.tolist()  
        # Drop the first column (user_id, item_id or context_id) by index:
        df = df.drop(df.columns[0], axis=1)
        # Round all values to 2 decimal places:
        df = df.round(2) 
        return df

    def get_avg_possible_values_by_attribute(self):
        """
        Gets the average of possible values by attribute in a file (user.csv, item.csv and context.csv).
        :return: The average of possible values by attribute in a file.
        """
        # replace non-numeric values with NaN
        df = self.df.apply(pd.to_numeric, errors='coerce')
        # calculate the average of each numeric column
        avg_by_column_serie = df.mean()
        # check for columns containing only non-numeric values and set the average to NaN
        for col in df.columns:
            if df[col].isna().all():
                avg_by_column_serie[col] = np.nan
        # Convert the Series to a DataFrame and reset the index:
        avg_possible_values_df = avg_by_column_serie.to_frame().reset_index(drop=True)
        df = avg_possible_values_df.T.reset_index(drop=True)        
        # Rename the columns:
        df.columns = avg_by_column_serie.index.tolist()   
        # Drop the first column (user_id, item_id or context_id) by index:
        df = df.drop(df.columns[0], axis=1)    
        # Round all values to 2 decimal places:
        df = df.round(2) 
        return df
    
    def get_sd_possible_values_by_attribute(self):
        """
        Gets the standard deviation of possible values by attribute in a file (user.csv, item.csv and context.csv).
        :return: The standard deviation of possible values by attribute in a file.
        """
        # replace non-numeric values with NaN
        df_aux = self.df.apply(pd.to_numeric, errors='coerce')
        # calculate standard deviation by column
        std_by_column_serie = df_aux.std() # self.df.std()        
        # check for columns containing only non-numeric values and set the average to NaN
        for col in df_aux.columns:
            if df_aux[col].isna().all():
                std_by_column_serie[col] = np.nan        
        # Convert the Series to a DataFrame and reset the index:
        sd_possible_values_df = std_by_column_serie.to_frame().reset_index(drop=True)
        df = sd_possible_values_df.T.reset_index(drop=True)        
        # Rename the columns:
        df.columns = std_by_column_serie.index.tolist()
        # Drop the first column (user_id, item_id or context_id) by index:
        df = df.drop(df.columns[0], axis=1)
        # Round all values to 2 decimal places:
        df = df.round(2) 
        return df
    
    def get_frequency_possible_values_by_attribute(self):
        # sourcery skip: dict-comprehension, inline-immediately-returned-variable
        """
        Gets the frequency of possible values by attribute in a file (user.csv, item.csv and context.csv).
        :return: The frequency of possible values by attribute in a file.
        """
        # calculate frequency by column
        freq_by_column_dict = {}
        for col in self.df.columns:
            freq_by_column_dict[col] = self.df[col].value_counts()
        return freq_by_column_dict
    
    def count_missing_values(self, replace_values=None):
        """
        Count missing values in the dataframe.
        :param dataframe: The dataframe to be analyzed.
        :param replace_values: A dictionary with the values to be replaced by NaN.
        :return: A dataframe with the number of missing values per attribute.
        """
        if replace_values is None:
            replace_values = {}
        for k,v in replace_values.items():
            self.df.replace(k, np.nan, inplace=True)
        missing_values = self.df.isnull().sum()
        missing_values = pd.DataFrame(missing_values, columns=["Count"])
        missing_values.reset_index(inplace=True)
        missing_values.rename(columns={"index": "Attribute name"}, inplace=True)
        return missing_values
    
    def column_attributes_count(self, column):
        """
        Count each attribute of a selected column.
        :param dataframe: The dataframe to be analyzed.
        :param column: The selected column.
        :return: A dataframe with the attribute and the number of occurrences.
        """        
        if self.df[column].dtype == 'datetime64[ns]':
            data = self.df.groupby(pd.Grouper(key=column, freq='M')).size().reset_index(name='count')
            data[column] = data[column].dt.strftime('%B %Y')  # Format dates to show month and year
        else:
            data = self.df.groupby(column).size().reset_index(name='count') # Group the data by the selected column and count the occurrences of each attribute            
        return data
    
    def statistics_by_user(self, df, selected_user, word):
        """
        Computes the statistics of items per user.
        :param data: The dataset to be analyzed.
        :param selected_user: The selected user.
        :param word: The word to be used in the statistics.
        :return: A dictionary with the statistics of items per user.
        """
        # Protect against ZeroDivisionError: division by zero
        if len(df) == 0:
            return {
                f"Average of {word} by user": 0,
                f"Variance of {word} by user": 0,
                f"Standard deviation of {word} by user": 0,
                f"Number of {word} not repeated by user": 0,
                f"Percent of {word} not repeated by user": 0,
                f"Number of {word} repeated by user": 0,
                f"Percent of {word} repeated by user": 0,
            }
        filtered_data = df[df['user_id'] == selected_user] #Filter the ratings dataset by user
        num_ratings = len(filtered_data)
        # Protect against ZeroDivisionError: division by zero
        if num_ratings == 0:
            return {
                f"Average of {word} by user": 0,
                f"Variance of {word} by user": 0,
                f"Standard deviation of {word} by user": 0,
                f"Number of {word} not repeated by user": 0,
                f"Percent of {word} not repeated by user": 0,
                f"Number of {word} repeated by user": 0,
                f"Percent of {word} repeated by user": 0,
            }
        num_items = filtered_data['item_id'].nunique()
        avg_items_by_user = df.groupby('user_id')['item_id'].nunique().mean()
        var_items_by_user = df.groupby('user_id')['item_id'].nunique().var()
        std_items_by_user = df.groupby('user_id')['item_id'].nunique().std()
        repeated_items_by_user = num_ratings - num_items
        non_repeated_items_by_user = num_items
        percent_repeated_items_by_user = repeated_items_by_user / num_ratings * 100
        percent_non_repeated_items_by_user = non_repeated_items_by_user / num_ratings * 100
        return {
            f"Average of {word} by user": avg_items_by_user,
            f"Variance of {word} by user": var_items_by_user,
            f"Standard deviation of {word} by user": std_items_by_user,
            f"Number of {word} not repeated by user": non_repeated_items_by_user,
            f"Percent of {word} not repeated by user": percent_non_repeated_items_by_user,
            f"Number of {word} repeated by user": repeated_items_by_user,
            f"Percent of {word} repeated by user": percent_repeated_items_by_user,
        }

    def statistics_by_attribute(self):
        """
        Calculate average and standard devuation per attribute and frequency and percentage of each attribute value.
        :param dataframe: The dataframe to be analyzed.
        :return: A list with the statistics of each attribute.
        """
        statistics = []
        for column in self.df.columns:
            if (self.df[column].dtype in ['int64', 'float64']) and (column not in ['user_id', 'item_id', 'context_id']):
                frequency = self.df[column].value_counts().reset_index()
                frequency.columns = ['Value', 'Frequency']
                percentage = self.df[column].value_counts(normalize=True).reset_index()
                percentage.columns = ['Value', 'Percentage']
                percentage['Percentage'] = percentage['Percentage'].map('{:,.2%}'.format) # Show the Percentage column as 4.35% instead of 0.0435
                statistics.append([column, round(self.df[column].mean(), 2), round(self.df[column].std(), 2), frequency, percentage])
        return statistics
    

# # user_df:
# user_path = 'resources/data_schema/user.csv' # 'resources/dataset_sts/user.csv'
# user_df = pd.read_csv(user_path, encoding='utf-8', index_col=False, sep=',')

# # item_df:
# item_path = 'resources/dataset_sts/item.csv'
# item_df = pd.read_csv(item_path, encoding='utf-8', index_col=False, sep=';')

# # context_df:
# context_path = 'resources/dataset_sts/context.csv'
# context_df = pd.read_csv(context_path, encoding='utf-8', index_col=False, sep=';')

# extract = ExtractStatisticsUIC(context_df)
# print(extract.get_number_id())
# print(extract.get_number_possible_values_by_attribute())
# print(extract.get_avg_possible_values_by_attribute())
# print(extract.get_sd_possible_values_by_attribute())
# print(extract.get_frequency_possible_values_by_attribute())
