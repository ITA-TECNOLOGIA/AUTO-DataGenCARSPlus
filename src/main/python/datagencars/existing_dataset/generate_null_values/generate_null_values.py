import random

import streamlit as st


class GenerateNullValues:

    def __init__(self):
        pass

    def regenerate_file(self, file_df, percentage_null):
        """
        Generating null values in the item or context file: "item.csv" or "context.csv".
        :param: The item or context file.
        :return: The item or context file with generated null values.  
        """
        if percentage_null > 0:
            # Create a progress bar
            progress_bar = st.progress(0.0)
            number_item = len(file_df)
            number_attributes = file_df.shape[1] - 1

            null_values = int((number_attributes * number_item * percentage_null) / 100)
            # If there are null values in the file, take this into account as part of the percentage of null values to be generated:
            if file_df.isnull().any().any():
                current_null_count = file_df.isnull().sum().sum()
                null_values = null_values - current_null_count
            
            # Generate random positions to be null
            for i in range(1, null_values+1):
                # Generate column to remove
                random_column = random.randint(1, number_attributes)
                # Generate row to remove
                random_row = random.randint(0, number_item-1)
                #print('Removing item column {} and row {}'.format(random_column, random_row))
                # Update the progress bar with each iteration                            
                progress_bar.progress(text=f'Generating {i} null values from {null_values}', value=(i) / null_values)
                # Remove value
                if file_df.iloc[random_row, random_column] != None:
                    file_df.iloc[random_row, random_column] = None
                    i = i + 1                          
        return file_df.copy()    
  