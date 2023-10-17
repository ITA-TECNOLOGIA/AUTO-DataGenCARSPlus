import console
import pandas as pd
import streamlit as st
from datagencars.existing_dataset.generate_null_values.generate_null_values import GenerateNullValues
from streamlit_app import config, help_information
from streamlit_app.preprocess_dataset import wf_util
from streamlit_app.workflow_graph import workflow_image


def generate(with_context, tab_generate_null_values_item, tab_generate_null_values_context=None):
    """
    """
    new_item_df = pd.DataFrame()
    new_context_df = pd.DataFrame()    
    if with_context:
        # Generating NULL values in context.csv:
        with tab_generate_null_values_context:
            new_context_df = generate_context(with_context)
    # Generating NULL values in item.csv:
    with tab_generate_null_values_item:
        new_item_df = generate_item(with_context)
    return new_item_df, new_context_df

def generate_item(with_context):
    """
    """
    # WF --> Generate NULL values:
    st.header(f'Workflow: Generate NULL values')
    # Help information:
    help_information.help_generate_nulls_wf()
    # Showing the initial image of the WF:
    if with_context:
        workflow_image.show_wf(wf_name='GenerateNULLValues', init_step="True", with_context="True", optional_value_list=[('NULLValuesC', str(True)), ('NULLValuesI', str(True))])
    else:
        workflow_image.show_wf(wf_name='GenerateNULLValues', init_step="False", with_context="False", optional_value_list=[('NULLValuesI', str(True))])
    st.markdown("""---""")
    
    # Showing progress messages in console:
    output = st.empty()  
    generate_null_value = GenerateNullValues()
    new_item_df = pd.DataFrame()  
    with console.st_log(output.code):
        __, item_df, __, __, __ = wf_util.load_dataset(file_type_list=['item'], wf_type='wf_generate_null_values')  
        percentage_null = st.number_input("Percentage of null values", min_value=1, max_value=100, value=20, key='number_input_percentage_nulls_item')
        if st.button(label='Generate', key='button_generate_null_values_item'):            
            new_item_df = generate_null_value.regenerate_file(file_df=item_df, percentage_null=percentage_null)
            with st.expander(label=f'Show the {config.ITEM_TYPE}.csv file with a {percentage_null} % of null values:'):
                # Showing the generated file:
                st.dataframe(new_item_df)    
                # Saving the generated file:
                wf_util.save_df(df_name=config.ITEM_TYPE+f'_{percentage_null}', df_value=new_item_df, extension='csv')
    return new_item_df

def generate_context(with_context):
    """
    """
    # WF --> Generate NULL values:
    st.header(f'Workflow: Generate NULL values')
    # Help information:
    help_information.help_generate_nulls_wf()
    # Showing the initial image of the WF:
    if with_context:
        workflow_image.show_wf(wf_name='GenerateNULLValues', init_step="True", with_context="True", optional_value_list=[('NULLValuesC', str(True)), ('NULLValuesI', str(True))])
    else:
        workflow_image.show_wf(wf_name='GenerateNULLValues', init_step="False", with_context="False", optional_value_list=[('NULLValuesI', str(True))])
    st.markdown("""---""")
    
    # Showing progress messages in console:
    output = st.empty()  
    generate_null_value = GenerateNullValues()
    new_context_df = pd.DataFrame()  
    with console.st_log(output.code):
        __, __, context_df, __, __ = wf_util.load_dataset(file_type_list=['context'], wf_type='wf_generate_null_values')
        percentage_null = st.number_input("Percentage of null values", min_value=1, max_value=100, value=20, key='number_input_percentage_nulls_context')
        if st.button(label='Generate', key='button_generate_null_values_context'):            
            new_context_df = generate_null_value.regenerate_file(file_df=context_df, percentage_null=percentage_null)
            with st.expander(label=f'Show the {config.ITEM_TYPE}.csv file with a {percentage_null} % of null values:'):
                # Showing the generated file:
                st.dataframe(new_context_df)    
                # Saving the generated file:
                wf_util.save_df(df_name=config.ITEM_TYPE+f'_{percentage_null}', df_value=new_context_df, extension='csv')
    return new_context_df




   

# def generate(with_context):
#     # WF --> Generate NULL values:
#     st.header('Workflow: Generate NULL values')
#     # Help information:
#     help_information.help_data_converter_wf()    
#     # Showing the initial image of the WF:    
#     if with_context:
#         workflow_image.show_wf(wf_name='GenerateNULLValues', init_step="True", with_context="True", optional_value_list=[('NULLValuesC', str(True)), ('NULLValuesI', str(True))])
#     else:
#         workflow_image.show_wf(wf_name='GenerateNULLValues', init_step="True", with_context="False", optional_value_list=[('NULLValuesC', str(True)), ('NULLValuesI', str(True))])
#     st.markdown("""---""")

#     # Loading dataset:    
#     if with_context:
#         st.header('Item or Context Files')
#         file_selectibox = st.selectbox(label='Available files:', options=['item', 'context'])
#         if file_selectibox == 'item':
#             file_type = config.ITEM_TYPE
#             __, df, __, __, __ = wf_util.load_dataset(file_type_list=['item'], wf_type='wf_generate_null_values')        
#         elif file_selectibox == 'context':
#             file_type = config.CONTEXT_TYPE
#             __, __, df, __, __ = wf_util.load_dataset(file_type_list=['context'], wf_type='wf_generate_null_values')
#     else:
#         st.header('Item File')
#         file_type = config.ITEM_TYPE
#         __, df, __, __, __ = wf_util.load_dataset(file_type_list=['item'], wf_type='wf_generate_null_values')    

#     # Generating NULL values:
#     output = st.empty()
#     generate_null_value = GenerateNullValues()
#     new_df = pd.DataFrame()    
#     with console.st_log(output.code):
#         percentage_null = st.number_input("Percentage of null values", min_value=1, max_value=100, value=20, key='number_input_percentage_nulls')
#         if st.button(label='Generate', key='button_generate_null_values'):            
#             new_df = generate_null_value.regenerate_file(file_df=df, percentage_null=percentage_null)
#             with st.expander(label=f'Show the {file_type}.csv file with a {percentage_null} % of null values:'):
#                 # Showing the generated file:
#                 st.dataframe(new_df)    
#                 # Saving the generated file:
#                 wf_util.save_df(df_name=file_type+f'_{percentage_null}', df_value=new_df, extension='csv')
