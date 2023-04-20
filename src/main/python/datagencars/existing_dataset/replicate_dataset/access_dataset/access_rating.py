import logging


class AccessRating:
        
    def __init__(self, ratings_df):
        self.ratings_df = ratings_df

    def get_min_rating(self):
        '''
        Gets the minimum rating value.
        :return: The minimum rating value.
        '''
        return self.ratings_df['rating'].min()
    
    def get_max_rating(self):
        '''
        Gets the maximum rating value.
        :return: The maximum rating value.
        '''
        return self.ratings_df['rating'].max()

    def get_user_id_list(self):
        '''
        Gets a list with unique values of user_id.
        :return: A list with unique values of user_id.
        '''        
        return sorted(self.ratings_df['user_id'].unique().tolist() )
    
    def get_item_id_list_from_user(self, user_id, unique_values=False):
        # sourcery skip: assign-if-exp, inline-immediately-returned-variable, lift-return-into-if
        '''
        Gets a list of item_id from a specific user.
        :param user_id: The user ID.
        :param unique_values: If unique_values=True, get only the unique values of the item_id column and current user (user_id). Default: unique_values=False.
        :raturn: A list of item_id from specific user.
        '''   
        if unique_values:
            item_id_list = self.ratings_df.loc[self.ratings_df['user_id'] == user_id, 'item_id'].unique().tolist()
        else:
            item_id_list = self.ratings_df.loc[self.ratings_df['user_id'] == user_id, 'item_id'].tolist()
        return item_id_list
    
    def get_context_id_list_from_user(self, user_id, unique_values=False):
        # sourcery skip: assign-if-exp, inline-immediately-returned-variable, lift-return-into-if
        '''
        Gets a list of context_id from a specific user.
        :param user_id: The user ID.
        :param unique_values: If unique_values=True, get only the unique values of the context_id column and current user (user_id). Default: unique_values=False.
        :raturn: A list of context_id from specific user.
        '''       
        if unique_values:
            context_id_list = self.ratings_df.loc[self.ratings_df['user_id'] == user_id, 'context_id'].unique().tolist()
        else:
            context_id_list = self.ratings_df.loc[self.ratings_df['user_id'] == user_id, 'context_id'].tolist()
        return context_id_list
    
    def get_rating_list_from_user(self, user_id):
        '''
        Gets a list of ratings from a specific user.
        :param user_id: The user ID.
        :return: A list of ratings from a specific user.
        '''         
        return self.ratings_df.loc[self.ratings_df['user_id'] == user_id, 'rating'].tolist()
    
    def get_rating_list_from_user_item(self, user_id, item_id):
        '''
        Gets a list of ratings from a specific user and item.
        :param user_id: The user ID.
        :param item_id: The item ID.
        :return: A list of ratings from a specific user and item.
        '''        
        return self.ratings_df.loc[(self.ratings_df['user_id'] == user_id) & (self.ratings_df['item_id'] == item_id), 'rating'].tolist()
    
    def get_rating_list_from_user_item_context(self, user_id, item_id, context_id):
        '''
        Gets a list of ratings from a specific user, item and context.
        :param user_id: The user ID.
        :param item_id: The item ID.
        :param context_id: The context ID.
        :return: A list of ratings from a specific user, item and context.
        '''        
        return self.ratings_df.loc[(self.ratings_df['user_id'] == user_id) & (self.ratings_df['item_id'] == item_id) & (self.ratings_df['context_id'] == context_id), 'rating'].tolist()  
