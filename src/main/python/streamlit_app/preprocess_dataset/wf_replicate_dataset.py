import console
import pandas as pd
import streamlit as st
from datagencars.existing_dataset.replicate_dataset.replicate_dataset import ReplicateDataset
from streamlit_app import config, help_information
from streamlit_app.preprocess_dataset import wf_util
from streamlit_app.workflow_graph import workflow_image


def generate(with_context):
    """
    Replicates an existing rating file.
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.    
    :return: The replicated rating dataframe.
    """
    # WF --> Replicate dataset:
    st.header('Workflow: Replicate dataset')  
    # Help information:
    help_information.help_replicate_dataset_wf()    
    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='ReplicateDataset', init_step='True', with_context=True, optional_value_list=[('NULLValues', str(True)), ('NULLValuesC', str(True)), ('NULLValuesI', str(True))])    
    st.markdown("""---""")

    # Loading dataset:
    st.write('Upload the following files: ')
    if with_context:        
        __, item_df, context_df, rating_df, user_profile_df = wf_util.load_dataset(file_type_list=['user', 'item', 'context', 'rating', 'user profile'], wf_type='wf_replicate_dataset')
    else:
        __, item_df, __, rating_df, user_profile_df = wf_util.load_dataset(file_type_list=['user', 'item', 'rating', 'user profile'], wf_type='wf_replicate_dataset')   
    
    # Showing the current image of the WF:
    st.markdown("""---""")
    st.write('Shows the applied workflow image:')
    if 'replace_context' not in st.session_state:
        st.session_state['replace_context'] = False
    if 'replace_item' not in st.session_state:
        st.session_state['replace_item'] = False
    workflow_image.show_wf(wf_name='ReplicateDataset', init_step='False', with_context=with_context, optional_value_list=[('NULLValues', str(st.session_state['replace_context'] or st.session_state['replace_item'])), ('NULLValuesC', str(st.session_state['replace_context'])), ('NULLValuesI', str(st.session_state['replace_item']))])    
    
    # Replicating dataset:
    output = st.empty()
    percentage_rating_variation = st.number_input(label='Percentage of rating variation:', value=25, key='percentage_rating_variation_rs')
    k = st.number_input('Enter the k ratings to take in the past:', min_value=1, step=1, value=10)
    new_rating_df = pd.DataFrame()
    if with_context:
        new_rating_df = button_replicate_dataset(with_context, rating_df, user_profile_df, item_df, percentage_rating_variation, k, output, context_df)
    else:
        new_rating_df = button_replicate_dataset(with_context, rating_df, user_profile_df, item_df, percentage_rating_variation, k, output)
    return new_rating_df

def button_replicate_dataset(with_context, rating_df, user_profile_df, item_df, percentage_rating_variation, k, output, context_df=None):
    """
    Executes a button to replicate a dataset (rating file).
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    :param rating_df: The rating dataframe to replicate.
    :param user_profile_df: The user profile (automatically generated).
    :param item_df: The item dataframe (it can be with or without NULL values).
    :param percentage_rating_variation: The percentage rating variation.
    :param output: The console output.
    :param context_df: The context dataframe (it can be with or without NULL values).
    :return: The replicated rating dataframe.
    """
    new_rating_df = pd.DataFrame()
    if st.button(label='Replicate', key='replicate_dataset'):        
        with console.st_log(output.code):            
            # With context:
            if with_context:
                if (not item_df.empty) and (not context_df.empty) and (not rating_df.empty) and (not user_profile_df.empty):     
                    print('Extracting statistics.')
                    print('Replicating the rating.csv file.')               
                    replicate_constructor = ReplicateDataset(rating_df, user_profile_df, item_df, context_df)                                        
                    new_rating_df = replicate_constructor.replicate_dataset(percentage_rating_variation, k)
                    print('Replicated data generation has finished.')
                    with st.expander(label=f'Show the replicated file: {config.RATING_TYPE}.csv'):
                        # Showing the replicated rating file:
                        st.dataframe(new_rating_df)    
                        # Saving the replicated rating file:
                        wf_util.save_df(df_name='rating', df_value=new_rating_df, extension='csv')
                else:
                    st.warning('The item, context, rating and user profile files must be uploaded.')
            else:
                # Without context:
                if (not item_df.empty) and (not rating_df.empty) and (not user_profile_df.empty):                   
                    print('Extracting statistics.')
                    print('Replicating the rating.csv file.')
                    replicate_constructor = ReplicateDataset(rating_df, user_profile_df, item_df)                                            
                    new_rating_df = replicate_constructor.replicate_dataset(percentage_rating_variation, k)
                    print('Replicated data generation has finished.')
                    with st.expander(label=f'Show the replicated file: {config.RATING_TYPE}.csv'):
                        # Showing the replicated rating file:
                        st.dataframe(new_rating_df)    
                        # Saving the replicated rating file:
                        wf_util.save_df(df_name='rating', df_value=new_rating_df, extension='csv')
                else:
                    st.warning('The item, rating and user profile files must be uploaded.')
    return new_rating_df
