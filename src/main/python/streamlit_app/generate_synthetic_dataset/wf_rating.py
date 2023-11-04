import console
import pandas as pd
import streamlit as st
from datagencars.synthetic_dataset.generator.generator_output_file.generator_explicit_rating_file import GeneratorExplicitRatingFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_implicit_rating_file import GeneratorImplicitRatingFile
from streamlit_app import config
from streamlit_app.generate_synthetic_dataset import wf_schema_util
from streamlit_app.preprocess_dataset import wf_util


def get_generation_config_schema(with_context):
    """
    Get the schema <generating_config.conf> for the generation of the rating file.    
    :return: The edited content of the <generating_config.conf> rating schema.
    """
    st.header('General Settings')    
    if st.checkbox('Upload the rating data generation configuration file', value=True, key=f'is_upload_{config.GENERATION_CONFIG_SCHEMA_NAME}'):
        # Uploading schema <"generation_config.conf">:
        schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.GENERATION_CONFIG_SCHEMA_NAME, tab_type='tab_rating')
    else:
        # Generating schema <"generation_config.conf">:
        schema_value = generate_generation_config_schema(with_context)
    # Editing schema:
    return wf_schema_util.edit_schema_file(schema_file_name=config.GENERATION_CONFIG_SCHEMA_NAME, schema_value=schema_value, tab_type='tab_rating') 

def generate_generation_config_schema(with_context):
    """
    Generate the schema file "generating_config.conf".
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    :return: The content of the "generating_config.conf" schema.
    """
    with st.expander(f"Generate generating_config_rating.conf"):
        st.write('Rating configuration')
        rating_value = '[rating] \n'
        rating_count = st.number_input(label='Number of ratings to generate:', value=0, key='rating_count')
        rating_min = st.number_input(label='Minimum value of the ratings:', value=1, key='rating_min')
        rating_max = st.number_input(label='Maximum value of the ratings:', value=5, key='rating_max')
        rating_impact = st.number_input(label='Impact of user expectatios in future ratings (%):', value=25, key='rating_impact')
        k_rating_past = st.number_input(label='Number of ratings in the past of a user to modify his/her current rating taking into account his/her expectations:', value=10, key='k_rating_past')
        rating_distribution = st.selectbox(label='Choose a distribution to generate the ratings:', options=['Uniform', 'Gaussian'])                        
        gaussian_distribution = True
        if rating_distribution == 'Uniform':
            gaussian_distribution = False            
        rating_value += ('number_rating=' + str(rating_count) + '\n' +
                        'minimum_value_rating=' + str(rating_min) + '\n' +
                        'maximum_value_rating=' + str(rating_max) + '\n' + 
                        'percentage_rating_variation=' + str(rating_impact) + '\n' +
                        'k_rating_past=' + str(k_rating_past) + '\n' +
                        'gaussian_distribution=' + str(gaussian_distribution) + '\n')
        with_timestamp_checkbox = st.checkbox(label='Generate timestamp the rating file?', value=False, key='with_timestamp_checkbox')
        if with_timestamp_checkbox:
            min_year_ts = st.number_input(label='From:', value=1980, key='date_min_generation_config')            
            max_year_ts = st.number_input(label='Until:', value=2022, key='date_max_generation_config')
            rating_value += ('minimum_date_timestamp='+str(min_year_ts)+'\n' +
                            'maximum_date_timestamp='+str(max_year_ts)+'\n')        
        even_distribution = st.checkbox(label='Users ratings should have a even distribution?', value=False, key='even_distribution')    
        rating_value += ('even_distribution='+str(even_distribution)+'\n') 
        if even_distribution == False:
            event_distribution_type = st.selectbox(label='Distribution type', options=['uniform', 'gaussian'])
        rating_value += ('even_distribution_type='+str(event_distribution_type)+'\n')

        # TODO: Añadir reglas rating implicitos
    return rating_value

def get_user_item_df():
    """
    Load dataframes containing user and item data.
    :return: The user and item dataframes.    
    """    
    st.header('User and Item Files')    
    # Uploading <user.csv>:
    user_df = wf_util.load_one_file(file_type='user', wf_type='wf_generate_explicit_rating')         
    # Uploading <item.csv>:
    item_df = wf_util.load_one_file(file_type='item', wf_type='wf_generate_explicit_rating')
    return user_df, item_df

