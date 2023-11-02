import console
import numpy as np
import pandas as pd
import streamlit as st
from datagencars.existing_dataset.generate_user_profile.generate_user_profile_dataset import GenerateUserProfileDataset
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_context import AccessContext
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_item import AccessItem
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_user import AccessUser
from streamlit_app import config, help_information
from streamlit_app.preprocess_dataset import wf_util
from streamlit_app.workflow_graph import workflow_image


def generate(with_context, only_automatic=False):
    """
    Generates the user profile.
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    """
    # WF --> Generate user profile:
    st.header('Workflow: Generate user profile')
    # Help information:
    help_information.help_user_profile_wf()
    # Worflow image:
    optional_value_list = [('NULLValues', str(True)), ('NULLValuesC', str(True)), ('NULLValuesI', str(True)), ('UPManual', 'True'), ('UPAutomatic', 'True')]
    workflow_image.show_wf(wf_name='GenerateUserProfile', init_step='True', with_context=True, optional_value_list=optional_value_list)
    st.markdown("""---""")

    # Loading dataset:   
    st.write('Upload the following files: ')     
    if with_context:
        user_df, item_df, context_df, rating_df, __ = wf_util.load_dataset(file_type_list=config.DATASET_CARS, wf_type='wf_user_profile')        
        # Getting the attribute names:    
        access_context = AccessContext(context_df=context_df)
        all_context_attribute_list = access_context.get_context_attribute_list()
        relevant_context_attribute_list = set_attribute_list(file_type=config.CONTEXT_TYPE, attribute_list=all_context_attribute_list)              
    else:
        context_df = pd.DataFrame()
        user_df, item_df, __, rating_df, __ = wf_util.load_dataset(file_type_list=config.DATASET_RS, wf_type='wf_user_profile')    
    # Getting the item attribute names:
    access_item = AccessItem(item_df=item_df)
    all_item_attribute_list = access_item.get_item_attribute_list()      
    relevant_item_attribute_list = set_attribute_list(file_type=config.ITEM_TYPE, attribute_list=all_item_attribute_list)
    # Choosing user profile generation options (manual or automatic):
    if only_automatic:
        up_options = st.selectbox(label='Choose an option to generate the user profile:', options=['Automatic'])
    else:
        up_options = st.selectbox(label='Choose an option to generate the user profile:', options=config.UP_OPTIONS)
    # Automatic generation of the user profile:
    user_profile_df = pd.DataFrame()
    if 'replace_context' not in st.session_state:
        st.session_state['replace_context'] = False
    if 'replace_item' not in st.session_state:
        st.session_state['replace_item'] = False
    if up_options == 'Automatic':
        # Help information:
        help_information.help_user_profile_automatic()
        # Showing the current image of the WF:
        optional_value_list = [('NULLValues', str(st.session_state['replace_context'] or st.session_state['replace_item'])), ('NULLValuesC', str(st.session_state['replace_context'])), ('NULLValuesI', str(st.session_state['replace_item'])), ('UPManual', 'False'), ('UPAutomatic', 'True')]                
        workflow_image.show_wf(wf_name='GenerateUserProfile', init_step='False', with_context=with_context, optional_value_list=optional_value_list)
    
        # Generating user profiles:
        if with_context:            
            if (not item_df.empty) and (not context_df.empty) and (not rating_df.empty):
                user_profile_df = generate_user_profile_automatic(item_attribute_list=relevant_item_attribute_list, rating_df=rating_df, item_df=item_df, context_df=context_df, context_attribute_list=relevant_context_attribute_list)
            else:
                st.warning('The item, context and rating files must be uploaded.')
        else:            
            if (not item_df.empty) and (not rating_df.empty):            
                user_profile_df = generate_user_profile_automatic(item_attribute_list=relevant_item_attribute_list, rating_df=rating_df, item_df=item_df)
            else:
                st.warning('The item and rating files must be uploaded.')
    # Manual generation of the user profile:
    elif up_options == 'Manual':
        if (not user_df.empty) and (not item_df.empty) and (not context_df.empty) and (not rating_df.empty):
            # Help information:
            help_information.help_user_profile_manual()  
            # Showing the current image of the WF:
            optional_value_list = [('NULLValues', str(st.session_state['replace_context'] or st.session_state['replace_item'])), ('NULLValuesC', str(st.session_state['replace_context'])), ('NULLValuesI', str(st.session_state['replace_item'])), ('UPManual', 'True'), ('UPAutomatic', 'False')]            
            workflow_image.show_wf(wf_name='GenerateUserProfile', init_step='False', with_context=with_context, optional_value_list=optional_value_list) 

            # Getting the number of user profiles to be generated:
            access_user = AccessUser(user_df=user_df)
            number_user_profile = access_user.get_count_user_profile_id()
            is_dinamic_row = False
            if number_user_profile == 0:
                number_user_profile = st.number_input(label='Specifies the number of user profiles to be generated:', value=3, key='number_user_profile')
                is_dinamic_row = True
            # Getting the item attribute value possibles:
            item_possible_value_map = {}
            for item_attribute in relevant_item_attribute_list:
                item_possible_value_map[item_attribute] = access_item.get_item_possible_value_list_from_attributte(attribute_name=item_attribute)        
            if with_context:
                # Getting the context attribute value possibles:
                context_possible_value_map = {}
                for context_attribute in relevant_context_attribute_list:
                    context_possible_value_map[context_attribute] = access_context.get_context_possible_value_list_from_attributte(attribute_name=context_attribute)                    
                attribute_column_list = ['user_profile_id']+relevant_item_attribute_list+relevant_context_attribute_list+['other']
                user_profile_df = generate_user_profile_manual(number_user_profile=int(number_user_profile), is_dinamic_row=is_dinamic_row, attribute_column_list=attribute_column_list, item_possible_value_map=item_possible_value_map, context_possible_value_map=context_possible_value_map)
            else:                
                attribute_column_list = ['user_profile_id']+relevant_item_attribute_list+['other']
                user_profile_df = generate_user_profile_manual(number_user_profile=int(number_user_profile), is_dinamic_row=is_dinamic_row, attribute_column_list=attribute_column_list, item_possible_value_map=item_possible_value_map)
        else:
            st.warning('All files must be uploaded.')
    return user_profile_df

