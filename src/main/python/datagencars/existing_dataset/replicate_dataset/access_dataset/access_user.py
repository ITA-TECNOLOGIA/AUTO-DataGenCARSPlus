import logging


class AccessUser:

    def __init__(self, user_df):
        self.user_df = user_df

    def get_user_id_list(self):
        '''
        Gets a list with unique values of user_id.
        :return: A list with unique values of user_id.
        '''        
        return sorted(self.user_df['user_id'].unique().tolist())
    
    def get_user_attribute_list(self):
        '''
        Gets a list of user attributes.
        :return: A list of user attributes.
        '''
        return [col for col in self.user_df.columns if col != 'user_id']
