import pandas as pd
import numpy as np
import random


class AccessUserProfile():
    """
    Access the user profile values.
    @author Maria del Carmen Rodriguez-Hernandez 
    """
    def __init__(self, user_profile_df):
        self.user_profile_df = user_profile_df

    def get_vector_from_user_profile(self, user_profile_id):
        """
        Gets an attribute name list and a attribute value list for a specific user profile.
        :param user_profile_id: The ID of the user profile.
        :return: An attribute name list and a attribute value list for a specific user profile.
        """               
        up_vector_df = self.user_profile_df.loc[self.user_profile_df['user_profile_id'] == int(user_profile_id)]
        up_vector = up_vector_df.drop('user_profile_id', axis=1)
        # Get the column names:
        attribute_name_list = up_vector.columns.tolist()
        # Get the values for the single row:
        attribute_value_list = up_vector.values[0].tolist()
        return attribute_name_list, attribute_value_list
    
    def get_atribute_name_list_other(self):
        """
        Gets an attribute name list ignoring the attribute 'user_profile_id' and including the attribute 'other' of the user profile.
        :return: An attribute name list.
        """
        return [col for col in self.user_profile_df.columns if col != 'user_profile_id']     
    
    def get_atribute_name_list(self):
        """
        Gets an attribute name list ignoring the attribute 'user_profile_id' and 'other' of the user profile.
        :return: An attribute name list.
        """
        return [col for col in self.user_profile_df.columns if col not in ['user_profile_id', 'other']]
    
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
                elif attribute_value_list[idx] and not pd.isna(attribute_value_list[idx]):
                    # Calculating attribute_rating of "y" for one point (x,y) in the line:                              
                    position_array = attribute_possible_value_list[idx].index(attribute_value_list[idx])
                    attribute_rating = self.get_attribute_rating(position_array, minimum_value_rating, maximum_value_rating, attribute_possible_value_list[idx], importance_rank)
                else:
                    attribute_rating = 0
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
        rating_attribute = 0
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
