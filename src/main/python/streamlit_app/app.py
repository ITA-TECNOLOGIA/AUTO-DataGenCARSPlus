# import sys
# sys.path.append("/data/bfranco/auto_datagencars/src/main/python")
import streamlit as st
from streamlit_app import config
from streamlit_app.analysis_dataset.evaluation import (st_evaluation_cars,
                                                       st_evaluation_rs)
from streamlit_app.analysis_dataset.visualization import st_visualization
from streamlit_app.dashboard import user_behavior, user_register
from streamlit_app.generate_synthetic_dataset import (wf_dataset,
                                                      wf_implicit_rating)
from streamlit_app.preprocess_dataset import (wf_transform_attributes,
                                              wf_extend_dataset,
                                              wf_generate_user_profile,
                                              wf_recalculate_ratings,
                                              wf_replace_null_values,
                                              wf_generate_null_values,
                                              wf_replicate_dataset, wf_util)


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

# User Information register:
user_register.generate_implicit()
st.markdown("""---""")

# AUTO-DataGenCARS forms:
# Tool bar with AUTO-DataGenCARS options:
general_option = st.sidebar.selectbox(label='**Options available:**', options=config.GENERAL_OPTIONS)
# Selecting whether the dataset has contextual information:
with_context = st.sidebar.checkbox('With context', value=True)

####### Generate a synthetic dataset #######
if general_option == 'Generate a synthetic dataset':
    # Selecting a rating feedback option:
    feedback_option = st.sidebar.radio(label='Select a type of user feedback:', options=config.RATING_FEEDBACK_OPTIONS)
    # WF --> Explicit and Implicit ratings:
    wf_dataset.generate_synthtetic_dataset(with_context, feedback_option)
        
