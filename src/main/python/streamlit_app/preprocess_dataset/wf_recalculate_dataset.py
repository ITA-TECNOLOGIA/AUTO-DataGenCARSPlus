import console
import pandas as pd
import streamlit as st
from datagencars.existing_dataset.recalculate_rating.recalculate_rating import RecalculateRating
from streamlit_app import config, help_information
from streamlit_app.preprocess_dataset import wf_util
from streamlit_app.workflow_graph import workflow_image


def generate(with_context, null_values_i, null_values_c=None):
    """
    Recalculate ratings from an dataset, considering other desired user profiles.            
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    :param null_values_i: It is True if the NULL values are replaced in the item.csv file, and False otherwise.
    :param null_values_c: It is True if the NULL values are replaced in the context.csv file, and False otherwise.
    :return: The recalculated rating dataframe.
    """    
    # WF --> Recalculate ratings:
    st.header('Workflow: Recalculate ratings')
    # Help information:
    help_information.help_recalculate_ratings_wf()
    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='RecalculateRatings', init_step='False', with_context=with_context, optional_value_list=[('NULLValues', str(st.session_state.replace_context or st.session_state.replace_item)), ('NULLValuesC', str(st.session_state.replace_context)), ('NULLValuesI', str(st.session_state.replace_item))])
    st.markdown("""---""")

    # Loading dataset:
    st.write('Upload the following files: ')
    if with_context:
        __, item_df, context_df, rating_df, user_profile_df = wf_util.load_dataset(file_type_list=['user', 'item', 'context', 'rating', 'user profile'], wf_type='wf_extend_dataset')
    else:
        __, item_df, __, rating_df, user_profile_df = wf_util.load_dataset(file_type_list=['user', 'item', 'rating', 'user profile'], wf_type='wf_extend_dataset')   

    # Showing the current image of the WF:
    st.markdown("""---""")
    st.write('Shows the applied workflow image:')
    workflow_image.show_wf(wf_name='RecalculateRatings', init_step='False', with_context=with_context, optional_value_list=[('NULLValues', str(null_values_c or null_values_i)), ('NULLValuesC', str(null_values_c)), ('NULLValuesI', str(null_values_i))])

    # Recalculating dataset:
    output = st.empty()
    percentage_rating_variation = st.number_input(label='Percentage of rating variation:', value=25, key='percentage_rating_variation_rs')
    k = st.number_input('Enter the k ratings to take in the past:', min_value=1, step=1, value=10)
    new_rating_df = pd.DataFrame()
    if with_context:
        new_rating_df = button_recalculate_dataset(with_context, rating_df, user_profile_df, item_df, percentage_rating_variation, k, output, context_df)
    else:
        new_rating_df = button_recalculate_dataset(with_context, rating_df, user_profile_df, item_df, percentage_rating_variation, k, output)
    return new_rating_df

def button_recalculate_dataset(with_context, rating_df, user_profile_df, item_df, percentage_rating_variation, k, output, context_df=None):
    """
    Executes a button to recalculate a dataset (rating file).
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    :param rating_df: The rating dataframe to replicate.
    :param user_profile_df: The user profile (automatically generated).
    :param item_df: The item dataframe (it can be with or without NULL values).
    :param percentage_rating_variation: The percentage of rating variation.
    :param k: The k ratings to take in the past.
    :param output: The console output.
    :param context_df: The context dataframe (it can be with or without NULL values).
    :return: The recalculated rating dataframe.
    """
    increase_constructor = None       
    new_rating_df = pd.DataFrame()
    with console.st_log(output.code):            
        # With context:
        if with_context:
            if (not item_df.empty) and (not context_df.empty) and (not rating_df.empty) and (not user_profile_df.empty):                
                recalculate_constructor = RecalculateRating(rating_df, user_profile_df, item_df, context_df)
                new_rating_df = recalculate_ratings(recalculate_constructor, percentage_rating_variation, k)                
            else:
                st.warning('The user, item, context, rating and user profile files must be uploaded.')
        else:
            # Without context:
            if (not item_df.empty) and (not rating_df.empty) and (not user_profile_df.empty):                
                recalculate_constructor = RecalculateRating(rating_df, user_profile_df, item_df)
                new_rating_df = recalculate_ratings(recalculate_constructor, percentage_rating_variation, k)                
            else:
                st.warning('The user, item, rating and user profile files must be uploaded.')                    
    return new_rating_df

def recalculate_ratings(recalculate_constructor, percentage_rating_variation, k):
    """
    Extends dataset.
    :param recalculate_constructor: The object to recalculate the ratings of the dataset.
    :param percentage_rating_variation: The percentage of rating variation.
    :param k: The k ratings to take in the past.
    :return: The recalculated rating dataframe.
    """
    # Extending dataset:
    new_rating_df = pd.DataFrame()        
    # Increasing N ratings randomly:    
    if st.button(label='Recalculate', key='recalculate_dataset_random'):       
        print('Recalculating the rating.csv file.')
        new_rating_df = recalculate_constructor.recalculate_dataset(percentage_rating_variation, k)
        print('Recalculated data generation has finished.')
        with st.expander(label=f'Show the extended file: {config.RATING_TYPE}.csv'):                
            # Showing the replicated rating file:
            st.dataframe(new_rating_df)    
            # Saving the replicated rating file:
            wf_util.save_df(df_name='rating', df_value=new_rating_df, extension='csv')
    return new_rating_df
