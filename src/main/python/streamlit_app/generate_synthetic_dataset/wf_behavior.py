import console
import streamlit as st
import pandas as pd
from streamlit_app import config
from streamlit_app.preprocess_dataset import wf_util
from streamlit_app.generate_synthetic_dataset import wf_schema_util
from datagencars.synthetic_dataset.generate_synthetic_implicit_dataset import GenerateSyntheticImplicitDataset


def get_generation_config_schema():
    """
    Get the schema <generating_config_behavior.conf> for the generation of the behavior file.    
    :return: The edited content of the <generating_config_behavior.conf> schema.
    """
    st.header('General Settings')    
    if st.checkbox('Upload the behavior data generation configuration file', value=True, key=f'is_upload_{config.GENERATION_CONFIG_BEHAVIOR_SCHEMA_NAME}'):
        # Uploading schema <"generation_config_behavior.conf">:
        schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.GENERATION_CONFIG_BEHAVIOR_SCHEMA_NAME, tab_type='tab_behavior')
    else:
        # Generating schema <"generation_config_behavior.conf">:
        schema_value = generate_generation_config_schema()
    # Editing schema:
    return wf_schema_util.edit_schema_file(schema_file_name=config.GENERATION_CONFIG_BEHAVIOR_SCHEMA_NAME, schema_value=schema_value, tab_type='tab_behavior')

def generate_generation_config_schema():
    """
    Generate the schema <generating_config_behavior.conf> for the generation of the behavior file.    
    :return: The content of the <generating_config_behavior.conf> schema.
    """    
    with st.expander(f"Generate generating_config_behavior.conf"):
        # [dimension]        
        generation_config_behavior_schema = '[dimension] \n'
        behavior_count = st.number_input(label='Number of behaviors to generate:', value=0)      
        generation_config_behavior_schema += 'number_behavior=' + str(behavior_count) + '\n'
    return generation_config_behavior_schema

def get_behavior_schema():
    """
    Get the schema <behavior_schema.conf>.
    :return: The edited behavior schema content.
    """
    st.header('Behavior Schema')        
    if st.checkbox(f'Upload the data {config.BEHAVIOR_TYPE} schema file', value=True, key=f'is_upload_{config.BEHAVIOR_SCHEMA_NAME}_file'):
        # Uploading schema <behavior_schema.conf>:
        schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.BEHAVIOR_SCHEMA_NAME, tab_type='tab_behavior')
    else:
        # Generating schema <behavior_schema.conf:
        schema_value = wf_schema_util.get_schema_file(schema_type=config.BEHAVIOR_SCHEMA_NAME) 
    # Editing schema:    
    return wf_schema_util.edit_schema_file(schema_file_name=config.BEHAVIOR_SCHEMA_NAME, schema_value=schema_value, tab_type='tab_user')

def get_item_file_df():
    """
    Get the item file dataframe.
    :return: The item file dataframe.
    """
    item_file_df = pd.DataFrame()
    # Uploading item file:
    st.header(f'Data {config.ITEM_TYPE} file')
    item_file_df = wf_util.load_one_file(file_type=config.ITEM_TYPE, wf_type='tab_behavior')
    return item_file_df

def generate_behavior_file(generation_config, behavior_schema, item_file_df, item_schema):
    """
    Generates the behavior file.
    :param generation_config: The configuration file of behavior data.
    :return: The user file generated from the user schema.
    """
    behavior_file_df = pd.DataFrame()
    if st.button(label='Generate behavior file', key='button_tab_behavior'):
        if (len(behavior_schema) != 0) and len(item_file_df) != 0 and len(item_schema) != 0:
            output = st.empty()
            with console.st_log(output.code):
                print(f'Generating {config.BEHAVIOR_TYPE}.csv')
                generator = GenerateSyntheticImplicitDataset(generation_config=generation_config)
                behavior_file_df = generator.generate_behavior_file(behavior_schema=behavior_schema, item_df=item_file_df, item_schema=item_schema)
                print('Behavior file generation has finished.')   
                with st.expander(label=f'Show the generated {config.BEHAVIOR_TYPE}.csv file:'):
                    st.dataframe(behavior_file_df)
                    wf_util.save_df(df_name=config.BEHAVIOR_TYPE, df_value=behavior_file_df, extension='csv')
        else:
            st.warning(f'The behavior schema (behavior_schema.conf) and general setting (general_config.conf) files are required.')
    return behavior_file_df
