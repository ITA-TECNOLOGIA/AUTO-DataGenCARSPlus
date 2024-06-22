import math
import random

import numpy as np
import pandas as pd
from datagencars.existing_dataset.generate_user_profile.calculate_attribute_rating import CalculateAttributeRating
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_context import AccessContext
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_item import AccessItem
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_rating import AccessRating
import streamlit as st


class GenerateUserProfileDataset():

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

    def generate_user_profile(self, k_relevant_attributes, item_attribute_list, context_attribute_list=None):
        '''
        Gets the value of the weights (or unknown variables) by using LSMR method to generate the user profile.
        :param item_attribute_list: List of item attribute names.
        :param context_attribute_list: List of context attribute names.
        :param k_relevant_attributes: Number of relevant attributes to consider for generating user profiles.
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
            # Determining the A matrix:
            a_matrix, rank_vector = self.get_a_matrix(user_id, item_attribute_list, context_attribute_list)                                        
            a_matrix_df = pd.DataFrame(a_matrix)            
            # Determining the b vector:
            b_vector = self.get_b_vector(user_id)
            a_matrix_df['rating'] = b_vector  
            
            # Determining the x vector:
            # Seleccionar solo las columnas de géneros y multiplicar cada género por la calificación de la película
            attribute_columns = a_matrix_df.columns[:-1]  # Todos los géneros ignorando la última columna, que es el 'rating'.         
            weighted_attributes = a_matrix_df.loc[:, attribute_columns].multiply(a_matrix_df['rating'], axis=0)            
            # Sumar los valores ponderados para cada género
            sum_weighted_attributes = weighted_attributes.sum()            
            # Normalizar el perfil de género dividiendo por la suma total para hacer comparables los valores
            x_vector_series = sum_weighted_attributes / sum_weighted_attributes.sum()
            x_vector_list = x_vector_series.tolist()
            # print(x_vector_list)
            
            # NOTE: As the value of k_relevant_attributes nears 0, the rating values generated using the UP will be lower.
            if k_relevant_attributes > 0:
                # Create a zero vector of the same size as x_vector_list:
                scaled_vector = np.zeros_like(x_vector_list)
                # Determine the number of attributes to consider (minimum between k_relevant_attributes and the length of x_vector_list):
                n_relevant_attributes = min(k_relevant_attributes, len(x_vector_list))
                # Find the indices of the k_relevant_attributes highest values:
                top_indices = np.argsort(x_vector_list)[-n_relevant_attributes:]
                # Extract the k_relevant_attributes highest values:
                top_values = np.array(x_vector_list)[top_indices]
                # Scale the values so that they sum exactly to 1:
                scaled_top = top_values / top_values.sum()
                # Insert the scaled values in their corresponding positions:
                scaled_vector[top_indices] = scaled_top
                # Convert to list:
                x_vector = scaled_vector.tolist()
                # print(x_vector)   
            else:
                # If k_relevant_attributes is 0, use the original normalized list:
                x_vector = x_vector_list.copy()  # Use copy to avoid modifying the original list if needed later                
                             
            # Adding 'other' column:                        
            sum_weight_vector = round(sum(x_vector), 1)                
            weight_vector = [0.0] * (len(attribute_columns)+1)
            if sum_weight_vector == 0.0:
                weight_vector = x_vector+[1.0]
            elif math.isclose(sum_weight_vector, 1.0, abs_tol=1e-9):
                weight_vector = x_vector+[0.0]
            elif sum_weight_vector < 1.0:
                # Redondear la diferencia a 1 decimal y agregarlo como el peso del atributo "other"
                weight_vector = x_vector + [round(1.0 - sum_weight_vector, 1)]
            elif sum_weight_vector > 1.0:
                # Ajustar los pesos para asegurar que la suma sea 1.0
                normalized_weights = [x / sum_weight_vector for x in x_vector]
                weight_vector = normalized_weights + [0.0]                
            
            # Adding importance rank (+) o (-) to the weight:
            rank_weigth_list = []
            for idx, x in enumerate(weight_vector):
                if (x != 0.0) and (idx != len(weight_vector)-1): # ignoring the value of attribute 'other' because it must not have importance_rank.
                    rank_weigth_list.append(rank_vector[idx]+'|'+str(x))
                else:
                    rank_weigth_list.append(str(x))         
            user_profile_df.loc[len(user_profile_df)] = [int(user_id)]+rank_weigth_list            
            # Update the progress bar with each iteration                            
            progress_bar.progress(text=f'Generating user profile {user_id} from {len(user_id_list)}', value=(user_id) / len(user_id_list))
        return user_profile_df

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
                # Case: value_possible_list = [0, 1] or [1, 0], where 1 indicates presence of the attribute and 0 indicates absence.
                if len(value_possible_list) == 2 and ((0 in value_possible_list) and (1 in value_possible_list)):
                    if value_possible_list[0] == 0:                    
                        importance_rank = '(+)'
                    elif value_possible_list[0] == 1:      
                        importance_rank = '(-)'
                else:
                    importance_rank = '(-)' # Asumiendo que están ordenados de menor a mayor y el valor más pequeño es el más relevante.
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
                    attribute_rating = self.calculate_att_rating.get_attribute_rating(position_array, minimum_value_rating, maximum_value_rating, value_possible_list, importance_rank)                
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
