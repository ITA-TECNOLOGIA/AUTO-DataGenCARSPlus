import pandas as pd
import streamlit as st
from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from streamlit_app import config, help_information
from streamlit_app.generate_synthetic_dataset import wf_schema_util
from streamlit_app.preprocess_dataset import wf_generate_user_profile


def get_user_profile(with_context):
    """
    Retrieve or generate a user profile dataframe based on the chosen options.
    :param with_context: A boolean indicating whether to include context data.
    :return: A dataframe containing user profiles and an option indicating how the data was obtained.
    """       
    user_schema=item_schema=context_schema=''
    user_profile_df = pd.DataFrame()    
    # Generating <user_profile.csv>:             
    if with_context:
        user_schema = get_user_schema()
        item_schema = get_item_schema()
        context_schema = get_context_schema()
        if (len(user_schema) != 0) and (len(item_schema) != 0) and (len(context_schema) != 0):
            user_profile_df = generate_user_profile(user_schema, item_schema, context_schema)
        else:
            st.warning('The user, item and context schemas are required.')
    else:
        user_schema = get_user_schema()
        item_schema = get_item_schema()
        if (len(user_schema) != 0) and (len(item_schema) != 0):            
            user_profile_df = generate_user_profile(user_schema, item_schema)
        else:
            st.warning('The user and item schemas are required.')
    return user_profile_df

def get_user_schema():
    """
    Load the user schema.
    :return: The user schema.
    """
    st.header('User Schema')
    # Uploading <user_schema.conf>:
    user_schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.USER_SCHEMA_NAME, tab_type=f'tab_user_profile_user')
    # Editing schema:
    user_schema = wf_schema_util.edit_schema_file(schema_file_name=config.USER_SCHEMA_NAME, schema_value=user_schema_value, tab_type=f'tab_user_profile_user')         
    return user_schema

def get_item_schema():
    """
    Load the item schema.
    :return: The item schema.
    """
    st.header('Item Schema')
    # Uploading <item_schema.conf>:
    item_schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.ITEM_SCHEMA_NAME, tab_type=f'tab_user_profile_item')
    # Editing schema:
    item_schema = wf_schema_util.edit_schema_file(schema_file_name=config.ITEM_SCHEMA_NAME, schema_value=item_schema_value, tab_type=f'tab_user_profile_item')
    return item_schema

def get_context_schema():
    """
    Load the context schema.
    :return: The context schema.
    """
    st.header('Context Schema')
    # Uploading <context_schema.conf>: optional     
    context_schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.CONTEXT_SCHEMA_NAME, tab_type=f'tab_user_profile_context')
    # Editing schema:
    context_schema = wf_schema_util.edit_schema_file(schema_file_name=config.CONTEXT_SCHEMA_NAME, schema_value=context_schema_value, tab_type=f'tab_user_profile_context')
    return context_schema

def generate_user_profile(user_schema, item_schema, context_schema=None):
    """
    Generate the user profile file (user_profile.csv).
    :param user_schema: The content of the user schema file.
    :param item_schema: The content of the item schema file.
    :param context_schema: The content of the context schema file <optional>.
    :return: The content of the item profile file.
    """
    st.header('User Profile')
    # Help information:
    help_information.help_user_profile_manual()    
    with st.expander(label='Generate user_profile.csv'):
        # Adding column "id":
        attribute_column_list = ['user_profile_id']
        # Adding relevant item attribute columns:        
        item_access_schema = AccessSchema(file_str=item_schema)
        item_attribute_name_list = item_access_schema.get_important_attribute_name_list()
        attribute_column_list.extend(item_attribute_name_list)   
        item_possible_value_map = {}
        for item_attribute_name in item_attribute_name_list:
            item_possible_value_map[item_attribute_name] = item_access_schema.get_possible_values_attribute_list_from_name(attribute_name=item_attribute_name)                
        # Adding relevant context attribute columns:    
        context_possible_value_map = {}
        if context_schema:
            context_access_schema = AccessSchema(file_str=context_schema)
            context_attribute_name_list = context_access_schema.get_important_attribute_name_list()
            attribute_column_list.extend(context_attribute_name_list)            
            for context_attribute_name in context_attribute_name_list:
                context_possible_value_map = context_access_schema.get_possible_values_attribute_list_from_name(attribute_name=context_attribute_name)
        # Adding column "other":
        attribute_column_list.extend(['other']) 
        # Introducing the number of user profiles to generate:            
        user_access = AccessSchema(file_str=user_schema)
        initial_value = len(user_access.get_possible_values_attribute_list_from_name(attribute_name='user_profile_id'))
        number_user_profile = st.number_input(label='Number of user profiles:', value=initial_value, disabled=True)
        st.warning('**Observations:**')
        st.warning('- The number of profiles has been previously defined in the ```user_profile_id``` attribute of the ```user_schema.conf``` file. If you want to change it, you must first modify the ```user_schema.conf``` file.')                            
        st.warning('- If there is no contextual information in the matrix (based on item and/or context attributes), it is because the ```important_weight_attribute_x``` field of the item and/or context schemas is False. If certain item and/or context attribute names are required to be displayed in the matrix, you must edit the item and/or context schemas and set the ```important_weight_attribute_x field=True```.')
        # Generate user profile manual:                
        user_profile_df = wf_generate_user_profile.generate_user_profile_manual(number_user_profile, attribute_column_list, item_possible_value_map, context_possible_value_map)
    return user_profile_df
