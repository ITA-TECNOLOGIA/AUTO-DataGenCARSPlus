import io

import console
import pandas as pd
import streamlit as st
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_context import AccessContext
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_item import AccessItem
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_user import AccessUser
from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.generator.generator_output_file.generator_explicit_rating_file import GeneratorExplicitRatingFile
from streamlit_app import config, help_information
from streamlit_app.generate_synthetic_dataset import wf_schema_util
from streamlit_app.preprocess_dataset import wf_generate_user_profile, wf_util


def get_generation_config_schema(with_context):
    """
    Get the schema <generating_config.conf> for the generation of the rating file.    
    :return: The edited content of the <generating_config.conf> rating schema.
    """
    st.header('General settings')    
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
    with st.expander(f"Generate generating_config_user.conf"):
        # [dimension]    
        dimension_value = '[dimension] \n'
        user_count = st.number_input(label='Number of users to generate:', value=0)
        item_count = st.number_input(label='Number of items to generate:', value=0)
        if with_context:
            context_count = st.number_input(label='Number of contexts to generate:', value=0)
            dimension_value += ('number_user=' + str(user_count) + '\n' +
                                'number_item=' + str(item_count) + '\n' +
                                'number_context=' + str(context_count) + '\n')
        else:            
            dimension_value += ('number_user=' + str(user_count) + '\n' +
                            'number_item=' + str(item_count) + '\n')
        percentage_null_user = st.number_input(label='Percentage of null user values:', value=0)
        percentage_null_item = st.number_input(label='Percentage of null item values:', value=0)
        if with_context:
            percentage_null_context = st.number_input(label='Percentage of null context values:', value=0)
            dimension_value += ('percentage_user_null_value=' + str(percentage_null_user) + '\n' +
                                'percentage_item_null_value=' + str(percentage_null_item) + '\n' +
                                'percentage_context_null_value=' + str(percentage_null_context) + '\n')
        else:
            dimension_value += ('percentage_user_null_value=' + str(percentage_null_user) + '\n' +
                            'percentage_item_null_value=' + str(percentage_null_item) + '\n')
        st.markdown("""---""")
        # [rating]
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
        st.markdown("""---""")
        # [item profile]
        item_profile_value = ''            
        with_correlation_checkbox = st.checkbox(label='Apply correlation in the generation of the item file?', value=False, key='with_correlation_checkbox')
        if with_correlation_checkbox:
            st.write('Item profile configuration')
            item_profile_value = '[item profile] \n'
            probability_percentage_profile_1 = st.number_input(label='Profile probability percentage 1:', value=10)
            probability_percentage_profile_2 = st.number_input(label='Profile probability percentage 2:', value=30)
            probability_percentage_profile_3 = st.number_input(label='Profile probability percentage 3:', value=60)
            noise_percentage_profile_1 = st.number_input(label='Profile noise percentage 1:', value=20)
            noise_percentage_profile_2 = st.number_input(label='Profile noise percentage 2:', value=20)
            noise_percentage_profile_3 = st.number_input(label='Profile noise percentage 3:', value=20)            
            item_profile_value += ('probability_percentage_profile_1=' + str(probability_percentage_profile_1) + '\n' +
                                'probability_percentage_profile_2=' + str(probability_percentage_profile_2) + '\n' +
                                'probability_percentage_profile_3=' + str(probability_percentage_profile_3) + '\n' +
                                'noise_percentage_profile_1=' + str(noise_percentage_profile_1) + '\n' +
                                'noise_percentage_profile_2=' + str(noise_percentage_profile_2) + '\n' +
                                'noise_percentage_profile_3=' + str(noise_percentage_profile_3) + '\n')
        # Generating the text of the file <generation_config.conf>:
        generation_config_schema = dimension_value + '\n' + rating_value + '\n' + item_profile_value
    return generation_config_schema

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
    
