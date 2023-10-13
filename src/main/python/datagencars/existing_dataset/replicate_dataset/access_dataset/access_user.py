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
    
    def is_user_profile_id(self):
        """
        Check if the 'user_df' dataframe has a column named 'user_profile_id'.
        :return: True if the 'user_df' dataframe contains a 'user_profile_id' column, False otherwise.
        """
        if_user_profile_id = False
        if 'user_profile_id' in self.user_df.columns:
            if_user_profile_id = True
        return if_user_profile_id

    def get_count_user_profile_id(self):
        """
        Get the count of unique values in the 'user_profile_id' column of the 'user_df' dataframe.
        :return: The count of unique 'user_profile_id' values if the column exists, or 0 if it doesn't.
        """        
        count_user_profile_id = 0
        if self.is_user_profile_id():
            count_user_profile_id = self.user_df['user_profile_id'].nunique()
        return count_user_profile_id