def get_user_item_behavior_df():
    """
    Load dataframes containing user, item and behavior data.
    :return: The user, item and behavior dataframes.    
    """    
    st.header('User, Item and Behavior Files')    
    # Uploading <user.csv>:
    user_df = wf_util.load_one_file(file_type='user', wf_type='wf_generate_implicit_rating')
    # Uploading <item.csv>:
    item_df = wf_util.load_one_file(file_type='item', wf_type='wf_generate_implicit_rating')
    # Uploading <behavior.csv>:
    behavior_df = wf_util.load_one_file(file_type='behavior', wf_type='wf_generate_implicit_rating')
    return user_df, item_df, behavior_df

def get_user_item_context_df():
    """
    Load dataframes containing user, item and context data.
    :return: The user, item and context dataframes.             
    """
    st.header('User, Item and Context Files')
    # Uploading <user.csv>:
    user_df = wf_util.load_one_file(file_type='user', wf_type='wf_generate_explicit_rating')           
    # Uploading <item.csv>:
    item_df = wf_util.load_one_file(file_type='item', wf_type='wf_generate_explicit_rating')
    # Uploading <context.csv>:
    context_df = wf_util.load_one_file(file_type='context', wf_type='wf_generate_explicit_rating')
    return user_df, item_df, context_df

def get_user_item_context_behavior_df():
    """
    Load dataframes containing user, item, context and behavior data.
    :return: The user, item, context and behavior dataframes.             
    """
    st.header('User, Item, Context and Behavior Files')
    # Uploading <user.csv>:
    user_df = wf_util.load_one_file(file_type='user', wf_type='wf_generate_implicit_rating')
    # Uploading <item.csv>:
    item_df = wf_util.load_one_file(file_type='item', wf_type='wf_generate_implicit_rating')
    # Uploading <context.csv>:
    context_df = wf_util.load_one_file(file_type='context', wf_type='wf_generate_implicit_rating')
    # Uploading <behavior.csv>:
    behavior_df = wf_util.load_one_file(file_type='behavior', wf_type='wf_generate_implicit_rating')
    return user_df, item_df, context_df, behavior_df

def get_item_schema():
    """
    Load item schema.
    :return: The item schema.
    """    
    st.header('Item Schema')    
    # Uploading <item_schema.conf>:      
    item_schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.ITEM_SCHEMA_NAME, tab_type='tab_rating')
    # Editing schema:
    return wf_schema_util.edit_schema_file(schema_file_name=config.ITEM_SCHEMA_NAME, schema_value=item_schema_value, tab_type='tab_rating')

def get_item_context_schema():
    """
    Load item and context schemas.
    :return: The item and context schemas.
    """
    st.header('Item and Context Schemas')
    # Uploading <item_schema.conf>:
    item_schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.ITEM_SCHEMA_NAME, tab_type='tab_rating')
    # Editing schema:
    item_schema = wf_schema_util.edit_schema_file(schema_file_name=config.ITEM_SCHEMA_NAME, schema_value=item_schema_value, tab_type='tab_rating')

    # Uploading <context_schema.conf>:  
    context_schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.CONTEXT_SCHEMA_NAME, tab_type='tab_rating')
    # Editing schema:
    context_schema = wf_schema_util.edit_schema_file(schema_file_name=config.CONTEXT_SCHEMA_NAME, schema_value=context_schema_value, tab_type='tab_rating')
    return item_schema, context_schema

def get_user_profile():
    """
    Load user profile.
    :return: A dataframe with the user profile.
    """  
    st.header('User Profile')     
    # Uploading <user_profile.csv>:
    user_profile_df = wf_util.load_one_file(file_type='user_profile', wf_type='wf_generate_explicit_rating')
    return user_profile_df
    
