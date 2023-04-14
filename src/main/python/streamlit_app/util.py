import streamlit as st
import pandas as pd
import altair as alt
import numpy as np


def load_one_file(file_type):
    """
    """
    df = pd.DataFrame()    
    with st.expander(f"Upload your {file_type}.csv file"):
        separator = st.text_input(f"Enter the separator for your {file_type}.csv file (default is ';')", ";")
        uploaded_file = st.file_uploader(f"Select {file_type}.csv file", type="csv")
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
                    df = pd.read_csv(uploaded_file, sep=separator, names=column_names)
                    st.dataframe(df.head())
                except Exception as e:
                    st.error(f"An error occurred while reading the {file_type} file: {str(e)}")
                    df = None
    return df

def plot_column_attributes_count(data, column, sort):
    """
    """
    if sort == 'asc':
        sort_field = alt.EncodingSortField('count', order='ascending')
    elif sort == 'desc':
        sort_field = alt.EncodingSortField('count', order='descending') 
    else:
        sort_field = None
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X(column + ':O', title='Attribute values', sort=sort_field),
        y=alt.Y('count:Q', title='Count'),
        tooltip=[column, 'count']
    ).interactive()
    st.altair_chart(chart, use_container_width=True)
            
def print_statistics_by_attribute(statistics):
    """
    """
    for stat in statistics:
        st.subheader(stat[0])
        st.write('Average: ', stat[1])
        st.write('Standard deviation: ', stat[2])
        col1, col2 = st.columns(2)
        with col1:
            st.write('Frequencies:')
            st.dataframe(stat[3])
        with col2:
            st.write('Percentages:')
            st.dataframe(stat[4])

def correlation_matrix(df, label):
    """
    """
    corr_matrix = pd.DataFrame()
    columns_id = df.filter(regex='_id$').columns.tolist()
    columns_not_id = [col for col in df.columns if col not in columns_id]
    data_types = []
    for col in columns_not_id:     
        data_types.append({"Attribute": col, "Data Type": str(df[col].dtype)})
        break    
    selected_columns = st.multiselect("Select columns to analyze", columns_not_id, key='cm_'+label)
    method = st.selectbox("Select a method", ['pearson', 'kendall', 'spearman'], key='method_'+label)
    if st.button("Generate correlation matrix", key='button_'+label) and selected_columns:
        with st.spinner("Generating correlation matrix..."):
            merged_df_selected = df[selected_columns].copy()
            # Categorize non-numeric columns using label encoding:
            for col in merged_df_selected.select_dtypes(exclude=[np.number]):
                merged_df_selected[col], _ = merged_df_selected[col].factorize()            
            corr_matrix = merged_df_selected.corr(method=method)     
    return corr_matrix       
            