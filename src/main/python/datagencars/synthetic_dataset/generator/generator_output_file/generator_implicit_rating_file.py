import pandas as pd
from datetime import datetime

from datagencars.synthetic_dataset.generator.access_schema.access_generation_config import AccessGenerationConfig
from datagencars.synthetic_dataset.generator.generator_output_file.generator_file import GeneratorFile
from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema


class GeneratorImplicitRatingFile(GeneratorFile):
    '''
    Generates user ratings based on user behaviors and item properties.
    @author Marcos Caballero Yus
    '''

    def __init__(self, generation_config, item_df, behavior_df, context_df=None):
        """
        Initializes the GeneratorRatingImplicitFile with required DataFrames and configuration.
        :param generation_config: Configuration string for generating the rating file.
        :param item_df: DataFrame containing the item information.
        :param behavior_df: DataFrame containing the user behavior information.
        :param context_df: (Optional) DataFrame containing the context information.
        """
        self.access_generation_config = AccessGenerationConfig(file_str=generation_config)
        self.min_rating_value = self.access_generation_config.get_minimum_value_rating()
        self.max_rating_value = self.access_generation_config.get_maximum_value_rating()
        self.rules = self.access_generation_config.get_all_implicit_rating_rules()
        self.behavior_df = behavior_df
        self.item_df = item_df

        if context_df is None:
            context_df = pd.DataFrame()
        if not context_df.empty:
            # Context file (optional): context.csv
            self.context_df = context_df

    def datetime_to_timestamp(self, datetime_value):
        """
        Converts a datetime object to a timestamp.
        :param datetime_value: A datetime object.
        :return: A float representing the timestamp.
        """
        return datetime_value.timestamp()

    def string_to_datetime(self, datetime_string):
        """
        Converts a datetime string to a datetime object.
        :param datetime_string: A datetime string.
        :return: A datetime object.
        """
        return datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')
    
    def get_rating_and_timestamp(self, row, filtered_behavior):
        """
        Calculates rating and timestamp for the current user behavior row.
        :param row: A row from the filtered_behavior DataFrame.
        :param filtered_behavior: The filtered_behavior DataFrame with 'Update' object actions removed.
        :return: A tuple containing the rating and timestamp.
        """
        user_id = row['user_id']
        item_id = row['item_id']
        object_action = row['object_action']
        object_type = self.item_df.loc[self.item_df['item_id'] == item_id, 'object_type'].values[0]

        for rule in self.rules:
            if 'action' in rule and object_action == rule['action']:
                return rule['rating'], row['timestamp']
            elif ('object_type' in rule and object_type == rule['object_type'] and
                    'action_open' in rule and object_action == rule['action_open']):
                open_timestamp = row['timestamp']
                try:
                    close_timestamp = filtered_behavior.loc[
                        (filtered_behavior['user_id'] == user_id) &
                        (filtered_behavior['item_id'] == item_id) &
                        (filtered_behavior['object_action'] == rule['action_close']), 'timestamp'].values[0]
                except:
                    return 0, open_timestamp

                if rule['min_time'] < (close_timestamp - open_timestamp) < rule['max_time']:
                    return rule['rating_good'], open_timestamp
                else:
                    return rule['rating_bad'], open_timestamp

        return None, None
    
    def preprocess_behavior_df(self, with_context=False):
        # Filter behavior_df to remove 'Update' object_actions
        filtered_behavior = self.behavior_df.copy()[self.behavior_df['object_action'] != 'Update']

        # Convert non-numeric values in 'item_id' column to NaNs
        filtered_behavior['item_id'] = pd.to_numeric(filtered_behavior['item_id'], errors='coerce')
        # Drop rows with NaNs in the 'item_id' column
        filtered_behavior = filtered_behavior.dropna(subset=['item_id'])
        # Convert 'item_id' column data type to int
        filtered_behavior['item_id'] = filtered_behavior['item_id'].astype(int)
        # Convert 'timestamp' column to datetime objects
        filtered_behavior['timestamp'] = filtered_behavior['timestamp'].apply(lambda x: self.string_to_datetime(x))
        # Convert datetime objects to timestamps
        filtered_behavior['timestamp'] = filtered_behavior['timestamp'].apply(lambda x: self.datetime_to_timestamp(x))

        if with_context:
            # Filter behavior_df to get rows with 'Update' object_actions and 'Position' user_position
            update_position_behavior = self.behavior_df.copy()[(self.behavior_df['object_action'] == 'Update') &
                                                               (self.behavior_df['item_id'] == 'Position')]
            # Convert 'context_id' column data type to int
            update_position_behavior['context_id'] = update_position_behavior['context_id'].astype(int)
            # Create a dictionary with user_id as the key and context_id as the value
            user_context_dict = update_position_behavior.set_index('user_id')['context_id'].to_dict()
            # Update context_id in filtered_behavior based on the user_context_dict
            filtered_behavior['context_id'] = filtered_behavior['user_id'].map(user_context_dict)

        return filtered_behavior

    def generate_file(self, with_context=False):
        '''
        Generates the rating file based on the provided user behaviors and item properties.

        :param with_context: True if the file to be generated will be contextual and False otherwise.
        :return: A DataFrame with rating information (user_id, item_id, context_id <optional>, rating, timestamp).
        '''
        filtered_behavior = self.preprocess_behavior_df(with_context=True)

        # Create ratings DataFrame
        ratings = filtered_behavior.copy()
        ratings['rating'], ratings['initial_timestamp'] = zip(*ratings.apply(lambda row: self.get_rating_and_timestamp(row, filtered_behavior), axis=1))

        # Drop rows with missing ratings and rename the initial_timestamp column to timestamp
        ratings = ratings.dropna(subset=['rating', 'initial_timestamp'])

        # Drop the original 'timestamp' column and rename the 'initial_timestamp' column to 'timestamp'
        ratings = ratings.drop(columns=['timestamp'])
        ratings = ratings.rename(columns={'initial_timestamp': 'timestamp'})

        # Drop object_action, user_position, and behavior_id columns
        ratings = ratings.drop(columns=['object_action', 'user_position', 'behavior_id'])

        ratings['user_id'] = ratings['user_id'].astype(int)
        ratings['item_id'] = ratings['item_id'].astype(int)
        ratings['rating'] = ratings['rating'].astype(int)
        ratings['timestamp'] = pd.to_datetime(ratings['timestamp'], unit='s')

        return ratings.copy()