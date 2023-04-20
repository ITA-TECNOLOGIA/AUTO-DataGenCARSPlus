import pandas as pd
import math


class AccessContext:

    def __init__(self, context_df):
        self.context_df = context_df

    def get_context_id_list(self):
        '''
        Gets a list with unique values of context_id.
        :return: A list with unique values of context_id.
        '''        
        return sorted(self.context_df['context_id'].unique().tolist())

    def get_context_attribute_list(self):
        '''      
        Gets a list of context attributes.
        :return: A list of context attributes.
        '''
        return [col for col in self.context_df.columns if col != 'context_id']

    def get_context_value_from_context_attributte(self, context_id, attribute_name):
        '''
        Gets an context value from context_id and attribute name.
        :param context_id: The context ID.
        :param attribute_name: The attribute name.
        :return: An context value from context_id and attribute name.
        '''
        return self.context_df.loc[self.context_df['context_id'] == context_id, attribute_name].iloc[0]
    
    def get_context_possible_value_list_from_attributte(self, attribute_name):
        '''
        Gets a list of context possible values from a specific attribute.
        :param attribute_name: The attribute name.
        :return: A list of context possible values from a specific attribute.
        '''
        candidate_possible_value_list = self.context_df[attribute_name].unique().tolist()
        context_possible_value_list = [x for x in candidate_possible_value_list if not math.isnan(x)]        
        return sorted(context_possible_value_list)   
