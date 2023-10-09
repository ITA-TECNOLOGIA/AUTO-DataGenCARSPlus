import re
from abc import ABC

import pandas as pd


class ExtractStatistics(ABC):

    def __init__(self, df):
        self.df = df

    def get_attributes_and_ranges(self):        
        """
        List attributes, data types, and value ranges of the dataframe.
        :param dataframe: The dataframe to be analyzed.
        :return: A list of attributes, data types, and value ranges.
        """
        table = []
        df = self.df.copy()
        # Iterate through DataFrame columns and get value types
        for column_name, column in df.items():
            print(column_name)
            attribute_value_list = column.dropna()
            value_type_list = list(set(attribute_value_list.apply(type)))                   
            print(attribute_value_list[0])
            if len(value_type_list) == 1:  
                value_type = value_type_list[0]               
                # Type: int or float
                if value_type == int:
                    table.append([column_name, "int", f"[{min(attribute_value_list)} - {max(attribute_value_list)}]"])
                # Type: int or float
                elif value_type == float:
                    table.append([column_name, "float", f"[{min(attribute_value_list)} - {max(attribute_value_list)}]"])
                # Type: bool
                elif value_type == bool:
                    table.append([column_name, "bool", "[True, False]"])
                # Type: str
                elif value_type == str:                                                                         
                    # Type: object<date>
                    temp_list = attribute_value_list.tolist()
                    if bool(re.search(r'^[0-9/-:\s]', temp_list[0])):
                        min_date, max_date = self.get_date_ranges(date_list=list(attribute_value_list))
                        table.append([column_name, 'object', f"[{min_date} - {max_date}]"])
                    else:                                                                     
                        # Only str:
                        table.append([column_name, "str", list(set(attribute_value_list))])
        return table        
    
    def get_date_ranges(self, date_list):
        """
        Get the minimum and maximum dates from a list of date strings.
        :param date_list: A list of date strings in a specific format.
        :return: The minimum and maximum dates in 'YYYY-MM-DD' format.
        """
        datetime_obj = None
        # List of date formats to try for parsing:
        date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%m-%d-%Y", "%Y%m%d", "%d-%m-%Y"]
        # List of time formats to try for parsing:
        time_formats = ["%H:%M:%S", "%H:%M"]
        # Iterate through the date formats to parse the input date_list:
        for date_format in date_formats:            
            try:
                datetime_obj = pd.to_datetime(date_list, format=date_format)
                break
            except ValueError:
                # If parsing fails, try different time formats within the same date format:
                for time_format in time_formats:
                    format_str = f"{date_format} {time_format}"
                    try:
                        datetime_obj = pd.to_datetime(date_list, format=format_str)
                        break
                    except ValueError:
                        pass
                pass
            # If datetime_obj is successfully parsed, break out of the loop:        
            if datetime_obj is not None:
                break
        # If no valid datetime object is obtained, raise a ValueError:
        if datetime_obj is None:
            # raise ValueError("Unsupported datetime format")
            return None
        else:
            return datetime_obj.min().strftime('%Y-%m-%d'), datetime_obj.max().strftime('%Y-%m-%d')
