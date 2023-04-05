import logging

import pandas as pd
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_rating import ExtractStatisticsRating
import random

from datagencars.synthetic_dataset.generator.access_schema.access_user_profile import AccessUserProfile


class ReplicateDataset:
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

    def __init__(self, rating_df, user_profile_df):
        # Determining statistics:
        self.rating_statistics = ExtractStatisticsRating(rating_df)
        # Access to the user profile:
        self.access_user_profile = AccessUserProfile(user_profile_df)

    def replicate_dataset(self):
        """

        """
        # Users:
        for user_id in range(1, self.rating_statistics.get_number_users()+1):
            user_profile_id = user_id
            # Determining the number of ratings by user:
            number_ratings_by_user_df = self.rating_statistics.get_number_ratings_by_user()
            number_ratings_by_user = number_ratings_by_user_df.loc[number_ratings_by_user_df['user_id'] == user_id].iloc[0]
            for _ in number_ratings_by_user:
                # Items:            
                avg_items_df = self.rating_statistics.get_avg_items_by_user()
                avg_items = avg_items_df.loc[avg_items_df['user_id'] == int(user_id), 'avg_items'].iloc[0]
                std_items_df = self.rating_statistics.get_sd_items_by_user()
                std_items = std_items_df.loc[std_items_df['user_id'] == int(user_id), 'sd_items'].iloc[0]
                item_random = round(random.gauss(0, 1))
                item_random = max(1, min(item_random, self.rating_statistics.get_number_items()))
                item_id = round(avg_items + (std_items * item_random))

                # Contexts:
                if self.rating_statistics.get_number_contexts() != 0:
                    avg_contexts_df = self.rating_statistics.get_avg_contexts_by_user()
                    avg_contexts = avg_contexts_df.loc[avg_contexts_df['user_id'] == int(user_id), 'avg_contexts'].iloc[0]
                    std_contexts_df = self.rating_statistics.get_sd_contexts_by_user()
                    std_contexts = std_contexts_df.loc[std_contexts_df['user_id'] == int(user_id), 'sd_contexts'].iloc[0]
                    context_random = round(random.gauss(0, 1))
                    context_random = max(1, min(context_random, self.rating_statistics.get_number_contexts()))
                    context_id = round(avg_contexts + (std_contexts * context_random))
                    # Ratings:
                    rating = self.get_rating(user_profile_id, item_id, context_id)
                else:
                    # Ratings:
                    rating = self.get_rating(user_profile_id, item_id)   

                # Modifying the generated rating.                
                modified_rating = self.modify_rating_by_user_expectations(rating, k, user_rating_list, min_rating_value, max_rating_value)
                user_rating_list.append(rating)
                row_rating_list.append(modified_rating)


                attribute_name_list, value_list = self.access_user_profile.get_vector_from_user_profile(user_profile_id)
                print(attribute_name_list)
                print(value_list)

                print(user_id, item_id, context_id, rating_id)
                break

    def get_rating(self, user_profile_id, item_id, context_id=None):
        '''
        Determinig a rating value given weight and attribute rating vectors.
        :param user_profile_id: The user profile ID.
        :param item_id: The item ID.
        :param context_id: The context ID.
        :return: A rating value.
        '''
        # Getting attribute names.
        atribute_name_list = list(self.user_profile_df.columns.values)
        # Removing 'user_profile_id'.
        del atribute_name_list[0]
        # Getting the weight vector from user_profile_id.
        weight_vector = self.user_profile_df.loc[self.user_profile_df['user_profile_id'] == user_profile_id, atribute_name_list].values.tolist()[0]                
        # Getting the current attribute value and its possible values.
        if context_id:
            attribute_value_list, attribute_possible_value_list = self.get_attribute_value_and_possible_value_list(atribute_name_list, item_id, context_id)
        else:
            attribute_value_list, attribute_possible_value_list = self.get_attribute_value_and_possible_value_list(atribute_name_list, item_id)                 
        # Getting the range of rating values:
        minimum_value_rating = self.access_generation_config.get_minimum_value_rating()
        maximum_value_rating = self.access_generation_config.get_maximum_value_rating() 
        # Getting the attribute rating vector.
        attribute_rating_vector = self.get_attribute_rating_vector(weight_vector, attribute_value_list, attribute_possible_value_list, minimum_value_rating, maximum_value_rating, user_profile_attribute_list=atribute_name_list)

        if len(weight_vector) != len(attribute_rating_vector):
            raise ValueError('The vectors have not the same size.')
        
        rating = 0
        sum_weight = 0 # self.user_profile_df.loc[self.user_profile_df['user_profile_id'] == user_profile_id, 'other'].iloc[0]
        for idx, weight_importance in enumerate(weight_vector):
            # Getting importance and weight values:
            weight_importance_list = str(weight_importance).split('|')
            weight = 0
            if len(weight_importance_list) > 1:
                weight = float(weight_importance_list[1])
            else:
                weight = float(weight_importance)
            sum_weight += weight
            rating += weight * attribute_rating_vector[idx]
        if sum_weight != 1:
            raise ValueError('The weights not sum 1. You must verify the user_profile.csv file.')
        return round(rating, 2)
 

# rating_df:
rating_path = 'resources/dataset_sts/ratings.csv'
rating_df = pd.read_csv(rating_path, encoding='utf-8', index_col=False, sep=';')

# user_profile_df:
user_profile_path = 'resources/dataset_sts/user_profile.csv'
user_profile_df = pd.read_csv(user_profile_path, encoding='utf-8', index_col=False, sep=',')

replicate = ReplicateDataset(rating_df, user_profile_df)
replicate.replicate_dataset()