def generate_explicit_rating_file(with_context, generation_config, user_df, user_profile_df, item_df, item_schema=None, context_df=None, context_schema=None):
    """
    Generate a rating file based on the provided data and configuration.
    :param with_context: A boolean indicating whether to include context data.
    :param generation_config: The configuration for rating file generation.
    :param user_df: The dataframe with user data.
    :param user_profile_df: The dataframe with user profiles.
    :param item_df: The dataframe with item data.
    :param context_df: The dataframe with context data (optional).
    :param item_schema: The item schema (optional).
    :param context_schema: The context schema (optional).
    :return: A dataframe containing the generated rating data.
    """
    generator = None    
    rating_df = pd.DataFrame()
    if st.button(label='Generate rating file', key='button_tab_rating'):
        if with_context:  
            # The mandatory files to be uploaded are checked (including contextual information):
            if (not user_df.empty) and (not item_df.empty) and (not context_df.empty):
                # All files are uploaded, including item and context schemas:
                if (len(generation_config) !=0) and (item_schema) and (context_schema):
                    if (not user_profile_df.empty):
                        generator = GeneratorExplicitRatingFile(generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df, item_schema=item_schema, context_df=context_df, context_schema=context_schema)
                    else:
                        st.warning('The user profile file is required.')
                else:
                    st.warning('The generation_config, item and context schema files are required.')
            else:
                st.warning('The user, item and context files are required.')
        else:
            # The mandatory files to be uploaded are checked (without contextual information):
            if (not user_df.empty) and (not item_df.empty):
                # All files are uploaded, including the item schema:
                if (len(generation_config) !=0) and (item_schema):
                    if (not user_profile_df.empty):
                        generator = GeneratorExplicitRatingFile(generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df, item_schema=item_schema)
                    else:
                        st.warning('The user profile file is required.')                
                else:
                    st.warning('The generation_config and item schema files are required.')
            else:
                st.warning('The user and item files are required.')
        # Generating rating file (rating.csv):        
        if generator:
            output = st.empty()
            with console.st_log(output.code):              
                rating_df = generator.generate_file()
                print('Rating file generation has finished.') 
                # Showing <rating.csv>:
                with st.expander(label=f'Show the generated {config.RATING_TYPE}.csv file:'):
                    st.dataframe(rating_df)
                    wf_util.save_df(df_name=config.RATING_TYPE, df_value=rating_df, extension='csv')   
    return rating_df

def generate_implicit_rating_file(with_context, generation_config, user_df, item_df, behavior_df, context_df=None):
    """
    Generate a rating file based on the provided data and configuration.
    :param with_context: A boolean indicating whether to include context data.
    :param generation_config: The configuration for rating file generation.
    :param user_df: The dataframe with user data.
    :param item_df: The dataframe with item data.
    :param behavior_df: The dataframe with behavior data.
    :param context_df: The dataframe with context data (optional).
    :return: A dataframe containing the generated rating data.
    """
    generator = None    
    rating_df = pd.DataFrame()
    if st.button(label='Generate rating file', key='button_tab_rating'):
        if with_context:  
            # The mandatory files to be uploaded are checked (including contextual information):
            if (not user_df.empty) and (not item_df.empty) and (not behavior_df.empty) and (not context_df.empty):
                # All files are uploaded:
                if (len(generation_config) !=0):
                    generator = GeneratorImplicitRatingFile(generation_config=generation_config, item_df=item_df, behavior_df=behavior_df, context_df=context_df)
                else:
                    st.warning('The generation_config file is required.')
            else:
                st.warning('The user, item, behavior and context files are required.')
        else:
            # The mandatory files to be uploaded are checked (without contextual information):
            if (not user_df.empty) and (not item_df.empty) and (not behavior_df.empty):
                # All files are uploaded:
                if (len(generation_config) !=0):
                    generator = GeneratorImplicitRatingFile(generation_config=generation_config, user_df=user_df, item_df=item_df, behavior_df=behavior_df)
                else:
                    st.warning('The generation_config file is required.')
            else:
                st.warning('The user, item and behavior files are required.')
        # Generating rating file (rating.csv):        
        if generator:
            output = st.empty()
            with console.st_log(output.code):              
                rating_df = generator.generate_file()
                print('Rating file generation has finished.') 
                # Showing <rating.csv>:
                with st.expander(label=f'Show the generated {config.RATING_TYPE}.csv file:'):
                    st.dataframe(rating_df)
                    wf_util.save_df(df_name=config.RATING_TYPE, df_value=rating_df, extension='csv')
    return rating_df
