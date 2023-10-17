from datagencars.existing_dataset.generate_rating import GenerateRating
import streamlit as st


class RecalculateRating(GenerateRating):
    """
    Recalculate ratings from an dataset, considering other desired user profiles.
    Input:
        [U]  user.csv
        [I]  item.csv
        [C]  context.csv <optional>
        [UP] user_profile.csv
        [R]  rating.csv
    Ouput:
        [R]  rating.csv <modified>        
    """

    def __init__(self, rating_df, user_profile_df, user_df, item_df, context_df=None):
        super().__init__(rating_df, user_profile_df, user_df, item_df, context_df)        
        self.with_context = False
        if 'context_id' in rating_df.columns:  
            # Identifying whether with_context:
            self.with_context = True
        # rating_df:
        self.rating_df = rating_df
        self.number_users = self.rating_df['user_id'].nunique()
        # Create a progress bar
        self.progress_bar = st.progress(0.0) 

    def recalculate_dataset(self, percentage_rating_variation=25, k=10):
        """
        Recalculate ratings from an dataset, considering other desired user profiles.            
        :param percentage_rating_variation: The percentage of rating variation.
        :param k: The k ratings to take in the past.
        :return: A new dataset with recalculate ratings.
        """        
        self.rating_df['rating'] = self.rating_df.apply(lambda row: self.recalculate_rating(row, percentage_rating_variation, k), axis=1)
        return self.rating_df

    def recalculate_rating(self, row, percentage_rating_variation, k):
        """
        Recalculate one rating, row by row in a dataframe.
        :param row: The current row in the dataframe that is being modified.
        :param percentage_rating_variation: The percentage of rating variation.
        :param k: The k ratings to take in the past.
        :return: The modified rating.
        """
        user_id = row['user_id']
        item_id = row['item_id']
        user_profile_id = self.access_user.get_user_profile_id_from_user_id(user_id)
        if user_profile_id == 0:
            user_profile_id = user_id
        if self.with_context:
            context_id = row['context_id']
            rating = self.get_rating(user_profile_id, item_id, context_id)
        else:
            rating = self.get_rating(user_profile_id, item_id)         
        # The minimum value rating.
        min_rating_value = self.access_rating.get_min_rating()
        # The maximum value rating.
        max_rating_value = self.access_rating.get_max_rating()
        user_rating_list=self.access_rating.get_rating_list_from_user(user_id=user_id)
        # Modifying the generated rating.
        modified_rating = self.modify_rating_by_user_expectations(rating, k, user_rating_list, min_rating_value, max_rating_value, percentage_rating_variation)        
        # Update the progress bar with each iteration            
        self.progress_bar.progress(text=f'Generating user {user_id} from {self.number_users}', value=(user_id) / self.number_users) 
        return modified_rating
