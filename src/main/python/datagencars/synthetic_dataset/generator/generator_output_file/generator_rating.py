import ast
import logging
import random

import numpy as np
import pandas as pd
from datagencars.synthetic_dataset.generator.access_schema.access_generation_config import AccessGenerationConfig
from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema


class GeneratorRatingFile:
    '''     
    Generates user ratings. For that purpose, it obtains random combinations
    <user, item, context> and computes the corresponding rating by applying the
    data utility function defined in the corresponding user profile. To compute
    the rating, this class takes into account whether the user profile defines a
    preference for higher or lower values in the domain of values of each
    attribute and transforms each attribute value into a normalized score in the
    output range required (e.g., a value between one and five), through linear
    regression. As real users do not rate items by applying a precise
    mathematical function, potential noise or uncertainty for the rating
    generated can be simulated by defining a weight different from zero for the
    attribute others in the user profile. More-over, this class generates a
    random time and date (within the input allowable range of dates provided)
    representing the time instant when the user provided the rating; random
    timestamps are generated in such a way that the ratings of the users are
    mixed with each other so supporting situations where several ratings are
    provided by the same or by different users at approximately the same time.
     
    @author Maria del Carmen Rodriguez-Hernandez 
    '''

    def __init__(self, generation_config, user_df, user_profile_df, item_df, item_schema, context_df=None, context_schema=None):        
        # User profile: user_profile.csv
        self.user_profile_df = user_profile_df
        # Schema access: generation_config.conf
        self.access_generation_config = AccessGenerationConfig(file_str=generation_config)
        # User file: user.csv
        self.user_df = user_df
        # Item file: item.csv
        self.item_df = item_df
        # Item schema: item_schema.conf
        self.item_schema_access = AccessSchema(file_str=item_schema)
        # Context:
        if context_df is None: 
            context_df = pd.DataFrame()
        if not context_df.empty and context_schema:
            # Context file (optional): context.csv
            self.context_df = context_df
            # Context schema: context_schema.conf
            self.context_schema_access = AccessSchema(file_str=context_schema)

    def generate_file(self, with_context=False):
        # sourcery skip: assign-if-exp, extract-duplicate-method, hoist-statement-from-loop, low-code-quality, merge-list-append
        '''
        Generates the rating file.   
        :param with_context: True if the file to be generated will be contextual and False in the otherwise.
        :return: A dataframe with rating information (user_id, item_id, context_id <optional>, rating, timestamp). 
        '''     
        rating_df = None
        if with_context:
            rating_df = pd.DataFrame(columns=['user_id', 'item_id', 'context_id', 'rating', 'timestamp'])
        else:
            rating_df = pd.DataFrame(columns=['user_id', 'item_id', 'rating', 'timestamp'])

        # Getting the number of users.
        number_user = self.access_generation_config.get_number_user()
        user_id_list = self.user_df['user_id'].unique().tolist()
        # Getting the number of items.
        # number_item = self.access_generation_config.get_number_item()
        item_id_list = self.item_df['item_id'].unique().tolist()
        # Getting the number of contexts.
        if with_context:
            # number_context = self.access_generation_config.get_number_context()
            context_id_list = self.context_df['context_id'].unique().tolist()
        # Getting the number of ratings:
        number_ratings = self.access_generation_config.get_number_rating()
        # Determinig the number of rating by user:
        number_rating_by_user = int(number_ratings/number_user)               

        # Generating a timestamp list by day and in a range of years:
        minimum_year_ts = self.access_generation_config.get_minimum_year_timestamp()
        maximum_year_ts = self.access_generation_config.get_maximum_year_timestamp()
        start = pd.Timestamp(f'{minimum_year_ts}-01-01').strftime('%Y-%m-%d')
        end = pd.Timestamp(f'{maximum_year_ts}-12-31').strftime('%Y-%m-%d')
        timestamp_list = pd.date_range(start, end, freq='1d')

        # The k ratings to take in the past.
        k = self.access_generation_config.get_k_rating_past()
        # The minimum value rating.
        min_rating_value = self.access_generation_config.get_minimum_value_rating()
        # The maximum value rating.
        max_rating_value = self.access_generation_config.get_maximum_value_rating()

        # Iterating by user:
        for user_index in range(1, number_user+1):
            row_rating_list = []

            # Generating user_id:
            user_id = user_id_list[user_index-1]
            row_rating_list.append(user_id)   
         
            # Determining the initial timestamp for the current user:
            initial_timestamp = timestamp_list[random.randint(0, len(timestamp_list)-1)]     
            # Check if the initial_timestamp is near to minimum year.
            while (initial_timestamp.year == minimum_year_ts) and (initial_timestamp.month == 12) and ((31-initial_timestamp.day) < number_rating_by_user):
                initial_timestamp = timestamp_list[random.randint(0, len(timestamp_list)-1)]
            
            # Generating ratings for the current user:
            user_rating_list = []           
            for _ in range(number_rating_by_user):
                # Generating item_id:
                item_id = random.choice(item_id_list)
                row_rating_list.append(item_id)    

                # Generating context_id:
                if with_context:
                    context_id = random.choice(context_id_list)
                    row_rating_list.append(context_id)

                # Generating a rating for a specified user profile:                   
                user_profile_id = self.user_df.loc[self.user_df['user_id'] == user_id, 'user_profile_id'].iloc[0]                
                if with_context:
                    rating = self.get_rating(user_profile_id, item_id, context_id)
                else:
                    rating = self.get_rating(user_profile_id, item_id)        
                # Modifying the generated rating.                
                modified_rating = self.modify_rating_by_user_expectations(rating, k, user_rating_list, min_rating_value, max_rating_value)
                user_rating_list.append(rating)
                row_rating_list.append(modified_rating)

                # Generating timestamp:
                timestamp = initial_timestamp+pd.Timedelta(days=random.randint(1, 30), minutes=random.randint(1, 1440))                
                row_rating_list.append(timestamp)

                # Inserting row into dataframe:                
                rating_df.loc[len(rating_df.index)] = row_rating_list  
                row_rating_list.clear()     
                row_rating_list.append(user_id)                

        # Inserting remaining items to randomly selected users:        
        number_remaining_rating = number_ratings - (number_rating_by_user*number_user)
        for _ in range(number_remaining_rating):
            row_rating_list.clear()

            # Choosing user_id:
            user_id = random.choice(user_id_list)
            row_rating_list.append(user_id)            
            # Generating item_id:
            item_id = random.choice(item_id_list)
            row_rating_list.append(item_id)
            # Generating context_id:
            if with_context:
                context_id = random.choice(context_id_list)
                row_rating_list.append(context_id)
            # Generating a rating for a specified user profile:            
            user_profile_id = self.user_df.loc[self.user_df['user_id'] == str(user_id), 'user_profile_id'].iloc[0]
            if with_context:
                rating = self.get_rating(user_profile_id, item_id, context_id)
            else:
                rating = self.get_rating(user_profile_id, item_id)

            # Modifying the generated rating.
            user_rating_list = rating_df.loc[rating_df['user_id'] == user_id]['rating'].tolist()
            modified_rating = self.modify_rating_by_user_expectations(rating, k, user_rating_list, min_rating_value, max_rating_value)
            row_rating_list.append(modified_rating)

            # Generating timestamp:
            timestamp_df = rating_df.loc[rating_df['user_id']==user_id, ['timestamp']]
            timestamp_df.sort_values(by='timestamp', ascending=False, inplace=True)
            initial_timestamp = timestamp_df['timestamp'].tolist()[0]
            timestamp = initial_timestamp+pd.Timedelta(days=random.randint(1, 30), minutes=random.randint(1, 1440))            
            row_rating_list.append(timestamp)

            # Inserting row into dataframe:
            rating_df.loc[len(rating_df.index)] = row_rating_list            

        # Sorting and returning a rating_df by user_id and item_id, and reseting index.
        rating_df.sort_values(by=['user_id', 'timestamp'], ascending=True, na_position='first', inplace=True)
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
            if attribute_name in list(self.item_df.columns.values):
                attribute_value = self.item_df.loc[self.item_df['item_id'] == item_id, attribute_name].iloc[0]
                if (isinstance(attribute_value, (np.bool_, np.int64)) or '[' not in attribute_value):
                    attribute_value_list.append(attribute_value)
                else:
                    # Ckeck if is a list as str "['a', 'b']"
                    attribute_value_list.append(ast.literal_eval(attribute_value))
                # Getting possible values of the current attribute:         
                possible_value_list.append(self.item_schema_access.get_possible_values_attribute_list_from_name(attribute_name))
            elif context_id:
                # Getting values from context.csv
                if attribute_name in list(self.context_df.columns.values):
                    attribute_value_list.append(self.context_df.loc[self.context_df['context_id'] == context_id, attribute_name].iloc[0])
                    # Getting possible values of the current attribute:
                    possible_value_list.append(self.context_schema_access.get_possible_values_attribute_list_from_name(attribute_name))
        return attribute_value_list, possible_value_list
    
    def get_attribute_rating_vector(self, weight_vector, attribute_value_list, attribute_possible_value_list, minimum_value_rating, maximum_value_rating, user_profile_attribute_list):
        '''
        Get the attribute rating vector determined by using the user profile.
        :param weight_vector: The weight vector specified in the user profile.
        :param attribute_value_list: List of attribute values.
        :param attribute_possible_value_list: List of attribute possible values.
        :param minimum_value_rating: The minimum rating value. 
        :param maximum_value_rating: The maximum rating value. 
        :return: A vector of attribute ratings.
        '''
        attribute_rating_vector = []
        # Determining the rating by attribute, by using he line through of the two points:
        for idx, weight_importance in enumerate(weight_vector):
            # Getting importance and weight values:
            weight_importance_list = str(weight_importance).split('|')
            importance_rank = None
            if len(weight_importance_list) > 1:
                importance_rank = str(weight_importance_list[0]).strip() 

            # If the attribute is relevant for the user:
            attribute_rating = 0
            if (importance_rank is None and user_profile_attribute_list[idx] == 'other'):
                # Rating with noise (randomly):
                attribute_rating = random.randint(minimum_value_rating, maximum_value_rating)
            elif importance_rank:
                # Determining position_array: the position of "attribute_value" in "possible_value_list". For example, for: possible_value_list = ['free', '$', '$$', '$$$', '$$$$'] and attribute_value = '$', the position_array = 1
                if isinstance(attribute_value_list[idx], list):                                
                    # Calculating attribute_rating of "y" for two points (x,y) in the line:
                    sum_attribute_rating = 0
                    for att_value in attribute_value_list[idx]:
                        position_array = attribute_possible_value_list[idx].index(att_value)
                        attribute_rating_aux = self.get_attribute_rating(position_array, minimum_value_rating, maximum_value_rating, attribute_possible_value_list[idx], importance_rank)
                        sum_attribute_rating += attribute_rating_aux
                    attribute_rating = sum_attribute_rating/len(attribute_value_list[idx])
                else:
                    # Calculating attribute_rating of "y" for one point (x,y) in the line:                              
                    position_array = attribute_possible_value_list[idx].index(attribute_value_list[idx])
                    attribute_rating = self.get_attribute_rating(position_array, minimum_value_rating, maximum_value_rating, attribute_possible_value_list[idx], importance_rank)
            else:
                # If the attribute is not relevant for the user (weight=0 without label (+) or (-)):                            
                attribute_rating = 0
            attribute_rating_vector.append(attribute_rating)
        return attribute_rating_vector
        
    def get_attribute_rating(self, position_array, minimum_value_rating, maximum_value_rating, possible_value_list, importance_rank):
        # sourcery skip: move-assign, none-compare
        '''
        Get the rating of attribute, when the importance of the attribute is given.
        :param position_array: The position of the attribute value in the list of attribute value possibles.
        :param minimum_value_rating: The minimum value of the rating.
        :param maximum_value_rating: The maximum value of the rating.
        :param possible_value_list: The list of attribute possible values.
        :param importance_rank: The label with the importance ranking (+) or (-).
        :return: The rating of attribute.
        '''
        # Determining input_score: the x of the point <x,y> inside the line
        input_score = position_array + 1
        # Determining min_score_normalized: the minimum value of rating
        min_score_normalized = minimum_value_rating
        min_score_input = min_score_normalized
        # Determining max_score_normalized: the maximum value of rating
        max_score_normalized = maximum_value_rating
        # Determining max_score_input: the number of possible values for the current attribute
        max_score_input = len(possible_value_list)        
        # Checking the importance ranking of the current attribute:
        if importance_rank == '(+)':            
            rating_attribute = self.compute_y(min_score_input, min_score_normalized, max_score_input, max_score_normalized, input_score)
        elif importance_rank == '(-)':            
            rating_attribute = self.compute_y(max_score_input, min_score_normalized, min_score_input, max_score_normalized, input_score)
        return rating_attribute

    def compute_y(self, x0, y0, x1, y1, x):
        '''
        Gets the line through of the two points. Specifically, computes the values of Y for a straight line that goes through (x0,y0) and (x1,y1).	 
	    :param x0: The X0 value.
	    :param y0: The Y0 value.
	    :param x1: The X1 value.
	 	:param y1: The Y1 value.
	    :param x: The X value.
	    :return: The values of y for a straight line that goes through (x0,y0) and (x1,y1).
        '''
        return y0 + ((y1 - y0) / (x1 - x0)) * (x - x0)
    
    def modify_rating_by_user_expectations(self, rating, k, user_rating_list, min_rating_value, max_rating_value):
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
            # Determining the percentage of variation, specified in the generation_config.conf file:
            percentage_rating_variation = self.access_generation_config.get_percentage_rating_variation()
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
