import random

import pandas as pd
from datagencars.existing_dataset.generate_rating import GenerateRating


class IncreaseRating(GenerateRating):
    """
    Extend an existing dataset.
    Input:
        [U]  user.csv
        [I]  item.csv
        [C]  context.csv <optional>
        [UP] user_profile.csv
        [R]  rating.csv
    Ouput:
        [R]  rating.csv <extended>        
    """

    def __init__(self, rating_df, user_profile_df, item_df, context_df=None):
        super().__init__(rating_df, user_profile_df, item_df, context_df)        
        self.with_context = False
        if 'context_id' in rating_df.columns:  
            # Identifying whether with_context:
            self.with_context = True
        # rating_df:
        self.rating_df = rating_df     

    def extend_rating_by_user(self, number_rating, percentage_rating_variation=25, k=10):
        """
        Generate N items by user.        
        :param number_rating: The number of ratings to generate for each user.
        :param percentage_rating_variation: The percentage of rating variation.
        :param k: The k ratings to take in the past.
        :return: A dataset with N ratings extended by user.
        """
        # Initial DataFrame setup
        extended_rating_df = self.rating_df.copy()
        # Getting all user_id existing in the rating file:
        user_id_list = self.access_rating.get_user_id_list()
        # Extending dataset by user:
        for user_id in user_id_list:
            # Generating N ratings for the current user:
            for _ in range(number_rating):
                # Getting items not seen by user_id:
                items_not_seen_list = self.get_items_not_seen_from_user(user_id)
                # Generating a new instance for the current user_id:
                new_instance = self.generate_new_instance(user_id, items_not_seen_list, percentage_rating_variation, k)
                # Convert the dictionary to a DataFrame
                new_instance_df = pd.DataFrame([new_instance])                
                # Adding new instance in the rating file:                
                extended_rating_df = pd.concat([extended_rating_df, new_instance_df], ignore_index=True).copy()
        return self.sort_rating_df(extended_rating_df)

    def extend_rating_random(self, number_rating, percentage_rating_variation=25, k=10):
        """
        Generate N ratings randomly.
        :param number_rating: The number of new ratings to be generated in the rating file.
        :param percentage_rating_variation: The percentage of rating variation.
        :param k: The k ratings to take in the past.
        :return: A dataset extended with N ratings randomly.
        """
        # Initial DataFrame setup                     
        extended_rating_df = self.rating_df.copy()
        # Getting all user_id existing in the rating file:
        user_id_list = self.access_rating.get_user_id_list()
        # Generating N ratings for the current user:
        for _ in range(number_rating):
            # Selecting a randomly user id:
            user_id = random.choice(user_id_list)
            print(f'User selected: {user_id}')
            # Getting items not seen by user_id:          
            items_not_seen_list = self.get_items_not_seen_from_user(user_id)            
            new_instance = self.generate_new_instance(user_id, items_not_seen_list, percentage_rating_variation, k)
            # Convert the dictionary to a DataFrame
            new_instance_df = pd.DataFrame([new_instance])
            # Adding new instance in the rating file:            
            extended_rating_df = pd.concat([extended_rating_df, new_instance_df], ignore_index=True).copy()
        return self.sort_rating_df(extended_rating_df)

    def generate_new_instance(self, user_id, items_not_seen_list, percentage_rating_variation, k):
        """
        Generates a new instance for the rating file.
        :param user_id: The user id.
        :param items_not_seen_list: The items not seen by user_id.
        :param percentage_rating_variation: The percentage of rating variation.
        :param k: The k ratings to take in the past.
        :return: The new instance for the rating file.
        """
        item_id = random.choice(items_not_seen_list)                
        if self.with_context:                    
            context_id_list = self.access_context.get_context_id_list()
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
        # New generated instance:
        new_instance = {}           
        if self.with_context:            
            new_instance = {'user_id': user_id, 'item_id': item_id, 'context_id': context_id, 'rating': modified_rating}
        else:
            new_instance = {'user_id': user_id, 'item_id': item_id, 'rating': modified_rating}
        return new_instance

    def get_items_not_seen_from_user(self, user_id):
        """
        Gets the items not seen by the specified user_id.
        :param user_id:
        :return: The items not seen by the specified user_id.
        """
        items_not_seen_list = []
        # Fetching the list of items that this user has already rated:
        original_item_id_list = self.access_rating.get_item_id_list_from_user(user_id=user_id)
        all_item_id_list = self.access_item.get_item_list()
        # Excluding the items that the user has already rated:
        items_not_seen_list = list(set(all_item_id_list) - set(original_item_id_list))
        # If the user has seen all the items, he/she may be able to see the items again.
        if len(items_not_seen_list) == 0:
            items_not_seen_list = all_item_id_list
        return items_not_seen_list
    
    def sort_rating_df(self, rating_df):
        """
        Sort the rating dataframe by column.
        :param rating_df: The rating dataframe.
        :return: The sorted rating dataframe.
        """
        # Sorting and resetting index
        sort_columns = ['user_id', 'item_id', 'rating']
        if 'context_id' in rating_df.columns:
            sort_columns.insert(2, 'context_id')
        sorted_rating_df = rating_df.sort_values(by=sort_columns)
        sorted_rating_df.reset_index(drop=True, inplace=True) 
        return sorted_rating_df
