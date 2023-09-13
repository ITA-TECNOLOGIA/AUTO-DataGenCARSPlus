from ast import literal_eval
from collections import defaultdict

import altair as alt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_uic import ExtractStatisticsUIC
from matplotlib import pyplot as plt
from streamlit_app import config
from streamlit_app.preprocess_dataset import wf_util


def show_information(df, file_type):
    """
    Shows statistcis related to user, item, context or behavior df (missing values, data types, value ranges, attribute correlation, etc.).
    :param df: The DataFrame to display information about.
    :param file_type: The type of file (user, item, context or behavior).
    """
    if not df.empty:             
        # title:
        st.header(file_type.title())        
        # Show dataframe:            
        st.dataframe(df)        
        
        # Extracted statistics:
        extract_statistics = ExtractStatisticsUIC(df)
        # Showing missing values:
        show_missing_values(extract_statistics)
        # Showing attributes, data types and value ranges:
        show_data_types(extract_statistics)
        # Getting the attribute list:
        attribute_list = df.columns.tolist()
        attribute_list.remove(f'{file_type}_id')
        # Showing a frequency graphic by attribute:
        show_graphic_by_attribute(extract_statistics, attribute_list, file_type)
        
        # Showing only for user, item or context files:
        if file_type in ['user', 'item', 'context']:
            # Showing specific statistics related to user, item or context files:
            show_specific_statistics(extract_statistics, attribute_list, file_type)
            # Showing correlation between attributes:
            show_correlation_matrix(df, attribute_list, file_type)

        # Showing only for behavior file:
        if file_type == 'behavior':            
            show_user_navegation_map(behavior_df=df)
    else:
        st.warning(f"The {file_type} file ({file_type}.csv) has not been uploaded.")

def show_missing_values(extract_statistics):
    """
    Shows missing values in the dataframe.
    :param extract_statistics: The object to extract general statistics.
    """
    st.header("Missing values")
    missing_values = extract_statistics.count_missing_values(replace_values={"NULL":np.nan,-1:np.nan})                    
    st.table(missing_values)

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

def show_graphic_by_attribute(extract_statistics, attribute_list, file_type):
    """
    Shows a frequency graphic by attribute.
    :param extract_statistics: The object to extract general statistics.
    :param attribute_list: The list of attribute names (ignoring id: user_id, item_id, context_id or behavior_id).
    :param file_type: The type of file (user, item, context or behavior).
    """
    st.header("Analysis by attribute")
    if len(attribute_list) > 0:
        col1, col2 = st.columns(2)
        with col1:
            column = st.selectbox("Select an attribute", attribute_list, key=f'column2_{file_type}')
        with col2:
            sort = st.selectbox('Sort', ['none', 'asc', 'desc'], key=f'sort2_{file_type}')
        data = extract_statistics.column_attributes_count(column)
        if sort == 'asc':
            sort_field = alt.EncodingSortField('count', order='ascending')
        elif sort == 'desc':
            sort_field = alt.EncodingSortField('count', order='descending') 
        else:
            sort_field = None
        chart = alt.Chart(data).mark_bar().encode(x=alt.X(column + ':O', title='Attribute values', sort=sort_field), y=alt.Y('count:Q', title='Count'), tooltip=[column, 'count']).interactive()
        st.altair_chart(chart, use_container_width=True) 
    else:
        st.warning(f"No columns (without {file_type}_id) to show.")

