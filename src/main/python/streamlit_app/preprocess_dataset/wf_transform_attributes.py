import console
import pandas as pd
import streamlit as st
from datagencars.existing_dataset.transform_attributes.transform_rating import TransformRating
from streamlit_app import config, help_information
from streamlit_app.preprocess_dataset import wf_util
from streamlit_app.workflow_graph import workflow_image
import numpy as np
from datagencars.existing_dataset.transform_attributes.transform_uic import TransformUIC


def generate(with_context):
    """
    
    """ 
    tab_user_item_context, tab_rating = st.tabs(['User-Item-Context', 'Rating'])
    # TAB --> USER-ITEM-CONTEXT (Numerical to Categorical / Categorical to Numerical):
    with tab_user_item_context:
        transform_user_item_context(with_context)
    # TAB --> RATING (Binary to Preferencial / Preferencial to Binary):
    with tab_rating:
        transform_rating()

def transform_rating():
    """
    Processes and transforms rating values (preferencial to binary / binary to preferencial) in a DataFrame.    
    :return: The modified rating DataFrame after the Cast Ratings workflow.
    """
    # WF --> Transform Rating:
    st.header('Workflow: Transform Rating')
    # Help information:
    help_information.help_cast_rating_wf()
    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='TransformRating', init_step=True)

    # Loading dataset:
    st.write('Upload the following files: ')    
    __, __, __, rating_df, __ = wf_util.load_dataset(file_type_list=['rating'], wf_type='wf_transform_rating')
    st.markdown("""---""")

    # Transforming ratings to binary values:
    output = st.empty() 
    new_rating_df = pd.DataFrame()  
    with console.st_log(output.code):   
        if not rating_df.empty:
            generator = TransformRating(rating_df=rating_df)
            if generator.is_binary_rating():  
                print('The dataset has rating values of binary type (0 or 1).')
                scale = st.number_input("Enter the maximum value of the rating.", value=5)
                threshold_binary = st.number_input(f"Binary threshold (range from 1 to {scale})", value=3)
                print('Casting the rating value in the rating.csv file.')
                new_rating_df = generator.rating_binary_to_preferencial(scale, threshold=threshold_binary)
                print('The casting process has finished.')
                with st.expander(label=f'Show the modified rating file: {config.RATING_TYPE}.csv'):                
                    # Showing the replicated rating file:
                    st.dataframe(new_rating_df)    
                    # Saving the replicated rating file:
                    wf_util.save_df(df_name='rating', df_value=new_rating_df, extension='csv') 
            elif generator.is_preferencial_rating():
                min_rating = rating_df['rating'].min()
                max_rating = rating_df['rating'].max()
                print(f'The dataset has rating values of preferencial type in the range [{min_rating}, {max_rating}].')
                threshold_preferencial = st.number_input(f"Binary threshold (range from {min_rating} to {max_rating})", value=3)
                print('Casting the rating value in the rating.csv file.')
                new_rating_df = generator.rating_preferencial_to_binary(threshold=threshold_preferencial)
                print('The casting process has finished.')
                if st.checkbox(label="Do you want to change the vote label (e.g. 1 to 'like' and 0 to 'dislike')?", value=False, key='binary_set_rating_label'):
                    label_1 = st.text_input(label='Enter a label for the rating value 1:', value='like', key='text_input_label_1')
                    label_0 = st.text_input(label='Enter a label for the rating value 0:', value='dislike', key='text_input_label_0')
                    print(f'Changing the binary numeric rating value to a string label: 1 to {label_1} and 0 to {label_0}.')
                    new_rating_df = generator.set_binary_rating_label(label_1, label_0)
                    print('The rating value has been changed to a label.')
                with st.expander(label=f'Show the modified rating file: {config.RATING_TYPE}.csv'):                
                    # Showing the replicated rating file:
                    st.dataframe(new_rating_df)    
                    # Saving the replicated rating file:
                    wf_util.save_df(df_name='rating', df_value=new_rating_df, extension='csv')            
        else:            
            st.warning("The rating file has not been uploaded.")
    return new_rating_df

def transform_user_item_context(with_context):
    """
    Transforms user, item and contexts attributes (categorical to numerical / numerical to categorical).    
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    """
    # WF --> Transform User-Item-Context:
    st.header('Workflow: Transform User-Item-Context')
    # Help information:
    help_information.help_data_converter_wf()    
    # Showing the initial image of the WF:    
    file = 'F'
    num2cat = 'T' 
    workflow_image.show_wf(wf_name='TransformUIC', init_step='True', with_context=True, optional_value_list=[('Num2Cat', num2cat), ('file', file)])
    st.markdown("""---""")

    # Loading dataset:
    st.write('Upload the following files: ')
    if with_context:
        file_selectibox = st.selectbox(label='Files available:', options=['user', 'item', 'context'])
    else:
        file_selectibox = st.selectbox(label='Files available:', options=['user', 'item'])        
    if file_selectibox == 'user':
        df, __, __, __, __ = wf_util.load_dataset(file_type_list=['user'], wf_type='wf_transform_uic')
        file = 'U'
    elif file_selectibox == 'item':
        __, df, __, __, __ = wf_util.load_dataset(file_type_list=['item'], wf_type='wf_transform_uic')
        file = 'I'
    elif file_selectibox == 'context':
        __, __, df, __, __ = wf_util.load_dataset(file_type_list=['context'], wf_type='wf_transform_uic')   
        file = 'C'    
    st.markdown("""---""")    
    
    # Converting data:
    output = st.empty()
    data_converter = TransformUIC(df)
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
                workflow_image.show_wf(wf_name='TransformUIC', init_step='False', with_context=with_context, optional_value_list=[('Num2Cat', num2cat), ('file', file)])
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
                workflow_image.show_wf(wf_name='TransformUIC', init_step='False', with_context=with_context, optional_value_list=[('Num2Cat', num2cat), ('file', file)])
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
