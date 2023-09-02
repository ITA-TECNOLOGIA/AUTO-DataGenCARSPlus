import random


class CastRating:
    """
    Processes and converts different types of ratings (binary or preferencial) in a DataFrame.
    INPUT:
        [R] rating.csv
    OUTPUT:
        [R] rating.csv (modified)
    """

    def __init__(self, rating_df):        
        self.rating_df = rating_df

    def rating_preferencial_to_binary(self, threshold=3):
        """
        Transforms ratings based on value ranges (e.g., [1-5]) to binary values (e.g., [0-1]), by applying a threshold.
        :param threshold: The rating threshold.
        :return: A dataframe with binary ratings.
        """
        def binary_rating(rating):
            return 1 if rating >= threshold else 0        
        self.rating_df['rating'] = self.rating_df['rating'].apply(binary_rating)
        return self.rating_df
    
    def rating_binary_to_preferencial(self, scale=5, threshold=3):
        """
        Transforms binary ratings (0/1) to preferential ratings (1-5) based on a specified scale and theshold.
        :param scale: The scale for the preferential ratings (e.g., 5 for 1-5 scale).
        :param threshold: The rating threshold (e.g., scale=5 and threshold=3, rating 0--> [1, 2] and 1 --> [3, 4, 5]).
        :return: A dataframe with preferential ratings.
        """
        def preferential_rating(rating):            
            if rating == 1:
                candidate_rating_list = list(range(threshold, scale + 1))                
            elif rating == 0: 
                candidate_rating_list = list(range(1, threshold))
            return random.choice(candidate_rating_list)            
        self.rating_df['rating'] = self.rating_df['rating'].apply(preferential_rating)
        return self.rating_df

    def is_binary_rating(self):
        """
        Check if the 'rating' column has only two unique values (binary ratings: 1/0, 'yes'/'no', 'me gusta'/'no me gusta', ...).     
        :return: True if the 'rating' column has only two unique values, False otherwise.
        """
        unique_values = self.rating_df['rating'].dropna().unique()
        return len(unique_values) == 2
    
    def is_preferencial_rating(self):
        """
        Check if the 'rating' column has more than two unique values (preferencial ratings: 1-5, 1-10, ...).     
        :return: True if the 'rating' column has more than two unique values, False otherwise.
        """
        unique_values = self.rating_df['rating'].dropna().unique()
        return len(unique_values) > 2
    
    def set_binary_rating_label(self, label_1, label_0):        
        """
        Set binary rating value of a dataframe by labels (1 --> 'like', 0 --> 'dislike').
        :param label_1: The label to use for setting a rating of 1 ('like').
        :param label_0: The label to use for setting a rating of 0 ('dislike').
        """
        # Convert labels to lowercase to make the comparison case-insensitive
        label_1 = label_1.lower()
        label_0 = label_0.lower()
        # Set values based on the labels:          
        self.rating_df['rating'] = self.rating_df['rating'].apply(lambda x: label_1 if x == 1 else (label_0 if x == 0 else x))     
        return self.rating_df
