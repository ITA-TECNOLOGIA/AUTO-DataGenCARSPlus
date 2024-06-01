import base64

import pandas as pd
import streamlit as st


####### Common methods ######
def save_file(file_name, file_value, extension):
    """
    Save a schema file.
    :param file_name: The name of the schema file.
    :param file_value: The content of the schema file.
    :param extension: The file extension ('*.conf' or '*.csv').
    """
    if extension == 'conf':
        link_file = f'<a href="data:text/plain;base64,{base64.b64encode(file_value.encode()).decode()}" download="{file_name}.{extension}">Download</a>'
    elif extension == 'csv':
        link_file = f'<a href="data:file/csv;base64,{base64.b64encode(file_value.encode()).decode()}" download="{file_name}.{extension}">Download</a>'
    st.markdown(link_file, unsafe_allow_html=True)    

def save_df(df_name, df_value, extension):
    """
    Save a df file.
    :param df_name: The df file name.
    :param df_value: The df file content.
    :param extension: The file extension ('*.csv').
    """
    if not df_value.empty:
        link_df = f'<a href="data:file/csv;base64,{base64.b64encode(df_value.to_csv(index=False).encode()).decode()}" download="{df_name}.{extension}">Download</a>'
        st.markdown(link_df, unsafe_allow_html=True)

def show_schema_file(schema_file_name, schema_value):
    """
    Show the content of the specified schema file.
    :param schema_file_name: The schema file name.
    :param schema_value: The schema file content.
    """
    with st.expander(f"Show {schema_file_name}.conf"):
        st.text_area(label='Current file:', value=schema_value, height=500, disabled=True, key=f'true_edit_{schema_file_name}')

def load_dataset(file_type_list, wf_type):
    """
    Loads dataset files (user.csv, item.csv, context.csv and rating.csv) in dataframes.
    :param file_type_list: List of file types.
    :param wf_type: The file type.
    :return: Dataframes related to the uploaded dataset files.
    """
    user_df = pd.DataFrame()
    item_df = pd.DataFrame()
    context_df = pd.DataFrame()
    behavior_df = pd.DataFrame()
    rating_df = pd.DataFrame()
    user_profile_df = pd.DataFrame()    
    # Uploading a dataset:
    if 'user' in file_type_list:
        user_df = load_one_file(file_type='user', wf_type=wf_type)
    if 'item' in file_type_list:
        item_df = load_one_file(file_type='item', wf_type=wf_type)
    if 'context' in file_type_list:
        context_df = load_one_file(file_type='context', wf_type=wf_type)
    if 'behavior' in file_type_list:
        behavior_df = load_one_file(file_type='behavior', wf_type=wf_type)   
    if 'rating' in file_type_list:
        rating_df = load_one_file(file_type='rating', wf_type=wf_type)
    if 'user profile' in file_type_list:
        user_profile_df = load_one_file(file_type='user_profile', wf_type=wf_type)    
    return user_df, item_df, context_df, behavior_df, rating_df, user_profile_df

def load_one_file(file_type, wf_type):
    """
    Load only one file (user.csv, item.csv, context.csv or rating.csv).
    :param file_type: The file type.
    :return: A dataframe with the information of uploaded file.
    """
    df = pd.DataFrame()    
    with st.expander(f"Upload your {file_type}.csv file"):
        separator = st.text_input(label=f"Enter the separator for your {file_type}.csv file (default is ';')", value=";", key=f'text_input_{file_type}_{wf_type}')
        uploaded_file = st.file_uploader(label=f"Select {file_type}.csv file", type="csv", key=f'uploaded_file_{file_type}_{wf_type}')
        if uploaded_file is not None:
            if not separator:
                st.error('Please provide a separator.')
            else:
                # Read the header of the file to determine column names
                header = uploaded_file.readline().decode("utf-8").strip()
                column_names = header.split(separator)
                # Rename columns
                for i, col in enumerate(column_names):
                    if "user" in col.lower() and "id" in col.lower() and "profile" not in col.lower():
                        column_names[i] = "user_id"
                    elif "item" in col.lower() and "id" in col.lower():
                        column_names[i] = "item_id"
                    elif "context" in col.lower() and "id" in col.lower():
                        column_names[i] = "context_id"
                try:
                    df = pd.read_csv(uploaded_file, sep=separator, names=column_names, engine='python')                             
                    st.dataframe(df.head())
                except Exception as e:
                    st.error(f"An error occurred while reading the {file_type} file: {str(e)}")
                    df = None
    return df