####### Pre-process a dataset #######
elif general_option == 'Pre-process a dataset':    
    # Selecting a workflow option:
    wf_option = st.sidebar.radio(label='Select a workflow:', options=config.WF_OPTIONS)
    
    # WF --> Generate NULL values:
    if wf_option == 'Generate NULL values':        
        if with_context:
            # Setting tabs:
            tab_generate_null_values_item, tab_generate_null_values_context = st.tabs(['Generate NULL values (item.csv)', 'Generate NULL values (context.csv)'])            
            # Apply WF: "Generate NULL values":
            wf_generate_null_values.generate(with_context, tab_generate_null_values_item, tab_generate_null_values_context)
        else:
            # Setting tabs:
            tab_generate_null_values_item, tab_empty = st.tabs(['Generate NULL values (item.csv)', '-'])
            # Apply WF: "Generate NULL values":
            wf_generate_null_values.generate(with_context, tab_generate_null_values_item)   

    # WF --> Replace NULL values:
    elif wf_option == 'Replace NULL values':
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
        if with_context:
            # Setting tabs:
            tab_replace_null_values_item, tab_replace_null_values_context, tab_generate_user_profile = st.tabs(['Replace NULL values (item.csv)', 'Replace NULL values (context.csv)', 'Generate User Profile'])            
            # Apply WF: "Replace NULL values":
            wf_replace_null_values.generate(with_context, tab_replace_null_values_item, tab_replace_null_values_context)            
        else:
            # Setting tabs:
            tab_replace_null_values_item, tab_generate_user_profile = st.tabs(['Replace NULL values (item.csv)', 'Generate User Profile'])
            # Apply WF: "Replace NULL values":
            wf_replace_null_values.generate(with_context, tab_replace_null_values_item)               
        # Apply WF: "Generate User Profile":        
        with tab_generate_user_profile:
            wf_generate_user_profile.generate(with_context)

    # WF --> Replicate dataset:    
    elif wf_option == 'Replicate dataset':        
        st.empty()        
        if with_context:
            # Setting tabs:
            tab_replace_null_values_item, tab_replace_null_values_context, tab_generate_user_profile, tab_replicate_dataset = st.tabs(['Replace NULL values (item.csv)', 'Replace NULL values (context.csv)', 'Generate user profile', 'Replicate dataset'])
            # Apply WF: "Replace NULL values":            
            wf_replace_null_values.generate(with_context, tab_replace_null_values_item, tab_replace_null_values_context)            
        else:
            tab_replace_null_values_item, tab_generate_user_profile, tab_replicate_dataset = st.tabs(['Replace NULL values (item.csv)', 'Generate user profile', 'Replicate dataset'])
            # Apply WF: "Replace NULL values":
            wf_replace_null_values.generate(with_context, tab_replace_null_values_item)
        # Apply WF: "Generate User Profile":            
        with tab_generate_user_profile:
            wf_generate_user_profile.generate(with_context, only_automatic=True)
        # Apply WF: "Replicate Dataset":
        with tab_replicate_dataset:
            wf_replicate_dataset.generate(with_context) 

    # WF --> Extend dataset:
    elif wf_option == 'Extend dataset':        
        if with_context:
            # Setting tabs:
            tab_replace_null_values_item, tab_replace_null_values_context, tab_generate_user_profile, tab_extend_dataset = st.tabs(['Replace NULL values (item.csv)', 'Replace NULL values (context.csv)', 'Generate user profile', 'Extend dataset'])
            # Apply WF: "Replace NULL values":            
            wf_replace_null_values.generate(with_context, tab_replace_null_values_item, tab_replace_null_values_context)            
        else:
            tab_replace_null_values_item, tab_generate_user_profile, tab_extend_dataset = st.tabs(['Replace NULL values (item.csv)', 'Generate user profile', 'Extend dataset'])
            # Apply WF: "Replace NULL values":
            wf_replace_null_values.generate(with_context, tab_replace_null_values_item)
        # Apply WF: "Generate User Profile":            
        with tab_generate_user_profile:
            wf_generate_user_profile.generate(with_context, only_automatic=True)
        # Apply WF: "Extend Dataset":
        with tab_extend_dataset:
            if with_context:
                wf_extend_dataset.generate(with_context)
            else:
                wf_extend_dataset.generate(with_context)

    # WF --> Recalculate ratings:
    elif wf_option == 'Recalculate ratings':         
        if with_context:
            # Setting tabs:
            tab_replace_null_values_item, tab_replace_null_values_context, tab_generate_user_profile, tab_extend_dataset = st.tabs(['Replace NULL values (item.csv)', 'Replace NULL values (context.csv)', 'Generate user profile', 'Recalculate dataset'])
            # Apply WF: "Replace NULL values":            
            wf_replace_null_values.generate(with_context, tab_replace_null_values_item, tab_replace_null_values_context)          
        else:
            tab_replace_null_values_item, tab_generate_user_profile, tab_extend_dataset = st.tabs(['Replace NULL values (item.csv)', 'Generate user profile', 'Recalculate dataset'])
            # Apply WF: "Replace NULL values":
            wf_replace_null_values.generate(with_context, tab_replace_null_values_item)
        # Apply WF: "Generate User Profile":            
        with tab_generate_user_profile:
            wf_generate_user_profile.generate(with_context, only_automatic=True)
        # Apply WF: "Extend Dataset":
        with tab_extend_dataset:
            if with_context:
                wf_recalculate_ratings.generate(with_context)
            else:
                wf_recalculate_ratings.generate(with_context)

    # WF --> Transform attributes:
    elif wf_option == 'Transform attributes':
        wf_transform_attributes.generate(with_context)
    
####### Analysis a dataset #######
elif general_option == 'Analysis a dataset':    
    # Selecting a analysis option:
    analysis_option = st.sidebar.radio(label='Select one option:', options=config.ANLYSIS_OPTIONS)

    # Visualization:
    if analysis_option == 'Visualization':
        st_visualization.generate(with_context)

    # Evaluation:    
    elif analysis_option == 'Evaluation':
        # Loading rating file:
        st.write('Upload the following file: ')
        rating_df = wf_util.load_one_file(config.RATING_TYPE, wf_type='evaluation_rating_df')        

        # CARS Evaluation:
        if with_context:        
            st_evaluation_cars.generate(rating_df)
        # Traditional RS Evaluation:
        else:
            st_evaluation_rs.generate(rating_df)

####### Dashboard #######    
elif general_option == 'Dashboard':
    user_database_df = user_register.load_user_database()
    user_behavior.show_user_map(df=user_database_df)
    