import streamlit as st
from streamlit_app import config
from streamlit_app.analysis_dataset.visualization import st_visualization_rating, st_visualization_uicb
from streamlit_app.preprocess_dataset import wf_util


def generate(with_context):
    """
    Generates the data visualization.
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    """
    st.header('Data Visualization')
    
    # Loading a dataset:
    feedback_option = st.radio(label='Select a type of user feedback:', options=config.VISUALIZATION_OPTIONS)

    user_tab=item_tab=context_tab=behavior_tab=rating_tab= None
    if with_context:
        if feedback_option == 'Implicit ratings':            
            user_tab, item_tab, context_tab, behavior_tab, rating_tab = st.tabs(['Users', 'Items', 'Contexts', 'Behaviors', 'Ratings'])
        elif feedback_option == 'Explicit ratings':            
            user_tab, item_tab, context_tab, rating_tab = st.tabs(['Users', 'Items', 'Contexts', 'Ratings'])
    else:
        if feedback_option == 'Implicit ratings':            
            user_tab, item_tab, behavior_tab, rating_tab = st.tabs(['Users', 'Items', 'Behaviors', 'Ratings'])
        elif feedback_option == 'Explicit ratings':
            user_tab, item_tab, rating_tab = st.tabs(['Users', 'Items', 'Ratings'])

    # TAB --> Users:
    if user_tab:
        with user_tab:
            # Loading user file:
            user_df = wf_util.load_one_file(config.USER_TYPE, wf_type='tab_user')
            # Visualizing user information:
            st_visualization_uicb.show_information(df=user_df, file_type=config.USER_TYPE)
    # TAB --> Items:
    if item_tab:
        with item_tab:
            # Loading item file:
            item_df = wf_util.load_one_file(config.ITEM_TYPE, wf_type='tab_item')
            # Visualizing item information:
            st_visualization_uicb.show_information(df=item_df, file_type=config.ITEM_TYPE)
    # TAB --> Contexts:
    if context_tab:
        with context_tab:
            # Loading context file:
            context_df = wf_util.load_one_file(config.CONTEXT_TYPE, wf_type='tab_context')
            # Visualizing context information:
            st_visualization_uicb.show_information(df=context_df, file_type=config.CONTEXT_TYPE)
    # TAB --> Behaviors:
    if behavior_tab:
        with behavior_tab:
            # Loading behavior file:
            behavior_df = wf_util.load_one_file(config.BEHAVIOR_TYPE, wf_type='tab_behavior')            
            # Visualizing rating information:
            st_visualization_uicb.show_information(df=behavior_df, file_type=config.BEHAVIOR_TYPE)
    # TAB --> Ratings:
    if rating_tab:
        with rating_tab:
            # Loading rating file:
            rating_df = wf_util.load_one_file(config.RATING_TYPE, wf_type='tab_rating')
            # Visualizing rating information:
            st_visualization_rating.show_information(rating_df=rating_df, with_context=with_context)   
