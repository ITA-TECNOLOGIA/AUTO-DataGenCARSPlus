import os

import altair as alt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_rating import ExtractStatisticsRating
from matplotlib import pyplot as plt
from streamlit_app import config
from streamlit_app.preprocess_dataset import wf_util


def show_information(rating_df, with_context):
    """
    Shows information and statistics about the rating DataFrame.
    :param rating_df: The DataFrame containing ratings.
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    """    
    if not rating_df.empty:
        # Title:    
        st.header(config.RATING_TYPE.title())
        
        # Show dataframe:
        with st.expander(label=f'Show the {config.RATING_TYPE}.csv file'):
            st.dataframe(rating_df)

        # Extracted statistics:
        extract_statistics = ExtractStatisticsRating(rating_df=rating_df)
        # Showing general statistics:        
        show_general_statistics(with_context, extract_statistics)               
        # Showing attributes, data types and value ranges:
        show_data_types(extract_statistics)
        # Showing histogram of ratings:
        show_rating_histogram(rating_df)
        # Showing the rating statistics:
        show_rating_statistics(with_context, rating_df)
        # Showing number of items by user:
        show_items_by_user(rating_df)
        
        # Showing statistics per user:
        st.header("Statistics per user")
        user_id_list = list(rating_df['user_id'].unique())                    
        selected_user = st.selectbox(label="Select a user:", options=user_id_list, key="selected_user_id")           
        # Showing the evolution of a user's preferences or interests through time:
        show_user_preference_evolution(selected_user, rating_df)
        # Showing item statistics:
        show_item_statistics_from_user(selected_user, extract_statistics)
        # Showing context statistics:
        show_context_statistics_from_user(selected_user, extract_statistics, with_context)
        # Showing rating statistics:
        show_rating_statistics_from_user(selected_user, extract_statistics)        
    else:
        st.warning(f"The rating file ({config.RATING_TYPE}.csv) has not been uploaded.")

def show_general_statistics(with_context, extract_statistics):
    """
    Shows general statistics.
    :param with_context: True if the file to be generated will be contextual and False in the otherwise.
    :param extract_statistics: Instance of ExtractStatisticsRating class.
    :return: A dataframe with general statistics.
    """
    st.header("General statistics")
    unique_users = extract_statistics.get_number_users()
    unique_items = extract_statistics.get_number_items()
    unique_counts = {"Users": unique_users, "Items": unique_items}
    if with_context:
        unique_contexts = extract_statistics.get_number_contexts()
        unique_counts["Contexts"] = unique_contexts
    unique_ratings = extract_statistics.get_number_ratings()
    unique_counts["Ratings"] = unique_ratings
    general_statistics_df = pd.DataFrame.from_dict(unique_counts, orient='index', columns=['Count'])
    general_statistics_df.reset_index(inplace=True)
    general_statistics_df.rename(columns={"index": "Attribute name"}, inplace=True)                    
    st.table(general_statistics_df)
    return general_statistics_df

def show_data_types(extract_statistics):
    """
    Shows attributes, data types and value ranges of the dataframe.
    :param extract_statistics: The object to extract general statistics.
    :return: A dataframe with information related to attributes, data types and value ranges.
    """    
    st.header("Attributes, data types and value ranges")
    data_type_df = extract_statistics.get_attributes_and_ranges()
    st.table(pd.DataFrame(data_type_df, columns=["Attribute name", "Data type", "Value ranges"]))
    return data_type_df

def show_rating_histogram(rating_df):
    """
    Shows a histogram of ratings.
    :param rating_df: The rating dataframe.
    """
    st.header("Histogram of ratings")
    # Count the frequency of each rating:
    counts = np.bincount(rating_df['rating'])[np.nonzero(np.bincount(rating_df['rating']))] 
    histogram_df = pd.DataFrame({'Type of ratings': np.arange(1, len(counts) + 1), 'Number of ratings': counts})
    chart = alt.Chart(histogram_df).mark_bar(color='#0099CC').encode(x=alt.X('Type of ratings:O', axis=alt.Axis(title='Type of ratings')), y=alt.Y('Number of ratings:Q', axis=alt.Axis(title='Number of ratings')), tooltip=['Type of ratings', 'Number of ratings']) # .properties(title={'text': 'Histogram of ratings', 'fontSize': 16,})
    st.altair_chart(chart, use_container_width=True)

