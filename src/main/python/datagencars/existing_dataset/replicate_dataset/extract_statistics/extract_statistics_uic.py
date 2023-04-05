import pandas as pd
import numpy as np


class ExtractStatisticsUIC:

    def __init__(self, uic_df):
        self.uic_df = uic_df

    def get_number_id(self):
        """
        Gets the number of IDs (user_id, item_id and context_id) in a file (user.csv, item.csv and context.csv).
        :return: The number of IDs in a file.
        """        
        return self.uic_df.shape[0]
    
    def get_number_possible_values_by_attribute(self):
        """
        Gets the number of possible values by attribute in a file (user.csv, item.csv and context.csv).
        :return: The number of possible values by attribute in a file.
        """
        # Get the number of possible values by column:
        number_possible_values_serie = self.uic_df.apply(lambda x: len(x.value_counts()))        
        # Convert the Series to a DataFrame and reset the index:
        number_possible_values_df = number_possible_values_serie.to_frame().reset_index(drop=True)
        df = number_possible_values_df.T.reset_index(drop=True)        
        # Rename the columns:
        df.columns = number_possible_values_serie.index.tolist()        
        return df

    def get_avg_possible_values_by_attribute(self):
        """
        Gets the average of possible values by attribute in a file (user.csv, item.csv and context.csv).
        :return: The average of possible values by attribute in a file.
        """
        # replace non-numeric values with NaN
        df = self.uic_df.apply(pd.to_numeric, errors='coerce')
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
        return df
    
    def get_sd_possible_values_by_attribute(self):
        """
        Gets the standard deviation of possible values by attribute in a file (user.csv, item.csv and context.csv).
        :return: The standard deviation of possible values by attribute in a file.
        """
        # replace non-numeric values with NaN
        df = self.uic_df.apply(pd.to_numeric, errors='coerce')
        # calculate standard deviation by column
        std_by_column_serie = self.uic_df.std()        
        # check for columns containing only non-numeric values and set the average to NaN
        for col in df.columns:
            if df[col].isna().all():
                std_by_column_serie[col] = np.nan        
        # Convert the Series to a DataFrame and reset the index:
        sd_possible_values_df = std_by_column_serie.to_frame().reset_index(drop=True)
        df = sd_possible_values_df.T.reset_index(drop=True)        
        # Rename the columns:
        df.columns = std_by_column_serie.index.tolist()
        return df
    
    def get_frequency_possible_values_by_attribute(self):
        # sourcery skip: dict-comprehension, inline-immediately-returned-variable
        """
        Gets the frequency of possible values by attribute in a file (user.csv, item.csv and context.csv).
        :return: The frequency of possible values by attribute in a file.
        """
        # calculate frequency by column
        freq_by_column_dict = {}
        for col in self.uic_df.columns:
            freq_by_column_dict[col] = self.uic_df[col].value_counts()
        return freq_by_column_dict
    
    ########################## PENDING TO REVIEW ##########################
    def list_attributes_and_ranges(self, dataframe):
        # sourcery skip: low-code-quality, remove-redundant-pass, use-contextlib-suppress
        """
        List attributes, data types, and value ranges of the dataframe.
        :param dataframe: The dataframe to be analyzed.
        :return: A list of attributes, data types, and value ranges.
        """
        table = []
        for column in dataframe.columns:
            if dataframe[column].dtype in ['int64', 'float64']:
                table.append([column, dataframe[column].dtype, f"{dataframe[column].min()} - {dataframe[column].max()}"])
            elif dataframe[column].dtype == 'object':
                try:
                    dtype = dataframe[column].dtype
                    datetime_obj = None
                    date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%m-%d-%Y", "%Y%m%d", "%d-%m-%Y"]
                    time_formats = ["%H:%M:%S", "%H:%M"]
                    for date_format in date_formats:
                        try:
                            datetime_obj = pd.to_datetime(dataframe[column], format=date_format)
                            break
                        except ValueError:
                            for time_format in time_formats:
                                format_str = f"{date_format} {time_format}"
                                try:
                                    datetime_obj = pd.to_datetime(dataframe[column], format=format_str)
                                    break
                                except ValueError:
                                    pass
                            pass
                        if datetime_obj is not None:
                            break
                    if datetime_obj is None:
                        raise ValueError("Unsupported datetime format")
                    table.append([column, dtype, f"{datetime_obj.min().strftime('%Y-%m-%d')} - {datetime_obj.max().strftime('%Y-%m-%d')}"])
                except ValueError as e:
                    unique_values = dataframe[column].unique()
                    unique_values_str = ', '.join([str(value) for value in unique_values])
                    table.append([column, dataframe[column].dtype, unique_values_str])
            elif dataframe[column].dtype == 'datetime64[ns]':
                table.append([column, dataframe[column].dtype, f"{dataframe[column].min().strftime('%Y-%m-%d')} - {dataframe[column].max().strftime('%Y-%m-%d')}"])
            else:
                table.append([column, dataframe[column].dtype, "Unsupported data type"])
        return table

    def column_attributes_count(self, dataframe, column):
        """
        Count each attribute of a selected column.
        :param dataframe: The dataframe to be analyzed.
        :param column: The selected column.
        :return: A dataframe with the attribute and the number of occurrences.
        """
        if dataframe[column].dtype == 'datetime64[ns]':
            data = dataframe.groupby(pd.Grouper(key=column, freq='M')).size().reset_index(name='count')
            data[column] = data[column].dt.strftime('%B %Y')  # Format dates to show month and year
        else:
            data = dataframe.groupby(column).size().reset_index(name='count') # Group the data by the selected column and count the occurrences of each attribute            
        return data

    def count_missing_values(self, dataframe, replace_values=None):
        """
        Count missing values in the dataframe.
        :param dataframe: The dataframe to be analyzed.
        :param replace_values: A dictionary with the values to be replaced by NaN.
        :return: A dataframe with the number of missing values per attribute.
        """
        if replace_values is None:
            replace_values = {}
        for k,v in replace_values.items():
            dataframe.replace(k, np.nan, inplace=True)
        missing_values = dataframe.isnull().sum()
        missing_values = pd.DataFrame(missing_values, columns=["Count"])
        missing_values.reset_index(inplace=True)
        missing_values.rename(columns={"index": "Attribute name"}, inplace=True)
        return missing_values

    def general_statistics(self, data):
        """
        Extract general statistics from the dataset.
        :param data: The dataset to be analyzed.
        :return: A dictionary with the number of users, items, contexts, and ratings.
        """
        num_users = data['user_id'].nunique()
        num_items = data['item_id'].nunique()
        num_contexts = data['context_id'].nunique()
        num_ratings = data[['user_id', 'item_id', 'context_id']].nunique().sum()
        return {
            "Number of userID": num_users,
            "Number of itemID": num_items,
            "Number of contextID": num_contexts,
            "Number of ratings": num_ratings
        }

    def statistics_by_user(self, data, selected_user, word):
        """
        Computes the statistics of items per user.
        :param data: The dataset to be analyzed.
        :param selected_user: The selected user.
        :param word: The word to be used in the statistics.
        :return: A dictionary with the statistics of items per user.
        """
        # Protect against ZeroDivisionError: division by zero
        if len(data) == 0:
            return {
                f"Average of {word} by user": 0,
                f"Variance of {word} by user": 0,
                f"Standard deviation of {word} by user": 0,
                f"Number of {word} not repeated by user": 0,
                f"Percent of {word} not repeated by user": 0,
                f"Number of {word} repeated by user": 0,
                f"Percent of {word} repeated by user": 0,
            }
        filtered_data = data[data['user_id'] == selected_user] #Filter the ratings dataset by user
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
        avg_items_by_user = data.groupby('user_id')['item_id'].nunique().mean()
        var_items_by_user = data.groupby('user_id')['item_id'].nunique().var()
        std_items_by_user = data.groupby('user_id')['item_id'].nunique().std()
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

    def statistics_by_attribute(self, dataframe):
        """
        Calculate average and standard devuation per attribute and frequency and percentage of each attribute value.
        :param dataframe: The dataframe to be analyzed.
        :return: A list with the statistics of each attribute.
        """
        statistics = []
        for column in dataframe.columns:
            if (dataframe[column].dtype in ['int64', 'float64']) and (column not in ['user_id', 'item_id', 'context_id']):
                frequency = dataframe[column].value_counts().reset_index()
                frequency.columns = ['Value', 'Frequency']
                percentage = dataframe[column].value_counts(normalize=True).reset_index()
                percentage.columns = ['Value', 'Percentage']
                percentage['Percentage'] = percentage['Percentage'].map('{:,.2%}'.format) # Show the Percentage column as 4.35% instead of 0.0435
                statistics.append([column, round(dataframe[column].mean(), 2), round(dataframe[column].std(), 2), frequency, percentage])
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

# extract = ExtractStatisticsUIC(uic_df=context_df)
# print(extract.get_number_id())
# print(extract.get_number_possible_values_by_attribute())
# print(extract.get_avg_possible_values_by_attribute())
# print(extract.get_sd_possible_values_by_attribute())
# print(extract.get_frequency_possible_values_by_attribute())

