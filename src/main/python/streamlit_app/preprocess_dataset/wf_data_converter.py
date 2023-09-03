import console
import numpy as np
import pandas as pd
import streamlit as st
from datagencars.existing_dataset.data_converter.data_converter import DataConverter
from streamlit_app import config, help_information
from streamlit_app.preprocess_dataset import wf_util
from streamlit_app.workflow_graph import workflow_image


def generate(with_context):
    """
    Converts data between numerical and categorical representations.
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    """
    # WF --> Data converter:
    st.header('Workflow: Data converter')
    # Help information:
    help_information.help_data_converter_wf()    
    # Showing the initial image of the WF:    
    file = 'F'
    num2cat = 'T' 
    workflow_image.show_wf(wf_name='DataConverter', init_step='True', with_context=True, optional_value_list=[('Num2Cat', num2cat), ('file', file)])
    st.markdown("""---""")

    # Loading dataset:
    st.write('Upload the following files: ')
    if with_context:
        file_selectibox = st.selectbox(label='Files available:', options=['user', 'item', 'context'])
    else:
        file_selectibox = st.selectbox(label='Files available:', options=['user', 'item'])        
    if file_selectibox == 'user':
        df, __, __, __, __ = wf_util.load_dataset(file_type_list=['user'], wf_type='wf_data_converter')
        file = 'U'
    elif file_selectibox == 'item':
        __, df, __, __, __ = wf_util.load_dataset(file_type_list=['item'], wf_type='wf_data_converter')
        file = 'I'
    elif file_selectibox == 'context':
        __, __, df, __, __ = wf_util.load_dataset(file_type_list=['context'], wf_type='wf_data_converter')   
        file = 'C'    
    st.markdown("""---""")    
    
    # Converting data:
    output = st.empty() 
    data_converter = DataConverter(df)
    encoded_df = pd.DataFrame()
    option = st.radio(options=config.CONVERTER_DATA_OPTIONS, label='Select an option')
    with console.st_log(output.code):
        if not df.empty:
            # Numerical to categorical option:
            if option == 'From numerical to categorical':
                st.header("Numerical Encoding")
                # Help information:
                help_information.help_numerical_to_categorical()
                # Showing the image of the WF:            
                num2cat = 'True'
                workflow_image.show_wf(wf_name='DataConverter', init_step='False', with_context=with_context, optional_value_list=[('Num2Cat', num2cat), ('file', file)])
                # Converting numerical to categorical values:
                print('Introducing mapping values per attribute.')
                include_nan = st.checkbox(label="Include NaN values", value=False, key='nan_checkbox_numerical_to_categorical')
                mappings = {}
                for col in df.columns:
                    with st.expander(col):
                        if 'id' not in col.lower() and not pd.api.types.is_datetime64_dtype(df[col]) and not pd.api.types.is_object_dtype(df[col]): # Ignore ID, object and datetime columns
                            unique_values = sorted(df[col].unique())
                            st.write(f"Unique values: {', '.join(map(str, unique_values))}")
                            col_mappings = {}
                            for val in unique_values:
                                if not include_nan and pd.isna(val):
                                    col_mappings[val] = np.nan
                                    continue
                                else:
                                    mapping = st.text_input(f"Mapping for {val}", "", key=f"{col}_{val}")                                    
                                    if mapping:
                                        col_mappings[val] = mapping
                                    else:
                                        col_mappings[val] = val                                
                            st.write(col_mappings)
                            mappings[col] = col_mappings                
                if st.button("Convert", key='button_numerical_to_categorical'):
                    print('Converting numerical to categorical values.')                    
                    encoded_df = data_converter.numerical_to_categorical(mappings)
                    print('The conversion has finished.')
                    with st.expander(label=f'Show the file: {file_selectibox}.csv'):                
                        # Showing the replicated rating file:
                        st.dataframe(encoded_df)    
                        # Saving the replicated rating file:
                        wf_util.save_df(df_name=file_selectibox, df_value=encoded_df, extension='csv')
            # Categorical to numerical option:
            elif option == 'From categorical to numerical':
                st.header("Categorical Encoding")
                # Help information:
                help_information.help_categorical_to_numerical()
                # Showing the image of the WF:
                num2cat = 'False'
                workflow_image.show_wf(wf_name='DataConverter', init_step='False', with_context=with_context, optional_value_list=[('Num2Cat', num2cat), ('file', file)])
                # Converting categorical to numerical values:
                print('Introducing mapping values per attribute.')
                ignore_nan = st.checkbox(label="Ignore NaN values?", value=True, key='nan_checkbox_categorical_to_numerical')
                categorical_cols = [col for col in df.select_dtypes(exclude=[np.number]) if 'id' not in col.lower()]
                if categorical_cols:
                    selected_cols = st.multiselect("Select categorical columns to label encode:", categorical_cols)
                    if selected_cols:
                        if st.button("Convert", key='button_categorical_to_numerical'):  
                            print('Converting categorical to numerical values.')
                            encoded_df = data_converter.categorical_to_numerical(column_name_list=selected_cols, ignore_nan=ignore_nan)
                            print('The conversion has finished.')
                            with st.expander(label=f'Show the file: {file_selectibox}.csv'):                
                                # Showing the replicated rating file:
                                st.dataframe(encoded_df)    
                                # Saving the replicated rating file:
                                wf_util.save_df(df_name=file_selectibox, df_value=encoded_df, extension='csv')                  
                else:
                    st.write("No categorical columns found.")
        else:
            st.warning("The user, item or context file has not been uploaded.")
