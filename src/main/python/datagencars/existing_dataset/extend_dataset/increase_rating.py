import pandas as pd
import numpy as np
import random
from datagencars.existing_dataset.generate_rating import GenerateRating
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_user import AccessUser
from datagencars.synthetic_dataset.generator.access_schema.access_user_profile import AccessUserProfile

class IncreaseRating(GenerateRating):
    '''
    Replicate an existing dataset.

    Input:
        [U]  user.csv
        [I]  item.csv
        [C]  context.csv <optional>
        [R]  rating.csv

    Algorithm:
        Precondition: If the dataset is a single file, it is expected to be divided into user.csv, item.csv, context.csv <optional> and ratings.csv.
        1- extract_statistics (extract_statistics_rating, extract_statistics_uic):
        2- generate_user_profile:
        3- replicate_dataset:

    Ouput:
        [R]  rating.csv <replicated>        
    '''

    def __init__(self, rating_df, item_df, user_df, user_profile, context_df=None):
        super().__init__(rating_df, user_profile, item_df, context_df)
        # Access to the user profile: (not used)
        # access_user_profile = AccessUserProfile(user_profile)
        self.rating_df = rating_df
        self.item_df = item_df
        self.context_df = context_df
        self.user_id_list = user_df['user_id'].unique()
        # Access to the ratings.csv.
        self.access_user = AccessUser(user_df)

    def incremental_rating_by_user(self, user_ids, number_ratings, percentage_rating_variation=25, k=10):
        """
        Generate k items for a specific list of users.
        :param user_ids: A list of user IDs.
        :param number_ratings: The number of ratings to generate for each user.
        :param percentage_rating_variation: The percentage of rating variation.
        :param k: The k ratings to take in the past.
        :return: A dataset with k items for each user in the specified list.
        """
        # Initial DataFrame setup
        rating_df = pd.DataFrame(columns=['user_id', 'item_id', 'rating'])
        if 'context_id' in self.rating_df.columns:
            rating_df['context_id'] = None

        # Ensure user_ids is a list
        if not isinstance(user_ids, list):
            user_ids = [user_ids]

        for user_id in user_ids:
            # Fetching the list of items that this user has already rated:
            original_item_id_list = self.access_rating.get_item_id_list_from_user(user_id=user_id)
            all_item_id_list = self.item_df['item_id'].unique()
        
            # Excluding the items that the user has already rated:
            possible_item_id_list = list(set(all_item_id_list) - set(original_item_id_list))
        
            for _ in range(number_ratings):
                if not possible_item_id_list:  # Check if there are items left to rate
                    break
                
                item_id = random.choice(possible_item_id_list)
                
                if 'context_id' in rating_df.columns:
                    context_id_list = self.context_df['context_id'].unique()
                    context_id = random.choice(context_id_list)
                    rating = self.get_rating(user_id, item_id, context_id)
                else:
                    rating = self.get_rating(user_id, item_id)
                
                # The minimum value rating.
                min_rating_value = self.access_rating.get_min_rating()
                # The maximum value rating.
                max_rating_value = self.access_rating.get_max_rating()
                user_rating_list=self.access_rating.get_rating_list_from_user(user_id=user_id)   

                # Modifying the generated rating.
                modified_rating = self.modify_rating_by_user_expectations(rating, k, user_rating_list, min_rating_value, max_rating_value, percentage_rating_variation)

                # Adding a new row to rating_df:
                new_data = {'user_id': user_id, 'item_id': item_id, 'rating': modified_rating}
                if 'context_id' in rating_df.columns:
                    new_data['context_id'] = context_id
                rating_df = rating_df.append(new_data, ignore_index=True)

        # Sorting and resetting index
        sort_columns = ['user_id', 'item_id', 'rating']
        if 'context_id' in rating_df.columns:
            sort_columns.insert(2, 'context_id')
        rating_df = rating_df.sort_values(by=sort_columns)
        rating_df.reset_index(drop=True, inplace=True)
        
        return rating_df

    def incremental_rating_random(self, number_ratings, percentage_rating_variation=25, k=10):
        """
        Generate items for k random users.
        :param number_ratings: The number of random users.
        :param percentage_rating_variation: The percentage of rating variation.
        :param k: The k ratings to take in the past.
        :return: A dataset with items for the k random users.
        """
        rating_df = pd.DataFrame(columns=['user_id', 'item_id', 'rating'])
        if 'context_id' in self.rating_df.columns:
            rating_df['context_id'] = None
        
        if number_ratings <  len(self.user_id_list):
            number_ratings = len(self.user_id_list)

        random_users = random.choices(list(self.user_id_list), k=number_ratings)

        for user_id in random_users:
            # Following the same logic as in by_user method
            original_item_id_list = self.access_rating.get_item_id_list_from_user(user_id=user_id)
            all_item_id_list = self.item_df['item_id'].unique()
            possible_item_id_list = list(set(all_item_id_list) - set(original_item_id_list))
            # Ensure there are items left to rate
            if not possible_item_id_list:
                continue
            item_id = random.choice(possible_item_id_list)

            if 'context_id' in rating_df.columns:
                context_id_list = self.context_df['context_id'].unique()
                context_id = random.choice(context_id_list)
                rating = self.get_rating(user_id, item_id, context_id)
            else:
                rating = self.get_rating(user_id, item_id)

            # The minimum value rating.
            min_rating_value = self.access_rating.get_min_rating()
            # The maximum value rating.
            max_rating_value = self.access_rating.get_max_rating()
            user_rating_list=self.access_rating.get_rating_list_from_user(user_id=user_id)   

            # Modifying the generated rating.
            modified_rating = self.modify_rating_by_user_expectations(rating, k, user_rating_list, min_rating_value, max_rating_value, percentage_rating_variation)

            # Adding a new row to rating_df:
            new_data = {'user_id': user_id, 'item_id': item_id, 'rating': modified_rating}
            if 'context_id' in rating_df.columns:
                new_data['context_id'] = context_id
            rating_df = rating_df.append(new_data, ignore_index=True)

        # Sorting and resetting index
        sort_columns = ['user_id', 'item_id', 'rating']
        if 'context_id' in rating_df.columns:
            sort_columns.insert(2, 'context_id')
        rating_df = rating_df.sort_values(by=sort_columns)
        rating_df.reset_index(drop=True, inplace=True)
        
        return rating_df