def generate_user_profile_manual(number_user_profile, is_dinamic_row, attribute_column_list, item_possible_value_map, context_possible_value_map=None):  
    """
    Generate manually a user profile.
    :param number_user_profile: The number of user profiles to be generated.
    :param attribute_column_list: The attribute name list.
    :param item_possible_value_map: A map with item possible values.
    :param context_possible_value_map: A map with context possible values.
    :return: A dataframe with the content of the manually generated user profiles.
    """  
    weight_np = np.zeros(shape=(number_user_profile, len(attribute_column_list)), dtype=str)
    df = pd.DataFrame(weight_np, columns=attribute_column_list)
    for column in df.columns:
        df[column] = 0
    df['user_profile_id'] = df.index+1
    df['other'] = 1
    # Change the type of the first column to integer and the remaining columns to float:
    df['user_profile_id'] = df['user_profile_id'].astype(int)
    df.iloc[:, 1:] = df.iloc[:, 1:].astype(float)
    if is_dinamic_row:        
        user_profile_df = st.experimental_data_editor(df, num_rows="dynamic")
    else:
        user_profile_df = st.experimental_data_editor(df)
    # Getting possible values, in order to facilitate the importance ranking:
    attribute_possible_value_str = ''
    for attribute_column in attribute_column_list:    
        if attribute_column in item_possible_value_map:
            item_possible_value_list = item_possible_value_map[attribute_column]
            attribute_possible_value_str += f'- ```{attribute_column}``` : {item_possible_value_list}\n'
        elif attribute_column in context_possible_value_map:    
            context_possible_value_list = context_possible_value_map[attribute_column]            
            attribute_possible_value_str += f'- ```{attribute_column}``` : {context_possible_value_list}\n'     
    # # with st.expander('Show possible values by attribute, in order to facilitate the importance ranking'):
    st.markdown(attribute_possible_value_str)
    # Downloading user_profile.csv:
    is_sum_equal_to_1, user_profile_id_list = is_consistent(user_profile_df)
    if is_sum_equal_to_1:       
        # with st.expander(label='Show the generated user profile'):            
        # Iterate through columns (except the first and last) and apply the replacement logic
        for column in df.columns[1:-1]:                
            user_profile_df[column] = user_profile_df[column].apply(lambda x: f"({'-' if x < 0 else '+'})|{abs(x)}" if x != 0 else x)            
        # Transform all values in the "other" column to positive values:
        user_profile_df['other'] = user_profile_df['other'].abs()
        st.dataframe(user_profile_df)
        wf_util.save_df(df_name=config.USER_PROFILE_SCHEMA_NAME, df_value=user_profile_df, extension='csv')         
    else:
        st.warning(f'The following user_profile_id does not add up to 1: {user_profile_id_list}')     
    return user_profile_df

