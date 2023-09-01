import config
import streamlit as st
from streamlit_app.analysis_dataset import evaluation, visualization
from streamlit_app.generate_synthetic_dataset import (wf_explicit_rating,
                                                      wf_implicit_rating)
from streamlit_app.preprocess_dataset import (wf_extend_dataset,
                                              wf_generate_user_profile,
                                              wf_mapping_categorization,
                                              wf_ratings_to_binary,
                                              wf_recalculate_dataset,
                                              wf_replace_null_values,
                                              wf_replicate_dataset,
                                              wf_util)
import pandas as pd


# Setting the main page:
st.set_page_config(page_title=config.APP_TITLE,
                   page_icon=config.APP_ICON,
                   layout=config.APP_LAYOUT[0],
                   initial_sidebar_state=config.APP_INITIAL_SIDEBAR_STATE[0],
                   menu_items= None)

# Description, title and icon:
st.markdown("""---""")
col1, col2 = st.columns(2)
with col1:
    # Title:
    st.header(config.APP_TITLE)
    # Description:
    st.write(config.APP_DESCRIPTION)
with col2:    
    # Icon:
    st.image(image=config.APP_ICON, use_column_width=False, output_format="auto", width=180)
st.markdown("""---""")

# Tool bar with AUTO-DataGenCARS options:
general_option = st.sidebar.selectbox(label='**Options available:**', options=config.GENERAL_OPTIONS)
# Selecting whether the dataset has contextual information:
with_context = st.sidebar.checkbox('With context', value=True)

####### Generate a synthetic dataset #######
if general_option == 'Generate a synthetic dataset':
    # Selecting a rating feedback option:
    feedback_option = st.sidebar.radio(label='Select a type of user feedback:', options=config.RATING_FEEDBACK_OPTIONS)
    # WF --> Explicit ratings:
    if feedback_option == 'Explicit ratings':
        wf_explicit_rating.generate_synthtetic_dataset(with_context)   
    # # WF --> Implicit ratings:
    # elif feedback_option == 'Implicit ratings':   
    #     wf_implicit_rating.generate_synthtetic_dataset()
        
