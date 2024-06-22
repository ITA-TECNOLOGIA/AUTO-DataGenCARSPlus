import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)


class CalculateAttributeRating:

    def __init__(self):
        pass

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
        if x1 == x0:
            return y0
        else:            
            return y0 + (((y1 - y0) / (x1 - x0)) * (x - x0))