def get_user_profile(with_context):
    """
    Retrieve or generate a user profile dataframe based on the chosen options.
    :param with_context: A boolean indicating whether to include context data.
    :return: A dataframe containing user profiles and an option indicating how the data was obtained.
    """
    st.header('User profile')    
    user_profile_df = pd.DataFrame()
    up_option = ''
    # Generating or uploading <user_profile.csv>:
    if st.checkbox(f'Upload the data {config.USER_PROFILE_SCHEMA_NAME} file', value=True, key=f'is_upload_{config.USER_PROFILE_SCHEMA_NAME}_file'):
        # Uploading <user_profile.csv>:
        user_profile_df = upload_user_profile_file()
        up_option = 'upload-up'
    else:
        # Generating <user_profile.csv>:
        type_file = st.radio(label='Which files will you use to generate user profiles?', options=['Schemas (user_schema.conf, item_schema.conf and context_schema.conf <optional>)','Files (user.csv, item.csv and context.csv <optional>)'], key='radio_file_type')        
        if type_file == 'Schemas (user_schema.conf, item_schema.conf and context_schema.conf <optional>)':            
            up_option = 'upload-schema'
            if with_context:
                user_schema, item_schema, context_schema = get_user_item_context_schema()
                user_profile_df = get_user_profile_from_schema(user_schema, item_schema, context_schema)
            else:
                user_schema, item_schema = get_user_item_schema()
                user_profile_df = get_user_profile_from_schema(user_schema, item_schema)
        elif type_file == 'Files (user.csv, item.csv and context.csv <optional>)':
            up_option = 'upload-file'
            if with_context:
                user_df, item_df, context_df = get_user_item_context_df()
                user_profile_df = get_user_profile_from_file(user_df, item_df, context_df)
            else:
                user_df, item_df = get_user_item_df()
                user_profile_df = get_user_profile_from_file(user_df, item_df)
    return user_profile_df, up_option

def upload_user_profile_file():
    """
    Upload an existing user profile.
    :return: A dataframe with the user profile content.
    """
    user_profile_df = pd.DataFrame()
    with st.expander(label=f'Upload {config.USER_PROFILE_SCHEMA_NAME}.csv'):
        if user_profile_file := st.file_uploader(label='Choose the file:', key=f'{config.USER_PROFILE_SCHEMA_NAME}_tab_rating'):
            user_profile_value = user_profile_file.getvalue().decode("utf-8")
            user_profile_df = pd.read_csv(io.StringIO(user_profile_value))  
            st.dataframe(user_profile_df)
    return user_profile_df

def get_user_profile_from_schema(user_schema, item_schema, context_schema=None):
    """    
    Generate a user profile dataframe based on provided schema configurations.
    :param user_schema: The user schema.
    :param item_schema: The item schema.
    :param context_schema: The context schema <optional>.
    :return: A dataframe containing the generated user profiles based on the schemas.
    """   
    user_profile_df = pd.DataFrame() 
    # Generating <user_profile.csv> from schemas:   
    if (len(user_schema) != 0) and (len(item_schema) != 0) and (context_schema):
        # Getting <user_schema.conf>, <item_schema.conf> and <context_schema.conf> schemas:
        user_schema, item_schema, context_schema = get_user_item_context_schema()
        # Generating <user_profile.csv> from schemas:        
        user_profile_df = generate_user_profile_from_schema(user_schema, item_schema, context_schema)        
    elif (len(user_schema) != 0) and (len(item_schema) != 0) and (not context_schema):
        # Getting <user_schema.conf> and <item_schema.conf> schemas:
        user_schema, item_schema = get_user_item_schema()
        # Generating <user_profile.csv> for <user_schema.conf> and <item_schema.conf> schemas:        
        user_profile_df = generate_user_profile_from_schema(user_schema, item_schema)     
    else:
        st.warning('The user, item and context<optional> schemas are required.')
    return user_profile_df

