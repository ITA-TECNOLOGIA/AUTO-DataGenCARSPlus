import math
import pandas as pd


class AccessItem:

    def __init__(self, item_df):
        self.item_df = item_df

    def get_item_list(self):
        '''        
        '''
        return sorted(self.item_df['item_id'].unique().tolist())
    
    def get_item_attribute_list(self):
        '''        
        '''
        return [col for col in self.item_df.columns if col != 'item_id']
    
    def get_item_value_from_item_attributte(self, item_id, attribute_name):
        '''
        '''
        return self.item_df.loc[self.item_df['item_id'] == item_id, attribute_name].iloc[0]
    
    def get_item_possible_value_list_from_attributte(self, attribute_name):
        '''
        '''        
        candidate_possible_value_list = self.item_df[attribute_name].unique().tolist()
        item_possible_value_list = [x for x in candidate_possible_value_list if not math.isnan(x)]        
        return sorted(item_possible_value_list)
    

# # item_df:
# item_path = 'resources/dataset_sts/item.csv'
# item_df = pd.read_csv(item_path, encoding='utf-8', index_col=False, sep=';')

# ai = AccessItem(item_df)
# # print('get_item_list: ', ai.get_item_list())
# # print('get_item_attribute_list: ', ai.get_item_attribute_list())
# # print('get_item_value_from_item_attributte: ', ai.get_item_value_from_item_attributte(item_id=1, attribute_name='category1'))
# print('get_item_possible_value_list_from_attributte: ', ai.get_item_possible_value_list_from_attributte(attribute_name='category1'))
