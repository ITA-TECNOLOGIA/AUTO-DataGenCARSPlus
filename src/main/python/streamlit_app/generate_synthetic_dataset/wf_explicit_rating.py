import streamlit as st
from streamlit_app import config, help_information
from streamlit_app.generate_synthetic_dataset import (wf_context, wf_item,
                                                      wf_rating, wf_user)
from streamlit_app.workflow_graph import workflow_image


def generate_synthtetic_dataset(with_context):
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
        tab_user, tab_item, tab_context, tab_rating  = st.tabs(config.CONTEXT_TAB_LIST)
    else:        
        tab_user, tab_item, tab_rating = st.tabs(config.WITHOUT_CONTEXT_TAB_LIST)
             
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
        item_schema = wf_item.get_item_schema()           
        # Generating or uploading <item_profile.conf>:
        with_correlation = st.checkbox(f'Apply correlation between item attributes?', value=False, key=f'is_with_correlation_{config.ITEM_PROFILE_SCHEMA_NAME}_file')        
        if with_correlation:
            item_profile = wf_item.get_item_profile_schema()
            # Generating <item.csv> with correlation (item_profile.conf is required):
            wf_item.generate_item_file(generation_config=generation_config_item, item_schema=item_schema, item_profile=item_profile)
        else:
            # Generating <item.csv> without correlation (item_profile.conf is not required):
            wf_item.generate_item_file(generation_config=generation_config_item, item_schema=item_schema)
    # TAB --> Context:
    if with_context:
        with tab_context:
            # Generating or uploading <generation_config_context.conf>:
            generation_config = wf_context.get_generation_config_schema()        
            # Generating or uploading <context_schema.conf>:
            context_schema = wf_context.get_context_schema()            
            # Generating <context.csv>:
            wf_context.generate_context_file(generation_config=generation_config, context_schema=context_schema)
    # TAB --> Rating:
    with tab_rating:
        ###### Generation config #####: 
        # Generating or uploading <generation_config.conf>:           
        generation_config = wf_rating.get_generation_config_schema(with_context)        
                           
        ###### User profile #####:
        # Generating or uploading <user_profile.csv>:
        user_profile_df, up_option = wf_rating.get_user_profile(with_context)                      

        ###### Rating file #####:
        # Generating <rating.csv>:        
        wf_rating.get_rating_file(with_context=with_context, generation_config=generation_config, user_profile_df=user_profile_df, up_option=up_option)
