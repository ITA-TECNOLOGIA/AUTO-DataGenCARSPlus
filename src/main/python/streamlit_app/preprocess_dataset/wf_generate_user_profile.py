import console
import numpy as np
import pandas as pd
import streamlit as st
from datagencars.existing_dataset.generate_user_profile.generate_user_profile_dataset import GenerateUserProfileDataset
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_context import AccessContext
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_item import AccessItem
from streamlit_app import config, help_information
from streamlit_app.preprocess_dataset import wf_util
from streamlit_app.workflow_graph import workflow_image


def generate(with_context, null_values_i, null_values_c, only_automatic=False):
    """
    Generates the user profile.
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    """
    # WF --> Generate user profile:
    st.header('Workflow: Generate user profile')
    # Help information:
    help_information.help_user_profile_wf()
    # Worflow image:    
    optional_value_list = [('NULLValues', str(True)), ('NULLValuesC', str(st.session_state.replace_context)), ('NULLValuesI', str(st.session_state.replace_item)), ('UPManual', 'True'), ('UPAutomatic', 'True')]
    workflow_image.show_wf(wf_name='GenerateUserProfile', init_step='False', with_context=True, optional_value_list=optional_value_list)
    st.markdown("""---""")

    # Loading dataset:   
    st.write('Upload the following files: ')     
    if with_context:
        __, item_df, context_df, rating_df, __ = wf_util.load_dataset(file_type_list=config.DATASET_CARS, wf_type='wf_user_profile')        
        # Getting the attribute names:    
        access_context = AccessContext(context_df=context_df)
        all_context_attribute_list = access_context.get_context_attribute_list()
        relevant_context_attribute_list = set_attribute_list(file_type=config.CONTEXT_TYPE, attribute_list=all_context_attribute_list)              
    else:
        context_df = pd.DataFrame()
        __, item_df, __, rating_df, __ = wf_util.load_dataset(file_type_list=config.DATASET_RS, wf_type='wf_user_profile')    
    # Getting the item attribute names:
    access_item = AccessItem(item_df=item_df)
    all_item_attribute_list = access_item.get_item_attribute_list()      
    relevant_item_attribute_list = set_attribute_list(file_type=config.ITEM_TYPE, attribute_list=all_item_attribute_list)
    # Choosing user profile generation options (manual or automatic):
    if only_automatic:
        up_options = st.selectbox(label='Choose an option to generate the user profile:', options=['automatic'])
    else:
        up_options = st.selectbox(label='Choose an option to generate the user profile:', options=config.UP_OPTIONS)
    # Automatic generation of the user profile:
    user_profile_df = pd.DataFrame()
    if up_options == 'Automatic':
        # Help information:
        help_information.help_user_profile_automatic()
        # Showing the current image of the WF:
        workflow_image.show_wf(wf_name='GenerateUserProfile', init_step='False', with_context=with_context, optional_value_list=[('NULLValues', str(null_values_c or null_values_i)), ('NULLValuesC', str(null_values_c)), ('NULLValuesI', str(null_values_i)), ('UPManual', 'False'), ('UPAutomatic', 'True')])
    
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
        if (not item_df.empty) and (not context_df.empty) and (not rating_df.empty):
            # Help information:
            help_information.help_user_profile_manual()  
            # Showing the current image of the WF:
            workflow_image.show_wf(wf_name='GenerateUserProfile', init_step='False', with_context=with_context, optional_value_list=[('NULLValues', str(null_values_c or null_values_i)), ('NULLValuesC', str(null_values_c)), ('NULLValuesI', str(null_values_i)), ('UPManual', 'True'), ('UPAutomatic', 'False')]) 

            # Getting the number of user profiles to be generated:
            number_user_profile = st.number_input(label='Specifies the number of user profiles to be generated:', value=3, key='number_user_profile')
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
                user_profile_df = generate_user_profile_manual(number_user_profile=int(number_user_profile), attribute_column_list=attribute_column_list, item_possible_value_map=item_possible_value_map, context_possible_value_map=context_possible_value_map)
            else:                
                attribute_column_list = ['user_profile_id']+relevant_item_attribute_list+['other']
                user_profile_df = generate_user_profile_manual(number_user_profile=int(number_user_profile), attribute_column_list=attribute_column_list, item_possible_value_map=item_possible_value_map)    
        else:
            st.warning('The files must be uploaded.')
    return user_profile_df
    
