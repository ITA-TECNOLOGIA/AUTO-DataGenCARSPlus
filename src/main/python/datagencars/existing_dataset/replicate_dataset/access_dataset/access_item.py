import math


class AccessItem:

    def __init__(self, item_df):
        self.item_df = item_df

    def get_item_list(self):
        '''     
        Gets a list with unique values of item_id.
        :return: A list with unique values of item_id.
        '''        
        return sorted(self.item_df['item_id'].unique().tolist())
    
    def get_item_attribute_list(self):
        '''
        Gets a list of item attributes.
        :return: A list of item attributes.
        '''
        return [col for col in self.item_df.columns if col != 'item_id']
    
    def get_item_value_from_item_attributte(self, item_id, attribute_name):
        '''
        Gets an item value from item_id and attribute name.
        :param item_id: The item ID.
        :param attribute_name: The attribute name.
        :return: The item value.
        '''               
        return self.item_df.loc[self.item_df['item_id'] == item_id, attribute_name].iloc[0]
    
    def get_item_possible_value_list_from_attributte(self, attribute_name):
        '''
        Gets a list of item possible values from a specific attribute.
        :param attribute_name: The attribute name.
        :return: A list of item possible values from an specific attribute.
        '''        
        candidate_possible_value_list = self.item_df[attribute_name].unique().tolist()
        if self.item_df[attribute_name].isna().any():
            item_possible_value_list = [x for x in candidate_possible_value_list if not math.isnan(x)]      
        else:
            item_possible_value_list = candidate_possible_value_list
        return sorted(item_possible_value_list)
    