def show_rating_statistics(with_context, rating_df):
    """
    Show some rating statistics.
    :param with_context: True if the file to be generated will be contextual and False in the otherwise.
    :param rating_df: The rating dataframe.
    :return: A dataframe with rating statistics.
    """    
    summary_df = rating_df.describe()    
    if with_context:        
        summary_df = summary_df.drop(columns=['user_id', 'item_id', 'context_id'])
    else:        
        summary_df = summary_df.drop(columns=['user_id', 'item_id'])
    if 'timestamp' in summary_df.columns:
        summary_df = summary_df.drop(columns=['timestamp'])
    # Showing user_item_count_df:
    rating_summary_df = summary_df.T
    with st.expander(label='More details'):        
        st.dataframe(rating_summary_df)        
    return rating_summary_df

def show_items_by_user(rating_df):
    """
    Shows the number of items by user.
    :param rating_df: The rating dataframe.
    :return: A dataframe with the information related to the number of items by user.
    """
    st.header("Histogram of items by user")
    # Group data by user and count the number of items for each user
    user_item_count_df = rating_df.groupby('user_id')['item_id'].count().reset_index()    
    user_item_count_df.columns = ['User', 'Number of items']
    # Allow user to select sorting order
    sort_order = st.selectbox(label="Sort", options=["none", "asc", "desc"])
    # Sort the DataFrame based on user choice
    if sort_order == "asc":
        user_item_count_df = user_item_count_df.sort_values(by='Number of items', ascending=True)
    elif sort_order == "desc":
        user_item_count_df = user_item_count_df.sort_values(by='Number of items', ascending=False)
    # Create a bar chart using Altair
    chart = alt.Chart(user_item_count_df).mark_bar().encode(x=alt.X('User:N', sort=None), y='Number of items:Q', tooltip=['User:N', 'Number of items:Q']).properties(width=600, height=400) # title=f'Histogram of the number of items rated by user', 
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
    # Showing user_item_count_df:
    with st.expander(label='Show a table with the number of items by user'):
        st.dataframe(user_item_count_df)
        wf_util.save_df(df_name='number_items_by_user', df_value=user_item_count_df, extension='csv')
    return user_item_count_df

def show_user_preference_evolution(user_id, rating_df):
    """
    Showing the evolution of a user's preferences or interests through time.
    :param user_id: The current user.
    :param rating_df: The rating dataframe.    
    """
    if 'timestamp' in rating_df.columns:        
        # Filter data for the selected user:
        user_data_df = rating_df.loc[rating_df['user_id'] == user_id].copy()    
        # If the ratings are not integers:
        user_data_df['rating'] = user_data_df['rating'].round(0)
        # Check the data type of the timestamp column (timestamp or date values):
        column_dtype = rating_df['timestamp'].dtype     
        
        # Check if timestamp column contains timestamp values:
        if column_dtype == 'datetime64[ns]' or column_dtype == 'datetime64[ns, UTC]' or column_dtype == 'int64':            
            # Convert 'timestamp' to datetime format:
            user_data_df['timestamp'] = pd.to_datetime(user_data_df['timestamp'], unit='s')                    
            user_data_df['timestamp'] = user_data_df['timestamp'].dt.date
        else:            
            # In this case, the column value are dates (not timestamps):
            user_data_df['timestamp'] = pd.to_datetime(user_data_df['timestamp']).dt.date    
        # Set the size of the Matplotlib figure (adjust width and height as needed)
        plt.figure(figsize=(10, 8))
        # Display user preference evolution image:
        fig = sns.boxplot(data=user_data_df, x="timestamp", y="rating")        
        # Set Y-axis ticks to display all unique rating values:
        plt.yticks(user_data_df['rating'].unique(), fontsize=10)
        # Set X-axis labels to display only the text of dates and rotate them vertically
        date_labels = user_data_df['timestamp'].unique()        
        # Rotate the labels vertically:
        plt.xticks(range(len(date_labels)), date_labels, rotation=30, fontsize=10)        
        # Save the figure to a temporary file
        tmp_file = "temp_plot.png"
        fig.figure.savefig(tmp_file)
        # Display the saved image in Streamlit
        st.image(tmp_file)
        # Optionally, you can remove the temporary file after displaying it        
        os.remove(tmp_file)        
        # Showing df:
        with st.expander(label='Show tables related to the evolution of user preferences'):
            # Showing describe df:
            describe_df = user_data_df.groupby('timestamp').rating.describe()
            st.dataframe(describe_df)
            wf_util.save_df(df_name='user_preference_evolution_describe', df_value=describe_df, extension='csv')    
            # Showing user preference evolution df:
            st.dataframe(user_data_df)
            wf_util.save_df(df_name='user_preference_evolution', df_value=user_data_df, extension='csv')            

