from abc import ABC
import pandas as pd


class ExtractStatistics(ABC):

    def __init__(self, df):
        self.df = df

    def get_attributes_and_ranges(self): # list_attributes_and_ranges
        # sourcery skip: low-code-quality, remove-redundant-pass, use-contextlib-suppress
        """
        List attributes, data types, and value ranges of the dataframe.
        :param dataframe: The dataframe to be analyzed.
        :return: A list of attributes, data types, and value ranges.
        """        
        table = []
        for column in self.df.columns:
            if self.df[column].dtype in ['int64', 'float64']:
                table.append([column, self.df[column].dtype, f"{self.df[column].min()} - {self.df[column].max()}"])
            elif self.df[column].dtype == 'bool':
                table.append([column, self.df[column].dtype, "True, False"])
            elif self.df[column].dtype == 'object':
                try:
                    dtype = self.df[column].dtype
                    datetime_obj = None
                    date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%m-%d-%Y", "%Y%m%d", "%d-%m-%Y"]
                    time_formats = ["%H:%M:%S", "%H:%M"]
                    for date_format in date_formats:
                        try:
                            datetime_obj = pd.to_datetime(self.df[column], format=date_format)
                            break
                        except ValueError:
                            for time_format in time_formats:
                                format_str = f"{date_format} {time_format}"
                                try:
                                    datetime_obj = pd.to_datetime(self.df[column], format=format_str)
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
                    unique_values = self.df[column].unique()
                    unique_values_str = ', '.join([str(value) for value in unique_values])
                    table.append([column, self.df[column].dtype, unique_values_str])
            elif self.df[column].dtype == 'datetime64[ns]':
                table.append([column, self.df[column].dtype, f"{self.df[column].min().strftime('%Y-%m-%d')} - {self.df[column].max().strftime('%Y-%m-%d')}"])
            else:
                table.append([column, self.df[column].dtype, "Unsupported data type"])
        return table