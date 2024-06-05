import logging
import math
import random

import numpy as np
import pandas as pd
from datagencars.existing_dataset.generate_user_profile.calculate_attribute_rating import CalculateAttributeRating
from datagencars.existing_dataset.generate_user_profile.generate_user_profile import GenerateUserProfile
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_context import AccessContext
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_item import AccessItem
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_rating import AccessRating
import streamlit as st
from decimal import Decimal, ROUND_HALF_DOWN


class GenerateUserProfileDataset(GenerateUserProfile):

    '''
    Generates a user profile automatically from the original dataset. 
    For that, the LSMR method (An Iterative Algorithm for Sparse Least-Squares Problems)
    was used. [https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.lsmr.html]

    Input:
        [I] item.csv
        [C] context.csv
        [R] ratings.csv
    Output:
        [UP] user_profile.csv
    '''

    def __init__(self, rating_df, item_df, context_df=None):        
        # Item file: item.csv        
        self.access_item = AccessItem(item_df)
        # Context file (optional): context.csv   
        self.is_context = None
        if context_df is None:
            context_df = pd.DataFrame()
            self.is_context = False
        elif not context_df.empty:
            self.access_context = AccessContext(context_df)   
            self.is_context = True         
        # Rating file: ratings.csv        
        self.access_rating = AccessRating(rating_df)  
        self.calculate_att_rating = CalculateAttributeRating()      

    def generate_user_profile(self, item_attribute_list, context_attribute_list=None):
        '''
        Gets the value of the weights (or unknown variables) by using LSMR method to generate the user profile.
        :param item_attribute_list: List of item attribute names.
        :param context_attribute_list: List of context attribute names.
        :return: A dataframe with the automatically generated user profile.
        '''
        # Getting attribute names:        
        if self.is_context:            
            attribute_list = ['user_profile_id']+item_attribute_list+context_attribute_list+['other']
        else:
            attribute_list = ['user_profile_id']+item_attribute_list+['other']        
        # Initialiting user profile dataframe:
        user_profile_df = pd.DataFrame(columns=attribute_list)
        # Getting user ID list:
        user_id_list = self.access_rating.get_user_id_list()
        # Determining weigth vectors by user:
        # Create a progress bar
        progress_bar = st.progress(0.0) 
        for user_id in user_id_list:
            # Determining the x vector:
            a_matrix, rank_vector = self.get_a_matrix(user_id, item_attribute_list, context_attribute_list)
            b_vector = self.get_b_vector(user_id)
            x_vector = self.get_x_weigths(A=a_matrix.to_numpy(), b=b_vector)[0].tolist()
            not_nan_x_vector = [0.0 if np.isnan(x) else round(x, 1) for x in x_vector]
            if any(x < 0 or math.copysign(1, x) < 0 for x in not_nan_x_vector):                
                # Replace negative or -0.0 values with 0.0:                
                not_nan_x_vector = [0.0 if x < 0 or math.copysign(1, x) < 0 else round(x, 1) for x in not_nan_x_vector]

            # Adding other value:
            sum_weight_vector = sum(not_nan_x_vector)
            weight_vector = []           
            if sum_weight_vector == 0.0:
                weight_vector = not_nan_x_vector+[1.0]
            elif sum_weight_vector == 1:
                weight_vector = not_nan_x_vector+[0.0]
            elif sum_weight_vector < 1:                
                weight_vector = not_nan_x_vector+[round(1.0-sum_weight_vector, 1)]
            elif sum_weight_vector > 1:
                # Adjust the weight values to ensure that the sum is 1.
                weight_vector = self.adjust_weights(not_nan_x_vector)+[0.0]                

            # Adding importance rank (+) o (-) to the weight:
            rank_weigth_list = []
            for idx, x in enumerate(weight_vector):
                if (x != 0.0) and (idx != len(weight_vector)-1): # ignoring the value of attribute 'other' because it must not have importance_rank.
                    rank_weigth_list.append(rank_vector[idx]+'|'+str(x))
                else:
                    rank_weigth_list.append(str(x))         
            user_profile_df.loc[len(user_profile_df)] = [int(user_id)]+rank_weigth_list # +[sum(weight_vector)]
            # Update the progress bar with each iteration                            
            progress_bar.progress(text=f'Generating user profile {user_id} from {len(user_id_list)}', value=(user_id) / len(user_id_list))
        return user_profile_df

    def adjust_weights(self, not_nan_x_vector):
        """
        Adjusts and normalizes a list of weights (not_nan_x_vector) to sum up to 1.0, with each weight rounded to one decimal place.
        This method uses Decimal for precision and a more refined strategy for distributing rounding errors.

        :param not_nan_x_vector: A list of non-NaN, non-negative numerical values representing initial weights.
        :return: A list of adjusted weights, rounded to one decimal place, where the sum of all weights is exactly 1.0.
        """
        # Convert weights to Decimal for precise arithmetic, avoiding floating-point issues
        weight_vector = [Decimal(str(x)) for x in not_nan_x_vector]

        # Calculate the sum of the original weights
        sum_original = sum(weight_vector)
        if sum_original == 0:
            return [Decimal('0.0')] * len(weight_vector)  # Avoid division by zero

        # Normalize weights so they sum to 1, rounding down to minimize initial rounding error
        normalized_weights = [x / sum_original for x in weight_vector]
        rounded_weights = [x.quantize(Decimal('0.1'), rounding=ROUND_HALF_DOWN) for x in normalized_weights]

        # Calculate the rounding error
        rounding_error = Decimal('1.0') - sum(rounded_weights)

        # Distribute the rounding error
        for i in range(len(rounded_weights)):
            if rounding_error <= 0:
                break
            if rounding_error > 0 and rounded_weights[i] < Decimal('1.0') - Decimal('0.1'):
                # Adjust the weight, ensuring it doesn't exceed 1.0
                rounded_weights[i] += Decimal('0.1')
                rounding_error -= Decimal('0.1')

        # Final pass to ensure sum is exactly 1.0, adjust the weight with the least impact
        if rounding_error > 0:
            for i in range(len(rounded_weights)):
                if rounded_weights[i] + rounding_error <= Decimal('1.0'):
                    rounded_weights[i] += rounding_error
                    break

        return [float(x) for x in rounded_weights]


    def get_a_matrix(self, user_id, item_attribute_list, context_attribute_list):  # sourcery skip: extract-duplicate-method, extract-method, for-append-to-extend, inline-immediately-returned-variable, low-code-quality, merge-list-append, move-assign-in-block, use-dictionary-union
        '''
        Gets the matrix A.
        :param user_id: The user ID of the current user.
        :param item_attribute_list: List of item attribute names.
        :param context_attribute_list: List of context attribute names.
        :return: The matrix A.
        '''        
        # Analysing ITEMS by user_id:              
        # Getting item_id_list from user_id:
        item_id_list = self.access_rating.get_item_id_list_from_user(user_id)
        # Getting item values and their possible values:
        item_value_possible_dict = {}
        item_value_list = []
        for item_id in item_id_list:
            value_list = []
            for item_atribute_name in item_attribute_list:
                item_value = self.access_item.get_item_value_from_item_attribute(item_id, attribute_name=item_atribute_name)
                item_possible_value_list = self.access_item.get_item_possible_value_list_from_attribute(attribute_name=item_atribute_name)                
                item_value_possible_dict[item_atribute_name] = item_possible_value_list
                value_list.append(item_value)
            item_value_list.append(tuple(value_list))
        df_item_attribute_value = pd.DataFrame(item_value_list, columns=item_attribute_list)

        # Analysing CONTEXTS by user_id:
        if self.is_context:            
            # Getting context_id_list from user_id:
            context_id_list = self.access_rating.get_context_id_list_from_user(user_id)
            # Getting context values and their possible values:
            context_value_possible_dict = {}
            context_value_list = []
            for context_id in context_id_list:
                value_list = []
                for context_atribute_name in context_attribute_list:
                    context_value = self.access_context.get_context_value_from_context_attribute(context_id, attribute_name=context_atribute_name)
                    context_possible_value_list = self.access_context.get_context_possible_value_list_from_attribute(attribute_name=context_atribute_name)                
                    context_value_possible_dict[context_atribute_name] = context_possible_value_list
                    value_list.append(context_value)
                context_value_list.append(tuple(value_list))
            df_context_attribute_value = pd.DataFrame(context_value_list, columns=context_attribute_list)
            value_possible_dict = {**item_value_possible_dict, **context_value_possible_dict}            
            df_attribute_value = pd.concat([df_item_attribute_value, df_context_attribute_value], axis=1)   
        else:
            value_possible_dict = item_value_possible_dict
            df_attribute_value = pd.concat([df_item_attribute_value], axis=1)       

        # Calculating attribute ratings:        
        minimum_value_rating = self.access_rating.get_min_rating()
        maximum_value_rating = self.access_rating.get_max_rating()      
        if self.is_context:  
            attribute_list = item_attribute_list+context_attribute_list
        else:
            attribute_list = item_attribute_list
        # Initializing the matrix A[MxN]:
        a_matrix = pd.DataFrame(columns=attribute_list)        
        rank_vector = []
        # Iterate over columns
        for attribute_name_column, value_series in df_attribute_value.items():            
            attribute_value_list = value_series.tolist()            
            value_possible_list = []
            for x in value_possible_dict[attribute_name_column]:
                if isinstance(x, (int, float)) and not math.isnan(x):
                    value_possible_list.append(x)
                else:
                    value_possible_list.append(x)            
            importance_rank = ''
            # is_numeric: check if all non-NaN values are numeric                
            if all(isinstance(x, (int, float)) for x in value_possible_list):
                importance_rank = '(-)' # The numbers are sorted from smallest to largest.                                
            elif all(isinstance(x, bool) for x in value_possible_list):
                # is_boolean: check if all non-NaN values are boolean
                importance_rank = '(+)' if value_possible_list[0] == False else '(-)'                       
            elif all(isinstance(x, str) for x in value_possible_list):
                # is_string: check if all non-NaN values are string: TODO --> No tenemos la manera de saber el orden (hablar con silarri@itainnova.es)
                importance_rank = random.choice(['(-)', '(+)'])   
            rank_vector.append(importance_rank)
            attribute_rating_list = []
            for attribute_value in attribute_value_list:
                if isinstance(attribute_value, (int, float)) and math.isnan(attribute_value):
                    attribute_rating = 0
                    importance_rank = ''
                else:
                    position_array = value_possible_list.index(attribute_value)                                 
                    attribute_rating = self.calculate_att_rating.get_attribute_rating(position_array, minimum_value_rating, maximum_value_rating, attribute_value_list, importance_rank)                
                attribute_rating_list.append(attribute_rating)                            
            a_matrix[attribute_name_column] = attribute_rating_list            
        return a_matrix, rank_vector

    def get_b_vector(self, user_id):
        # sourcery skip: inline-immediately-returned-variable
        '''
        Gets the b vector, which is the rating list of the current user (user_id).
        :param user_id: The user ID of the current user.
        :return: The b vector.
        '''
        rating_list = self.access_rating.get_rating_list_from_user(user_id)
        b_vector = np.array(rating_list, dtype=float)
        return b_vector    