def get_user_item_schema(is_user):
    """
    Load schema containing user and item data.
    :return: The user and item schema. 
    """    
    user_schema=item_schema=''    
    if is_user:
        st.header('User and Item Schemas')
        # Uploading <user_schema.conf>: optional
        user_schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.USER_SCHEMA_NAME, tab_type='tab_rating')
        # Editing schema:
        user_schema = wf_schema_util.edit_schema_file(schema_file_name=config.USER_SCHEMA_NAME, schema_value=user_schema_value, tab_type='tab_rating')         
    else:
        st.header('Item Schema')
    # Uploading <item_schema.conf>: optional
    item_schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.ITEM_SCHEMA_NAME, tab_type='tab_rating')
    # Editing schema:
    item_schema = wf_schema_util.edit_schema_file(schema_file_name=config.ITEM_SCHEMA_NAME, schema_value=item_schema_value, tab_type='tab_rating')
    return user_schema, item_schema
    
def get_user_item_context_schema(is_user):
    """
    Load schemas containing user, item and context data.
    :return: The user, item and context schemas.
    """
    user_schema=item_schema=context_schema=''    
    if is_user:
        st.header('User, Item and Context Schemas')           
        # Uploading <user_schema.conf>: optional
        user_schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.USER_SCHEMA_NAME, tab_type='tab_rating')
        # Editing schema:
        user_schema = wf_schema_util.edit_schema_file(schema_file_name=config.USER_SCHEMA_NAME, schema_value=user_schema_value, tab_type='tab_rating')             
    else:
        st.header('Item and Context Schemas')               
    # Uploading <item_schema.conf>: optional
    item_schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.ITEM_SCHEMA_NAME, tab_type='tab_rating')
    # Editing schema:
    item_schema = wf_schema_util.edit_schema_file(schema_file_name=config.ITEM_SCHEMA_NAME, schema_value=item_schema_value, tab_type='tab_rating')
    # Uploading <context_schema.conf>: optional     
    context_schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.CONTEXT_SCHEMA_NAME, tab_type='tab_rating')
    # Editing schema:
    context_schema = wf_schema_util.edit_schema_file(schema_file_name=config.CONTEXT_SCHEMA_NAME, schema_value=context_schema_value, tab_type='tab_rating')
    return user_schema, item_schema, context_schema
    
def generate_user_profile_from_schema(user_schema, item_schema, context_schema=None):
    """
    Generate the user profile file (user_profile.csv).
    :param user_schema: The content of the user schema file.
    :param item_schema: The content of the item schema file.
    :param context_schema: The content of the context schema file <optional>.
    :return: The content of the item profile file.
    """
    # Help information:
    help_information.help_user_profile_manual()    
    # Adding column "id":
    attribute_column_list = ['user_profile_id']
    # Adding relevant item attribute columns:        
    item_access_schema = AccessSchema(file_str=item_schema)
    item_attribute_name_list = item_access_schema.get_important_attribute_name_list()
    attribute_column_list.extend(item_attribute_name_list)   
    item_possible_value_map = {}
    for item_attribute_name in item_attribute_name_list:
        item_possible_value_map[item_attribute_name] = item_access_schema.get_possible_values_attribute_list_from_name(attribute_name=item_attribute_name)                
    # Adding relevant context attribute columns:    
    if context_schema:
        context_access_schema = AccessSchema(file_str=context_schema)
        context_attribute_name_list = context_access_schema.get_important_attribute_name_list()
        attribute_column_list.extend(context_attribute_name_list)
        context_possible_value_map = {}
        for context_attribute_name in context_attribute_name_list:
            context_possible_value_map = context_access_schema.get_possible_values_attribute_list_from_name(attribute_name=context_attribute_name)
    # Adding column "other":
    attribute_column_list.extend(['other']) 
    # Introducing the number of user profiles to generate:            
    user_access = AccessSchema(file_str=user_schema)
    initial_value = len(user_access.get_possible_values_attribute_list_from_name(attribute_name='user_profile_id'))
    number_user_profile = st.number_input(label='Number of user profiles:', value=initial_value, disabled=True)
    st.warning('The number of profiles has been previously defined in the ```user_profile_id``` attribute of the ```user_schema.conf``` file. If you want to change it, you must first modify the ```user_schema.conf``` file.')                            
    # Generate user profile manual:                
    user_profile_df = wf_generate_user_profile.generate_user_profile_manual(number_user_profile, attribute_column_list, item_possible_value_map, context_possible_value_map)
    return user_profile_df

