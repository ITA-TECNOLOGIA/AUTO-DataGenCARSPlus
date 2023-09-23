from abc import ABC
import re
import pandas as pd
import json


class ExtractStatistics(ABC):

    def __init__(self, df):
        self.df = df

    def try_loads(self, s):
        try:
            s = s.replace("'", '"')
            return json.loads(s)
        except:
            return None
    
    # Function to get the type of non-missing values in a column
    def get_column_value_types(self, column):
        non_missing_values = column.dropna()
        value_types = non_missing_values.apply(type)
        return value_types

    def get_attributes_and_ranges(self):
        # sourcery skip: low-code-quality, remove-redundant-pass, use-contextlib-suppress
        """
        List attributes, data types, and value ranges of the dataframe.
        :param dataframe: The dataframe to be analyzed.
        :return: A list of attributes, data types, and value ranges.
        """
        table = []
        df = self.df.copy()
        # Iterate through DataFrame columns and get value types
        for column_name, column in df.items():
            attribute_value_list = column.dropna()
            value_type_list = list(set(attribute_value_list.apply(type)))                   
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
        datetime_obj = None
        date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%m-%d-%Y", "%Y%m%d", "%d-%m-%Y"]
        time_formats = ["%H:%M:%S", "%H:%M"]
        for date_format in date_formats:            
            try:
                datetime_obj = pd.to_datetime(date_list, format=date_format)
                break
            except ValueError:
                for time_format in time_formats:
                    format_str = f"{date_format} {time_format}"
                    try:
                        datetime_obj = pd.to_datetime(date_list, format=format_str)
                        break
                    except ValueError:
                        pass
                pass
            if datetime_obj is not None:
                break
        if datetime_obj is None:
            raise ValueError("Unsupported datetime format")
        return datetime_obj.min().strftime('%Y-%m-%d'), datetime_obj.max().strftime('%Y-%m-%d')

# df_path = 'resources/rating.csv'
# df = pd.read_csv(df_path, encoding='utf-8', index_col=False, sep=',')        
# extract = ExtractStatistics(df)
# table = extract.get_attributes_and_ranges()
# print(table)

# # List of date strings
# date_strings = ['17-1-1961', '6-12-1964', '12-9-1967', '20-8-1967', '6-6-1994', '25-1-1984', '26-3-1963', '19-7-1966', '20-8-1975', '28-1-1969', '23-7-1963', '20-6-1999', '15-12-1979', '10-10-1975', '23-10-1982', '3-3-1978', '11-1-1963', '20-9-1991', '19-8-1967', '6-2-1985', '6-10-1994', '18-11-1973', '25-2-1983', '24-12-1984', '8-5-1991', '25-6-1980', '27-5-1984', '28-2-1959', '13-2-1974', '14-3-1988', '6-12-1970', '9-1-1964', '9-3-1992', '28-2-1976', '4-3-1966', '21-11-1968', '18-10-1996', '4-12-1973', '23-5-1988', '6-8-1999', '28-1-1995', '23-2-1988', '17-3-1990', '5-11-1964', '10-5-1994', '3-1-1987', '15-12-1964', '31-8-1965', '12-8-1975', '23-9-1979', '18-1-1979', '5-12-1984', '4-2-1961', '3-1-1981', '5-12-1965', '15-8-1967', '28-3-1996', '15-7-1974', '18-4-1978'] # Your list of date strings
# print(extract.get_date_ranges(date_list=date_strings))

# # Regex pattern to match various date formats
# # date_pattern = r"\d{4}(?:[-/]\d{2}[-/]\d{2}|\d{2}[/]\d{2}[/]\d{4}|\d{2}[-]\d{2}[-]\d{4}|\d{8})"
# date_pattern = r"(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|\d{2}/\d{2}/\d{4}|\d{4}/\d{2}/\d{2}|\d{2}-\d{2}-\d{4}|\d{8}|\d{2}-\d{2}-\d{4})"

# # Test the regex pattern with sample strings
# sample_strings = ["2023-09-23", "23/09/2023", "09/23/2023", "2023/09/23", "09-23-2023", "20230923", "23-09-2023", "Invalid Date"]
# # '23/09/2023', '09-23-2023', '20230923', '23-09-2023'
# for sample_string in sample_strings:
#     if re.match(date_pattern, sample_string):
#         print(f"'{sample_string}' matches the date pattern.")
#     else:
#         print(f"'{sample_string}' does not match the date pattern.")



