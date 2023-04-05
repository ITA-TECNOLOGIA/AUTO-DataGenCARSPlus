import pandas as pd


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
        up_vector_df = self.user_profile_df.loc[self.user_profile_df['user_profile_id'] == user_profile_id]
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


# rating_df:
user_profile_path = 'resources/data_schema/user_profile.csv'
user_profile_df = pd.read_csv(user_profile_path, encoding='utf-8', index_col=False, sep=',')

access = AccessUserProfile(user_profile_df)
# attribute_name_list, attribute_value_list = access.get_vector_from_user_profile(user_profile_id=1)
# print(attribute_name_list)
# print(attribute_value_list)
print(access.get_atribute_name_list_other())
print(access.get_atribute_name_list())