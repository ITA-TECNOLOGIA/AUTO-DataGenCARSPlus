import pandas as pd


class AccessUser:

    def __init__(self, user_df):
        self.user_df = user_df

    def get_user_id_list(self):
        '''
        '''        
        return sorted(self.user_df['user_id'].unique().tolist())
    
    def get_user_attribute_list(self):
        '''
        
        '''
        return [col for col in self.user_df.columns if col != 'user_id']


# # user_df:
# user_path = 'resources/dataset_sts/user.csv'
# user_df = pd.read_csv(user_path, encoding='utf-8', index_col=False, sep=';')

# ac = AccessUser(user_df)
# # print('get_user_id_list: ', ac.get_user_id_list())
# # print('get_user_attribute_list: ', ac.get_user_attribute_list())