####### Pre-process a dataset #######
elif general_option == 'Pre-process a dataset':    
    # Selecting a workflow option:
    wf_option = st.sidebar.radio(label='Select a workflow:', options=config.WF_OPTIONS)
    
    # WF --> Replace NULL values:
    if wf_option == 'Replace NULL values':        
        if with_context:
            # Setting tabs:
            tab_replace_null_values_item, tab_replace_null_values_context = st.tabs(['Replace NULL values (item.csv)', 'Replace NULL values (context.csv)'])            
            # Apply WF: "Replace NULL values":
            wf_replace_null_values.generate(with_context, tab_replace_null_values_item, tab_replace_null_values_context)
        else:
            # Setting tabs:
            tab_replace_null_values_item, tab_empty = st.tabs(['Replace NULL values (item.csv)', '-'])
            # Apply WF: "Replace NULL values":
            wf_replace_null_values.generate(with_context, tab_replace_null_values_item)        
        
    # WF --> Generate User Profile:
    elif wf_option == 'Generate user profile':
        null_values_i = True
        null_values_c = True
        if with_context:
            # Setting tabs:
            tab_replace_null_values_item, tab_replace_null_values_context, tab_generate_user_profile = st.tabs(['Replace NULL values (item.csv)', 'Replace NULL values (context.csv)', 'Generate User Profile'])            
            # Apply WF: "Replace NULL values":
            new_item_df, new_context_df = wf_replace_null_values.generate(with_context, tab_replace_null_values_item, tab_replace_null_values_context)
            if new_item_df.empty:
                null_values_i = False
            if new_context_df.empty:
                null_values_c = False
        else:
            # Setting tabs:
            tab_replace_null_values_item, tab_generate_user_profile = st.tabs(['Replace NULL values (item.csv)', 'Generate User Profile'])
            # Apply WF: "Replace NULL values":
            new_item_df, __ = wf_replace_null_values.generate(with_context, tab_replace_null_values_item)   
            if new_item_df.empty:
                null_values_i = False     
        # Apply WF: "Generate User Profile":        
        with tab_generate_user_profile:
            wf_generate_user_profile.generate(with_context, null_values_i, null_values_c)

    # WF --> Replicate dataset:    
    elif wf_option == 'Replicate dataset':
        null_values_i = True
        null_values_c = True
        if with_context:
            # Setting tabs:
            tab_replace_null_values_item, tab_replace_null_values_context, tab_generate_user_profile, tab_replicate_dataset = st.tabs(['Replace NULL values (item.csv)', 'Replace NULL values (context.csv)', 'Generate user profile', 'Replicate dataset'])
            # Apply WF: "Replace NULL values":            
            new_item_df, new_context_df = wf_replace_null_values.generate(with_context, tab_replace_null_values_item, tab_replace_null_values_context)
            if new_item_df.empty:
                null_values_i = False
            if new_context_df.empty:
                null_values_c = False
        else:
            tab_replace_null_values_item, tab_generate_user_profile, tab_replicate_dataset = st.tabs(['Replace NULL values (item.csv)', 'Generate user profile', 'Replicate dataset'])
            # Apply WF: "Replace NULL values":
            new_item_df, __ = wf_replace_null_values.generate(with_context, tab_replace_null_values_item)            
            if new_item_df.empty:
                null_values_i = False
        # Apply WF: "Generate User Profile":            
        with tab_generate_user_profile:
            wf_generate_user_profile.generate(with_context, null_values_i, null_values_c, only_automatic=True)
        # Apply WF: "Replicate Dataset":
        with tab_replicate_dataset:
            if with_context:
                wf_replicate_dataset.generate(with_context, null_values_i, null_values_c)
            else:
                wf_replicate_dataset.generate(with_context, null_values_i)

    # WF --> Extend dataset:
    elif wf_option == 'Extend dataset':
        null_values_i = True
        null_values_c = True
        if with_context:
            # Setting tabs:
            tab_replace_null_values_item, tab_replace_null_values_context, tab_generate_user_profile, tab_extend_dataset = st.tabs(['Replace NULL values (item.csv)', 'Replace NULL values (context.csv)', 'Generate user profile', 'Extend dataset'])
            # Apply WF: "Replace NULL values":            
            new_item_df, new_context_df = wf_replace_null_values.generate(with_context, tab_replace_null_values_item, tab_replace_null_values_context)
            if new_item_df.empty:
                null_values_i = False
            if new_context_df.empty:
                null_values_c = False
        else:
            tab_replace_null_values_item, tab_generate_user_profile, tab_extend_dataset = st.tabs(['Replace NULL values (item.csv)', 'Generate user profile', 'Extend dataset'])
            # Apply WF: "Replace NULL values":
            new_item_df, __ = wf_replace_null_values.generate(with_context, tab_replace_null_values_item)            
            if new_item_df.empty:
                null_values_i = False
        # Apply WF: "Generate User Profile":            
        with tab_generate_user_profile:
            wf_generate_user_profile.generate(with_context, null_values_i, null_values_c, only_automatic=True)
        # Apply WF: "Extend Dataset":
        with tab_extend_dataset:
            if with_context:
                wf_extend_dataset.generate(with_context, null_values_i, null_values_c)
            else:
                wf_extend_dataset.generate(with_context, null_values_i)       

    # WF --> Recalculate ratings:
    elif wf_option == 'Recalculate ratings': 
       wf_recalculate_dataset.generate()

    # # WF --> Ratings to binary:
    # elif wf_option == 'Ratings to binary':    
    #     wf_ratings_to_binary.generate()
    # # WF --> Mapping categorization
    # elif wf_option == 'Mapping categorization':
    #     wf_mapping_categorization.generate()

# ####### Analysis a dataset #######
# elif general_option == 'Analysis a dataset':
#     # Loading a dataset:
#     st.header('Load dataset')
#     if with_context:
#         user_df, item_df, context_df, rating_df = util.load_dataset(file_type_list=['user', 'item', 'context', 'rating'])
#     else:
#         user_df, item_df, __, rating_df = util.load_dataset(file_type_list=['user', 'item', 'rating'])
#     # 
#     if "lars" and "side_lars" in st.session_state:
#         lars = st.session_state["lars"]
#         side_lars = st.session_state["side_lars"]
#         if lars and side_lars:
#             behavior_df = util.load_one_file('behavior')
#     # Selecting a analysis option:
#     analysis_option = st.sidebar.radio(label='Select one option:', options=config.ANLYSIS_OPTIONS)
#     # Visualization:
#     if analysis_option == 'Visualization':
#         visualization
#     # Evaluation:    
#     elif analysis_option == 'Evaluation':
#         evaluation
  