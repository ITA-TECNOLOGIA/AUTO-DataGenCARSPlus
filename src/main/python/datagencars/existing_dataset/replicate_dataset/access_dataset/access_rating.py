import pandas as pd


class AccessRating:
        
    def __init__(self, ratings_df):
        self.ratings_df = ratings_df

    def get_min_rating(self):
        '''
        '''
        return self.ratings_df['rating'].min()
    
    def get_max_rating(self):
        '''
        '''
        return self.ratings_df['rating'].max()

    def get_user_id_list(self):
        '''
        '''        
        return sorted(self.ratings_df['user_id'].unique().tolist() )
    
    def get_item_id_list_from_user(self, user_id, unique_values=False):
        # sourcery skip: assign-if-exp, inline-immediately-returned-variable, lift-return-into-if
        '''
        '''   
        if unique_values:
            item_id_list = self.ratings_df.loc[self.ratings_df['user_id'] == user_id, 'item_id'].unique().tolist()
        else:
            item_id_list = self.ratings_df.loc[self.ratings_df['user_id'] == user_id, 'item_id'].tolist()
        return item_id_list
    
    def get_context_id_list_from_user(self, user_id, unique_values=False):
        # sourcery skip: assign-if-exp, inline-immediately-returned-variable, lift-return-into-if
        '''
        '''       
        if unique_values:
            context_id_list = self.ratings_df.loc[self.ratings_df['user_id'] == user_id, 'context_id'].unique().tolist()
        else:
            context_id_list = self.ratings_df.loc[self.ratings_df['user_id'] == user_id, 'context_id'].tolist()
        return context_id_list
    
    def get_rating_list_from_user(self, user_id):
        '''
        '''         
        return self.ratings_df.loc[self.ratings_df['user_id'] == user_id, 'rating'].tolist()
    
    def get_rating_list_from_user_item(self, user_id, item_id):
        '''
        '''        
        return self.ratings_df.loc[(self.ratings_df['user_id'] == user_id) & (self.ratings_df['item_id'] == item_id), 'rating'].tolist()
    
    def get_rating_list_from_user_item_context(self, user_id, item_id, context_id):
        '''
        '''        
        return self.ratings_df.loc[(self.ratings_df['user_id'] == user_id) & (self.ratings_df['item_id'] == item_id) & (self.ratings_df['context_id'] == context_id), 'rating'].tolist()
    

# # rating_df:
# rating_path = 'resources/dataset_sts/ratings.csv'
# ratings_df = pd.read_csv(rating_path, encoding='utf-8', index_col=False, sep=';')

# ar = AccessRating(ratings_df)

# # print('get_user_id_list: ', ar.get_user_id_list())
# # print('get_item_id_list_from_user: ', ar.get_item_id_list_from_user(user_id=1))
# # print('get_context_id_list_from_user: ', ar.get_context_id_list_from_user(user_id=1))
# # print('get_rating_list_from_user: ', ar.get_rating_list_from_user(user_id=1))
# # print('get_rating_list_from_user_item: ', ar.get_rating_list_from_user_item(user_id=1, item_id=1))
# # print('get_rating_list_from_user_item_context: ', ar.get_rating_list_from_user_item_context(user_id=1, item_id=1, context_id=1))

# print('get_min_rating: ', ar.get_min_rating())
# print('get_max_rating: ', ar.get_max_rating())