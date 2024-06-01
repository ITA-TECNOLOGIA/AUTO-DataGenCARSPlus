import console
import pandas as pd
import streamlit as st
from datagencars.existing_dataset.extend_dataset.increase_rating_explicit import IncreaseRatingExplicit
from datagencars.existing_dataset.extend_dataset.increase_rating_implicit import IncreaseRatingImplicit
from streamlit_app.generate_synthetic_dataset import wf_behavior, wf_rating
from streamlit_app import config, help_information
from streamlit_app.preprocess_dataset import wf_util
from streamlit_app.workflow_graph import workflow_image

def generate(with_context, feedback_option):
    """
    Extends an existing rating file.
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    :param null_values_i: It is True if the NULL values are replaced in the item.csv file, and False otherwise.
    :param null_values_c: It is True if the NULL values are replaced in the context.csv file, and False otherwise.
    :return: The extended rating dataframe.
    """
    # WF --> Extend dataset:
    st.header('Workflow: Extend dataset')  
    # Help information:
    help_information.help_extend_dataset_wf()    
    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='ExtendDataset', init_step='True', with_context=True, optional_value_list=[('NULLValues', str(True)), ('NULLValuesC', str(True)), ('NULLValuesI', str(True))])
    st.markdown("""---""")

    # Loading dataset:
    st.write('Upload the following files: ')
    if feedback_option == 'Explicit ratings':
        if with_context:
            user_df, item_df, context_df, __, rating_df, user_profile_df = wf_util.load_dataset(file_type_list=['user', 'item', 'context', 'rating', 'user profile'], wf_type='wf_extend_dataset')
        else:
            user_df, item_df, __, __, rating_df, user_profile_df = wf_util.load_dataset(file_type_list=['user', 'item', 'rating', 'user profile'], wf_type='wf_extend_dataset')   
    elif feedback_option == 'Implicit ratings':
        if with_context:
            __, item_df, context_df, behavior_df, rating_df, __ = wf_util.load_dataset(file_type_list=['item', 'context', 'behavior', 'rating'], wf_type='wf_extend_dataset')
            generation_config_behavior = wf_behavior.get_generation_config_schema()
            generation_config_rating = wf_rating.get_generation_config_schema(with_context, implicit=True)
            behavior_schema = wf_behavior.get_behavior_schema()
            item_schema = wf_rating.get_item_schema()

    # Showing the current image of the WF:
    st.markdown("""---""")
    st.write('Shows the applied workflow image:')
    if 'replace_context' not in st.session_state:
        st.session_state['replace_context'] = False
    if 'replace_item' not in st.session_state:
        st.session_state['replace_item'] = False
    workflow_image.show_wf(wf_name='ExtendDataset', init_step='False', with_context=with_context, optional_value_list=[('NULLValues', str(st.session_state['replace_context'] or st.session_state['replace_item'])), ('NULLValuesC', str(st.session_state['replace_context'])), ('NULLValuesI', str(st.session_state['replace_item']))])

    # Extending dataset:
    output = st.empty()    
    if feedback_option == 'Explicit ratings':
        number_rating = st.number_input(label='Enter the number of ratings to extend in the rating file:', min_value=1, step=1, value=1)
        percentage_rating_variation = st.number_input(label='Percentage of rating variation:', value=25, key='percentage_rating_variation_rs')
        k = st.number_input(label='Enter the k ratings to take in the past:', min_value=1, step=1, value=10)
        option = st.selectbox(label='How would you like to extend the dataset?', options=['Select one option', 'N ratings randomly (some users)', 'N ratings for each user'])
    elif feedback_option == 'Implicit ratings':
        number_rating = st.number_input(label='Enter the number of ratings to extend in the rating file:', min_value=1, step=1, value=1)
        option = st.selectbox(label='How would you like to extend the dataset?', options=['Select one option', 'N ratings randomly (some users)', 'N ratings for each user'])
    
    new_rating_df = pd.DataFrame()
    if feedback_option == 'Explicit ratings':
        if with_context:
            new_rating_df = button_extend_dataset(feedback_option, with_context, rating_df, user_profile_df, user_df, item_df, number_rating, percentage_rating_variation, k, option, output, context_df)
        else:
            new_rating_df = button_extend_dataset(feedback_option, with_context, rating_df, user_profile_df, user_df, item_df, number_rating, percentage_rating_variation, k, option, output)
    elif feedback_option == 'Implicit ratings':
        if with_context:
            new_rating_df = button_extend_dataset(feedback_option, with_context, rating_df, None, None, item_df, number_rating, None, None, option, output, context_df, behavior_df, generation_config_behavior, generation_config_rating, behavior_schema, item_schema)
    return new_rating_df