def generate_user_profile_manual(number_user_profile, attribute_column_list, item_possible_value_map, context_possible_value_map=None):
    """
    Generate manually a user profile.
    :param number_user_profile: The number of user profiles to be generated.
    :param attribute_column_list: The attribute name list.
    :param item_possible_value_map: A map with item possible values.
    :param context_possible_value_map: A map with context possible values.
    :return: A dataframe with the content of the manually generated user profiles.
    """   
    user_profile_df = None    
    inconsistent = False
    # Randomly fill a dataframe and cache it:
    weight_np = np.zeros(shape=(number_user_profile, len(attribute_column_list)), dtype=str)
    @st.cache(allow_output_mutation=True)    
    def get_dataframe():
        df = pd.DataFrame(weight_np, columns=attribute_column_list)
        for column in df.columns:
            df[column] = 0
        df['user_profile_id'] = df.index+1
        df['other'] = 1
        df = df.astype(str)
        return df            
    user_profile_df = get_dataframe()
    export_df = user_profile_df.copy()
    # Create row, column, and value inputs:
    col_row, col_col, col_val = st.columns(3)
    with col_row:
        # Choosing the row index:
        row = st.number_input('row (profile)', max_value=user_profile_df.shape[0]) #, value=1
    col = 0
    with col_col:
        # Choosing the column index:
        attribute_column_list_box = attribute_column_list.copy()
        attribute_column_list_box.remove('other')
        attribute_column_list_box.remove('user_profile_id')
        if len(attribute_column_list_box) > 0:
            selected_attribute = st.selectbox(label='column (attribute)', options=attribute_column_list_box)
            attribute_position = attribute_column_list_box.index(selected_attribute)
            col = attribute_position
            # Getting possible values, in order to facilitate the importance ranking:
            if selected_attribute in item_possible_value_map:
                item_possible_value_list = item_possible_value_map[selected_attribute]
                st.warning(item_possible_value_list)    
            elif selected_attribute in context_possible_value_map:    
                context_possible_value_list = context_possible_value_map[selected_attribute]
                st.warning(context_possible_value_list)
    with col_val:   
        # Inserting weight value:
        value = st.text_input(label='weight (with range [-1,1])', value=0)      
        st.warning('Examples of values to be entered: -1, -0.6, 0, +0.4 or 0.4, +1 or 1')
        # Checking attribute weights:                    
        # Float number:
        if ('.' in str(value)) or (',' in str(value)):
            # Negative number:
            if float(value) < -1.0:
                st.warning('The ```weight``` must be greater than -1.')  
            else:
                # Range [0-1]:
                if float(value) > 1.0:
                    st.warning('The ```weight``` value must be in the range ```[-1,1]```.')  
        else:
            # Negative number:
            if int(value) < -1:
                st.warning('The ```weight``` must be greater than -1.')  
            else:
                # Range [0-1]:
                if (int(value) > 1):
                    st.warning('The ```weight``` value must be in the range ```[-1,1]```.')
    # Change the entry at (row, col) to the given weight value:
    if not user_profile_df.empty:
        print(user_profile_df.values[row][col+1])
        user_profile_df.values[row][col+1] = str(value)
    else:
        st.warning("user_profile_df is empty.")
    other_value = 1
    for column in attribute_column_list:
        if column != 'user_profile_id' and column != 'other':
            other_value = float(abs(other_value-abs(float(user_profile_df.values[row][attribute_column_list.index(column)]))))
    if not user_profile_df.empty:
        user_profile_df.values[row][len(user_profile_df.columns)-1] = f"{other_value:.1f}"
    else:
        st.warning("user_profile_df is empty.")
    if not user_profile_df.empty:
        if float(user_profile_df.values[row][len(user_profile_df.columns)-1]) < 0 or float(user_profile_df.values[row][len(user_profile_df.columns)-1]) > 1:
            st.warning('Values in a row for user must equal 1')
            inconsistent = True
        else:
            for index, row in user_profile_df.iterrows():
                for column in user_profile_df.columns:
                    if column != 'user_profile_id' and column != 'other':
                        if float(row[column]) > 0:
                            export_df.values[index][attribute_column_list.index(column)] = f'(+)|{str(abs(float(row[column])))}'
                        elif float(row[column]) < 0:
                            export_df.values[index][attribute_column_list.index(column)] = f'(-)|{str(abs(float(row[column])))}'
                        else:
                            export_df.values[index][attribute_column_list.index(column)] = f'0'
                    if column == 'other':
                        if float(row[column]) == 0:
                            export_df.values[index][attribute_column_list.index(column)] = f'0'
                        else:
                            export_df.values[index][attribute_column_list.index(column)] = f'{str(abs(float(row[column])))}'
    else:
        st.warning("user_profile_df is empty.")
    # Show the user profile dataframe:
    help_information.help_user_profile_id()
    st.dataframe(export_df)
    # Downloading user_profile.csv:
    if not inconsistent:
        wf_util.save_df(df_name=config.USER_PROFILE_IMAGE_SCHEMA_NAME, df_value=export_df, extension='csv')        
    return export_df 

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
                            wf_util.save_df(df_name=config.USER_PROFILE_IMAGE_SCHEMA_NAME, df_value=user_profile_df, extension='csv')                             
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
                        wf_util.save_df(df_name=config.USER_PROFILE_IMAGE_SCHEMA_NAME, df_value=user_profile_df, extension='csv')  
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
