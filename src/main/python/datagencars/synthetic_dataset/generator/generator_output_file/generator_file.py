from abc import ABC, abstractmethod
import pandas as pd
import random

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

    def generate_null_values(self, complete_file):
        """
        Generate null values in a dataframe based on the specified percentage.
        :param complete_file: A dataframe containing user, item or context data.
        :return: A copy of the dataframe with generated null values.
        """
        percentage_null = self.access_generation_config.get_number_user_null()
        if percentage_null > 0:
            number_user = self.access_generation_config.get_number_user()
            number_attributes = self.schema_access.get_number_attributes() - 1 # user_profile_id cannot be null
            null_values = int((number_attributes * number_user * percentage_null) / 100)
            # Generate random positions to be null
            for i in range(1, null_values+1):
                # Generate column to remove
                random_column = random.randint(1, number_attributes)
                # Generate row to remove
                random_row = random.randint(0, number_user-1)            
                # Remove value
                if complete_file.iloc[random_row, random_column] != None:
                    complete_file.iloc[random_row, random_column] = None
                    i = i + 1            
        return complete_file.copy()
