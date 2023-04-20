import pandas as pd
import math


class AccessContext:

    def __init__(self, context_df):
        self.context_df = context_df

    def get_context_id_list(self):
        '''
        '''        
        return sorted(self.context_df['context_id'].unique().tolist())

    def get_context_attribute_list(self):
        '''        
        '''
        return [col for col in self.context_df.columns if col != 'context_id']

    def get_context_value_from_context_attributte(self, context_id, attribute_name):
        '''
        '''
        return self.context_df.loc[self.context_df['context_id'] == context_id, attribute_name].iloc[0]
    
    def get_context_possible_value_list_from_attributte(self, attribute_name):
        '''
        '''
        candidate_possible_value_list = self.context_df[attribute_name].unique().tolist()
        context_possible_value_list = [x for x in candidate_possible_value_list if not math.isnan(x)]        
        return sorted(context_possible_value_list)
    

# # context_df:
# context_path = 'resources/dataset_sts/context.csv'
# context_df = pd.read_csv(context_path, encoding='utf-8', index_col=False, sep=';')

# ac = AccessContext(context_df)
# print('get_context_id_list: ', ac.get_context_id_list())
# print('get_context_attribute_list: ', ac.get_context_attribute_list())
# print(ac.get_context_possible_value_list_from_attributte(attribute_name='temperature'))
