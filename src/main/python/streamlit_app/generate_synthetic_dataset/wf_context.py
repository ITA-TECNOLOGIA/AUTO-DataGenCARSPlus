import console
import pandas as pd
import streamlit as st
from datagencars.synthetic_dataset.generator.generator_output_file.generator_context_file import GeneratorContextFile
from streamlit_app import config
from streamlit_app.generate_synthetic_dataset import wf_schema_util
from streamlit_app.preprocess_dataset import wf_util


def get_generation_config_schema():
    """
    Get the schema <generating_config_context.conf> for the generation of the context file.    
    :return: The edited content of the <generating_config_context.conf> schema.
    """
    st.header('General Settings')    
    if st.checkbox('Upload the context data generation configuration file', value=True, key=f'is_upload_{config.GENERATION_CONFIG_CONTEXT_SCHEMA_NAME}'):
        # Uploading schema <"generating_config_context.conf">:
        schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.GENERATION_CONFIG_CONTEXT_SCHEMA_NAME, tab_type='tab_context')
    else:
        # Generating schema <"generating_config_context.conf">:
        schema_value = generate_generation_config_schema()
    # Editing schema:    
    return wf_schema_util.edit_schema_file(schema_file_name=config.GENERATION_CONFIG_CONTEXT_SCHEMA_NAME, schema_value=schema_value, tab_type='tab_context')

def generate_generation_config_schema():
    """
    Generate the schema <generating_config_context.conf> for the generation of the context file.    
    :return: The content of the <generating_config_context.conf> schema.
    """    
    with st.expander(f"Generate generating_config_context.conf"):
        # [dimension]        
        generation_config_context_schema = '[dimension] \n'
        context_count = st.number_input(label='Number of contexts to generate:', value=0)      
        generation_config_context_schema += 'number_context=' + str(context_count) + '\n'    
        percentage_null_context = st.number_input(label='Percentage of null context values:', value=0)
        generation_config_context_schema += 'percentage_context_null_value=' + str(percentage_null_context) + '\n'
    return generation_config_context_schema

def get_context_schema():
    """
    Get the schema <context_schema.conf>.
    :return: The edited context schema content.
    """
    st.header('Context Schema')        
    if st.checkbox(f'Upload the data {config.CONTEXT_TYPE} schema file', value=True, key=f'is_upload_{config.CONTEXT_SCHEMA_NAME}_file'):
        # Uploading schema <context_schema.conf>:
        schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.CONTEXT_SCHEMA_NAME, tab_type='tab_context')
    else:
        # Generating schema <context_schema.conf:
        schema_value = wf_schema_util.get_schema_file(schema_type=config.CONTEXT_SCHEMA_NAME) 
    # Editing schema:    
    return wf_schema_util.edit_schema_file(schema_file_name=config.CONTEXT_SCHEMA_NAME, schema_value=schema_value, tab_type='tab_context')

def generate_context_file(generation_config, context_schema):    
    """
    Generates the context file from context_schema. 
    :param context_schema: The context schema. It should contain information about contexts.
    :param generation_config: The configuration file.
    :return: The context file generated from the context schema.
    """           
    context_file_df = pd.DataFrame()
    if st.button(label='Generate context file', key='button_tab_context'):            
        if (len(context_schema) != 0) and (len(generation_config) != 0):
            output = st.empty()
            with console.st_log(output.code): 
                print(f'Generating {config.CONTEXT_TYPE}.csv')   
                generator = GeneratorContextFile(generation_config=generation_config, context_schema=context_schema)            
                context_file_df = generator.generate_file()
                print('Context file generation has finished.')   
                with st.expander(label=f'Show the generated {config.CONTEXT_TYPE}.csv file:'):
                    st.dataframe(context_file_df)
                    wf_util.save_df(df_name=config.CONTEXT_TYPE, df_value=context_file_df, extension='csv')
        else:
            st.warning(f'The context schema (context_schema.conf) and general setting (general_config.conf) files are required.')
    return context_file_df