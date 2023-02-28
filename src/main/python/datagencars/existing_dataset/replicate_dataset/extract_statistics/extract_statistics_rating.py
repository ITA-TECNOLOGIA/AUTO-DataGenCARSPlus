import numpy as np
import pandas as pd

def replace_missing_values(df):
    """
    Replace missing values "NULL" and -1 with NaN
    :param df: The ratings dataset
    :return: The ratings dataset with missing values replaced
    """
    for k,v in {"NULL":np.nan,-1:np.nan}.items():
        df.replace(k, np.nan, inplace=True)
    return df

def count_unique(data):
    """
    Count unique users, items, contexts and timestamps
    :param data: The ratings dataset
    :return: The number of unique users, items, contexts and timestamps
    """
    unique_users = data["user_id"].nunique()
    unique_items = data["item_id"].nunique()
    unique_counts = {"Users": unique_users, "Items": unique_items}
    if 'context_id' in data.columns:
        unique_contexts = data["context_id"].nunique()
        unique_counts["Contexts"] = unique_contexts
    if 'timestamp' in data.columns:
        unique_timestamps = data["timestamp"].nunique()
        unique_counts["Timestamps"] = unique_timestamps
    unique_ratings = data["rating"].nunique()
    unique_counts["Ratings"] = unique_ratings
    unique_counts_df = pd.DataFrame.from_dict(unique_counts, orient='index', columns=['Count'])
    unique_counts_df.reset_index(inplace=True)
    unique_counts_df.rename(columns={"index": "Attribute name"}, inplace=True)

    return unique_counts_df

def count_items_voted_by_user(data, selected_user):
    """
    Count the number of items voted by a user
    :param data: The ratings dataset
    :param selected_user: The selected user
    :return: The number of items voted by the user
    """
    filtered_ratings_df = data[data['user_id'] == selected_user] #Filter the ratings dataset by user
    total_count = len(filtered_ratings_df["item_id"])
    counts_items = filtered_ratings_df.groupby("item_id").size()
    unique_items = np.unique(filtered_ratings_df["item_id"]) #Obtain the unique values and convert them to list
    counts_items = filtered_ratings_df["item_id"].value_counts()
    
    num_users = len(data["user_id"].unique())
    percent_ratings_by_user = (total_count / num_users) * 100
    
    return counts_items, unique_items, total_count, percent_ratings_by_user

def calculate_vote_stats(data, selected_user):
    """
    Calculate the vote standard deviation and average vote per user and for all of the users
    :param data: The ratings dataset
    :param selected_user: The selected user
    :return: The calculated statistics
    """
    # Filter the ratings dataset by user
    if selected_user == "All users":
        filtered_ratings = data
    else:
        filtered_ratings = data[data['user_id'] == selected_user]

    # Calculate the vote standard deviation and average vote per user and for all of the users
    stats = {}
    if len(filtered_ratings) > 0:
        vote_std = filtered_ratings['rating'].std()
        user_avg_vote = filtered_ratings.groupby('user_id')['rating'].mean().to_dict()
        all_users_avg_vote = filtered_ratings['rating'].mean()

        if selected_user != "All users":
            stats[f"Average vote for user {selected_user}"] = f"{user_avg_vote[selected_user]:.2f}"
            stats[f"Vote standard deviation for user {selected_user}"] = f"{vote_std:.2f}"
        else:
            stats["Average vote for all users"] = f"{all_users_avg_vote:.2f}"
            stats[f"Vote standard deviation for all users"] = f"{vote_std:.2f}"
        
    return stats