def show_specific_statistics(extract_statistics, attribute_list, file_type):
    """
    Shows specific statistics related to user, item or context files.
    :param extract_statistics: The object to extract general statistics.
    :param attribute_list: The list of attribute names (ignoring id: user_id, item_id or context_id).
    :param file_type: The type of file (user, item or context).
    """    
    st.header("Extracted statistics")
    st.write(f'Number total of {file_type}s: ', extract_statistics.get_number_id())
    st.write('Analyzing possible values per attribute:')
    if len(attribute_list) > 0:
        number_possible_values_df = extract_statistics.get_number_possible_values_by_attribute()
        avg_possible_values_df = extract_statistics.get_avg_possible_values_by_attribute()
        sd_possible_values_df = extract_statistics.get_sd_possible_values_by_attribute()                                        
        extracted_statistics_df = pd.concat([number_possible_values_df, avg_possible_values_df, sd_possible_values_df])                    
        # Insert the new column at index 0:
        label_column_list = ['count', 'average', 'standard deviation']                    
        extracted_statistics_df.insert(loc=0, column='possible values', value=label_column_list)                  
        if extracted_statistics_df.isnull().values.any():
            st.warning('If there are <NA> values, it is because these attributes have Nan or string values.')
        st.dataframe(extracted_statistics_df)                    
        # Showing more details:
        with st.expander('More details'):
            statistics = extract_statistics.statistics_by_attribute()                    
            for stat in statistics:
                st.subheader(stat[0])
                st.write('Average: ', stat[1])
                st.write('Standard deviation: ', stat[2])
                col1, col2 = st.columns(2)
                with col1:
                    st.write('Frequencies:')
                    st.dataframe(stat[3])
                with col2:
                    st.write('Percentages:')
                    st.dataframe(stat[4])
    else:
        st.warning(f"No columns (without {file_type}_id) to show.")
    
def show_correlation_matrix(df, attribute_list, file_type):
    """
    Shows a correlation matrix for selected attributes.    
    :param df: The DataFrame containing the data.
    :param attribute_list: The list of attribute names (ignoring id: user_id, item_id or context_id).
    :param file_type: The label to display.
    :return: The correlation matrix.
    """
    st.header("Correlation between attributes")
    corr_matrix = pd.DataFrame()
    if len(attribute_list) > 1:
        columns_id = df.filter(regex='_id$').columns.tolist()
        columns_not_id = [col for col in df.columns if col not in columns_id]
        data_types = []
        for col in columns_not_id:     
            data_types.append({"Attribute": col, "Data Type": str(df[col].dtype)})
            break    
        selected_columns = st.multiselect("Select columns to analyze", columns_not_id, key='cm_'+file_type)
        method = st.selectbox("Select a method", ['pearson', 'kendall', 'spearman'], key='method_'+file_type)
        if st.button("Generate correlation matrix", key='button_'+file_type) and selected_columns:
            with st.spinner("Generating correlation matrix..."):
                merged_df_selected = df[selected_columns].copy()
                # Categorize non-numeric columns using label encoding:
                for col in merged_df_selected.select_dtypes(exclude=[np.number]):
                    merged_df_selected[col], _ = merged_df_selected[col].factorize()            
                corr_matrix = merged_df_selected.corr(method=method)
        if not corr_matrix.empty:                        
            fig, ax = plt.subplots(figsize=(10, 10))                    
            sns.heatmap(corr_matrix, vmin=-1, vmax=1, center=0, cmap='coolwarm', annot=True, fmt=".2f", ax=ax)
            st.pyplot(fig)
    else:
        st.warning(f"At least two columns needed to show correlation.")            
    return corr_matrix