def get_user_profile_from_file(user_df, item_df, context_df=None):  
    """
    Generate a user profile dataframe from provided user, item and context dataframes.
    :param user_df: The user dataframe.
    :param item_df: The item dataframe.
    :param context_df: The context dataframe <optional>.
    :return: A dataframe containing the generated user profiles based on the provided dataframes.
    """
    user_profile_df = pd.DataFrame()  
    # Generating <user_profile.csv> from file:   
    if (not user_df.empty) and (not item_df.empty) and (not context_df.empty):
        # Generating <user_profile.csv> for <user.csv>, <item.csv> and <context.csv> files:        
        user_profile_df = generate_user_profile_from_file(user_df, item_df, context_df)        
    elif (not user_df.empty) and (not item_df.empty) and (context_df.empty):
        # Generating <user_profile.csv> for <user.csv> and <item.csv> files:        
        user_profile_df = generate_user_profile_from_file(user_df, item_df)        
    else:
        st.warning('The user, item and context<optional> files are required.')
    return user_profile_df

def generate_user_profile_from_file(user_df, item_df, context_df=None):
    """
    Generate the user profile file (user_profile.csv).
    :param user_df: The content of the user file.
    :param item_df: The content of the item file.
    :param context_df: The content of the context file <optional>.
    :return: The content of the item profile file.
    """
    # Help information:
    help_information.help_user_profile_manual()
    # Adding column "id":
    attribute_column_list = ['user_profile_id']
    # Adding relevant item attribute columns:
    item_access = AccessItem(item_df=item_df)    
    item_attribute_name_list = item_access.get_item_attribute_list()
    attribute_column_list.extend(item_attribute_name_list)
    item_possible_value_map = {}
    for item_attribute_name in item_attribute_name_list:
        item_possible_value_map[item_attribute_name] = item_access.get_item_possible_value_list_from_attributte(attribute_name=item_attribute_name)
    # Adding relevant context attribute columns:
    if context_df:
        context_access = AccessContext(item_df=context_df)            
        context_attribute_name_list = context_access.get_context_attribute_list()
        attribute_column_list.extend(context_attribute_name_list)
        context_possible_value_map = {}
        for context_attribute_name in context_attribute_name_list:
            context_possible_value_map = context_access.get_context_possible_value_list_from_attributte(attribute_name=context_attribute_name)
    # Adding column "other":
    attribute_column_list.extend(['other']) 
    # Introducing the number of user profiles to generate:   
    user_access = AccessUser(user_df=user_df)      
    count_user_profile_id = user_access.get_count_user_profile_id()
    if count_user_profile_id != 0:
        number_user_profile = st.number_input(label='Number of user profiles:', value=count_user_profile_id, disabled=True)
    else:
        number_user_profile = st.number_input(label='Number of user profiles:', value=4, disabled=True)    
    # Generate user profile manual:                
    user_profile_df = wf_generate_user_profile.generate_user_profile_manual(number_user_profile, attribute_column_list, item_possible_value_map, context_possible_value_map)
    return user_profile_df

