import streamlit as st
from streamlit_app import config, help_information
from streamlit_app.generate_synthetic_dataset import (wf_context, wf_item,
                                                      wf_rating, wf_user,
                                                      wf_user_profile, wf_behavior)
from streamlit_app.workflow_graph import workflow_image


def generate_synthtetic_dataset(with_context, feedback_option):
    """
    Generates a synthetic dataset with explicit ratings.
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    """ 
    # Help information:
    help_information.help_explicit_rating_wf()

    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='GenerateSyntheticDataset(Explicit_ratings)', init_step='True', with_context=with_context, optional_value_list=[("UP", "Manual")])
    
    # Loading available tabs:
    if with_context:  
        if feedback_option == 'Implicit ratings':      
            tab_user, tab_item, tab_context, tab_behavior, tab_rating  = st.tabs(config.CONTEXT_IMPLICIT_TAB_LIST) 
        else:
            tab_user, tab_item, tab_context, tab_user_profile, tab_rating  = st.tabs(config.CONTEXT_EXPLICIT_TAB_LIST)
    else:        
        if feedback_option == 'Explicit ratings':
            tab_user, tab_item, tab_user_profile, tab_rating = st.tabs(config.WITHOUT_CONTEXT_EXPLICIT_TAB_LIST)
        else:
            tab_user, tab_item, tab_behavior, tab_rating = st.tabs(config.WITHOUT_CONTEXT_IMPLICIT_TAB_LIST)
             
    # TAB --> User:
    with tab_user:
        # Generating or uploading <generation_config_user.conf>:
        generation_config = wf_user.get_generation_config_schema()        
        # Generating or uploading <user_schema.conf>:
        user_schema = wf_user.get_user_schema()              
        # Generating <user.csv>:
        wf_user.generate_user_file(generation_config=generation_config, user_schema=user_schema)
    # TAB --> Item and Item Profile:
    with tab_item:
        # Generating or uploading <generation_config_item.conf>:
        generation_config_item = wf_item.get_generation_config_schema()
        # Generating or uploading <user_schema.conf>:
        item_schema = wf_item.get_item_schema(n=1)
        # Generating or uploading <item_profile.conf>:
        with_correlation = st.checkbox(f'Apply correlation between item attributes?', value=False, key=f'is_with_correlation_{config.ITEM_PROFILE_SCHEMA_NAME}_file')        
        if with_correlation:
            item_profile = wf_item.get_item_profile_schema()
            # Generating <item.csv> with correlation (item_profile.conf is required):
            item_file_df = wf_item.generate_item_file(generation_config=generation_config_item, item_schema=item_schema, item_profile=item_profile)
        else:
            # Generating <item.csv> without correlation (item_profile.conf is not required):
            item_file_df = wf_item.generate_item_file(generation_config=generation_config_item, item_schema=item_schema)
    # TAB --> Context:
    if with_context:
        with tab_context:
            # Generating or uploading <generation_config_context.conf>:
            generation_config = wf_context.get_generation_config_schema()        
            # Generating or uploading <context_schema.conf>:
            context_schema = wf_context.get_context_schema()            
            # Generating <context.csv>:
            wf_context.generate_context_file(generation_config=generation_config, context_schema=context_schema)    
    if feedback_option == 'Implicit ratings':
        with tab_behavior:
            generation_config = wf_behavior.get_generation_config_schema()
            behavior_schema = wf_behavior.get_behavior_schema()
            item_schema = wf_item.get_item_schema(n=2)
            item_file_df = wf_behavior.get_item_file_df()
            wf_behavior.generate_behavior_file(generation_config, behavior_schema, item_file_df, item_schema)
    if feedback_option == 'Explicit ratings':
        # TAB --> User Profile:
        with tab_user_profile:
            ###### User profile #####:
            # Generating <user_profile.csv>:
            user_profile_df = wf_user_profile.get_user_profile(with_context)
    # TAB --> Rating:
    with tab_rating: 
        ###### Generation config #####: 
        # Generating or uploading <generation_config.conf>:           
        generation_config = wf_rating.get_generation_config_schema(with_context, implicit=True)

        ###### Item and context schemas #####:
        # Uploading <item_schema.conf> or <context_schema.conf>:
        if feedback_option == 'Explicit ratings': 
            if with_context:
                item_schema, context_schema = wf_rating.get_item_context_schema()
            else:
                item_schema = wf_rating.get_item_schema(n=3)

        ###### User, Item and context files #####:
        # Uploading <user.csv>, <item.csv> or <context.csv> or <behavior.csv>:
        if with_context:
            if feedback_option == 'Implicit ratings': 
                user_df, item_df, context_df, behavior_df = wf_rating.get_user_item_context_behavior_df()
            else:
                # Explicit ratings:
                user_df, item_df, context_df = wf_rating.get_user_item_context_df()
        else:
            if feedback_option == 'Implicit ratings': 
                user_df, item_df, behavior_df = wf_rating.get_user_item_behavior_df()
            else:
                # Explicit ratings:
                user_df, item_df = wf_rating.get_user_item_df()

        ###### User profile #####:
        # Uploading <user_profile.csv>:
        if feedback_option == 'Explicit ratings': 
            user_profile_df = wf_rating.get_user_profile()

        ###### Rating file #####:
        # Generating <rating.csv>:
        if with_context:
            if feedback_option == 'Implicit ratings':
                # TODO generate_implicit_rating_file() 
                wf_rating.generate_implicit_rating_file(with_context=with_context, generation_config=generation_config, user_df=user_df, item_df=item_df, context_df=context_df, behavior_df=behavior_df)
            else:
                # Explicit ratings:
                # TODO generate_explicit_rating_file()
                wf_rating.generate_explicit_rating_file(with_context=with_context, generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df, item_schema=item_schema, context_df=context_df, context_schema=context_schema)
        else:
            if feedback_option == 'Implicit ratings':
                # TODO generate_implicit_rating_file()
                wf_rating.generate_implicit_rating_file(with_context=with_context, generation_config=generation_config, user_df=user_df, item_df=item_df, behavior_df=behavior_df)
            else:
                # Explicit ratings:
                # TODO generate_explicit_rating_file()
                wf_rating.generate_explicit_rating_file(with_context=with_context, generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df, item_schema=item_schema)