def button_extend_dataset(feedback_option, with_context, rating_df, user_profile_df, user_df, item_df, number_rating, percentage_rating_variation, k, option, output, context_df=None, behavior_df=None, generation_config_behavior=None, generation_config_rating=None, behavior_schema=None, item_schema=None):
    """
    Executes a button to replicate a dataset (rating file).
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    :param rating_df: The rating dataframe to replicate.
    :param user_profile_df: The user profile (automatically generated).
    :param item_df: The item dataframe (it can be with or without NULL values).
    :param number_rating: The number of ratings to generate for each user.
    :param percentage_rating_variation: The percentage of rating variation.
    :param k: The k ratings to take in the past.
    :param option: The option selected by user ('N ratings randomly (some users)' or 'N ratings for each user').
    :param output: The console output.
    :param context_df: The context dataframe (it can be with or without NULL values).
    :return: The extended rating dataframe.
    """     
    increase_constructor = None       
    new_rating_df = pd.DataFrame()
    with console.st_log(output.code):
        if feedback_option == 'Explicit ratings':          
            # With context:
            if with_context:
                if (not item_df.empty) and (not context_df.empty) and (not rating_df.empty) and (not user_profile_df.empty):                
                    increase_constructor = IncreaseRatingExplicit(rating_df, user_profile_df, user_df, item_df, context_df)
                    new_rating_df = extend_dataset(increase_constructor, number_rating, percentage_rating_variation, k, option, feedback_option)
                    if new_rating_df.shape[0] > 1:
                        total_extended_ratings = int(new_rating_df.shape[0]- rating_df.shape[0])
                        print(f'The datase has been extended: {total_extended_ratings} ratings.')
                else:
                    st.warning('The user, item, context, rating and user profile files must be uploaded.')
            else:
                # Without context:
                if (not item_df.empty) and (not rating_df.empty) and (not user_profile_df.empty):                
                    increase_constructor = IncreaseRatingExplicit(rating_df, user_profile_df, user_df, item_df)
                    new_rating_df = extend_dataset(increase_constructor, number_rating, percentage_rating_variation, k, option, feedback_option)
                    if new_rating_df.shape[0] > 1:
                        total_extended_ratings = int(new_rating_df.shape[0]- rating_df.shape[0])
                        print(f'The datase has been extended: {total_extended_ratings} ratings.')
                else:
                    st.warning('The user, item, rating and user profile files must be uploaded.')
        elif feedback_option == 'Implicit ratings':
            if with_context:
                if (not item_df.empty) and (not behavior_df.empty) and (not context_df.empty):
                    increase_constructor = IncreaseRatingImplicit(generation_config_behavior, generation_config_rating, behavior_schema, behavior_df, item_df, item_schema, context_df)                                  
                    new_rating_df = extend_dataset(increase_constructor, number_rating, None, None, option, feedback_option, behavior_df, rating_df)
                    if new_rating_df.shape[0] > 1:
                        total_extended_ratings = int(new_rating_df.shape[0]- rating_df.shape[0])
                        print(f'The datase has been extended: {total_extended_ratings} ratings.')
                else:
                    st.warning('The user, item, context, rating, user profile and behavior files must be uploaded.')
    return new_rating_df

