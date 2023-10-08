import console
import pandas as pd
import streamlit as st
from streamlit_app import config, help_information
from streamlit_app.workflow_graph import workflow_image
from streamlit_app.preprocess_dataset import wf_util
from datagencars.existing_dataset.generate_null_values.generate_null_values import GenerateNullValues


def generate(with_context):
    # WF --> Generate NULL values:
    st.header('Workflow: Generate NULL values')
    # Help information:
    help_information.help_data_converter_wf()    
    # Showing the initial image of the WF:    
    if with_context:
        workflow_image.show_wf(wf_name='GenerateNULLValues', init_step="True", with_context="True", optional_value_list=[('NULLValuesC', str(True)), ('NULLValuesI', str(True))])
    else:
        workflow_image.show_wf(wf_name='GenerateNULLValues', init_step="True", with_context="False", optional_value_list=[('NULLValuesC', str(True)), ('NULLValuesI', str(True))])
    st.markdown("""---""")

    # Loading dataset:
    st.write('Upload the following files: ')
    if with_context:
        file_selectibox = st.selectbox(label='Files available:', options=['item', 'context'])
    else:
        file_selectibox = st.selectbox(label='Files available:', options=['item'])        
    if file_selectibox == 'item':
        file_type = config.ITEM_TYPE
        __, df, __, __, __ = wf_util.load_dataset(file_type_list=['item'], wf_type='wf_generate_null_values')        
    elif file_selectibox == 'context':
        file_type = config.CONTEXT_TYPE
        __, __, df, __, __ = wf_util.load_dataset(file_type_list=['context'], wf_type='wf_generate_null_values')
    st.markdown("""---""")  

    # Generating NULL values:
    output = st.empty()
    generate_null_value = GenerateNullValues()
    new_df = pd.DataFrame()    
    with console.st_log(output.code):
        percentage_null_tuple = st.number_input("Percentage of null values", min_value=1, max_value=100, value=20, key='number_input_percentage_nulls'),
        percentage_null = percentage_null_tuple[0]
        new_df = generate_null_value.regenerate_file(file_df=df, percentage_null=percentage_null)
        with st.expander(label=f'Show the {file_type}.csv file with a {percentage_null} % of null values:'):
            # Showing the generated file:
            st.dataframe(new_df)    
            # Saving the generated file:
            wf_util.save_df(df_name=file_type+f'_{percentage_null}', df_value=new_df, extension='csv')
