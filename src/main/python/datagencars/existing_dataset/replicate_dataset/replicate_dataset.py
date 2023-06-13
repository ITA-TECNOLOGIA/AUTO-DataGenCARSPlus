import logging

import pandas as pd
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_context import AccessContext
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_item import AccessItem
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_rating import AccessRating
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_rating import ExtractStatisticsRating
import random
import numpy as np
import ast

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

    def __init__(self, rating_df, user_profile_df, item_df, context_df=None):
        # Determining statistics:
        self.rating_statistics = ExtractStatisticsRating(rating_df)
        # Access to the user profile:
        self.access_user_profile = AccessUserProfile(user_profile_df)
        # Access to the item.csv.
        self.access_item = AccessItem(item_df)
        # Access to the context.csv.
        self.access_context = AccessContext(context_df)
        # Access to the ratings.csv.
        self.access_rating = AccessRating(rating_df)

    def replicate_dataset(self, percentage_rating_variation):
        """
        Replicates an original dataset.
        :param percentage_rating_variation: The percentage of rating variation.
        :return: A replicated dataset.
        """
        rating_df = None
        if self.rating_statistics.get_number_contexts() != 0:
            rating_df = pd.DataFrame(columns=['user_id', 'item_id', 'context_id', 'rating'])
        else:
            rating_df = pd.DataFrame(columns=['user_id', 'item_id', 'rating'])

        # The k ratings to take in the past.
        k = 10
        # The minimum value rating.
        min_rating_value = self.access_rating.get_min_rating()
        # The maximum value rating.
        max_rating_value = self.access_rating.get_max_rating()
        user_id_list = []
        item_id_list = []
        context_id_list = []
        rating_list = [] 
        for user_id in range(1, self.rating_statistics.get_number_users()+1):
            user_profile_id = user_id     
            #print('user_id: ', user_id)
            # Items:            
            original_item_id_list = self.access_rating.get_item_id_list_from_user(user_id=user_id)
            avg_items_df = self.rating_statistics.get_avg_items_by_user()
            avg_items = avg_items_df.loc[avg_items_df['user_id'] == int(user_id), 'avg_items'].iloc[0]
            std_items_df = self.rating_statistics.get_sd_items_by_user()
            std_items = std_items_df.loc[std_items_df['user_id'] == int(user_id), 'sd_items'].iloc[0]    
            minimum_item_id = min(original_item_id_list)
            maximum_item_id = max(original_item_id_list)        
            new_item_id_list = np.random.normal(loc=avg_items, scale=std_items, size=len(original_item_id_list))
            new_item_id_list = np.clip(new_item_id_list, minimum_item_id, maximum_item_id)  # clip values to min and max
            new_item_id_list = new_item_id_list.round().astype(int)  # round to integers            
            item_id_list.extend(new_item_id_list.tolist())
            # Contexts:
            if self.rating_statistics.get_number_contexts() != 0:
                original_context_id_list = self.access_rating.get_context_id_list_from_user(user_id=user_id)
                avg_contexts_df = self.rating_statistics.get_avg_contexts_by_user()
                avg_contexts = avg_contexts_df.loc[avg_contexts_df['user_id'] == int(user_id), 'avg_contexts'].iloc[0]
                std_contexts_df = self.rating_statistics.get_sd_contexts_by_user()
                std_contexts = std_contexts_df.loc[std_contexts_df['user_id'] == int(user_id), 'sd_contexts'].iloc[0]
                minimum_context_id = min(original_context_id_list)
                maximum_context_id = max(original_context_id_list) 
                new_context_id_list = np.random.normal(loc=avg_contexts, scale=std_contexts, size=len(original_context_id_list))
                new_context_id_list = np.clip(new_context_id_list, minimum_context_id, maximum_context_id)  # clip values to min and max
                new_context_id_list = new_context_id_list.round().astype(int)  # round to integers
                context_id_list.extend(new_context_id_list.tolist())                
            # Ratings:
            user_rating_list = []                        
            for idx, item_id in enumerate(new_item_id_list):                
                # Contexts:
                if self.rating_statistics.get_number_contexts() != 0:   
                    context_id=new_context_id_list[idx]             
                    rating = self.get_rating(user_profile_id, item_id, context_id)
                else:                
                    rating = self.get_rating(user_profile_id, item_id)                    
                # Generated rating.
                user_rating_list.append(rating)
                # Modifying the generated rating.                
                modified_rating = self.modify_rating_by_user_expectations(rating, k, user_rating_list, min_rating_value, max_rating_value, percentage_rating_variation)
                rating_list.append(modified_rating)
            # Users:
            k = len(original_item_id_list)
            user_id_list.extend([int(user_id)] * k)                            
        if rating_df.empty:
            rating_df['user_id'] = user_id_list
            rating_df['item_id'] = item_id_list
            if self.rating_statistics.get_number_contexts() != 0:
                rating_df['context_id'] = context_id_list
            rating_df['rating'] = rating_list           
        # Contexts:
        if self.rating_statistics.get_number_contexts() != 0:
            # Sorting and returning a rating_df by user_id and item_id.
            rating_df = rating_df.sort_values(by=['user_id', 'item_id', 'context_id'], ascending=[True, True, True], na_position='first')
        else:
            rating_df = rating_df.sort_values(by=['user_id', 'item_id'], ascending=[True, True], na_position='first')
        # Reseting index.
        rating_df.reset_index(drop=True, inplace=True)
        return rating_df
    
    def get_rating(self, user_profile_id, item_id, context_id=None):
        '''
        Determinig a rating value given weight and attribute rating vectors.
        :param user_profile_id: The user profile ID.
        :param item_id: The item ID.
        :param context_id: The context ID.
        :return: A rating value.
        '''       
        # Getting the attribute name list and atribute value list of the user_profile_id.
        atribute_name_list, atribute_value_list = self.access_user_profile.get_vector_from_user_profile(user_profile_id)        

        # Getting the current attribute value and its possible values.
        if context_id:
            attribute_value_list, attribute_possible_value_list = self.get_attribute_value_and_possible_value_list(atribute_name_list, item_id, context_id)
        else:
            attribute_value_list, attribute_possible_value_list = self.get_attribute_value_and_possible_value_list(atribute_name_list, item_id)                 
        # Getting the range of rating values:
        minimum_value_rating = self.access_rating.get_min_rating()
        maximum_value_rating = self.access_rating.get_max_rating()
        # Getting the attribute rating vector.
        attribute_rating_vector = self.access_user_profile.get_attribute_rating_vector(atribute_value_list, attribute_value_list, attribute_possible_value_list, minimum_value_rating, maximum_value_rating, user_profile_attribute_list=atribute_name_list)

        if len(atribute_value_list) != len(attribute_rating_vector):
            raise ValueError('The vectors have not the same size.')
        
        rating = 0
        sum_weight = 0 # self.user_profile_df.loc[self.user_profile_df['user_profile_id'] == user_profile_id, 'other'].iloc[0]
        for idx, weight_importance in enumerate(atribute_value_list):
            # Getting importance and weight values:
            weight_importance_list = str(weight_importance).split('|')
            weight = 0
            if len(weight_importance_list) > 1:
                weight = float(weight_importance_list[1])
            else:
                weight = float(weight_importance)
            sum_weight += weight
            rating += weight * attribute_rating_vector[idx]        
        if round(sum_weight) != 1:
            raise ValueError(f'The weights not sum 1 (sum weight: {sum_weight}). You must verify the user_profile.csv file (user profile: {user_profile_id}).')
        return round(rating, 2)
    
    def get_attribute_value_and_possible_value_list(self, atribute_name_list, item_id, context_id=None):
        '''
        Get the attribute value and its possible values.
        :param atribute_name_list: The list of attribute names.
        :param item_id: The item ID of the current user.
        :param context_id: The context ID of the current user <optional>.
        :return: The attribute value and its possible values.
        '''
        attribute_value_list = []
        possible_value_list = []
        for attribute_name in atribute_name_list:
            # Getting values from item.csv
            if attribute_name in self.access_item.get_item_attribute_list():
                attribute_value = self.access_item.get_item_value_from_item_attributte(item_id, attribute_name)                
                if ((isinstance(attribute_value, (np.bool_, np.int64, np.float64))) or ('[' not in attribute_value)):
                    attribute_value_list.append(attribute_value)
                else:
                    # Ckeck if is a list as str "['a', 'b']"
                    attribute_value_list.append(ast.literal_eval(attribute_value))
                # Getting possible values of the current attribute:
                possible_value_list.append(self.access_item.get_item_possible_value_list_from_attributte(attribute_name))
            elif context_id:
                # Getting values from context.csv
                if attribute_name in self.access_context.get_context_attribute_list():
                    attribute_value_list.append(self.access_context.get_context_value_from_context_attributte(context_id, attribute_name))                    
                    # Getting possible values of the current attribute:
                    possible_value_list.append(self.access_context.get_context_possible_value_list_from_attributte(attribute_name))
        return attribute_value_list, possible_value_list
    
    def modify_rating_by_user_expectations(self, rating, k, user_rating_list, min_rating_value, max_rating_value, percentage_rating_variation):
        '''
        Modifies the rating value with the user expectations.
        :param rating: The original rating (determined by using the user_profile).
        :param k: The k ratings to take in the past.
        :return: The modified rating value by using the user expectations.
        ''' 
        rating_modified = None        
        # Determinig the last k ratings of the current user in the past.
        number_ratings = len(user_rating_list)
        k_last_rating_list = []
        if (number_ratings < k) or (number_ratings == k):
            k_last_rating_list = user_rating_list
        else:            
            k_last_rating_list = user_rating_list[-k:]
        if len(k_last_rating_list) != 0:
            # Determing the rating average of the current user in the past:
            avg = np.average(k_last_rating_list)          
            # Determining the rating variation:
            rating_variation = abs((rating - avg) * (percentage_rating_variation/100))              

            # Modifiying the rating value:
            if rating > avg:
                rating_modified = rating + rating_variation
            elif rating < avg:
                rating_modified = rating - rating_variation
            else:            
                rating_modified = rating # avg=0

            # Validating the modified rating value:
            if rating_modified > max_rating_value:
                # Avoid obtaining a modified rating higher than the maximum rating.
                rating_modified = min(max_rating_value, rating_modified)
            elif rating_modified < min_rating_value:
                # Avoid obtaining a modified rating lower than the minimum rating.
                rating_modified = max(min_rating_value, rating_modified)
        else:
            rating_modified = rating
        return round(rating_modified , 2)
 