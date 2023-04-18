import logging
import random

import numpy as np
import pandas as pd
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_context import AccessContext
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_item import AccessItem
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_rating import AccessRating
from datagencars.existing_dataset.replicate_dataset.generate_user_profile.calculate_attribute_rating import CalculateAttributeRating
from scipy.sparse.linalg import lsmr
import math


class GenerateUserProfile:

    '''
    Generates a user profile automatically from the original dataset. 
    For that, the LSMR method (An Iterative Algorithm for Sparse Least-Squares Problems)
    was used. [https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.lsmr.html]

    Input:
        [I] item.csv
        [C] context.csv
        [R] ratings.csv
    '''

    def __init__(self, ratings_df, item_df, context_df=None):        
        # Item file: item.csv        
        self.access_item = AccessItem(item_df)
        # Context file (optional): context.csv   
        self.is_context = False
        if not context_df.empty:                   
            self.access_context = AccessContext(context_df)      
            self.is_context = True    
        # Rating file: ratings.csv        
        self.access_rating = AccessRating(ratings_df)  
        self.calculate_att_rating = CalculateAttributeRating()      

    def generate_user_profile(self):
        '''
        Gets the value of the weights (or unknown variables) by using LSMR method to generate the user profile.
        '''
        # Getting attribute names:
        item_attribute_name_list = self.access_item.get_item_attribute_list()
        context_attribute_name_list = self.access_context.get_context_attribute_list()
        attribute_list = ['user_profile_id']+item_attribute_name_list+context_attribute_name_list+['other'] # , 'sum'
        # Initialiting user profile dataframe:
        user_profile_df = pd.DataFrame(columns=attribute_list)
        # Getting user ID list:
        user_id_list = self.access_rating.get_user_id_list()
        # Determining weigth vectors by user:
        for user_id in user_id_list:
            # Determining the x vector:
            a_matrix, rank_vector = self.get_a_matrix(user_id)
            b_vector = self.get_b_vector(user_id)
            x_vector = self.get_x_weigths(A=a_matrix.to_numpy(), b=b_vector)[0].tolist()
            not_nan_x_vector = [0.0 if np.isnan(x) else x for x in x_vector]

            # Adding other value:
            sum_weight_vector = sum(not_nan_x_vector)
            weight_vector = []
            if sum_weight_vector == 0.0:
                weight_vector = not_nan_x_vector+[1.0]
            elif sum_weight_vector == 1:
                weight_vector = not_nan_x_vector+[0.0]
            elif sum_weight_vector < 1:                
                weight_vector = not_nan_x_vector+[1.0-sum_weight_vector]
            elif sum_weight_vector > 1:
                # Adjust the weight values to ensure that the sum is 1.               
                weight_vector = [x/sum_weight_vector for x in not_nan_x_vector] +[0.0]            

            # Adding importance rank (+) o (-) to the weight:
            rank_weigth_list = []
            for idx, x in enumerate(weight_vector):
                if (x != 0.0) and (idx != len(weight_vector)-1): # ignoring the value of attribute 'other' because it must not have importance_rank.
                    rank_weigth_list.append(rank_vector[idx]+'|'+str(x))
                else:
                    rank_weigth_list.append(str(x))            
            user_profile_df.loc[len(user_profile_df)] = [int(user_id)]+rank_weigth_list # +[sum(weight_vector)]
        return user_profile_df

    def get_a_matrix(self, user_id):    # sourcery skip: extract-duplicate-method, extract-method, for-append-to-extend, inline-immediately-returned-variable, low-code-quality, merge-list-append, move-assign-in-block, use-dictionary-union
        '''
        '''        
        # Analysing ITEMS by user_id:
        # Getting item attibute names:
        item_attribute_name_list = self.access_item.get_item_attribute_list()
        # Getting item_id_list from user_id:
        item_id_list = self.access_rating.get_item_id_list_from_user(user_id)
        # Getting item values and their possible values:
        item_value_possible_dict = {}
        item_value_list = []
        for item_id in item_id_list:
            value_list = []
            for item_atribute_name in item_attribute_name_list:
                item_value = self.access_item.get_item_value_from_item_attributte(item_id, attribute_name=item_atribute_name)
                item_possible_value_list = self.access_item.get_item_possible_value_list_from_attributte(attribute_name=item_atribute_name)                
                item_value_possible_dict[item_atribute_name] = item_possible_value_list
                value_list.append(item_value)
            item_value_list.append(tuple(value_list))
        df_item_attribute_value = pd.DataFrame(item_value_list, columns=item_attribute_name_list)

        # Analysing CONTEXTS by user_id:
        if self.is_context:
            # Getting context attibute names:
            context_attribute_name_list = self.access_context.get_context_attribute_list()
            # Getting context_id_list from user_id:
            context_id_list = self.access_rating.get_context_id_list_from_user(user_id)
            # Getting context values and their possible values:
            context_value_possible_dict = {}
            context_value_list = []
            for context_id in context_id_list:
                value_list = []
                for context_atribute_name in context_attribute_name_list:
                    context_value = self.access_context.get_context_value_from_context_attributte(context_id, attribute_name=context_atribute_name)
                    context_possible_value_list = self.access_context.get_context_possible_value_list_from_attributte(attribute_name=context_atribute_name)                
                    context_value_possible_dict[context_atribute_name] = context_possible_value_list
                    value_list.append(context_value)
                context_value_list.append(tuple(value_list))
            df_context_attribute_value = pd.DataFrame(context_value_list, columns=context_attribute_name_list)
            value_possible_dict = {**item_value_possible_dict, **context_value_possible_dict}            
            df_attribute_value = pd.concat([df_item_attribute_value, df_context_attribute_value], axis=1)   
        else:
            value_possible_dict = item_value_possible_dict
            df_attribute_value = pd.concat([df_item_attribute_value], axis=1)       

        # Calculating attribute ratings:        
        minimum_value_rating = self.access_rating.get_min_rating()
        maximum_value_rating = self.access_rating.get_max_rating()
        attribute_list = item_attribute_name_list+context_attribute_name_list
        # Initializing the matrix A[MxN]:
        a_matrix = pd.DataFrame(columns=attribute_list)        
        rank_vector = []
        # Iterate over columns
        for attribute_name_column, value_series in df_attribute_value.items():            
            attribute_value_list = value_series.tolist()
            value_possible_list = [x for x in value_possible_dict[attribute_name_column] if not math.isnan(x)]  
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
                if math.isnan(attribute_value):
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

    def get_x_weigths(self, A, b):
        '''
        LSMR (An Iterative Algorithm for Sparse Least-Squares Problems), implemented in scipy.
        It solves the system of linear equations: A*X = B        
        
        :param A: Rectangular matrix in the linear system of dimension MxN, where all cases are allowed: M=N, M>N or M<N. The matrix A may be dense or sparse (usually sparse).
        :param b: Vector in the linear system of length N.
        :param X: Vector of float (Least-square solution), which are the incognites (or weigths) to be solved, by using the method => lsmr(A, b).

        In this case, for example for user 1:        
            A: These are the ratings per contextual attribute (items and/or contexts), generated by a user's utility function, for each item that the user evaluated.
            b: It is the set of item ratings of user 1.
            X: It is the set of relevance weights that are automatically determined, by each user, to the attributes of items and/or contexts, found in the user profile. And the (+) or (-) is the order of priority assigned by the users to the possible values of these attributes.

        '''
        return lsmr(A, b)


# item_df:
item_path = 'resources/dataset_sts/item.csv'
item_df = pd.read_csv(item_path, encoding='utf-8', index_col=False, sep=';')

# context_df:
context_path = 'resources/dataset_sts/context.csv'
context_df = pd.read_csv(context_path, encoding='utf-8', index_col=False, sep=';')

# rating_df:
rating_path = 'resources/dataset_sts/ratings.csv'
ratings_df = pd.read_csv(rating_path, encoding='utf-8', index_col=False, sep=';')

gup = GenerateUserProfile(ratings_df, item_df, context_df)
user_profile_df = gup.generate_user_profile()
print(user_profile_df.shape)
user_profile_df.to_csv('resources/dataset_sts/user_profile.csv', sep=',', index=False, index_label='index')