def show_user_navegation_map(behavior_df):
    """
    Shows the user navegation in a room.
    :param behavior_df: The behavior dataframe.
    :param item_df: The item dataframe.
    """
    st.header('Virtual World Map')            
    # Load item file:    
    st.write(f'The {config.ITEM_TYPE}.csv is required to draw the user navigation map:')
    item_df = wf_util.load_one_file(config.ITEM_TYPE, wf_type='tab_behavior_item')
    if not item_df.empty:            
        # Create a dictionary of colors and assign a unique color to each object_type
        unique_object_types = item_df['object_type'].unique()
        colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_object_types)))
        color_map = {object_type: color for object_type, color in zip(unique_object_types, colors)}
        behavior_df['item_id'] = behavior_df['item_id'].astype(str)
        item_df['item_id'] = item_df['item_id'].astype(str)
        data = pd.merge(behavior_df, item_df, left_on='item_id', right_on='item_id', how='left')
        update_data = data[data['object_action'] == 'Update']
        # Extract positions and convert them to a list of tuples
        update_data['user_position'] = update_data['user_position'].apply(lambda x: literal_eval(x) if x else None)
        update_data = update_data.dropna(subset=['user_position'])
        unique_user_ids = update_data['user_id'].unique()        
        rooms_input = st.text_input(f"Introduce rooms as list of dictionaries. For example: {config.EXAMPLE_ROOM_LIST}")
        if rooms_input:                    
            rooms = literal_eval(rooms_input)
            room_ids = [room['id'] for room in rooms]
            selected_rooms = st.multiselect('Select rooms to plot:', options=room_ids)
            selected_users = st.multiselect('Select users to plot:', options=unique_user_ids)
            selected_data = st.selectbox('Select data to plot:', options=['Items and Users', 'Only Items', 'Only Users', ])
            if st.button('Show Map'):
                plt.figure(figsize=(10, 10))
                # Draw the object_types and save the references for the legend
                markers = []
                labels = []
                for user_id in selected_users:
                    user_data = update_data[update_data['user_id'] == user_id]
                    # Convert the 'timestamp' column to a numeric Unix timestamp
                    user_data['timestamp'] = pd.to_datetime(user_data['timestamp'])
                    user_data['timestamp'] = user_data['timestamp'].apply(lambda x: pd.Timestamp(x).timestamp())
                    # Group the data by session
                    sessions = defaultdict(list)
                    for _, row in user_data.iterrows():
                        user_id = row['user_id']
                        timestamp = row['timestamp']
                        session_id = np.argmin([abs(r['timestamp'] - timestamp) for _, r in user_data.iterrows() if r['user_id'] == user_id])
                        session_timestamp = np.mean([r['timestamp'] for _, r in user_data.iterrows() if r['user_id'] == user_id and np.argmin([abs(r2['timestamp'] - r['timestamp']) for _, r2 in user_data.iterrows() if r2['user_id'] == user_id]) == session_id])
                        sessions[(user_id, session_timestamp)].append(row.to_dict())
                    for (user_id, session_timestamp), session_data in sessions.items():
                        if len(session_data) > 1:
                            for room in rooms:
                                if room['id'] in selected_rooms:
                                    plt.gca().add_patch(plt.Rectangle((room['x_min'], room['z_min']), room['x_max'] - room['x_min'], room['z_max'] - room['z_min'], fill=None, edgecolor='black', linestyle='--'))
                                    plt.text(room['x_min'] + (room['x_max'] - room['x_min']) / 2, room['z_min'] + (room['z_max'] - room['z_min']) / 2, f"ID: {room['id']}", fontsize=12, ha='center', va='center')
                            if selected_data in ['Only Items', 'Items and Users']:
                                for __, row in item_df.iterrows():
                                    pos = literal_eval(row['object_position'])
                                    marker = plt.scatter(pos[0], pos[2], marker='s', color=color_map[row['object_type']])                                    
                                    if row['object_type'] not in labels:
                                        markers.append(marker)
                                        labels.append(row['object_type'])
                            if selected_data in ['Only Users', 'Items and Users']:
                                positions = [d['user_position'] for d in session_data]
                                timestamps = [d['timestamp'] for d in session_data]
                                x_coords = list(pos[0] for pos in positions)
                                z_coords = list(pos[2] for pos in positions)
                                plt.plot(x_coords, z_coords, label=f'User {user_id}, Session {session_timestamp}', linestyle='--', marker='o')
                                # Print the timestamps for the session:
                                # st.write(f"Timestamps for User {user_id}, Session {session_timestamp}:")
                                # for i, time in enumerate(timestamps):
                                #     st.write(f"Step {i+1}: {time}")
                plt.title("Virtual world map")
                plt.xlabel('X')
                plt.ylabel('Z')
                # Adjust the limits of the graph according to the selected rooms
                x_mins, x_maxs = zip(*[(room['x_min'], room['x_max']) for room in rooms if room['id'] in selected_rooms])
                z_mins, z_maxs = zip(*[(room['z_min'], room['z_max']) for room in rooms if room['id'] in selected_rooms])
                plt.xlim(min(x_mins), max(x_maxs))
                plt.ylim(min(z_mins), max(z_maxs))
                plt.legend(handles=markers+plt.gca().get_legend_handles_labels()[0], labels=labels+plt.gca().get_legend_handles_labels()[1])
                plt.grid(True)
                st.pyplot(plt.gcf())
                plt.clf()
    else:
        st.warning(f"The {config.ITEM_TYPE} file ({config.ITEM_TYPE}.csv) has not been uploaded.")
