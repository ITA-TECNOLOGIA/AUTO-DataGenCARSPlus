import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_rating import ExtractStatisticsRating
from streamlit_app import config


def show_information(rating_df, with_context):
    """
    Shows information and statistics about the rating DataFrame.
    :param rating_df: The DataFrame containing ratings.
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    """    
    if not rating_df.empty:        
        st.header("Rating file")  
        # Show rating dataframe:                
        st.dataframe(rating_df)
        # Extracted statistics:
        extract_statistics_rating = ExtractStatisticsRating(rating_df=rating_df)
        # General statistics:
        st.header("General statistics")
        unique_users = extract_statistics_rating.get_number_users()
        unique_items = extract_statistics_rating.get_number_items()
        unique_counts = {"Users": unique_users, "Items": unique_items}
        if with_context:
            unique_contexts = extract_statistics_rating.get_number_contexts()
            unique_counts["Contexts"] = unique_contexts
        unique_ratings = extract_statistics_rating.get_number_ratings()
        unique_counts["Ratings"] = unique_ratings
        unique_counts_df = pd.DataFrame.from_dict(unique_counts, orient='index', columns=['Count'])
        unique_counts_df.reset_index(inplace=True)
        unique_counts_df.rename(columns={"index": "Attribute name"}, inplace=True)                    
        st.table(unique_counts_df)               
        # Attributes, data types and value ranges:
        st.header("Attributes, data types and value ranges")
        table6 = extract_statistics_rating.get_attributes_and_ranges()
        st.table(pd.DataFrame(table6, columns=["Attribute name", "Data type", "Value ranges"]))
        # Histogram of ratings:
        st.header("Histogram of ratings")
        # Count the frequency of each rating:
        counts = np.bincount(rating_df['rating'])[np.nonzero(np.bincount(rating_df['rating']))] 
        df6 = pd.DataFrame({'Type of ratings': np.arange(1, len(counts) + 1), 'Number of ratings': counts})
        chart6 = alt.Chart(df6).mark_bar(color='#0099CC').encode(x=alt.X('Type of ratings:O', axis=alt.Axis(title='Type of ratings')), y=alt.Y('Number of ratings:Q', axis=alt.Axis(title='Number of ratings')), tooltip=['Type of ratings', 'Number of ratings']).properties(title={'text': 'Histogram of ratings', 'fontSize': 16,})
        st.altair_chart(chart6, use_container_width=True)
        # Statistics per user:
        st.header("Statistics per user")
        users = list(rating_df['user_id'].unique())                    
        selected_user = st.selectbox("Select a user:", users, key="selected_user_tab6")   
        # Items per user:
        st.markdown("*Items*")                           
        counts_items, unique_items, total_count = extract_statistics_rating.get_number_items_from_user(selected_user)
        df = pd.DataFrame({'Type of items': counts_items.index, 'Number of items': counts_items.values})                    
        counts_items = pd.Series(counts_items, name='Number of items').reset_index()
        counts_items = counts_items.rename(columns={'index': 'Type of items'})
        chart = alt.Chart(counts_items).mark_bar(color="#0099CC").encode(x=alt.X('Type of items:O', axis=alt.Axis(labelExpr='datum.value', title='Type of items')), y=alt.Y('Number of items:Q', axis=alt.Axis(title='Number of items')), tooltip=['Type of items', 'Number of items']).properties(title={"text": [f"Histogram of items rated per user {str(selected_user)} (total={total_count})"],"fontSize": 16,})
        st.altair_chart(chart, use_container_width=True) 
        # Statistics of items:
        item_statistics_dict = {}         
        # Number of items by user:           
        number_items_df = extract_statistics_rating.get_number_ratings_by_user()
        number_items = number_items_df.loc[number_items_df['user_id'] == selected_user, 'count_ratings'].iloc[0]
        # Percentage of items by user:
        percentage_items_df = extract_statistics_rating.get_percentage_ratings_by_user()                    
        percentage_items = percentage_items_df.loc[percentage_items_df['user_id'] == selected_user, 'percentage_ratings'].iloc[0]
        # Average of items by user:    
        avg_items_df = extract_statistics_rating.get_avg_items_by_user()
        avg_items = avg_items_df.loc[avg_items_df['user_id'] == selected_user, 'avg_items'].iloc[0]
        # Variance of items by user:
        variance_items_df = extract_statistics_rating.get_variance_items_by_user()
        variance_items = variance_items_df.loc[variance_items_df['user_id'] == selected_user, 'variance_items'].iloc[0]                    
        # Standard deviation of items by user:
        sd_items_df = extract_statistics_rating.get_sd_items_by_user()                    
        sd_items = sd_items_df.loc[sd_items_df['user_id'] == selected_user, 'sd_items'].iloc[0]                    
        # Number of not repeated items by user:                    
        number_not_repeated_items_df = extract_statistics_rating.get_number_not_repeated_items_by_user()
        number_not_repeated_items = number_not_repeated_items_df.loc[number_not_repeated_items_df['user_id'] == selected_user, 'not_repeated_items'].iloc[0]
        # Percentage of not repeated items by user:                    
        percentage_not_repeated_items_df = extract_statistics_rating.get_percentage_not_repeated_items_by_user()
        percentage_not_repeated_items = percentage_not_repeated_items_df.loc[percentage_not_repeated_items_df['user_id'] == selected_user, 'percentage_not_repeated_items'].iloc[0]
        # Percentage of not repeated items by user:                    
        percentage_repeated_items_df = extract_statistics_rating.get_percentage_repeated_items_by_user()
        percentage_repeated_items = percentage_repeated_items_df.loc[percentage_repeated_items_df['user_id'] == selected_user, 'porcentage_repeated_items'].iloc[0]
        item_statistics_dict['user_id'] = [selected_user]
        item_statistics_dict['count'] = [number_items]
        item_statistics_dict['percentage'] = [percentage_items]
        item_statistics_dict['average'] = [avg_items]                  
        item_statistics_dict['variance'] = [variance_items]                  
        item_statistics_dict['standard deviation'] = [sd_items]      
        item_statistics_dict['not repeated items'] = [number_not_repeated_items]
        item_statistics_dict['percentage not repeated items'] = [percentage_not_repeated_items]
        item_statistics_dict['percentage repeated items'] = [percentage_repeated_items]
        item_statistics_df = pd.DataFrame(item_statistics_dict)
        st.dataframe(item_statistics_df)   
        if with_context:
            # Contexts per user:                    
            st.markdown("*Contexts*")
            # Statistics of contexts:
            context_statistics_dict = {}         
            # Number of contexts by user:           
            number_contexts_df = extract_statistics_rating.get_number_ratings_by_user()
            number_contexts = number_contexts_df.loc[number_contexts_df['user_id'] == selected_user, 'count_ratings'].iloc[0]
            # Percentage of contexts by user:
            percentage_contexts_df = extract_statistics_rating.get_percentage_ratings_by_user()
            percentage_contexts = percentage_contexts_df.loc[percentage_contexts_df['user_id'] == selected_user, 'percentage_ratings'].iloc[0]
            # Average of contexts by user:    
            avg_contexts_df = extract_statistics_rating.get_avg_contexts_by_user()
            avg_contexts = avg_contexts_df.loc[avg_contexts_df['user_id'] == selected_user, 'avg_contexts'].iloc[0]
            # Variance of contexts by user:
            variance_contexts_df = extract_statistics_rating.get_variance_contexts_by_user()
            variance_contexts = variance_contexts_df.loc[variance_contexts_df['user_id'] == selected_user, 'variance_contexts'].iloc[0]
            # Standard deviation of contexts by user:
            sd_contexts_df = extract_statistics_rating.get_sd_contexts_by_user()                    
            sd_contexts = sd_contexts_df.loc[sd_contexts_df['user_id'] == selected_user, 'sd_contexts'].iloc[0]                    
            # Number of not repeated contexts by user:                    
            number_not_repeated_contexts_df = extract_statistics_rating.get_number_not_repeated_contexts_by_user()
            number_not_repeated_contexts = number_not_repeated_contexts_df.loc[number_not_repeated_contexts_df['user_id'] == selected_user, 'not_repeated_contexts'].iloc[0]
            # Percentage of not repeated contexts by user:                    
            percentage_not_repeated_contexts_df = extract_statistics_rating.get_percentage_not_repeated_contexts_by_user()
            percentage_not_repeated_contexts = percentage_not_repeated_contexts_df.loc[percentage_not_repeated_contexts_df['user_id'] == selected_user, 'percentage_not_repeated_contexts'].iloc[0]
            # Percentage of not repeated contexts by user:                    
            percentage_repeated_contexts_df = extract_statistics_rating.get_percentage_repeated_contexts_by_user()
            percentage_repeated_contexts = percentage_repeated_contexts_df.loc[percentage_repeated_contexts_df['user_id'] == selected_user, 'porcentage_repeated_contexts'].iloc[0]
            context_statistics_dict['user_id'] = [selected_user]
            context_statistics_dict['count'] = [number_contexts]
            context_statistics_dict['percentage'] = [percentage_contexts]
            context_statistics_dict['average'] = [avg_contexts]                  
            context_statistics_dict['variance'] = [variance_contexts]                  
            context_statistics_dict['standard deviation'] = [sd_contexts] 
            context_statistics_dict['not repeated contexts'] = [number_not_repeated_contexts]
            context_statistics_dict['percentage not repeated contexts'] = [percentage_not_repeated_contexts]
            context_statistics_dict['percentage repeated contexts'] = [percentage_repeated_contexts]     
            context_statistics_df = pd.DataFrame(context_statistics_dict)
            st.dataframe(context_statistics_df)    
            # Ratings per user:                    
            st.markdown("*Ratings*")                  
            rating_statistics_dict = {}         
            # Number of ratings by user:           
            number_ratings_df = extract_statistics_rating.get_number_ratings_by_user()
            number_ratings = number_ratings_df.loc[number_ratings_df['user_id'] == selected_user, 'count_ratings'].iloc[0]
            # Percentage of ratings by user:
            percentage_ratings_df = extract_statistics_rating.get_percentage_ratings_by_user()                    
            percentage_ratings = percentage_ratings_df.loc[percentage_ratings_df['user_id'] == selected_user, 'percentage_ratings'].iloc[0]
            # Average of ratings by user:    
            avg_ratings_df = extract_statistics_rating.get_avg_ratings_by_user()
            avg_ratings = avg_ratings_df.loc[avg_ratings_df['user_id'] == selected_user, 'avg_ratings'].iloc[0]
            # Variance of ratings by user:
            variance_ratings_df = extract_statistics_rating.get_variance_ratings_by_user()
            variance_ratings = variance_ratings_df.loc[variance_ratings_df['user_id'] == selected_user, 'variance_ratings'].iloc[0]
            # Standard deviation of ratings by user:
            sd_ratings_df = extract_statistics_rating.get_sd_items_by_user()                    
            sd_ratings = sd_ratings_df.loc[sd_ratings_df['user_id'] == selected_user, 'sd_items'].iloc[0]                    
            rating_statistics_dict['user_id'] = [selected_user]
            rating_statistics_dict['count'] = [number_ratings]
            rating_statistics_dict['percentage'] = [percentage_ratings]  
            rating_statistics_dict['average'] = [avg_ratings]                  
            rating_statistics_dict['variance'] = [variance_ratings]                  
            rating_statistics_dict['standard deviation'] = [sd_ratings]      
            rating_statistics_df = pd.DataFrame(rating_statistics_dict)
            st.dataframe(rating_statistics_df)        
    else:
        st.warning(f"The rating file ({config.RATING_TYPE}.csv) has not been uploaded.")
