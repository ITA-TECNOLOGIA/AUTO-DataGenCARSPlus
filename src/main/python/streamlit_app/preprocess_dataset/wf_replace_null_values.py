import config
import streamlit as st
from datagencars.existing_dataset.replace_null_values import ReplaceNullValues
from streamlit_app import help_information
from streamlit_app.preprocess_dataset import wf_util
from streamlit_app.preprocess_dataset.wf_util import save_df
from streamlit_app.workflow_graph import workflow_image


def generate(with_context):
    """
    Replaces NULL values in the item or context schema files.
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    """
    # Schema file options according to contextual information.
    if with_context:
        file_selectibox = st.selectbox(label='Files available:', options=config.IC_WF_REPLACE_NULL_VALUES)
    else:
        file_selectibox = st.selectbox(label='Files available:', options=config.I_WF_REPLACE_NULL_VALUES)

    # Loading dataset:    
    if file_selectibox == 'item':
        _, df, _, _ = wf_util.load_dataset(file_type_list=['item'])
        schema = wf_util.infer_schema(df)
    elif file_selectibox == 'context':
        _, _, df, _ = wf_util.load_dataset(file_type_list=['context'])
        schema = wf_util.infer_schema(df)    
    wf_util.show_schema_file(schema_file_name=file_selectibox, schema_value=schema)
    
    # WF --> Replace NULL values:
    st.header('Apply workflow: Replace NULL values')

    # Help information:
    help_information.help_replace_nulls_wf()

    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='ReplaceNULLValues', init_step="True", with_context="True", optional_value_list=[('NULLValuesC', str(True)), ('NULLValuesI', str(True))])    
    st.tabs(['Replace NULL values'])
    if file_selectibox == 'context':
        workflow_image.show_wf(wf_name='ReplaceNULLValues', init_step="False", with_context=with_context, optional_value_list=[('NULLValuesC', str(True)), ('NULLValuesI', str(False))])
    else:
        workflow_image.show_wf(wf_name='ReplaceNULLValues', init_step="False", with_context=with_context, optional_value_list=[('NULLValuesC', str(False)), ('NULLValuesI', str(True))])
    
    # TAB --> Replace NULL values:    
    if not df.empty:
        if st.button(label='Replace NULL Values', key='button_replace_nulls'):
            print('Replacing NULL Values')
            replacenulls = ReplaceNullValues(df)
            if file_selectibox == 'item':
                new_df = replacenulls.regenerate_item_file(schema)
            elif file_selectibox == 'context':
                new_df = replacenulls.regenerate_context_file(schema)
            # Show the new schema file with replaced null values:    
            st.dataframe(new_df)
            # Downloading user_profile.csv:
            save_df(df_name=file_selectibox, df_value=new_df, extension='csv')            
    else:
        st.warning("The item file or context file have not been uploaded.")
