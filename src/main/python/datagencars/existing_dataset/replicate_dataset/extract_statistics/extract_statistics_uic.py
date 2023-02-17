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
                unique_values = dataframe[column].dropna().unique()
                unique_values_str = ', '.join([str(value) for value in unique_values])
                table.append([column, dataframe[column].dtype, unique_values_str])
        else:
            table.append([column, dataframe[column].dtype, "unsupported data type"])
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

def replace_count_missing_values(dataframe, replace_values={}):
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
