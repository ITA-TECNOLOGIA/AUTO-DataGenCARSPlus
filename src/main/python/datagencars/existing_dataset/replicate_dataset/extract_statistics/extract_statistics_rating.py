import numpy as np
import pandas as pd
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics import ExtractStatistics


class ExtractStatisticsRating(ExtractStatistics):

    def __init__(self, rating_df):
        super().__init__(rating_df)
    
    def get_number_ratings(self):
        """
        Gets the number of ratings.
        :return: The number of ratings.
        """
        return self.df.shape[0]  

    def get_number_users(self):
        """
        Gets the number total of users.
        :return: The number total of users.
        """
        return self.df['user_id'].nunique()
    
    def get_number_items(self):
        """
        Gets the number total of items.
        :return: The number total of items.
        """
        return self.df['item_id'].nunique()
    
    def get_number_contexts(self):
        """
        Gets the number total of contexts.
        :return: The number total of contexts.
        """
        return self.df['context_id'].nunique() if 'context_id' in self.df else 0
    
    def get_number_ratings_by_user(self):
        """
        Gets the number ratings by user.
        :return: The number ratings by user.
        """
        count_serie = self.df['user_id'].value_counts()        
        # Convert the Series to a self.dfFrame and reset the index:
        df = count_serie.to_frame().reset_index()
        # Rename the columns:
        df.columns = ['user_id', 'count_ratings']
        return df    
    
    def get_percentage_ratings_by_user(self):
        """
        Gets percentage of ratings by user.
        :return: The percentage of ratings by user.
        """
        number_ratings_by_user_df = self.get_number_ratings_by_user() 
        number_ratings_by_user_df['percentage_ratings'] = number_ratings_by_user_df['count_ratings'].apply(lambda x: (x*100)/self.get_number_ratings())
        percentage_ratings_by_user_df = number_ratings_by_user_df[['user_id', 'percentage_ratings']]
        # Round the float column to two decimal places:
        df = percentage_ratings_by_user_df.copy()
        df['percentage_ratings'] = df['percentage_ratings'].round(2)
        return df
    
    def get_avg_ratings_by_user(self):
        """
        Gets the average of ratings by user.
        :return: The average of ratings by user.
        """        
        avg_ratings_serie = self.df.groupby('user_id')['rating'].mean()
        # Convert the Series to a self.dfFrame and reset the index:
        df = avg_ratings_serie.to_frame().reset_index()
        # Rename the columns:
        df.columns = ['user_id', 'avg_ratings']
        return df.round(2)
    
    def get_variance_ratings_by_user(self):
        """
        Gets the variance of ratings by user.
        :return: The variance of ratings by user.
        """   
        variance_serie = self.df.groupby('user_id')['rating'].var()
        # Convert the Series to a self.dfFrame and reset the index:
        variance_df = variance_serie.to_frame().reset_index()
        # Rename the columns:
        variance_df.columns = ['user_id', 'variance_ratings']
        # Round the float column to two decimal places:
        variance_df['variance_ratings'] = variance_df['variance_ratings'].round(2)
        return variance_df
    
    def get_sd_ratings_by_user(self):
        """
        Gets the standard deviation of ratings by user.
        :return: The standard deviation of ratings by user.
        """
        # Group the self.dfframe by 'Group' column and apply the lambda function to the 'Values' column:
        sd_serie = self.df.groupby('user_id')['rating'].apply(lambda x: np.std(x))
        # Convert the Series to a self.dfFrame and reset the index:
        sd_df = sd_serie.to_frame().reset_index()
        # Rename the columns:
        sd_df.columns = ['user_id', 'sd_ratings']
        # Round the float column to two decimal places:
        sd_df['sd_ratings'] = sd_df['sd_ratings'].round(2)
        return sd_df
        
    def get_number_items_from_user(self, selected_user):
        """
        Gets the number of items rated by a user.
        :param selected_user: The selected user.
        :return: The number of items rated by the user.
        """        
        filtered_ratings_df = self.df[self.df['user_id'] == selected_user] # Filter the ratings self.dfset by user.
        total_count = len(filtered_ratings_df["item_id"])
        counts_items = filtered_ratings_df.groupby("item_id").size()
        unique_items = np.unique(filtered_ratings_df["item_id"]) # Obtain the unique values and convert them to list.
        counts_items = filtered_ratings_df["item_id"].value_counts()        
        return counts_items, unique_items, total_count
        
    def get_avg_items_by_user(self):
        """
        Gets the average of items by user.
        :return: The average of items by user.
        """   
        sum_serie = self.df.groupby('user_id')['item_id'].sum()        
        # Convert the Series to a self.dfFrame and reset the index:
        sum_df = sum_serie.to_frame().reset_index()
        # Rename the columns:
        sum_df.columns = ['user_id', 'sum']        
        sum_df['avg_items'] = sum_df['sum'].apply(lambda x: x/self.get_number_items())
        # Round the float column to two decimal places:
        sum_df['avg_items'] = sum_df['avg_items'].round(2)
        return sum_df[['user_id', 'avg_items']]
            
    def get_variance_items_by_user(self):
        """
        Gets the variance of items by user.
        :return: The variance of items by user.
        """   
        variance_serie = self.df.groupby('user_id')['item_id'].var()
        # Convert the Series to a self.dfFrame and reset the index:
        variance_df = variance_serie.to_frame().reset_index()
        # Rename the columns:
        variance_df.columns = ['user_id', 'variance_items']
        # Round the float column to two decimal places:
        variance_df['variance_items'] = variance_df['variance_items'].round(2)
        return variance_df
    
    def get_sd_items_by_user(self):
        """
        Gets the standard deviation of items by user.
        :return: The standard deviation of items by user.
        """
        # Group the self.dfframe by 'Group' column and apply the lambda function to the 'Values' column:
        sd_serie = self.df.groupby('user_id')['item_id'].apply(lambda x: np.std(x))
        # Convert the Series to a self.dfFrame and reset the index:
        sd_df = sd_serie.to_frame().reset_index()
        # Rename the columns:
        sd_df.columns = ['user_id', 'sd_items']
        # Round the float column to two decimal places:
        sd_df['sd_items'] = sd_df['sd_items'].round(2)
        return sd_df
    
    def get_number_not_repeated_items_by_user(self):
        """
        Gets the number of items not repeated by user.
        :return: The number of items not repeated by user. If the user_id does not have any repeated items, then it will have a value of 0.
        """
        # Group by 'Group' column and count the number of not repeated values in 'Values' column:
        not_repeated_items_series = self.df.groupby('user_id')['item_id'].value_counts().loc[lambda x: x==1].groupby(level=0).count()
        # Convert the Series to a self.dfFrame and reset the index:
        not_repeated_items_df = not_repeated_items_series.to_frame().reset_index()
        # Rename the columns:
        not_repeated_items_df.columns = ['user_id', 'not_repeated_items']
        # Merge self.dfframes on 'user_id' column:
        merged_df = pd.merge(not_repeated_items_df[['user_id', 'not_repeated_items']], self.df[['user_id']], on='user_id', how='outer')
        # Fill missing values with 0:
        merged_df['not_repeated_items'] = merged_df['not_repeated_items'].fillna(0)
        # Drop duplicates:
        merged_df = merged_df.drop_duplicates()
        # Casting: float to int.
        merged_df['not_repeated_items'] = merged_df['not_repeated_items'].astype(int)
        return merged_df.sort_values(by='user_id')
    
    def get_percentage_not_repeated_items_by_user(self):
        """
        Gets the porcentage of items not repeated by user.
        :return: The porcentage of items not repeated by user. If the user_id does not have any repeated items, then it will have a value of 0.
        """
        not_repeated_items_df = self.get_number_not_repeated_items_by_user()
        number_items_by_user_df = self.get_number_ratings_by_user()
        # Merge self.dfframes on 'user_id' column:
        merged_df = pd.merge(not_repeated_items_df[['user_id', 'not_repeated_items']], number_items_by_user_df[['user_id', 'count_ratings']], on='user_id', how='outer')
        # Calculate percentage
        merged_df['percentage_not_repeated_items'] = ((merged_df['not_repeated_items']*100)/merged_df['count_ratings'])
        # Round the float column to two decimal places:
        merged_df['percentage_not_repeated_items'] = merged_df['percentage_not_repeated_items'].round(2)
        # Drop two columns in place:
        merged_df.drop(columns=['not_repeated_items', 'count_ratings'], inplace=True)        
        return merged_df
        
    def get_percentage_repeated_items_by_user(self):
        """
        Gets the porcentage of items repeated by user.
        :return: The porcentage of items repeated by user.
        """
        not_repeated_items_df = self.get_number_not_repeated_items_by_user()
        number_items_by_user_df = self.get_number_ratings_by_user()
        # Merge self.dfframes on 'user_id' column:
        merged_df = pd.merge(not_repeated_items_df[['user_id', 'not_repeated_items']], number_items_by_user_df[['user_id', 'count_ratings']], on='user_id', how='outer')
        merged_df['repeated_items'] = merged_df['count_ratings'] - merged_df['not_repeated_items']

        # Calculate percentage
        merged_df['porcentage_repeated_items'] = ((merged_df['repeated_items']*100)/merged_df['count_ratings'])
        # Round the float column to two decimal places:
        merged_df['porcentage_repeated_items'] = merged_df['porcentage_repeated_items'].round(2)
        # Drop two columns in place:
        merged_df.drop(columns=['not_repeated_items', 'count_ratings', 'repeated_items'], inplace=True)
        return merged_df
    
    def get_avg_contexts_by_user(self):
        """
        Gets the average of contexts by user.
        :return: The average of contexts by user.
        """   
        sum_serie = self.df.groupby('user_id')['context_id'].sum()        
        # Convert the Series to a self.dfFrame and reset the index:
        sum_df = sum_serie.to_frame().reset_index()
        # Rename the columns:
        sum_df.columns = ['user_id', 'sum']       
        sum_df['avg_contexts'] = sum_df['sum'].apply(lambda x: x/self.get_number_contexts())
        # Round the float column to two decimal places:
        sum_df['avg_contexts'] = sum_df['avg_contexts'].round(2)
        return sum_df[['user_id', 'avg_contexts']]
    
    def get_variance_contexts_by_user(self):
        """
        Gets the variance of contexts by user.
        :return: The variance of contexts by user.
        """
        variance_serie = self.df.groupby('user_id')['context_id'].var()
        # Convert the Series to a self.dfFrame and reset the index:
        variance_df = variance_serie.to_frame().reset_index()
        # Rename the columns:
        variance_df.columns = ['user_id', 'variance_contexts']
        # Round the float column to two decimal places:
        variance_df['variance_contexts'] = variance_df['variance_contexts'].round(2)
        return variance_df
        
    def get_sd_contexts_by_user(self):
        """
        Gets the standard deviation of contexts by user.
        :return: The standard deviation of contexts by user.
        """
        # Group the self.dfframe by 'Group' column and apply the lambda function to the 'Values' column:
        sd_serie = self.df.groupby('user_id')['context_id'].apply(lambda x: np.std(x))
        # Convert the Series to a self.dfFrame and reset the index:
        sd_df = sd_serie.to_frame().reset_index()
        # Rename the columns:
        sd_df.columns = ['user_id', 'sd_contexts']
        # Round the float column to two decimal places:
        sd_df['sd_contexts'] = sd_df['sd_contexts'].round(2)
        return sd_df
    
    def get_number_not_repeated_contexts_by_user(self):
        """
        Gets the number of contexts not repeated by user.
        :return: The number of contexts not repeated by user. If the user_id does not have any repeated contexts, then it will have a value of 0.
        """
        # Group by 'Group' column and count the number of not repeated values in 'Values' column:
        not_repeated_contexts_series = self.df.groupby('user_id')['context_id'].value_counts().loc[lambda x: x==1].groupby(level=0).count()
        # Convert the Series to a self.dfFrame and reset the index:
        not_repeated_contexts_df = not_repeated_contexts_series.to_frame().reset_index()
        # Rename the columns:
        not_repeated_contexts_df.columns = ['user_id', 'not_repeated_contexts']
        # Merge self.dfframes on 'user_id' column:
        merged_df = pd.merge(not_repeated_contexts_df[['user_id', 'not_repeated_contexts']], self.df[['user_id']], on='user_id', how='outer')
        # Fill missing values with 0:
        merged_df['not_repeated_contexts'] = merged_df['not_repeated_contexts'].fillna(0)
        # Drop duplicates:
        merged_df = merged_df.drop_duplicates()
        # Casting: float to int.
        merged_df['not_repeated_contexts'] = merged_df['not_repeated_contexts'].astype(int)
        return merged_df.sort_values(by='user_id')

    def get_percentage_not_repeated_contexts_by_user(self):
        """
        Gets the porcentage of contexts not repeated by user.
        :return: The porcentage of contexts not repeated by user. If the user_id does not have any repeated contexts, then it will have a value of 0.
        """
        not_repeated_contexts_df = self.get_number_not_repeated_contexts_by_user()
        number_contexts_by_user_df = self.get_number_ratings_by_user()
        # Merge self.dfframes on 'user_id' column:
        merged_df = pd.merge(not_repeated_contexts_df[['user_id', 'not_repeated_contexts']], number_contexts_by_user_df[['user_id', 'count_ratings']], on='user_id', how='outer')
        # Calculate percentage
        merged_df['percentage_not_repeated_contexts'] = ((merged_df['not_repeated_contexts']*100)/merged_df['count_ratings'])
        # Round the float column to two decimal places:
        merged_df['percentage_not_repeated_contexts'] = merged_df['percentage_not_repeated_contexts'].round(2)
        # Drop two columns in place:
        merged_df.drop(columns=['not_repeated_contexts', 'count_ratings'], inplace=True)        
        return merged_df    
        
    def get_percentage_repeated_contexts_by_user(self):
        """
        Gets the porcentage of contexts repeated by user.
        :return: The porcentage of contexts repeated by user.
        """
        not_repeated_contexts_df = self.get_number_not_repeated_contexts_by_user()
        number_contexts_by_user_df = self.get_number_ratings_by_user()
        # Merge self.dfframes on 'user_id' column:
        merged_df = pd.merge(not_repeated_contexts_df[['user_id', 'not_repeated_contexts']], number_contexts_by_user_df[['user_id', 'count_ratings']], on='user_id', how='outer')
        merged_df['repeated_contexts'] = merged_df['count_ratings'] - merged_df['not_repeated_contexts']

        # Calculate percentage
        merged_df['porcentage_repeated_contexts'] = ((merged_df['repeated_contexts']*100)/merged_df['count_ratings'])
        # Round the float column to two decimal places:
        merged_df['porcentage_repeated_contexts'] = merged_df['porcentage_repeated_contexts'].round(2)
        # Drop two columns in place:
        merged_df.drop(columns=['not_repeated_contexts', 'count_ratings', 'repeated_contexts'], inplace=True)
        return merged_df    
