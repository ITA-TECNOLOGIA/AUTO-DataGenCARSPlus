import pandas as pd
import numpy as np
from datagencars.existing_dataset.generate_rating import GenerateRating
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_rating import ExtractStatisticsRating

class ReplicateDataset(GenerateRating):
    """
    Replicate an existing dataset.

    Input:
        [U]  user.csv
        [I]  item.csv
        [C]  context.csv <optional>
        [R]  rating.csv

    Algorithm:
        Precondition: If the dataset is a single file, it is expected to be divided into user.csv, item.csv, context.csv <optional> and ratings.csv.
        1- extract_statistics (extract_statistics_rating, extract_statistics_uic):
        2- generate_user_profile:
        3- replicate_dataset:

    Ouput:
        [R]  rating.csv <replicated>        
    """

    def __init__(self, rating_df, user_profile_df, item_df, context_df=None):
        super().__init__(rating_df, user_profile_df, item_df, context_df)
        # Determining statistics:
        self.rating_statistics = ExtractStatisticsRating(rating_df)

    def replicate_dataset(self, percentage_rating_variation=25, k=10):
        """
        Replicates an original dataset.
        :param percentage_rating_variation: The percentage of rating variation.
        :param k: The k ratings to take in the past.
        :return: A replicated dataset.
        """
        rating_df = None
        if self.rating_statistics.get_number_contexts() != 0:
            rating_df = pd.DataFrame(columns=['user_id', 'item_id', 'context_id', 'rating'])
        else:
            rating_df = pd.DataFrame(columns=['user_id', 'item_id', 'rating'])
               
        # The minimum value rating.
        min_rating_value = self.access_rating.get_min_rating()
        # The maximum value rating.
        max_rating_value = self.access_rating.get_max_rating()
        user_id_list = []
        item_id_list = []
        context_id_list = []
        rating_list = [] 
        for user_id in range(1, self.rating_statistics.get_number_users()+1):
            user_profile_id = user_id     
            #print('user_id: ', user_id)
            # Items:            
            original_item_id_list = self.access_rating.get_item_id_list_from_user(user_id=user_id)
            avg_items_df = self.rating_statistics.get_avg_items_by_user()
            avg_items = avg_items_df.loc[avg_items_df['user_id'] == int(user_id), 'avg_items'].iloc[0]
            std_items_df = self.rating_statistics.get_sd_items_by_user()
            std_items = std_items_df.loc[std_items_df['user_id'] == int(user_id), 'sd_items'].iloc[0]    
            minimum_item_id = min(original_item_id_list)
            maximum_item_id = max(original_item_id_list)        
            new_item_id_list = np.random.normal(loc=avg_items, scale=std_items, size=len(original_item_id_list))
            new_item_id_list = np.clip(new_item_id_list, minimum_item_id, maximum_item_id)  # clip values to min and max
            new_item_id_list = new_item_id_list.round().astype(int)  # round to integers            
            item_id_list.extend(new_item_id_list.tolist())
            # Contexts:
            if self.rating_statistics.get_number_contexts() != 0:
                original_context_id_list = self.access_rating.get_context_id_list_from_user(user_id=user_id)
                avg_contexts_df = self.rating_statistics.get_avg_contexts_by_user()
                avg_contexts = avg_contexts_df.loc[avg_contexts_df['user_id'] == int(user_id), 'avg_contexts'].iloc[0]
                std_contexts_df = self.rating_statistics.get_sd_contexts_by_user()
                std_contexts = std_contexts_df.loc[std_contexts_df['user_id'] == int(user_id), 'sd_contexts'].iloc[0]
                minimum_context_id = min(original_context_id_list)
                maximum_context_id = max(original_context_id_list) 
                new_context_id_list = np.random.normal(loc=avg_contexts, scale=std_contexts, size=len(original_context_id_list))
                new_context_id_list = np.clip(new_context_id_list, minimum_context_id, maximum_context_id)  # clip values to min and max
                new_context_id_list = new_context_id_list.round().astype(int)  # round to integers
                context_id_list.extend(new_context_id_list.tolist())                
            # Ratings:
            user_rating_list = []                        
            for idx, item_id in enumerate(new_item_id_list):                
                # Contexts:
                if self.rating_statistics.get_number_contexts() != 0:   
                    context_id=new_context_id_list[idx]             
                    rating = self.get_rating(user_profile_id, item_id, context_id)
                else:                
                    rating = self.get_rating(user_profile_id, item_id)                    
                # Generated rating.
                user_rating_list.append(rating)
                # Modifying the generated rating.                
                modified_rating = self.modify_rating_by_user_expectations(rating, k, user_rating_list, min_rating_value, max_rating_value, percentage_rating_variation)
                rating_list.append(modified_rating)
            # Users:
            k = len(original_item_id_list)
            user_id_list.extend([int(user_id)] * k)                            
        if rating_df.empty:
            rating_df['user_id'] = user_id_list
            rating_df['item_id'] = item_id_list
            if self.rating_statistics.get_number_contexts() != 0:
                rating_df['context_id'] = context_id_list
            rating_df['rating'] = rating_list           
        # Contexts:
        if self.rating_statistics.get_number_contexts() != 0:
            # Sorting and returning a rating_df by user_id and item_id.
            rating_df = rating_df.sort_values(by=['user_id', 'item_id', 'context_id'], ascending=[True, True, True], na_position='first')
        else:
            rating_df = rating_df.sort_values(by=['user_id', 'item_id'], ascending=[True, True], na_position='first')
        # Reseting index.
        rating_df.reset_index(drop=True, inplace=True)
        return rating_df
 