def get_rating_file(with_context, generation_config, user_profile_df, up_option):
    """
    Generate a rating file dataframe based on configuration and user profiles.
    :param with_context: A boolean indicating whether to include context data.
    :param generation_config: General settings for rating generation.
    :param user_profile_df: A dataframe containing user profiles.
    :param up_option: An option indicating how the user profile data was obtained.
    :return: A dtaframe containing the generated rating data.
    """    
    rating_df = pd.DataFrame()
    if (len(generation_config) != 0) and (len(up_option) != 0) and (not user_profile_df.empty):        
        if up_option == 'upload-schema':
            if with_context:
                __, item_schema, context_schema = get_user_item_context_schema(is_user=False)
                user_df, item_df, context_df = get_user_item_context_df()            
                rating_df = generate_rating_file(with_context, generation_config, user_df, user_profile_df, item_df, item_schema, context_df, context_schema)
            else:
                __, item_schema = get_user_item_schema(is_user=False)
                user_df, item_df = get_user_item_context_df()        
                rating_df = generate_rating_file(with_context, generation_config, user_df, user_profile_df, item_df, item_schema)
        elif up_option == 'upload-file':
            if with_context:
                user_df, item_df, context_df = get_user_item_context_df()
                rating_df = generate_rating_file(with_context, generation_config, user_df, user_profile_df, item_df, context_df)
            else:
                user_df, item_df = get_user_item_df()
                rating_df = generate_rating_file(with_context, generation_config, user_df, user_profile_df, item_df)
        elif up_option == 'upload-up':
            type_file = st.radio(label='Which files will you use to choose the contextual attribute possible values during rating generation?', options=['Schemas (item_schema.conf and context_schema.conf <optional>)','Files (item.csv and context.csv <optional>)'], key='radio_file_type_ratings')
            if type_file == 'Schemas (item_schema.conf and context_schema.conf <optional>)':            
                if with_context:
                    __, item_schema, context_schema = get_user_item_context_schema(is_user=False)
                    user_df, item_df, context_df = get_user_item_context_df()            
                    rating_df = generate_rating_file(with_context=with_context, generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df, item_schema=item_schema, context_df=context_df, context_schema=context_schema)
                else:
                    __, item_schema = get_user_item_schema(is_user=False)
                    user_df, item_df = get_user_item_context_df()        
                    rating_df = generate_rating_file(with_context=with_context, generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df, item_schema=item_schema)
            elif type_file == 'Files (item.csv and context.csv <optional>)':                
                if with_context:
                    user_df, item_df, context_df = get_user_item_context_df()
                    rating_df = generate_rating_file(with_context=with_context, generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df, context_df=context_df)
                else:
                    user_df, item_df = get_user_item_df()
                    rating_df = generate_rating_file(with_context=with_context, generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df)
    else:
        st.warning('The general settings and the user profile file must be previously generated.')
    return rating_df

def generate_rating_file(with_context, generation_config, user_df, user_profile_df, item_df, item_schema=None, context_df=None, context_schema=None):
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
            if (len(generation_config) !=0) and (not user_df.empty) and (not user_profile_df.empty) and (not item_df.empty) and (not context_df.empty):
                # All files are uploaded, including item and context schemas:  
                if (item_schema) and (context_schema):
                    generator = GeneratorExplicitRatingFile(generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df, item_schema=item_schema, context_df=context_df, context_schema=context_schema)
                # All files are uploaded, except context schema:
                elif (item_schema) and (not context_schema):
                    generator = GeneratorExplicitRatingFile(generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df, item_schema=item_schema, context_df=context_df)
                # All files are uploaded, except item schema:
                elif (not item_schema) and (context_schema):
                    generator = GeneratorExplicitRatingFile(generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df, context_df=context_df, context_schema=context_schema)
                # All files are uploaded, except item and context schemas:
                else:                    
                    generator = GeneratorExplicitRatingFile(generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df, context_df=context_df)                        
            else:
                st.warning('The schema files are required.')
        else:
            # The mandatory files to be uploaded are checked (without contextual information):
            if (len(generation_config) !=0) and (not user_df.empty) and (not user_profile_df.empty) and (not item_df.empty):
                # All files are uploaded, including the item schema:
                if item_schema:
                    generator = GeneratorExplicitRatingFile(generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df, item_schema=item_schema)
                # All files are uploaded, except item schema:
                else:
                    generator = GeneratorExplicitRatingFile(generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df)
            else:
                st.warning('The files are required.')
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
