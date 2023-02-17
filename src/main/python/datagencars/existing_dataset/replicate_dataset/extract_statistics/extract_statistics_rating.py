import numpy as np
import pandas as pd

def replace_missing_values(df):
    """
    Replace missing values "NULL" and -1 with NaN
    """
    for k,v in {"NULL":np.nan,-1:np.nan}.items():
        df.replace(k, np.nan, inplace=True)
    return df

def count_unique(data):
    """
    Count unique users, items, contexts and timestamps
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
    filtered_ratings_df = data['rating'][data['rating']['user_id'] == selected_user] #Filter the ratings dataset by user
    total_count = len(filtered_ratings_df["item_id"])
    counts_items = filtered_ratings_df.groupby("item_id").size()
    unique_items = np.unique(filtered_ratings_df["item_id"]) #Obtain the unique values and convert them to list
    counts_items = filtered_ratings_df["item_id"].value_counts()

    return counts_items, unique_items, total_count

def calculate_vote_stats(data, selected_user):
    # Filter the ratings dataset by user
    if selected_user == "All users":
        filtered_ratings = data['rating']
    else:
        filtered_ratings = data['rating'][data['rating']['user_id'] == selected_user]

    # Calculate the vote standard deviation and average vote per user and for all of the users
    stats = {}
    if len(filtered_ratings) > 0:
        vote_std = filtered_ratings['rating'].std()
        user_avg_vote = filtered_ratings.groupby('user_id')['rating'].mean().to_dict()
        all_users_avg_vote = filtered_ratings['rating'].mean()

        stats["Vote standard deviation"] = f"{vote_std:.2f}"
        stats["Average vote for all users"] = f"{all_users_avg_vote:.2f}"
        if selected_user != "All users":
            stats[f"Average vote for user {selected_user}"] = f"{user_avg_vote[selected_user]:.2f}"
        
    return stats

