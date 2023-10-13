import console
import pandas as pd
import streamlit as st
from datagencars.synthetic_dataset.generator.generator_output_file.generator_user_file import GeneratorUserFile
from streamlit_app import config
from streamlit_app.generate_synthetic_dataset import wf_schema_util
from streamlit_app.preprocess_dataset import wf_util


def get_generation_config_schema():
    """
    Get the schema <generating_config_user.conf> for the generation of the user file.    
    :return: The edited content of the <generating_config_user.conf> schema.
    """
    st.header('General settings')    
    if st.checkbox('Upload the user data generation configuration file', value=True, key=f'is_upload_{config.GENERATION_CONFIG_USER_SCHEMA_NAME}'):
        # Uploading schema <"generation_config_user.conf">:
        schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.GENERATION_CONFIG_USER_SCHEMA_NAME, tab_type='tab_user')
    else:
        # Generating schema <"generation_config_user.conf">:
        schema_value = generate_generation_config_schema()
    # Editing schema:    
    return wf_schema_util.edit_schema_file(schema_file_name=config.GENERATION_CONFIG_USER_SCHEMA_NAME, schema_value=schema_value, tab_type='tab_user')

def generate_generation_config_schema():
    """
    Generate the schema <generating_config_user.conf> for the generation of the user file.    
    :return: The content of the <generating_config_user.conf> schema.
    """    
    with st.expander(f"Generate generating_config_user.conf"):
        # [dimension]        
        generation_config_user_schema = '[dimension] \n'
        user_count = st.number_input(label='Number of users to generate:', value=0)      
        generation_config_user_schema += 'number_user=' + str(user_count) + '\n'    
        percentage_null_user = st.number_input(label='Percentage of null user values:', value=0)
        generation_config_user_schema += 'percentage_user_null_value=' + str(percentage_null_user) + '\n'
    return generation_config_user_schema

def get_user_schema():
    """
    Get the schema <user_schema.conf>.
    :return: The edited user schema content.
    """
    st.header('Users')        
    if st.checkbox(f'Upload the data {config.USER_TYPE} schema file', value=True, key=f'is_upload_{config.USER_SCHEMA_NAME}_file'):
        # Uploading schema <user_schema.conf>:
        schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.USER_SCHEMA_NAME, tab_type='tab_user')
    else:
        # Generating schema <user_schema.conf:
        schema_value = wf_schema_util.get_schema_file(schema_type=config.USER_SCHEMA_NAME) 
    # Editing schema:    
    return wf_schema_util.edit_schema_file(schema_file_name=config.USER_SCHEMA_NAME, schema_value=schema_value, tab_type='tab_user')

def generate_user_file(generation_config, user_schema):
    """
    Generates the user file from user_schema. 
    :param generation_config: The configuration file of user data.
    :param user_schema: The user schema. It should contain information about users.    
    :return: The user file generated from the user schema.
    """
    user_file_df = pd.DataFrame()    
    if st.button(label='Generate user file', key='button_tab_user'):            
        if (len(user_schema) != 0) and (len(generation_config) != 0):
            output = st.empty()
            with console.st_log(output.code): 
                print(f'Generating {config.USER_TYPE}.csv')   
                generator = GeneratorUserFile(generation_config=generation_config, user_schema=user_schema)
                user_file_df = generator.generate_file()
                print('User file generation has finished.')   
                with st.expander(label=f'Show the generated {config.USER_TYPE}.csv file:'):
                    st.dataframe(user_file_df)
                    wf_util.save_df(df_name=config.USER_TYPE, df_value=user_file_df, extension='csv')
        else:
            st.warning(f'The user schema (user_schema.conf) and general setting (general_config.conf) files are required.')
    return user_file_df
