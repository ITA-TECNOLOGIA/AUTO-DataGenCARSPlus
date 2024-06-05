from ast import literal_eval

import altair as alt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_uic import ExtractStatisticsUIC
from matplotlib import pyplot as plt
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
        with st.expander(label=f'Show the {file_type}.csv file'):
            st.dataframe(df)
        
        # Extracted statistics:
        extract_statistics = ExtractStatisticsUIC(df)
        # Showing general statistics (user, item or context): 
        # Getting the attribute list:
        attribute_list = df.columns.tolist()
        attribute_list.remove(f'{file_type}_id')      
        if file_type in ['user', 'item', 'context']:
            # Showing specific statistics related to user, item or context files:
            show_attribute_statistics(df, file_type, attribute_list)
            show_more_statistics_by_attribute(extract_statistics)            
        # Showing missing values:
        show_missing_values(extract_statistics)
        # Showing attributes, data types and value ranges:
        show_data_types(extract_statistics)       
        # Showing a frequency graphic by attribute:
        show_graphic_by_attribute(extract_statistics, attribute_list, file_type) 
        if file_type in ['user', 'item', 'context']:
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
        chart = alt.Chart(data).mark_bar().encode(x=alt.X(column + ':O', sort=sort_field, axis=alt.Axis(title=column, labelFontSize=16, titleFontSize=16)), 
                                                  y=alt.Y('count:Q', axis=alt.Axis(title=column, labelFontSize=16, titleFontSize=16)), 
                                                  tooltip=[column, 'count']).interactive()
        st.altair_chart(chart, use_container_width=True) 
    else:
        st.warning(f"No columns (without {file_type}_id) to show.")

def show_attribute_statistics_calculated(extract_statistics, attribute_list, file_type):
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
    else:
        st.warning(f"No columns (without {file_type}_id) to show.")
    return extracted_statistics_df

def show_more_statistics_by_attribute(extract_statistics):
    """
    """
    # Showing more details:
    with st.expander('More details'):
        statistics = extract_statistics.statistics_by_attribute()                    
        for stat in statistics:
            st.subheader(stat[0])
            # st.write('Average: ', stat[1])
            # st.write('Standard deviation: ', stat[2])
            col1, col2 = st.columns(2)
            with col1:
                st.write('Frequencies:')
                st.dataframe(stat[3])
            with col2:
                st.write('Percentages:')
                st.dataframe(stat[4])

def show_attribute_statistics(df, file_type, attribute_list):
    """
    Show some rating statistics.    
    :param df: The rating dataframe.
    :param file_type: The type of file (user, item, context or behavior).
    :return: A dataframe with user, item or context statistics.
    """  
    st.header('General statistics')
    if len(attribute_list) > 0:
        summary_df = df.describe()
        summary_df = summary_df.drop(columns=[f"{file_type}_id"])
        if not summary_df.empty:
            st.dataframe(summary_df)
        else:
            st.warning(f"No columns (without {file_type}_id) to show.")
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
    Shows the user navigation in a room with an option to display rooms.
    :param behavior_df: The behavior dataframe.
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
        update_data['user_position'] = update_data['user_position'].apply(lambda x: literal_eval(x) if x else None)
        update_data = update_data.dropna(subset=['user_position'])
        unique_user_ids = update_data['user_id'].unique()        
        
        # Add an option to display rooms
        display_rooms = st.checkbox("Display Rooms?", value=True)

        if display_rooms:
            rooms_input = st.text_input(f"Introduce rooms as list of dictionaries. For example: {config.EXAMPLE_ROOM_LIST}")
            if rooms_input:                    
                rooms = literal_eval(rooms_input)
                room_ids = [room['id'] for room in rooms]
                selected_rooms = st.multiselect('Select rooms to plot:', options=room_ids)

        selected_users = st.multiselect('Select users to plot:', options=unique_user_ids)
        selected_data = st.selectbox('Select data to plot:', options=['Items and Users', 'Only Items', 'Only Users'])
        
        if st.button('Show Map'):
            plt.figure(figsize=(10, 10))
            # If display_rooms is True, draw the rooms
            if display_rooms and rooms_input:
                for room in rooms:
                    if room['id'] in selected_rooms:
                        plt.gca().add_patch(plt.Rectangle((room['x_min'], room['z_min']), room['x_max'] - room['x_min'], room['z_max'] - room['z_min'], fill=None, edgecolor='black', linestyle='--'))
                        plt.text(room['x_min'] + (room['x_max'] - room['x_min']) / 2, room['z_min'] + (room['z_max'] - room['z_min']) / 2, f"ID: {room['id']}", fontsize=12, ha='center', va='center')

            # The rest of the plotting logic remains the same...

            # Draw the object_types and save the references for the legend
            markers, labels = [], []
            for user_id in selected_users:
                user_data = update_data[update_data['user_id'] == user_id]
                # ...
                # Plotting logic for items and users goes here
                # ...

            plt.title("Virtual world map")
            plt.xlabel('X')
            plt.ylabel('Y') # Z for Imascono
            if display_rooms and rooms_input:
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
