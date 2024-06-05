from abc import ABC, abstractmethod
import random
import pandas as pd

from datagencars.synthetic_dataset.generator.access_schema.access_generation_config import AccessGenerationConfig
from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema


class GeneratorFile(ABC):

    def __init__(self, generation_config, schema):
        self.access_generation_config = None
        if generation_config != None:
            # Access generation config.
            self.access_generation_config = AccessGenerationConfig(file_str=generation_config)
        # Schema access.
        self.schema_access = AccessSchema(file_str=schema)
        # Getting attribute names:
        attribute_name_list = self.schema_access.get_attribute_name_list()
        self.file_df = pd.DataFrame(columns=attribute_name_list)

    @abstractmethod
    def generate_file(self):
        pass
    
    def generate_null_value_global(self, file_df, percentage_null_value_global):
        """
        Generate null values in the complete dataframe based on the specified percentage.
        :param file_df: A dataframe containing user, item or context data.
        :param percentage_null_value_global: The global percentage of null user values to randomly generate in the complete dataset.
        :return: A copy of the user complete dataframe with generated null values.
        """    
        # Calculate the total number of rows in the dataframe
        total_rows = file_df.shape[0]
        number_attributes = self.schema_access.get_number_attributes()
        null_values = int((number_attributes * total_rows * percentage_null_value_global) / 100)
        # Generate random positions to be null.
        for i in range(1, null_values+1):
            # Generate column to remove.
            random_column = random.randint(1, number_attributes)
            # Generate row to remove.
            random_row = random.randint(0, total_rows-1)            
            # Remove value. 
            if file_df.iloc[random_row, random_column] != '':
                file_df.iloc[random_row, random_column] = ''
                i = i + 1     
        return file_df.copy()
    
    def generate_null_value_attribute(self, file_df, percentage_null_value_attribute_list):
        """
        Generate null values in the dataframe by attribute column based on the specified percentage.
        Each column will have values replaced with null values randomly based on the given percentage.
        
        :param file_df: A dataframe containing user, item or context data.
        :param percentage_null_value_column: The percentage of null values to randomly generate by attribute column.
        :return: A modified copy of the dataframe with generated null values.
        """
        # Calculate the total number of rows in the dataframe
        total_rows = file_df.shape[0]        
        # Iterate over each column in the dataframe        
        for index_column, column_name in enumerate(file_df.columns[1:], start=0):
            percentage_null_value_column = percentage_null_value_attribute_list[index_column]
            # Calculate the number of null values to generate for the column
            null_values_count = int((total_rows * percentage_null_value_column) / 100)
            # Generate random indices for the rows that will have null values
            index_row = random.sample(range(total_rows), null_values_count)
            if str(file_df.loc[index_row, column_name]) != '':
                # Assign '' to these indices in the column
                file_df.loc[index_row, column_name] = ''  # Using '' to represent null values
        # Return a copy of the dataframe with the modifications
        return file_df.copy()