def extend_dataset(increase_constructor, number_rating, percentage_rating_variation, k, option, feedback_option, behavior_df=None, rating_df=None):
    """
    Extends dataset.
    :param increase_constructor: The object to extend the dataset.
    :param percentage_rating_variation: The percentage of rating variation.
    :param k: The k ratings to take in the past.
    The option selected by user ('N ratings randomly (some users)' or 'N ratings for each user').
    :return: The extended rating dataframe.
    """
    # Extending dataset:
    new_rating_df = pd.DataFrame()    
    extend_button = st.button(label='Extend', key='extend_dataset_random')
    # Increasing N ratings randomly:    
    if option == 'N ratings randomly (some users)':
        if feedback_option == 'Explicit ratings':
            if extend_button:      
                print('Extending the rating.csv file.')
                new_rating_df = increase_constructor.extend_rating_random(number_rating, percentage_rating_variation, k)
                print('Extended data generation has finished.')
                with st.expander(label=f'Show the extended file: {config.RATING_TYPE}.csv'):                
                    # Showing the replicated rating file:
                    st.dataframe(new_rating_df)
                    # Saving the replicated rating file:
                    wf_util.save_df(df_name='rating', df_value=new_rating_df, extension='csv')
        elif feedback_option == 'Implicit ratings':
            if extend_button:      
                print('Extending the behavior.csv and rating.csv files.')
                new_behavior_df, new_rating_df = increase_constructor.extend_rating_random(number_rating)
                # Append new_behaviors to the existing behaviors dataset
                updated_behaviors_df = pd.concat([behavior_df, new_behavior_df]).reset_index(drop=True)
                # Cast 'context_id' to int
                updated_behaviors_df['context_id'] = updated_behaviors_df['context_id'].fillna(0).astype(int)
                updated_behaviors_df = updated_behaviors_df.sort_values(by=['user_id']).reset_index(drop=True)
                # Append new_ratings to the existing ratings dataset
                updated_ratings_df = pd.concat([rating_df, new_rating_df]).reset_index(drop=True)
                # Cast 'context_id' to int
                updated_ratings_df['context_id'] = updated_ratings_df['context_id'].fillna(0).astype(int)
                updated_ratings_df = updated_ratings_df.sort_values(by=['user_id']).reset_index(drop=True)
                print('Extended data generation has finished.')
                with st.expander(label=f'Show the extended file: rating.csv'):
                    # Showing the replicated rating file:
                    st.dataframe(updated_ratings_df)
                    # Saving the replicated rating file:
                    wf_util.save_df(df_name='rating', df_value=updated_ratings_df, extension='csv')
                with st.expander(label=f'Show the extended file: behavior.csv'):
                    # Showing the replicated rating file:
                    st.dataframe(updated_behaviors_df)
                    # Saving the replicated rating file:
                    wf_util.save_df(df_name='behavior', df_value=updated_behaviors_df, extension='csv')
    elif option == 'N ratings for each user':   
        if feedback_option == 'Explicit ratings':   
            if extend_button:  
                print('Extending the rating.csv file.')
                new_rating_df = increase_constructor.extend_rating_by_user(number_rating, percentage_rating_variation=None, k=None)            
                print('Extended data generation has finished.')
                with st.expander(label=f'Show the extended file: {config.RATING_TYPE}.csv'):                
                    # Showing the replicated rating file:
                    st.dataframe(new_rating_df)    
                    # Saving the replicated rating file:
                    wf_util.save_df(df_name='rating', df_value=new_rating_df, extension='csv')
        elif feedback_option == 'Implicit ratings':
            st.write('TODO')        
    else:
        if extend_button: 
            st.warning('The dataset extension type has not been selected.')
    return new_rating_df