def is_consistent(df):
    # Check if the sum of values in each row is 1, ignoring the "user_profile_id" column:
    row_sums = df.iloc[:, 1:].abs().sum(axis=1)
    is_sum_equal_to_1 = row_sums.eq(1)    
    # Get user_profile_id values that do not sum to 1
    user_profile_id_list = df[~is_sum_equal_to_1]['user_profile_id'].tolist()    
    return is_sum_equal_to_1.all(), user_profile_id_list

def generate_user_profile_automatic(item_attribute_list, rating_df, item_df, context_df=None, context_attribute_list=None):
    """
    Generate automatically a user profile.
    :param rating_df: The rating dataframe.
    :param item_df: The item dataframe.
    :param context_df: The context dataframe.
    :return: A dataframe with the content of the automatically generated user profiles.
    """    
    output = st.empty()
    with console.st_log(output.code):
        # Generate user profile, by using an original dataset:
        generate_up_dataset = None
        user_profile_df = pd.DataFrame()                    
        # With context:
        if (context_df is not None) and (not context_df.empty):                
            if (not item_df.empty) and (not context_df.empty) and (not rating_df.empty):
                    if st.button(label='Generate', key='button_generate_up_cars'):
                        print('Automatically generating user profiles.')                    
                        generate_up_dataset = GenerateUserProfileDataset(rating_df, item_df, context_df)
                        user_profile_df = generate_up_dataset.generate_user_profile(item_attribute_list, context_attribute_list)
                        with st.expander(label=f'Show the generated user profile file.'):
                            st.dataframe(user_profile_df)
                            wf_util.save_df(df_name=config.USER_PROFILE_SCHEMA_NAME, df_value=user_profile_df, extension='csv')                             
                        print('The user profile has been generated.')                                                    
            else:
                st.warning("The item, context and rating files have not been uploaded.")
        else:
            # Without context:            
            if (not item_df.empty) and (not rating_df.empty):
                if st.button(label='Generate', key='button_generate_up_rs'):
                    print('Automatically generating user profiles.')                    
                    generate_up_dataset = GenerateUserProfileDataset(rating_df, item_df)
                    user_profile_df = generate_up_dataset.generate_user_profile(item_attribute_list)
                    with st.expander(label=f'Show the generated user profile file.'):
                        st.dataframe(user_profile_df)
                        wf_util.save_df(df_name=config.USER_PROFILE_SCHEMA_NAME, df_value=user_profile_df, extension='csv')  
                    print('The user profile has been generated.')
            else:
                st.warning("The item and rating files have not been uploaded.")    
    return user_profile_df

def set_attribute_list(file_type, attribute_list):
    """
    Setting the list of relevant item or context attributes before generating user profiles.
    :param file_type: The file type (item or context file).
    :param attribute_list: List of all available attributes in the file (item or context file).
    :return: The relevant attribute list.
    """
    attribute_relevant_list = []
    all_attribute_relevant = st.checkbox(label=f'All attributes of the {file_type}.csv file are relevant?', value=True)
    if all_attribute_relevant:
        attribute_relevant_list = attribute_list
    else:
        attribute_relevant_list = list(st.multiselect(label=f'Select the relevant {file_type} attributes.', options=attribute_list, key=f'multiselect_relevant_attributes_{file_type}'))
    return attribute_relevant_list
