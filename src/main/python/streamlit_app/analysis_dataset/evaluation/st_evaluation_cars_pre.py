import math

import pandas as pd
import streamlit as st
from datagencars import util
from streamlit_app import config
from streamlit_app.analysis_dataset.evaluation import st_evaluation_rs
from streamlit_app.preprocess_dataset import wf_util


def evaluate_prefiltering_paradigm(rating_df):
    """
    Evaluates the pre-filtering paradigm.
    :param rating_df: The rating dataframe.
    """
    # Step 1: The contextual information is used to filter the CARS dataset.    
    filtered_rs_rating_df = build_knowledge_base(rating_df)

    # Step 2: Evaluate a traditional RS.
    if not filtered_rs_rating_df.empty:        
        st_evaluation_rs.generate(rating_df=filtered_rs_rating_df)    
    
    # Step 3: The resulting set of recommendations is adjusted (contextualized) for each user by using contextual information.
    # TODO

def build_knowledge_base(rating_df):
    """
    Filters the contextual information in the CARS dataset.
    :param rating_df: The rating dataframe.
    :return: A filtered dataframe.
    """    
    # Loading item and context files:
    st.markdown("""---""")
    st.header('Filter the context information')
    st.write('If you are applying the Pre-filtering paradigm, upload the following files to select the features of the knowledge base: ')
    item_df = wf_util.load_one_file(file_type=config.ITEM_TYPE, wf_type='evaluation_cars_item_df') 
    context_df = wf_util.load_one_file(file_type=config.CONTEXT_TYPE, wf_type='evaluation_cars_context_df')
    # Building the traditional RS knowledge base:
    traditional_knowledge_base_df = pd.DataFrame()    
    merge_df = pd.DataFrame()
    filtered_df = pd.DataFrame()
    if (not item_df.empty) and (not context_df.empty):        
        # Merging rating_df, item_df and context_id dataframes:
        if 'context_id' not in rating_df.columns:
            st.error(f'The uploaded {config.RATING_TYPE} file must contain contextual information (context_id).')
        else:
            if not item_df.empty:
                merge_df = rating_df.merge(item_df, on='item_id')
            if not context_df.empty:
                merge_df = merge_df.merge(context_df, on='context_id')
            filtered_df = merge_df.copy()
            with st.expander(label='Show the dataset uploaded with the included contextual information'):
                st.dataframe(merge_df)
                wf_util.save_df(df_name='information_contextual_rating', df_value=merge_df, extension='csv')
            # Filtering contextual information:       
            st.markdown("""---""")
            st.markdown('**Contextual values selection**')
            attribute_list = merge_df.columns[4:].tolist()
            attribute_selected_list = st.multiselect(label='Select attributes', options=attribute_list, default=attribute_list, key='attribute_names')
            attribute_value_map = {}
            for attribute_name in attribute_selected_list:
                # All attribute values:
                atribute_value_list = merge_df[attribute_name].unique().tolist()
                # Remove NaN values using a list comprehension
                attribute_value_not_nan_list = []
                for attribute_value in atribute_value_list:
                    if not math.isnan(attribute_value):
                        attribute_value_not_nan_list.append(attribute_value)                
                # Selected attribute values:
                attribute_value_selected_list = st.multiselect(label=f'Select contextual values to filter the dataset for the attribute: {attribute_name}', options=attribute_value_not_nan_list, default=attribute_value_not_nan_list, key=f'attribute_values_{attribute_name}')                
                attribute_value_map[attribute_name] = attribute_value_selected_list
            # Reducing the CARS dataset to a 2D dataset, by using the contextual information:
            # if st.button(label='Filter', key='button_filter_dataset'):
            # Iterate through the dictionary and filter the DataFrame
            for attribute, values_to_filter in attribute_value_map.items():                    
                filtered_df = filtered_df[filtered_df[attribute].isin(values_to_filter)]
            # Removing duplicate values:
            filtered_df = filtered_df.drop_duplicates()
            # Sorting dataset by user_id, item_id and context_id:
            filtered_df = util.sort_rating_df(filtered_df)
            # Resetting values of the index column:
            filtered_df.reset_index(drop=True, inplace=True)
            # Showing the CARS dataset filtered by contextual information:
            with st.expander(label=f'Show the CARS dataset filtered by contextual information {attribute_selected_list}'):
                st.dataframe(filtered_df)
                wf_util.save_df(df_name='prefiltered_rating', df_value=filtered_df, extension='csv')
            # Removing the contextual information and context_id:
            traditional_knowledge_base_df = filtered_df.copy()
            if not traditional_knowledge_base_df.empty:                
                traditional_knowledge_base_df = traditional_knowledge_base_df.drop(columns=attribute_list+['context_id'])
                # Removing duplicate values:
                traditional_knowledge_base_df = traditional_knowledge_base_df.drop_duplicates()
                # Sorting dataset by user_id, item_id and context_id:                
                traditional_knowledge_base_df = util.sort_rating_df(traditional_knowledge_base_df)
                # Resetting values of the index column:
                traditional_knowledge_base_df.reset_index(drop=True, inplace=True)
                # Showing the 2D dataset built:
                with st.expander(label='Show the 2D dataset built (it will be used to evaluate a traditional RS)'):
                    st.dataframe(traditional_knowledge_base_df)
                    wf_util.save_df(df_name='rating', df_value=traditional_knowledge_base_df, extension='csv')
                print('The 2D dataset has been built, by filtering contextual information.')
            else:
                st.warning('The resulting rating dataset (2D) is empty, as a result of contextual filtering.')
    else:
        st.warning("The item and context files have not been uploaded.")
    return traditional_knowledge_base_df