def show_item_statistics_from_user(user_id, extract_statistics):
    """
    Shows a dataframe with item statistics.
    :param user_id: The current user.
    :param extract_statistics: The instance to extract general statistics.
    :return: A dataframe with item statistics.
    """    
    st.markdown("*Item statistics*")
    item_statistics_dict = {}         
    # Number of items by user:           
    number_items_df = extract_statistics.get_number_ratings_by_user()
    number_items = number_items_df.loc[number_items_df['user_id'] == user_id, 'count_ratings'].iloc[0]
    # Percentage of items by user:
    percentage_items_df = extract_statistics.get_percentage_ratings_by_user()                    
    percentage_items = percentage_items_df.loc[percentage_items_df['user_id'] == user_id, 'percentage_ratings'].iloc[0]
    # Average of items by user:    
    avg_items_df = extract_statistics.get_avg_items_by_user()
    avg_items = avg_items_df.loc[avg_items_df['user_id'] == user_id, 'avg_items'].iloc[0]
    # Variance of items by user:
    variance_items_df = extract_statistics.get_variance_items_by_user()
    variance_items = variance_items_df.loc[variance_items_df['user_id'] == user_id, 'variance_items'].iloc[0]                    
    # Standard deviation of items by user:
    sd_items_df = extract_statistics.get_sd_items_by_user()                    
    sd_items = sd_items_df.loc[sd_items_df['user_id'] == user_id, 'sd_items'].iloc[0]                    
    # Number of not repeated items by user:                    
    number_not_repeated_items_df = extract_statistics.get_number_not_repeated_items_by_user()
    number_not_repeated_items = number_not_repeated_items_df.loc[number_not_repeated_items_df['user_id'] == user_id, 'not_repeated_items'].iloc[0]
    # Percentage of not repeated items by user:                    
    percentage_not_repeated_items_df = extract_statistics.get_percentage_not_repeated_items_by_user()
    percentage_not_repeated_items = percentage_not_repeated_items_df.loc[percentage_not_repeated_items_df['user_id'] == user_id, 'percentage_not_repeated_items'].iloc[0]
    # Percentage of not repeated items by user:                    
    percentage_repeated_items_df = extract_statistics.get_percentage_repeated_items_by_user()
    percentage_repeated_items = percentage_repeated_items_df.loc[percentage_repeated_items_df['user_id'] == user_id, 'porcentage_repeated_items'].iloc[0]
    item_statistics_dict['user_id'] = [user_id]
    item_statistics_dict['count'] = [number_items]
    item_statistics_dict['percentage'] = [percentage_items]
    item_statistics_dict['average'] = [avg_items]                  
    item_statistics_dict['variance'] = [variance_items]                  
    item_statistics_dict['standard deviation'] = [sd_items]      
    item_statistics_dict['not repeated items'] = [number_not_repeated_items]
    item_statistics_dict['percentage not repeated items'] = [percentage_not_repeated_items]
    item_statistics_dict['percentage repeated items'] = [percentage_repeated_items]
    item_statistics_df = pd.DataFrame(item_statistics_dict)        
    # Set the index label for the first row:
    item_statistics_df = item_statistics_df.rename(index={item_statistics_df.index[0]: 'item_id'})
    st.dataframe(item_statistics_df)
    return item_statistics_df

