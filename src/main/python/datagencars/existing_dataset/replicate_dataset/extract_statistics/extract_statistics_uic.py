import pandas as pd
import numpy as np

def list_attributes_and_ranges(dataframe):
    """
    List attributes, data types, and value ranges of the dataframe.
    """
    table = []
    for column in dataframe.columns:
        if dataframe[column].dtype in ['int64', 'float64']:
            table.append([column, dataframe[column].dtype, f"{dataframe[column].min()} - {dataframe[column].max()}"])
        elif dataframe[column].dtype == 'object':
            try:
                dataframe[column] = pd.to_datetime(dataframe[column], format='%d/%m/%Y')
                table.append([column, dataframe[column].dtype, f"{dataframe[column].min().strftime('%Y-%m-%d')} - {dataframe[column].max().strftime('%Y-%m-%d')}"])
            except ValueError:
                unique_values = dataframe[column].unique() #.dropna().unique()
                unique_values_str = ', '.join([str(value) for value in unique_values])
                table.append([column, dataframe[column].dtype, unique_values_str])
        else:
            table.append([column, dataframe[column].dtype, "Unsupported data type"])
    return table

def column_attributes_count(dataframe, column):
    """
    Count each attribute of a selected column.
    """
    if dataframe[column].dtype == 'datetime64[ns]':
        data = dataframe.groupby(pd.Grouper(key=column, freq='M')).size().reset_index(name='count')
        data[column] = data[column].dt.strftime('%B %Y')  # Format dates to show month and year
    else:
        data = dataframe.groupby(column).size().reset_index(name='count') # Group the data by the selected column and count the occurrences of each attribute            
    return data

def count_missing_values(dataframe, replace_values={}):
    """
    Count missing values in the dataframe.
    """
    for k,v in replace_values.items():
        dataframe.replace(k, np.nan, inplace=True)
    missing_values = dataframe.isnull().sum()
    missing_values = pd.DataFrame(missing_values, columns=["Count"])
    missing_values.reset_index(inplace=True)
    missing_values.rename(columns={"index": "Attribute name"}, inplace=True)
    return missing_values

def general_statistics(data):
    """
    Extract general statistics from the dataset.
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

def statistics_by_user(data, selected_user, word):
    """
    Computes the statistics of items per user.
    """
    filtered_data = data[data['user_id'] == selected_user] #Filter the ratings dataset by user
    num_ratings = len(filtered_data)
    num_items = filtered_data['item_id'].nunique()
    items_per_rating = num_items / num_ratings
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

def statistics_by_attribute(dataframe):
    """
    Calculate average and standard devuation per attribute and frequency and percentage of each attribute value. 
    """
    statistics = []
    for column in dataframe.columns:
        if dataframe[column].dtype in ['int64', 'float64']:
            if column not in ['user_id', 'item_id', 'context_id']:
                frequency = dataframe[column].value_counts().reset_index()
                frequency.columns = ['Value', 'Frequency']

                # # Convert from dataframe to string (e.g. Value 96 --> 4 times)
                # frequency['index'] = frequency['index'].astype(str) + ' --> ' + frequency[column].astype(str) + ' times'
                # # Convert from dataframe to list
                # frequency = frequency['index'].tolist()
                # # Convert from list to string with each of the elements of the list separated by a new line
                # frequency = "\n".join(frequency)
                # print(frequency)

                percentage = dataframe[column].value_counts(normalize=True).reset_index()
                percentage.columns = ['Value', 'Percentage']
                # Show the Percentage column as 4.35% instead of 0.0435
                percentage['Percentage'] = percentage['Percentage'].map('{:,.2%}'.format)

                statistics.append([column, round(dataframe[column].mean(), 2), round(dataframe[column].std(), 2), frequency, percentage])
    return statistics
