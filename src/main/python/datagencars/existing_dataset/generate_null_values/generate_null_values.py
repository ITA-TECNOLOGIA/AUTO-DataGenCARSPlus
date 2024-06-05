import random
import pandas as pd
import streamlit as st
import numpy as np


class GenerateNullValues:

    def __init__(self):
        pass
    
    def generate_null_value_global(self, file_df, percentage_null):
        """
        Generate null values in the item or context file: "item.csv" or "context.csv".
        :param file_df: DataFrame containing the data.
        :param percentage_null: Percentage of total values that should be null.
        :return: DataFrame with generated null values.
        """
        if percentage_null <= 0:
            return file_df.copy()
        
        number_items = len(file_df)
        number_attributes = file_df.shape[1] - 1
        total_values = number_items * number_attributes
        existing_null_count = file_df.isnull().sum().sum()
        desired_null_count = int(total_values * (percentage_null / 100))
        
        additional_nulls_needed = desired_null_count - existing_null_count
        
        if additional_nulls_needed <= 0:
            st.warning(f'Since the item file already contains {existing_null_count/total_values * 100:.2f}% null values, no modifications have been made.')
            return file_df.copy()   
             
        progress_bar = st.progress(0.0)
        # Randomly assign null values to the DataFrame:
        current_nulls_generated = 0
        attempts = 0
        while current_nulls_generated < additional_nulls_needed and attempts < additional_nulls_needed * 10:
            random_row = random.randint(0, number_items - 1)
            random_column = random.randint(1, number_attributes)  # Assuming column index starts at 1 for data
            if pd.notna(file_df.iat[random_row, random_column]):
                file_df.iat[random_row, random_column] = np.nan
                current_nulls_generated += 1
                progress_percentage = current_nulls_generated / additional_nulls_needed
                progress_bar.progress(progress_percentage)
            attempts += 1
        if attempts == additional_nulls_needed * 10:
            st.warning('Not enough non-null entries to replace. Consider reducing the percentage of null values.')
        return file_df.copy()
    
    def generate_null_value_attribute(self, file_df, percentage_null_value_attribute_list):
        """
        Generate null values in the dataframe by attribute column based on the specified percentage.
        Each column will have values replaced with null values randomly based on the given percentage.
        Updates the progress bar and checks if the existing null values meet or exceed the desired count.

        :param file_df: A dataframe containing user, item or context data.
        :param percentage_null_value_attribute_list: The percentage of null values to randomly generate by attribute column.
        :return: A modified copy of the dataframe with generated null values.
        """        
        progress_bar = st.progress(0.0)
        total_columns = len(file_df.columns[1:])  # Exclude the first column assuming it's an identifier

        for index_column, column_name in enumerate(file_df.columns[1:], start=1):
            try:
                # Ensure the percentage value is treated as a float
                percentage_value = float(percentage_null_value_attribute_list[index_column - 1])
                number_items = len(file_df[column_name].tolist())
                null_values_count = int((number_items * percentage_value) / 100)
            except ValueError:
                st.error(f"Error: Non-numeric percentage value provided for column {column_name}. Please provide a numeric value.")
                continue  # Skip to the next column

            if null_values_count == 0:
                # Skip further processing for this column as no nulls are intended to be added
                progress_percentage = index_column / total_columns
                progress_bar.progress(progress_percentage)
                continue

            existing_nulls = file_df[column_name].isnull().sum()

            if existing_nulls >= null_values_count:
                st.warning(f'Column "{column_name}" already contains {existing_nulls}/{number_items} null values, which meets or exceeds the desired count of {null_values_count} ({percentage_value}%)/{number_items-existing_nulls} (not null values). No modifications made.')
                # Update progress bar after each column is processed
                progress_percentage = index_column / total_columns
                progress_bar.progress(progress_percentage)
                continue

            # Calculate additional nulls needed
            additional_nulls_needed = null_values_count - existing_nulls
            non_null_indices = list(file_df[file_df[column_name].notnull()].index)
            additional_nulls_needed = min(additional_nulls_needed, len(non_null_indices))

            if additional_nulls_needed > 0:
                index_row = random.sample(non_null_indices, additional_nulls_needed)
                file_df.loc[index_row, column_name] = np.nan  # Assign NaN to represent null values

            # Update progress bar after each column is processed
            progress_percentage = index_column / total_columns
            progress_bar.progress(progress_percentage)
        return file_df.copy()
    
    def display_null_statistics(self, file_df):
        """
        Display statistics about null values in the DataFrame, excluding the first column.
        
        This function calculates and displays the total number of null values in the DataFrame
        (excluding the first column), along with their percentage of the total dataset. It also
        calculates and displays the number of null values and their percentage for each column
        (excluding the first column).
        
        Parameters:
        - file_df (pd.DataFrame): The DataFrame for which null statistics are calculated.
        """

        # Exclude the first column from the analysis
        file_df_analysis = file_df.iloc[:, 1:]  # This slices out the first column

        # Calculate the total number of nulls and their percentage over the dataset excluding the first column
        total_nulls = file_df_analysis.isnull().sum().sum()
        total_entries = file_df_analysis.size
        percentage_total_nulls = (total_nulls / total_entries) * 100
        
        # Display global null statistics        
        st.markdown("""**Null value statistics (excluding the first column):**""")
        st.markdown(f"""Total null values: ```{total_nulls}```""")
        st.markdown(f"""Percentage of null values: ```{percentage_total_nulls:.2f}%```""")
        
        # Calculate nulls per column and their percentage
        nulls_per_column = file_df_analysis.isnull().sum()
        entries_per_column = len(file_df_analysis)
        percentage_per_column = (nulls_per_column / entries_per_column) * 100
        
        # Create a DataFrame to display per-column results
        column_stats = pd.DataFrame({
            'Attribute': file_df_analysis.columns,
            'Nulls': nulls_per_column.values,
            'Percentage of nulls (%)': percentage_per_column.values
        })
        
        # Display null statistics per column        
        st.markdown("""**Null value statistics by attribute (excluding the first column):**""")
        st.dataframe(column_stats.style.format("{:.2f}", subset='Percentage of nulls (%)'))