def show_context_statistics_from_user(user_id, extract_statistics, with_context):
    """
    Shows a dataframe with context statistics.
    :param with_context: True if the file to be generated will be contextual and False in the otherwise.
    :param user_id: The current user.
    :param extract_statistics: The instance to extract general statistics.
    :return: A dataframe with context statistics.
    """
    if with_context:
        # Contexts per user:                    
        st.markdown("*Context statistics*")
        # Statistics of contexts:
        context_statistics_dict = {}         
        # Number of contexts by user:           
        number_contexts_df = extract_statistics.get_number_ratings_by_user()
        number_contexts = number_contexts_df.loc[number_contexts_df['user_id'] == user_id, 'count_ratings'].iloc[0]
        # Percentage of contexts by user:
        percentage_contexts_df = extract_statistics.get_percentage_ratings_by_user()
        percentage_contexts = percentage_contexts_df.loc[percentage_contexts_df['user_id'] == user_id, 'percentage_ratings'].iloc[0]
        # Average of contexts by user:    
        avg_contexts_df = extract_statistics.get_avg_contexts_by_user()
        avg_contexts = avg_contexts_df.loc[avg_contexts_df['user_id'] == user_id, 'avg_contexts'].iloc[0]
        # Variance of contexts by user:
        variance_contexts_df = extract_statistics.get_variance_contexts_by_user()
        variance_contexts = variance_contexts_df.loc[variance_contexts_df['user_id'] == user_id, 'variance_contexts'].iloc[0]
        # Standard deviation of contexts by user:
        sd_contexts_df = extract_statistics.get_sd_contexts_by_user()                    
        sd_contexts = sd_contexts_df.loc[sd_contexts_df['user_id'] == user_id, 'sd_contexts'].iloc[0]                    
        # Number of not repeated contexts by user:                    
        number_not_repeated_contexts_df = extract_statistics.get_number_not_repeated_contexts_by_user()
        number_not_repeated_contexts = number_not_repeated_contexts_df.loc[number_not_repeated_contexts_df['user_id'] == user_id, 'not_repeated_contexts'].iloc[0]
        # Percentage of not repeated contexts by user:                    
        percentage_not_repeated_contexts_df = extract_statistics.get_percentage_not_repeated_contexts_by_user()
        percentage_not_repeated_contexts = percentage_not_repeated_contexts_df.loc[percentage_not_repeated_contexts_df['user_id'] == user_id, 'percentage_not_repeated_contexts'].iloc[0]
        # Percentage of not repeated contexts by user:                    
        percentage_repeated_contexts_df = extract_statistics.get_percentage_repeated_contexts_by_user()
        percentage_repeated_contexts = percentage_repeated_contexts_df.loc[percentage_repeated_contexts_df['user_id'] == user_id, 'porcentage_repeated_contexts'].iloc[0]
        context_statistics_dict['user_id'] = [user_id]
        context_statistics_dict['count'] = [number_contexts]
        context_statistics_dict['percentage'] = [percentage_contexts]
        context_statistics_dict['average'] = [avg_contexts]                  
        context_statistics_dict['variance'] = [variance_contexts]                  
        context_statistics_dict['standard deviation'] = [sd_contexts] 
        context_statistics_dict['not repeated contexts'] = [number_not_repeated_contexts]
        context_statistics_dict['percentage not repeated contexts'] = [percentage_not_repeated_contexts]
        context_statistics_dict['percentage repeated contexts'] = [percentage_repeated_contexts]     
        context_statistics_df = pd.DataFrame(context_statistics_dict)
        # Set the index label for the first row:
        context_statistics_df = context_statistics_df.rename(index={context_statistics_df.index[0]: 'context_id'})
        st.dataframe(context_statistics_df)

def show_rating_statistics_from_user(user_id, extract_statistics):
    """
    Shows a dataframe with rating statistics.    
    :param user_id: The current user.
    :param extract_statistics: The instance to extract general statistics.
    :return: A dataframe with rating statistics.
    """
    st.markdown("*Rating statistics*")                  
    rating_statistics_dict = {}         
    # Number of ratings by user:           
    number_ratings_df = extract_statistics.get_number_ratings_by_user()
    number_ratings = number_ratings_df.loc[number_ratings_df['user_id'] == user_id, 'count_ratings'].iloc[0]
    # Percentage of ratings by user:
    percentage_ratings_df = extract_statistics.get_percentage_ratings_by_user()                    
    percentage_ratings = percentage_ratings_df.loc[percentage_ratings_df['user_id'] == user_id, 'percentage_ratings'].iloc[0]
    # Average of ratings by user:    
    avg_ratings_df = extract_statistics.get_avg_ratings_by_user()
    avg_ratings = avg_ratings_df.loc[avg_ratings_df['user_id'] == user_id, 'avg_ratings'].iloc[0]
    # Variance of ratings by user:
    variance_ratings_df = extract_statistics.get_variance_ratings_by_user()
    variance_ratings = variance_ratings_df.loc[variance_ratings_df['user_id'] == user_id, 'variance_ratings'].iloc[0]
    # Standard deviation of ratings by user:
    sd_ratings_df = extract_statistics.get_sd_items_by_user()                    
    sd_ratings = sd_ratings_df.loc[sd_ratings_df['user_id'] == user_id, 'sd_items'].iloc[0]                    
    rating_statistics_dict['user_id'] = [user_id]
    rating_statistics_dict['count'] = [number_ratings]
    rating_statistics_dict['percentage'] = [percentage_ratings]  
    rating_statistics_dict['average'] = [avg_ratings]                  
    rating_statistics_dict['variance'] = [variance_ratings]                  
    rating_statistics_dict['standard deviation'] = [sd_ratings]      
    rating_statistics_df = pd.DataFrame(rating_statistics_dict)
    # Set the index label for the first row:
    rating_statistics_df = rating_statistics_df.rename(index={rating_statistics_df.index[0]: 'rating'})
    st.dataframe(rating_statistics_df)
    return rating_statistics_df
