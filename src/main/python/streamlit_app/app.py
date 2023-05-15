import base64
import io
import os
import altair as alt
import config
import console
import datagencars.evaluation.rs_surprise.surprise_helpers as surprise_helpers
import datagencars.evaluation.sklearn_helpers as sklearn_helpers
import datagencars.existing_dataset.binary_ratings as binary_ratings
import datagencars.existing_dataset.label_encoding as label_encoding
import datagencars.existing_dataset.mapping_categorization as mapping_categorization
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_rating import ExtractStatisticsRating
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_uic import ExtractStatisticsUIC
from datagencars.generate_user_profile.generate_user_profile_dataset import GenerateUserProfileDataset
from datagencars.existing_dataset.replicate_dataset.replicate_dataset import ReplicateDataset
from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.rating_explicit import RatingExplicit
from streamlit_app import util
from workflow.graph_generate import Workflow


# Setting the main page:
st.set_page_config(page_title='AUTO-DataGenCARS',
                   page_icon=config.AUTO_DATAGENCARS_ICON,
                   layout="centered", # "centered", "wide"
                   initial_sidebar_state="auto", # "expanded", "auto", "collapsed"
                   menu_items= None)

# Description, title and icon:
st.markdown("""---""")
col1, col2 = st.columns(2)
with col1:
    # Title:
    st.header('AUTO-DataGenCARS')
    # Description:
    st.write('It is a complete Python-based synthetic dataset generator for the evaluation of Context-Aware Recommendation Systems (CARS) to obtain the required datasets for any type of scenario desired.')
with col2:    
    # Icon:
    st.image(image=config.AUTO_DATAGENCARS_ICON, use_column_width=False, output_format="auto", width=180)
st.markdown("""---""")

# Tool bar:
general_option = st.sidebar.selectbox(label='**Options available:**', options=['Select one option', 'Generate a synthetic dataset', 'Pre-process a dataset', 'Analysis a dataset'])
with_context = st.sidebar.checkbox('With context', value=True)
wf = Workflow( config.WORKFLOWS_DESCRIPTION)

####### Generate a synthetic dataset #######
if general_option == 'Generate a synthetic dataset':
    init_step = 'True'
    feedback_option_radio = st.sidebar.radio(label='Select a type of user feedback:', options=['Explicit ratings', 'Implicit ratings'])
    if feedback_option_radio == 'Explicit ratings':
        feedback = 'explicit'
        with st.expander(label='Help information'):
            st.markdown("""Workflow to generate a completely-synthetic dataset based on explicit ratings.""")
        with st.expander(label='Workflow'):
            json_opt_params = {}
            json_opt_params['CARS'] = str(with_context)
            json_opt_params['UP'] = 'Manual'
            json_opt_params['init_step'] = init_step
            path = wf.create_workflow('GenerateSyntheticDataset(Explicit_ratings)', json_opt_params)            
            st.image(image=path, use_column_width=False, output_format="auto", width=650)  
            os.remove(path)      
        inconsistent = False
        # AVAILABLE TABS:
        if with_context:
            context = True
            tab_generation, tab_user, tab_item, tab_context, tab_user_profile, tab_run  = st.tabs(['Generation', 'Users', 'Items', 'Contexts', 'User profile', 'Run'])
        else:
            context = False
            tab_generation, tab_user, tab_item, tab_user_profile, tab_run = st.tabs(['Generation', 'Users', 'Items', 'User profile', 'Run'])
        # GENERATION SETTING TAB:
        with_correlation_checkbox = False
        with tab_generation:
            st.header('Generation')
            # Uploading the file: "generation_config.conf"
            generation_config_value = ''
            if is_upload_generation := st.checkbox('Upload the data generation configuration file', value=True, key='is_upload_generation'):    
                with st.expander(f"Upload generation_config.conf"):
                    if generation_config_file := st.file_uploader(label='Choose the file:', key='generation_config_file'):
                        generation_config_value = generation_config_file.getvalue().decode("utf-8")                
            else:
                # Generating the file: "generation_config.conf"
                # [dimension]
                st.write('General configuration')
                dimension_value = '[dimension] \n'
                user_count = st.number_input(label='Number of users to generate:', value=0)
                item_count = st.number_input(label='Number of items to generate:', value=0)
                if context:
                    context_count = st.number_input(label='Number of contexts to generate:', value=0)
                    dimension_value += ('number_user=' + str(user_count) + '\n' +
                                        'number_item=' + str(item_count) + '\n' +
                                        'number_context=' + str(context_count) + '\n')
                else:            
                    dimension_value = ('number_user=' + str(user_count) + '\n' +
                                    'number_item=' + str(item_count) + '\n')
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
                generation_config_value = dimension_value + '\n' + rating_value + '\n' + item_profile_value
            # Edit file:
            with st.expander(f"Show generation_config.conf"):
                if edit_config_file := st.checkbox(label='Edit file?', key='edit_config_file'):
                    config_file_text_area = st.text_area(label='Current file:', value=generation_config_value, height=500)
                else:               
                    config_file_text_area = st.text_area(label='Current file:', value=generation_config_value, height=500, disabled=True)    
            link_generation_config = f'<a href="data:text/plain;base64,{base64.b64encode(config_file_text_area.encode()).decode()}" download="generation_config.conf">Download</a>'
            st.markdown(link_generation_config, unsafe_allow_html=True)                                
        # USER TAB:
        with tab_user:        
            st.header('Users')
            schema_type = 'user'
            user_schema_value = util.generate_schema_file(schema_type)
        # ITEM TAB:
        with tab_item:
            st.header('Items')
            schema_type = 'item'
            item_schema_value = util.generate_schema_file(schema_type)
            st.markdown("""---""")
            # Item profile:
            item_profile_value = ''
            item_profile_text_area = ''  
            if is_upload_item_profile := st.checkbox('Upload the item profile file', value=True, key='is_upload_item_profile'):
                with st.expander("Upload item_profile.conf"):
                    if item_profile_file := st.file_uploader(label='Choose the file:', key='item_profile_file'):
                        item_profile_value = item_profile_file.getvalue().decode("utf-8")
            else:
                # [global]   
                item_profile_value += '[global]'+'\n'
                number_profiles = st.number_input(label='Number of profiles to generate:', value=3, key='number_profiles')
                item_profile_value += 'number_profiles='+str(number_profiles)+'\n'
                item_profile_value += '\n'
                # [name]
                item_profile_value += '[name]'+'\n'
                pn_text_area = st.empty()                        
                profile_name_text_area = pn_text_area.text_area(label='Introduce item profile values to the list (split by comma): good, normal, bad', key='profile_name_text_area')
                pn_possible_value_list = profile_name_text_area.split(',')            
                for i, item_profile_name in enumerate(pn_possible_value_list):
                    item_profile_value += 'name_profile_'+str(i+1)+'='+str(item_profile_name).strip()+'\n'
                item_profile_value += '\n'
                # [order]
                item_profile_value += '[order]'+'\n'            
                st.write('Examples of importance order:')
                st.markdown("""- ascending: ``` quality food=[bad, normal, good] ``` """)
                st.markdown("""- descending: ``` quality food=[good, normal, bad] ``` """)
                ranking_order_original = st.selectbox(label='Select an order of importance?', options=['descending', 'ascending'])
                if ranking_order_original == 'ascending':
                    ranking_order_profile = 'asc'
                elif ranking_order_original == 'descending':
                    ranking_order_profile = 'desc'
                item_profile_value += 'ranking_order_profile='+str(ranking_order_profile)+'\n'
                item_profile_value += '\n'
                # [overlap]
                item_profile_value += '[overlap]'+'\n'            
                overlap_midpoint_left_profile = st.number_input(label='Overlapping at the midpoint on the left:', value=1, key='overlap_midpoint_left_profile')
                overlap_midpoint_right_profile = st.number_input(label='Overlapping at the midpoint on the right:', value=1, key='overlap_midpoint_right_profile')
                st.markdown(
                """ 
                ```python
                # Example 1: overlapping at the midpoint on the left and the right
                item_profile_names = ['bad', 'normal', 'good'] 
                overlap_midpoint_left_profile = 0 
                overlap_midpoint_right_profile = 0 
                good_profile =   ['good'] 
                normal_profile =   ['normal'] 
                bad_profile =   ['bad'] 
                ``` 
                """)
                st.markdown(""" 
                ```python
                # Example 2: overlapping at the midpoint on the left and the right
                item_profile_names = ['bad', 'normal', 'good']
                overlap_midpoint_left_profile = 1
                overlap_midpoint_right_profile = 1
                good_item_profile =   ['good']
                normal_item_profile =   ['bad', 'normal', 'good']
                bad_item_profile =   ['bad']
                ``` 
                """)
                item_profile_value += 'overlap_midpoint_left_profile='+str(overlap_midpoint_left_profile)+'\n'
                item_profile_value += 'overlap_midpoint_right_profile='+str(overlap_midpoint_right_profile)+'\n'
                item_profile_value += '\n'            
            # Show generated schema file:
            with st.expander("Show item_profile.conf"):
                iprof_text_area = st.empty()
                if st.checkbox(label='Edit file?', key='edit_item_profile'):
                    item_profile_text_area = iprof_text_area.text_area(label='Current file:', value=item_profile_value, height=500, key='item_profile_text_area')
                else:
                    item_profile_text_area = iprof_text_area.text_area(label='Current file:', value=item_profile_value, height=500, disabled=True, key='item_profile_text_area')
            link_item_profile = f'<a href="data:text/plain;base64,{base64.b64encode(item_profile_text_area.encode()).decode()}" download="item_profile.conf">Download</a>'
            st.markdown(link_item_profile, unsafe_allow_html=True)          
        # CONTEXT TAB:
        if with_context:
            with tab_context:
                st.header('Contexts')
                schema_type = 'context'
                context_schema_value = util.generate_schema_file(schema_type) 
        # USER PROFILE TAB:
        with tab_user_profile:
            st.header('User profile')        
            user_profile_df = None
            if st.checkbox(label='Import the user profile?', value=True):
                with st.expander(label='Upload user_profile.csv'):
                    if user_profile_file := st.file_uploader(label='Choose the file:', key='user_profile_file'):
                        user_profile_value = user_profile_file.getvalue().decode("utf-8")
                        user_profile_df = pd.read_csv(io.StringIO(user_profile_value))  
                        st.dataframe(user_profile_df)                    
            else:
                # Adding column "id":
                attribute_column_list = ['user_profile_id']
                # Adding relevant item attribute columns:        
                item_access_schema = AccessSchema(file_str=item_schema_value)
                attribute_column_list.extend(item_access_schema.get_important_attribute_name_list())        
                # Adding relevant context attribute columns:    
                if with_context:
                    context_access_schema = AccessSchema(file_str=context_schema_value)
                    attribute_column_list.extend(context_access_schema.get_important_attribute_name_list())
                # Adding column "other":
                attribute_column_list.extend(['other'])
                with st.expander(label='Help information'):
                    st.write('Insert weight values in the user profile matrix, considering the following:')            
                    st.markdown("""* First of all, you will have to specify the ```number of user profiles``` to be generated. """)
                    st.markdown("""* The user profile matrix consists of relevant attribute names related to the items and/or contexts. """)
                    st.markdown("""* The values of the user profile matrix must have values between ```[0-1]```. Except column ```user_profile_id``` which must be an ```integer``` value and start at ```1```. """)
                    st.markdown("""* Attributes that are not relevant for the user profile must have a ```weight=0```. """)
                    st.markdown("""* Each row of the user profile matrix must sum to ```1```. """)
                    st.markdown("""* In the ```row``` and ```column``` input fields, you must indicate the row index and the column attribute name (respectively), where the user's relevance weight will be inserted through the ```weight``` field. """)            
                    st.markdown("""* In the ```weight``` input field, you must indicate the order and weight of importance of each attribute. For example:  ```(-)|0.1``` or ```(+)|0.1)```. """)                
                    st.markdown(
                    """
                    * Weights may be associated with symbols or labels ```(-)``` and ```(+)```, which indicate the order of preference of attribute values for that user profile. The ```(-)``` label must indicate that the order of preference of the attribute values is from left to right, while the ```(+)``` label indicates the reverse order of preference (from right to left). For example, for the attribute ```distance``` and possible values ```[near, fear]```: 
                    * **Example 1:** If the user indicates the label ``(-)``, it means that he/she prefers recommendations of nearby places (because he/she does not have a car or a bicycle or a bus as a means of transport to go to distant places).
                    * **Example 2:** If the user indicates the label ``(+)``, it means that he does not mind receiving recommendations from places far away from him/ (because he has a car as a means of transport to go to distant places).
                    """)
                    st.markdown(
                    """
                    * The special attribute ```other``` represents unknown factors or noise. This allows modelling realistic scenarios where user profiles are not fully defined. For example:
                    * **Example 1:** The user with ```user_profile_id=2```,  with a ```weight=0.2``` in the attribute ```other```, considers that ```20%``` of the ratings provided by the user of that profile, is due to unknown factors. 
                    * **Example 2:** The user with ```user_profile_id=3```, with a ```weight=1``` in the attribute ```other```, represents users who behave in a completely unpredictable way. This is because the ratings provided by users cannot be explained by any of the attributes that define the user profile. """)
                    st.write('Example of user profile matrix:')
                    st.image(image=config.USER_PROFILE, use_column_width=True, output_format="auto") # , width=350            
                # Introducing the number of user profiles to generate:            
                user_access = AccessSchema(file_str=user_schema_value)
                initial_value = len(user_access.get_possible_values_attribute_list_from_name(attribute_name='user_profile_id'))
                number_user_profile = st.number_input(label='Number of user profiles', value=initial_value)
                # Randomly fill a dataframe and cache it
                weight_np = np.zeros(shape=(number_user_profile, len(attribute_column_list)), dtype=str)
                @st.cache(allow_output_mutation=True)
                def get_dataframe():
                    df = pd.DataFrame(weight_np, columns=attribute_column_list)
                    for column in df.columns:
                        df[column] = 0
                    df['user_profile_id'] = df.index+1
                    df['other'] = 1
                    df = df.astype(str)
                    # user_profile_id_list = list(range(1, number_user_profile+1))
                    # df['user_profile_id'] = user_profile_id_list
                    return df            
                user_profile_df = get_dataframe()
                export_df = user_profile_df.copy()
                # Create row, column, and value inputs:
                col_row, col_col, col_val = st.columns(3)
                with col_row:
                    # Choosing the row index:
                    row = st.number_input('row (profile)', max_value=user_profile_df.shape[0]) #, value=1
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
                        item_possible_value_list = item_access_schema.get_possible_values_attribute_list_from_name(attribute_name=selected_attribute)                
                        if with_context:
                            context_possible_value_list = context_access_schema.get_possible_values_attribute_list_from_name(attribute_name=selected_attribute)
                            if (len(item_possible_value_list) != 0) and (len(context_possible_value_list) == 0):
                                st.warning(item_possible_value_list)
                            elif (len(item_possible_value_list) == 0) and (len(context_possible_value_list) != 0):
                                st.warning(context_possible_value_list)                   
                        else:
                            if (len(item_possible_value_list) != 0):
                                st.warning(item_possible_value_list)                    
                with col_val:   
                    # Inserting weight value:
                    value = st.text_input(label='weight (with range [-1,1])', value=0)      
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
                        other_value = float(other_value-abs(float(user_profile_df.values[row][attribute_column_list.index(column)])))
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
                st.markdown(""" Please, note that the ```user_profile_id``` column must start at ```1```, while the rest of values must be in the range ```[-1,1]```.""")
                st.dataframe(user_profile_df)
                # Downloading user_profile.csv:
                if not inconsistent:
                    link_user_profile = f'<a href="data:file/csv;base64,{base64.b64encode(export_df.to_csv(index=False).encode()).decode()}" download="user_profile.csv">Download</a>'
                    st.markdown(link_user_profile, unsafe_allow_html=True)
        # RUN TAB:
        with tab_run:                   
            col_run, col_stop = st.columns(2)        
            with col_run:
                button_run = st.button(label='Run', key='button_run')
            with col_stop:
                button_stop = st.button(label='Stop', key='button_stop')        
            generator = RatingExplicit(generation_config=generation_config_value)
            output = st.empty()
            with console.st_log(output.code):
                if not inconsistent:
                    if button_run:
                        if context:
                            steps = 4
                        else: 
                            steps = 3
                        current_step = 0
                        print('Starting execution')
                        # Check if all the files required for the synthetic data generation exist.                    
                        # Checking the existence of the file: "user_schema.conf"  
                        progress_text = f'Generating data .....step {current_step + 1} from {steps}'
                        my_bar = st.progress(0, text=progress_text)
                        if user_schema_value:
                            st.write('user.csv')
                            print('Generating user.csv')           
                            user_file_df = generator.generate_user_file(user_schema=user_schema_value)                           
                            st.dataframe(user_file_df)
                            link_user = f'<a href="data:file/csv;base64,{base64.b64encode(user_file_df.to_csv(index=False).encode()).decode()}" download="user.csv">Download user CSV</a>'
                            st.markdown(link_user, unsafe_allow_html=True)              
                        else:
                            st.warning('The user schema file (user_schema.conf) is required.')
                        current_step = current_step + 1
                        if button_stop:
                            st.experimental_rerun()
                        else:
                            # Checking the existence of the file: "item_schema.conf"            
                            my_bar.progress(int(100/steps)*current_step, f'Generating data Step {current_step + 1} from {steps}: ')
                            if item_schema_value:
                                st.write('item.csv')
                                print('Generating item.csv')                    
                                item_file_df = generator.generate_item_file(item_schema=item_schema_value, item_profile=item_profile_value, with_correlation=with_correlation_checkbox)
                                st.dataframe(item_file_df)   
                                link_item = f'<a href="data:file/csv;base64,{base64.b64encode(item_file_df.to_csv(index=False).encode()).decode()}" download="item.csv">Download item CSV</a>'
                                st.markdown(link_item, unsafe_allow_html=True)
                                current_step = current_step + 1
                            else:
                                st.warning('The item schema file (item_schema.conf) is required.')
                            my_bar.progress(int(100/steps*current_step), f'Generating data Step {current_step + 1} from {steps}: ')
                            if button_stop:
                                st.experimental_rerun()
                            else:
                                if context:
                                    # Checking the existence of the file: "context_schema.conf"                             
                                    if context_schema_value:
                                        st.write('context.csv')
                                        print('Generating context.csv')                        
                                        context_file_df = generator.generate_context_file(context_schema=context_schema_value)
                                        st.dataframe(context_file_df)
                                        link_context = f'<a href="data:file/csv;base64,{base64.b64encode(context_file_df.to_csv(index=False).encode()).decode()}" download="context.csv">Download context CSV</a>'
                                        st.markdown(link_context, unsafe_allow_html=True)
                                        current_step = current_step + 1
                                    else:
                                        st.warning('The context schema file (context_schema.conf) is required.')               
                                # Checking the existence of the file: "generation_config.conf" 
                                my_bar.progress(int(100/steps*current_step), f'Generating data Step {current_step + 1} from {steps}: ')
                                if button_stop:
                                    st.experimental_rerun()
                                else:
                                    if config_file_text_area:
                                        st.write('rating.csv')
                                        print('Generating rating.csv')           
                                        if with_context:
                                            rating_file_df = generator.generate_rating_file(user_df=user_file_df, user_profile_df=user_profile_df, item_df=item_file_df, item_schema=item_schema_value, with_context=with_context, context_df=context_file_df, context_schema=context_schema_value)        
                                        else:
                                            rating_file_df = generator.generate_rating_file(user_df=user_file_df, user_profile_df=user_profile_df, item_df=item_file_df, item_schema=item_schema_value)
                                        st.dataframe(rating_file_df)
                                        link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(rating_file_df.to_csv(index=False).encode()).decode()}" download="rating.csv">Download rating CSV</a>'
                                        st.markdown(link_rating, unsafe_allow_html=True)
                                    else:
                                        st.warning('The configuration file (generation_config.conf) is required.')
                                    print('Synthetic data generation has finished.')   
                                    my_bar.progress(100, 'Synthetic data generation has finished.')    
                else:
                    st.warning('Before generating data ensure all files are correctly generated.')
    elif feedback_option_radio == 'Implicit ratings':
        if with_context:
            lars = st.sidebar.checkbox('LARS', value=True)
            if lars:
                side_lars = st.sidebar.checkbox('SocIal-Distance prEserving', value=True)
        feedback = 'implicit'
        with st.expander(label='Help information'):
            st.markdown("""Workflow to generate a completely-synthetic dataset based on implicit ratings.""")
        with st.expander(label='Workflow'):
            json_opt_params = {}
            json_opt_params['CARS'] = str(with_context)
            json_opt_params['UP'] = 'Manual'
            json_opt_params['init_step'] = init_step
            path = wf.create_workflow('GenerateSyntheticDataset(Implicit_ratings)', json_opt_params)            
            st.image(image=path, use_column_width=False, output_format="auto", width=650)  
            os.remove(path)      
        inconsistent = False
        # AVAILABLE TABS:
        if with_context and lars and side_lars:
            context = True
            tab_generation, tab_user, tab_item, tab_context, tab_behavior, tab_run  = st.tabs(['Generation', 'Users', 'Items', 'Contexts', 'Behavior', 'Run'])
            # GENERATION SETTING TAB:
            generation_config_value = util.generation_settings(tab_generation)
            # with_correlation_checkbox = False
            # with tab_generation:
            #     st.header('Generation')
            #     # Uploading the file: "generation_config.conf"
            #     generation_config_value = ''
            #     if is_upload_generation := st.checkbox('Upload the data generation configuration file', value=True, key='is_upload_generation'):    
            #         with st.expander(f"Upload generation_config.conf"):
            #             if generation_config_file := st.file_uploader(label='Choose the file:', key='generation_config_file'):
            #                 generation_config_value = generation_config_file.getvalue().decode("utf-8")
            #     else:
            #         # Generating the file: "generation_config.conf"
            #         # [dimension]
            #         st.write('General configuration')
            #         dimension_value = '[dimension] \n'
            #         user_count = st.number_input(label='Number of users to generate:', value=0)
            #         item_count = st.number_input(label='Number of items to generate:', value=0)
            #         context_count = st.number_input(label='Number of contexts to generate:', value=0)

            #         dimension_value += ('number_user=' + str(user_count) + '\n' +
            #                             'number_item=' + str(item_count) + '\n' +
            #                             'number_context=' + str(context_count) + '\n')
            #         st.markdown("""---""")

            #         # [behavior]
            #         st.write('Behavior configuration')
            #         behavior_value = '[behavior] \n'
            #         number_behavior = st.number_input(label='Number of behaviors:', value=0)
            #         session_time = st.number_input(label='Session time (seconds):', value=3600)
            #         min_interval_behavior = st.number_input(label='Minimum interval between behaviors (seconds):', value=1)
            #         max_interval_behavior = st.number_input(label='Maximum interval between behaviors (seconds):', value=300)
            #         min_radius = st.number_input(label='Minimum radius:', value=1)
            #         max_radius = st.number_input(label='Maximum radius:', value=5)
            #         door = st.text_input(label='Door:', value='0, 5, 5')
            #         interaction_threshold = st.number_input(label='Interaction threshold:', value=2.5)

            #         behavior_value += ('number_behavior=' + str(number_behavior) + '\n' +
            #                         'session_time=' + str(session_time) + '\n' +
            #                         'minimum_interval_behavior=' + str(min_interval_behavior) + '\n' +
            #                         'maximum_interval_behavior=' + str(max_interval_behavior) + '\n' +
            #                         'minimum_radius=' + str(min_radius) + '\n' +
            #                         'maximum_radius=' + str(max_radius) + '\n' +
            #                         'door=[' + door + ']\n' +
            #                         'interaction_threshold=' + str(interaction_threshold) + '\n')
            #         st.markdown("""---""")

            #         # [rating]
            #         st.write('Rating configuration')
            #         rating_value = '[rating] \n'
            #         rating_min = st.number_input(label='Minimum value of the ratings:', value=0)
            #         rating_max = st.number_input(label='Maximum value of the ratings:', value=1)
            #         min_year_ts = st.date_input(label='From:', value=date(2023, 1, 1))
            #         max_year_ts = st.date_input(label='Until:', value=date(2023, 4, 1))

            #         rating_value += ('minimum_value_rating=' + str(rating_min) + '\n' +
            #                         'maximum_value_rating=' + str(rating_max) + '\n' +
            #                         'minimum_date_timestamp=' + str(min_year_ts) + '\n' +
            #                         'maximum_date_timestamp=' + str(max_year_ts) + '\n')
            #         st.markdown("""---""")

            #         # [item profile]
            #         st.write('Item profile configuration')
            #         item_profile_value = '[item profile] \n'
            #         probability_percentage_profile_1 = st.number_input(label='Profile probability percentage 1:', value=10)
            #         probability_percentage_profile_2 = st.number_input(label='Profile probability percentage 2:', value=30)
            #         probability_percentage_profile_3 = st.number_input(label='Profile probability percentage 3:', value=60)
            #         noise_percentage_profile_1 = st.number_input(label='Profile noise percentage 1:', value=20)
            #         noise_percentage_profile_2 = st.number_input(label='Profile noise percentage2:', value=20)
            #         noise_percentage_profile_3 = st.number_input(label='Profile noise percentage 3:', value=20)

            #         item_profile_value += ('probability_percentage_profile_1=' + str(probability_percentage_profile_1) + '\n' +
            #         'probability_percentage_profile_2=' + str(probability_percentage_profile_2) + '\n' +
            #         'probability_percentage_profile_3=' + str(probability_percentage_profile_3) + '\n' +
            #         'noise_percentage_profile_1=' + str(noise_percentage_profile_1) + '\n' +
            #         'noise_percentage_profile_2=' + str(noise_percentage_profile_2) + '\n' +
            #         'noise_percentage_profile_3=' + str(noise_percentage_profile_3) + '\n')
            #         st.markdown("""---""")

            #         # Generate the configuration file
            #         generation_config_value = dimension_value + '\n' + behavior_value + '\n' + rating_value + '\n' + item_profile_value
            #     # Edit file:
            #     with st.expander(f"Show generation_config.conf"):
            #         if edit_config_file := st.checkbox(label='Edit file?', key='edit_config_file'):
            #             config_file_text_area = st.text_area(label='Current file:', value=generation_config_value, height=500)
            #         else:               
            #             config_file_text_area = st.text_area(label='Current file:', value=generation_config_value, height=500, disabled=True)    
            #     link_generation_config = f'<a href="data:text/plain;base64,{base64.b64encode(config_file_text_area.encode()).decode()}" download="generation_config.conf">Download</a>'
            #     st.markdown(link_generation_config, unsafe_allow_html=True)
            # USER TAB:
            with tab_user:        
                st.header('Users')
                schema_type = 'user'
                user_schema_value = util.generate_schema_file(schema_type)
            # ITEM TAB:
            with tab_item:
                st.header('Items')
                schema_type = 'item'
                item_schema_value = util.generate_schema_file(schema_type)
                st.markdown("""---""")
                # Item profile:
                item_profile_value = ''
                item_profile_text_area = ''  
                if is_upload_item_profile := st.checkbox('Upload the item profile file', value=True, key='is_upload_item_profile'):
                    with st.expander("Upload item_profile.conf"):
                        if item_profile_file := st.file_uploader(label='Choose the file:', key='item_profile_file'):
                            item_profile_value = item_profile_file.getvalue().decode("utf-8")
                else:
                    # [global]   
                    item_profile_value += '[global]'+'\n'
                    number_profiles = st.number_input(label='Number of profiles to generate:', value=3, key='number_profiles')
                    item_profile_value += 'number_profiles='+str(number_profiles)+'\n'
                    item_profile_value += '\n'
                    # [name]
                    item_profile_value += '[name]'+'\n'
                    pn_text_area = st.empty()                        
                    profile_name_text_area = pn_text_area.text_area(label='Introduce item profile values to the list (split by comma): good, normal, bad', key='profile_name_text_area')
                    pn_possible_value_list = profile_name_text_area.split(',')            
                    for i, item_profile_name in enumerate(pn_possible_value_list):
                        item_profile_value += 'name_profile_'+str(i+1)+'='+str(item_profile_name).strip()+'\n'
                    item_profile_value += '\n'
                    # [order]
                    item_profile_value += '[order]'+'\n'            
                    st.write('Examples of importance order:')
                    st.markdown("""- ascending: ``` quality food=[bad, normal, good] ``` """)
                    st.markdown("""- descending: ``` quality food=[good, normal, bad] ``` """)
                    ranking_order_original = st.selectbox(label='Select an order of importance?', options=['descending', 'ascending'])
                    if ranking_order_original == 'ascending':
                        ranking_order_profile = 'asc'
                    elif ranking_order_original == 'descending':
                        ranking_order_profile = 'desc'
                    item_profile_value += 'ranking_order_profile='+str(ranking_order_profile)+'\n'
                    item_profile_value += '\n'
                    # [overlap]
                    item_profile_value += '[overlap]'+'\n'            
                    overlap_midpoint_left_profile = st.number_input(label='Overlapping at the midpoint on the left:', value=1, key='overlap_midpoint_left_profile')
                    overlap_midpoint_right_profile = st.number_input(label='Overlapping at the midpoint on the right:', value=1, key='overlap_midpoint_right_profile')
                    st.markdown(
                    """ 
                    ```python
                    # Example 1: overlapping at the midpoint on the left and the right
                    item_profile_names = ['bad', 'normal', 'good'] 
                    overlap_midpoint_left_profile = 0 
                    overlap_midpoint_right_profile = 0 
                    good_profile =   ['good'] 
                    normal_profile =   ['normal'] 
                    bad_profile =   ['bad'] 
                    ``` 
                    """)
                    st.markdown(""" 
                    ```python
                    # Example 2: overlapping at the midpoint on the left and the right
                    item_profile_names = ['bad', 'normal', 'good']
                    overlap_midpoint_left_profile = 1
                    overlap_midpoint_right_profile = 1
                    good_item_profile =   ['good']
                    normal_item_profile =   ['bad', 'normal', 'good']
                    bad_item_profile =   ['bad']
                    ``` 
                    """)
                    item_profile_value += 'overlap_midpoint_left_profile='+str(overlap_midpoint_left_profile)+'\n'
                    item_profile_value += 'overlap_midpoint_right_profile='+str(overlap_midpoint_right_profile)+'\n'
                    item_profile_value += '\n'            
                # Show generated schema file:
                with st.expander("Show item_profile.conf"):
                    iprof_text_area = st.empty()
                    if st.checkbox(label='Edit file?', key='edit_item_profile'):
                        item_profile_text_area = iprof_text_area.text_area(label='Current file:', value=item_profile_value, height=500, key='item_profile_text_area')
                    else:
                        item_profile_text_area = iprof_text_area.text_area(label='Current file:', value=item_profile_value, height=500, disabled=True, key='item_profile_text_area')
                link_item_profile = f'<a href="data:text/plain;base64,{base64.b64encode(item_profile_text_area.encode()).decode()}" download="item_profile.conf">Download</a>'
                st.markdown(link_item_profile, unsafe_allow_html=True)
            # CONTEXT TAB:
            if with_context:
                with tab_context:
                    st.header('Contexts')
                    schema_type = 'context'
                    context_schema_value = util.generate_schema_file(schema_type) 
            # BEHAVIOR TAB:
            with tab_behavior:
                st.header('Behaviors')
                schema_type = 'behavior'
                context_schema_value = util.generate_schema_file(schema_type) 
            # RUN TAB:
            with tab_run:                   
                col_run, col_stop = st.columns(2)        
                with col_run:
                    button_run = st.button(label='Run', key='button_run')
                with col_stop:
                    button_stop = st.button(label='Stop', key='button_stop')        
                generator = RatingExplicit(generation_config=generation_config_value)
                output = st.empty()
                with console.st_log(output.code):
                    if not inconsistent:
                        if button_run:
                            if context:
                                steps = 4
                            else: 
                                steps = 3
                            current_step = 0
                            print('Starting execution')
                            # Check if all the files required for the synthetic data generation exist.                    
                            # Checking the existence of the file: "user_schema.conf"  
                            progress_text = f'Generating data .....step {current_step + 1} from {steps}'
                            my_bar = st.progress(0, text=progress_text)
                            if user_schema_value:
                                st.write('user.csv')
                                print('Generating user.csv')           
                                user_file_df = generator.generate_user_file(user_schema=user_schema_value)                           
                                st.dataframe(user_file_df)
                                link_user = f'<a href="data:file/csv;base64,{base64.b64encode(user_file_df.to_csv(index=False).encode()).decode()}" download="user.csv">Download user CSV</a>'
                                st.markdown(link_user, unsafe_allow_html=True)              
                            else:
                                st.warning('The user schema file (user_schema.conf) is required.')
                            current_step = current_step + 1
                            if button_stop:
                                st.experimental_rerun()
                            else:
                                # Checking the existence of the file: "item_schema.conf"            
                                my_bar.progress(int(100/steps)*current_step, f'Generating data Step {current_step + 1} from {steps}: ')
                                if item_schema_value:
                                    st.write('item.csv')
                                    print('Generating item.csv')                    
                                    item_file_df = generator.generate_item_file(item_schema=item_schema_value, item_profile=item_profile_value, with_correlation=with_correlation_checkbox)
                                    st.dataframe(item_file_df)   
                                    link_item = f'<a href="data:file/csv;base64,{base64.b64encode(item_file_df.to_csv(index=False).encode()).decode()}" download="item.csv">Download item CSV</a>'
                                    st.markdown(link_item, unsafe_allow_html=True)
                                    current_step = current_step + 1
                                else:
                                    st.warning('The item schema file (item_schema.conf) is required.')
                                my_bar.progress(int(100/steps*current_step), f'Generating data Step {current_step + 1} from {steps}: ')
                                if button_stop:
                                    st.experimental_rerun()
                                else:
                                    if context:
                                        # Checking the existence of the file: "context_schema.conf"                             
                                        if context_schema_value:
                                            st.write('context.csv')
                                            print('Generating context.csv')                        
                                            context_file_df = generator.generate_context_file(context_schema=context_schema_value)
                                            st.dataframe(context_file_df)
                                            link_context = f'<a href="data:file/csv;base64,{base64.b64encode(context_file_df.to_csv(index=False).encode()).decode()}" download="context.csv">Download context CSV</a>'
                                            st.markdown(link_context, unsafe_allow_html=True)
                                            current_step = current_step + 1
                                        else:
                                            st.warning('The context schema file (context_schema.conf) is required.')               
                                    # Checking the existence of the file: "generation_config.conf" 
                                    my_bar.progress(int(100/steps*current_step), f'Generating data Step {current_step + 1} from {steps}: ')
                                    if button_stop:
                                        st.experimental_rerun()
                                    else:
                                        if config_file_text_area:
                                            st.write('rating.csv')
                                            print('Generating rating.csv')           
                                            if with_context:
                                                rating_file_df = generator.generate_rating_file(user_df=user_file_df, user_profile_df=user_profile_df, item_df=item_file_df, item_schema=item_schema_value, with_context=with_context, context_df=context_file_df, context_schema=context_schema_value)        
                                            else:
                                                rating_file_df = generator.generate_rating_file(user_df=user_file_df, user_profile_df=user_profile_df, item_df=item_file_df, item_schema=item_schema_value)
                                            st.dataframe(rating_file_df)
                                            link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(rating_file_df.to_csv(index=False).encode()).decode()}" download="rating.csv">Download rating CSV</a>'
                                            st.markdown(link_rating, unsafe_allow_html=True)
                                        else:
                                            st.warning('The configuration file (generation_config.conf) is required.')
                                        print('Synthetic data generation has finished.')   
                                        my_bar.progress(100, 'Synthetic data generation has finished.')    
                    else:
                        st.warning('Before generating data ensure all files are correctly generated.')
####### Pre-process a dataset #######
elif general_option == 'Pre-process a dataset':        
    st.header('Load dataset')
    # WORKFLOWS:
    is_preprocess = st.sidebar.radio(label='Select a workflow:', options=['Replicate dataset', 'Extend dataset', 'Recalculate ratings', 'Replace NULL values', 'Generate user profile', 'Ratings to binary', 'Mapping categorization'])
    if is_preprocess == 'Replicate dataset':
        init_step = 'True'
        if with_context:
            user_df, item_df, context_df, rating_df = util.load_dataset(file_type_list=['user', 'item', 'context', 'rating'])
            st.session_state["context_df"] = context_df
        else:
            user_df, item_df, __, rating_df = util.load_dataset(file_type_list=['user', 'item', 'rating'])      
        st.session_state["user_df"] = user_df
        st.session_state["item_df"] = item_df      
        st.session_state["rating_df"] = rating_df

        st.header('Apply workflow: Replicate dataset')
        with st.expander(label='Help information'):
            st.markdown("""Workflow to generate a synthetic dataset similar to an existing one.""")
        with st.expander(label='Workflow'):
            json_opt_params = {}
            json_opt_params['CARS'] = str(with_context)
            json_opt_params['NULLValues'] = 'True'
            json_opt_params['init_step'] = init_step
            path = wf.create_workflow('ReplicateDataset', json_opt_params)
            image = st.image(image=path, use_column_width=False, output_format="auto", width=650)  
            os.remove(path)
              
        tab_preprocessing, tab_user_profile, tab_replicate  = st.tabs(['Pre-processing', 'User Profile', 'Replicate'])   
        new_item_df = pd.DataFrame()
        new_context_df = pd.DataFrame()
        # PRE-PROCESSING TAB:  
        with tab_preprocessing:
            output = st.empty()  
            with console.st_log(output.code):
                null_values = st.checkbox("Do you want to replace the null values?", value=True)                
                if null_values:
                    json_opt_params = {}
                    json_opt_params['CARS'] = str(with_context)
                    json_opt_params['NULLValues'] = str(null_values)
                    json_opt_params['init_step'] = init_step
                    path = wf.create_workflow('ReplicateDataset', json_opt_params)
                    image.empty()
                    image.image(image=path, use_column_width=False, output_format="auto", width=650)  
                    os.remove(path)                    
                    # Pre-processs: replace null values:
                    if with_context:
                        if (not item_df.empty) and (not context_df.empty):                                        
                            file_type_selectbox = st.selectbox(label='Select a file type:', options=['item', 'context'])
                            if st.button(label='Replace', key='button_replace_item_context'):
                                if file_type_selectbox == 'item':
                                    # Check if item_df has NaN values:
                                    print(f'Checking if {file_type_selectbox}.csv has NaN values.')
                                    if item_df.isnull().values.any():        
                                        print(f'Replacing NaN values.')
                                        new_item_df = pd.DataFrame() # TODO
                                        print('The null values have been replaced.')
                                        with st.expander(label=f'Show replicated file: {file_type_selectbox}.csv'):
                                            st.dataframe(new_item_df)
                                            link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(new_item_df.to_csv(index=False).encode()).decode()}" download="{file_type_selectbox}.csv">Download</a>'
                                            st.markdown(link_rating, unsafe_allow_html=True)
                                    else:
                                        new_item_df = item_df.copy()
                                        st.warning(f'The {file_type_selectbox}.csv file has no null values.')
                                    st.session_state["item_df"] = new_item_df
                                elif file_type_selectbox == 'context':
                                    # Check if context_df has NaN values:
                                    print(f'Checking if {file_type_selectbox}.csv has NaN values')
                                    if context_df.isnull().values.any():
                                        print(f'Replacing NaN values.')
                                        new_context_df = pd.DataFrame() # TODO
                                        print('The null values have been replaced.')
                                        with st.expander(label=f'Show replicated file: {file_type_selectbox}.csv'):
                                            st.dataframe(new_context_df)
                                            link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(new_context_df.to_csv(index=False).encode()).decode()}" download="{file_type_selectbox}.csv">Download</a>'
                                            st.markdown(link_rating, unsafe_allow_html=True)
                                    else:
                                        new_context_df = context_df.copy()
                                        st.warning(f'The {file_type_selectbox}.csv file has no null values.')
                                    st.session_state["context_df"] = new_context_df
                        else:
                            st.warning("The item and context files have not been uploaded.")
                    else:
                        if not item_df.empty:                                        
                            file_type_selectbox = st.selectbox(label='Select a file type:', options=['item'])
                            if st.button(label='Replace', key='button_replace_item'):
                                # Check if item_df has NaN values:
                                print(f'Checking if {file_type_selectbox}.csv has NaN values')
                                if item_df.isnull().values.any():
                                    print(f'Replacing NaN values.')
                                    new_item_df = pd.DataFrame() # TODO
                                    print('The null values have been replaced.')
                                    with st.expander(label=f'Show replicated file: {file_type_selectbox}.csv'):
                                        st.dataframe(new_item_df)
                                        link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(new_item_df.to_csv(index=False).encode()).decode()}" download="{file_type_selectbox}.csv">Download</a>'
                                        st.markdown(link_rating, unsafe_allow_html=True)
                                else:
                                    new_item_df = item_df.copy()
                                    st.warning(f'The {file_type_selectbox}.csv file has no null values.')
                                st.session_state["item_df"] = new_item_df
                        else:
                            st.warning("The item file has not been uploaded.")
                else:
                    init_step = 'False'
                    json_opt_params = {}
                    json_opt_params['CARS'] = str(with_context)
                    json_opt_params['NULLValues'] = str(null_values)
                    json_opt_params['init_step'] = init_step
                    path = wf.create_workflow('ReplicateDataset', json_opt_params)
                    image.empty()
                    image.image(image=path, use_column_width=False, output_format="auto", width=650)
                    os.remove(path)                    
        # USER PROFILE TAB:
        with tab_user_profile:
            output = st.empty()
            with console.st_log(output.code):
                # Generate user profile, by using an original dataset:
                generate_up = None
                user_profile_df = pd.DataFrame()                    
                if with_context:                     
                    # With context:
                    if (not item_df.empty and "item_df" in st.session_state) and (not context_df.empty and "context_df" in st.session_state) and (not rating_df.empty and "rating_df" in st.session_state):
                        if st.button(label='Generate', key='button_generate_up_cars'):
                            print('Automatically generating user profiles.')
                            generate_up = GenerateUserProfileDataset(st.session_state["rating_df"], st.session_state["item_df"], st.session_state["context_df"])
                            user_profile_df = util.generate_up(generate_up)
                            st.session_state["user_profile_df"] = user_profile_df
                            print('The user profile has been generated.')                                                    
                    else:
                        st.warning("The item, context and rating files have not been uploaded.")
                else:            
                    # Without context:                        
                    if (not item_df.empty and "item_df" in st.session_state) and (not rating_df.empty and "rating_df" in st.session_state): 
                        if st.button(label='Generate', key='button_generate_up_rs'):
                            print('Automatically generating user profiles.')
                            generate_up = GenerateUserProfileDataset(st.session_state["rating_df"], st.session_state["item_df"])
                            user_profile_df = util.generate_up(generate_up)
                            st.session_state["user_profile_df"] = user_profile_df
                            print('The user profile has been generated.')                               
                    else:
                        st.warning("The item and rating files have not been uploaded.")
        # REPLICATE TAB:
        with tab_replicate:
                output = st.empty()
                with console.st_log(output.code):
                    percentage_rating_variation = st.number_input(label='Percentage of rating variation:', value=25, key='percentage_rating_variation_rs')
                    if with_context:                        
                        # With context:
                        if (not item_df.empty and "item_df" in st.session_state) and (not context_df.empty and "context_df" in st.session_state) and (not rating_df.empty and "rating_df" in st.session_state):
                            if st.button(label='Replicate', key='button_replicate_cars'):
                                print('Extracting statistics.')
                                print('Replicating the rating.csv file.')
                                replicate_cars = ReplicateDataset( st.session_state["rating_df"],  st.session_state["user_profile_df"], st.session_state["item_df"], st.session_state["context_df"])                            
                                new_rating_df = replicate_cars.replicate_dataset(percentage_rating_variation)
                                st.session_state["rating_df"] = new_rating_df
                                with st.expander(label='Show the replicated file: rating.csv'):
                                    st.dataframe(st.session_state["rating_df"])
                                    link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(st.session_state["rating_df"].to_csv(index=False).encode()).decode()}" download="rating.csv">Download</a>'
                                    st.markdown(link_rating, unsafe_allow_html=True) 
                                print('Replicated data generation has finished.')
                        else:
                            st.warning("The item, context and rating files have not been uploaded.")
                    else:            
                        # Without context:                        
                        if (not item_df.empty and "item_df" in st.session_state) and (not rating_df.empty and "rating_df" in st.session_state):                             
                            if st.button(label='Replicate', key='button_replicate_rs'):
                                print('Extracting statistics.')
                                print('Replicating the rating.csv file.')
                                replicate_cars = ReplicateDataset( st.session_state["rating_df"],  st.session_state["user_profile_df"], st.session_state["item_df"])                                
                                new_rating_df = replicate_cars.replicate_dataset(percentage_rating_variation)
                                st.session_state["rating_df"] = new_rating_df
                                with st.expander(label='Show the replicated file: rating.csv'):
                                    st.dataframe(st.session_state["rating_df"])
                                    link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(st.session_state["rating_df"].to_csv(index=False).encode()).decode()}" download="rating.csv">Download</a>'
                                    st.markdown(link_rating, unsafe_allow_html=True)
                                print('Replicated data generation has finished.')
                        else:
                            st.warning("The item and rating files have not been uploaded.")
    elif is_preprocess == 'Extend dataset':        
        _, _, _, rating_df = util.load_dataset(file_type_list=['rating'])
        st.header('Apply workflow: Extend dataset')
        with st.expander(label='Help information'):
            st.markdown("""Workflow to generate a dataset of ratings incrementally.""")
        with st.expander(label='Workflow'):            
            st.write('TODO')
        st.write('TODO')
    elif is_preprocess == 'Recalculate ratings':          
        _, _, _, rating_df = util.load_dataset(file_type_list=['rating'])
        st.header('Apply workflow: Recalculate ratings')
        with st.expander(label='Help information'):
            st.markdown("""TODO""")
        with st.expander(label='Workflow'):
            st.write('TODO')
        st.write('TODO')        
    elif is_preprocess == 'Replace NULL values':
        file_selectibox = st.selectbox(label='Files available:', options=['item', 'context'])
        if file_selectibox == 'item':
            _, df, _, _ = util.load_dataset(file_type_list=['item'])
        elif file_selectibox == 'context':
            _, _, df, _ = util.load_dataset(file_type_list=['context'])
        st.header('Apply workflow: Replace NULL values')
        with st.expander(label='Help information'):
            st.markdown("""Workflow to complete unknown contextual information.""")
        with st.expander(label='Workflow'):
            st.write('TODO')
        st.write('TODO')
    elif is_preprocess == 'Generate user profile':
        if with_context:
            user_df, item_df, context_df, rating_df = util.load_dataset(file_type_list=['user', 'item', 'context', 'rating'])
        else:
            user_df, item_df, rating_df = util.load_dataset(file_type_list=['user', 'item', 'rating'])
        st.header('Apply workflow: Generate user profile')
        with st.expander(label='Help information'):
            st.markdown("""TODO""")
        with st.expander(label='Workflow'):
            st.write('TODO')
        st.write('TODO')
    elif is_preprocess == 'Ratings to binary':        
        _, _, _, rating_df = util.load_dataset(file_type_list=['rating'])
        st.header('Apply workflow: Ratings to binary')        
        with st.expander(label='Help information'):
            st.markdown("""This tool allows you to convert ratings to binary values. For example, if you have a dataset with ratings from ```1``` to ```5```, you can convert them to ```0``` and ```1```, where ```0``` represents a negative rating and ```1``` a positive one.""")
            st.markdown("""The tool will convert the ratings to binary values using a threshold. For example, if you set the threshold to ```3```, all ratings equal or greater than ```3``` will be converted to ```1```, and all ratings less than ```3``` will be converted to ```0```.""")                    
        with st.expander(label='Workflow'):
            json_opt_params = {}
            path = wf.create_workflow('RatingsToBinary', json_opt_params)
            st.image(image=path, use_column_width=False, output_format="auto", width=650)  
            os.remove(path)      
        if not rating_df.empty:            
            min_rating = rating_df['rating'].min()
            max_rating = rating_df['rating'].max()
            threshold = st.number_input(f"Binary threshold (range from {min_rating} to {max_rating})", min_value=min_rating, max_value=max_rating, value=3)
            df_binary = util.ratings_to_binary(rating_df, threshold)
            st.write("Converted ratings:")
            st.dataframe(df_binary.head())
            link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(df_binary.to_csv(index=False).encode()).decode()}" download="rating.csv">Download rating CSV</a>'
            st.markdown(link_rating, unsafe_allow_html=True)
        else:            
            st.warning("The rating file has not been uploaded.")
    elif is_preprocess == 'Mapping categorization':
        file_selectibox = st.selectbox(label='Files available:', options=['user', 'item', 'context'])
        file = 'F'
        num2cat = 'T'
        init_step = 'True'
        if file_selectibox == 'user':
            df, _, _, _ = util.load_dataset(file_type_list=['user'])
            file = 'U'
        elif file_selectibox == 'item':
            _, df, _, _ = util.load_dataset(file_type_list=['item'])
            file = 'I'
        elif file_selectibox == 'context':
            _, _, df, _ = util.load_dataset(file_type_list=['context'])   
            file = 'C'
        st.header('Apply workflow: Mapping categorization')
        with st.expander(label='Help information'):
            st.write('TODO')
        with st.expander(label='Workflow'):
            json_opt_params = {}
            json_opt_params['CARS'] = str(with_context)
            json_opt_params['Num2Cat'] = num2cat
            json_opt_params['init_step'] = init_step
            json_opt_params['file'] = file
            path = wf.create_workflow('MappingToCategorization', json_opt_params)
            image = st.image(image=path, use_column_width=False, output_format="auto", width=650)  
            os.remove(path)      
        option = st.radio(options=['From numerical to categorical', 'From categorical to numerical'], label='Select an option')
        if not df.empty:
            if option == 'From numerical to categorical':
                init_step = 'False'
                num2cat = 'True'
                json_opt_params = {}
                json_opt_params['CARS'] = str(with_context)
                json_opt_params['Num2Cat'] = num2cat
                json_opt_params['init_step'] = init_step
                json_opt_params['file'] = file
                path = wf.create_workflow('MappingToCategorization', json_opt_params)
                image.empty()
                image.image(image=path, use_column_width=False, output_format="auto", width=600)  
                os.remove(path)                 
                st.header("Category Encoding")
                with st.expander(label='Help information'):
                    st.markdown("""This workflow allows you to convert numerical values to categorical values. For example, you can convert the numerical values of a rating scale to the corresponding categories of the scale (e.g. ```1-2 -> Bad```, ```3-4 -> Average```, ```5 -> Good```).""")
                    st.markdown("""To use this tool, you need to upload a CSV file containing the numerical values to convert. Then, you need to specify the mapping for each numerical value. For example, you could to specify the following mappings: numerical values ```1```, ```2```, ```3```, ```4``` and ```5``` to categories ```Bad```, ```Average```, ```Good```, ```Very good``` and ```Excellent```, respectively.""")
                    st.markdown("""Objects and datetime values are ignored.""")                    
                include_nan = st.checkbox("Include NaN values")
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
                if st.button("Generate mapping"):
                    categorized_df = mapping_categorization.apply_mappings(df, mappings)
                    st.header("Categorized dataset:")
                    st.dataframe(categorized_df)
                    link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(categorized_df.to_csv(index=False).encode()).decode()}" download="{file_selectibox}.csv">Download</a>'
                    st.markdown(link_rating, unsafe_allow_html=True)
            else:
                num2cat = 'False'
                init_step = 'False'
                json_opt_params = {}
                json_opt_params['CARS'] = str(with_context)
                json_opt_params['Num2Cat'] = num2cat
                json_opt_params['init_step'] = init_step
                json_opt_params['file'] = file
                path = wf.create_workflow('MappingToCategorization', json_opt_params)
                image.empty()
                image.image(image=path, use_column_width=False, output_format="auto", width=600)  
                os.remove(path)         
                st.header("Label Encoding")
                with st.expander(label='Help information'):
                    st.markdown("""This workflow allows you to convert categorical values into numerical values.""")
                    st.markdown("""For example, you can convert the categorical values of a rating scale to the corresponding numerical values of the scale (e.g. ```Bad -> 1```, ```Average -> 2```, ```Good -> 3```, ```Very good -> 4```, ```Excellent -> 5```).""")
                    st.markdown("""To use this tool, you need to upload a CSV file containing the categorical values to convert. Then, you need to select the categorical columns to convert.""")
                categorical_cols = [col for col in df.select_dtypes(exclude=[np.number]) if 'id' not in col.lower()]
                if categorical_cols:
                    selected_cols = st.multiselect("Select categorical columns to label encode:", categorical_cols)
                    if selected_cols:
                        if st.button("Encode categorical columns"):
                            encoded_df = label_encoding.apply_label_encoder(df, selected_cols)
                            st.header("Encoded dataset:")
                            st.write(encoded_df)
                            link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(encoded_df.to_csv(index=False).encode()).decode()}" download="{file_selectibox}.csv">Download</a>'
                            st.markdown(link_rating, unsafe_allow_html=True)
                else:
                    st.write("No categorical columns found.")
        else:
            st.warning("The user, item or context file has not been uploaded.")

####### Analysis a dataset #######
elif general_option == 'Analysis a dataset':
    # LOAD DATASET:
    st.header('Load dataset')
    if with_context:
        user_df, item_df, context_df, rating_df = util.load_dataset(file_type_list=['user', 'item', 'context', 'rating'])
    else:
        user_df, item_df, __, rating_df = util.load_dataset(file_type_list=['user', 'item', 'rating'])
    if "lars" and "side_lars" in st.session_state:
        lars = st.session_state["lars"]
        side_lars = st.session_state["side_lars"]
        if lars and side_lars:
            behavior_df = util.load_one_file('behavior')
    is_analysis = st.sidebar.radio(label='Select one option:', options=['Visualization', 'Evaluation'])
    # VISUALIZATION:    
    if is_analysis == 'Visualization':
        st.header('Visualization')
        if with_context:
            user_tab, item_tab, context_tab, rating_tab = st.tabs(['Users', 'Items', 'Contexts', 'Ratings'])
        else:
            user_tab, item_tab, rating_tab = st.tabs(['Users', 'Items', 'Ratings'])   
        # Users tab:
        with user_tab:
            if not user_df.empty:
                try:
                    # User dataframe:
                    st.header("User file")
                    st.dataframe(user_df)                    
                    # Extracted statistics:
                    extract_statistics_user = ExtractStatisticsUIC(user_df)
                    # Missing values:
                    st.header("Missing values")
                    missing_values2 = extract_statistics_user.count_missing_values(replace_values={"NULL":np.nan,-1:np.nan})                    
                    st.table(missing_values2)                    
                    # Attributes, data types and value ranges:
                    st.header("Attributes, data types and value ranges")
                    table2 = extract_statistics_user.get_attributes_and_ranges()
                    st.table(pd.DataFrame(table2, columns=["Attribute name", "Data type", "Value ranges"]))
                    # Showing one figure by attribute:
                    st.header("Analysis by attribute")
                    col1, col2 = st.columns(2)
                    with col1:
                        user_attribute_list = user_df.columns.tolist()
                        user_attribute_list.remove('user_id')
                        column2 = st.selectbox("Select an attribute", user_attribute_list, key='column2')
                    with col2:
                        sort2 = st.selectbox('Sort', ['none', 'asc', 'desc'], key='sort2')
                    data2 = extract_statistics_user.column_attributes_count(column2)
                    util.plot_column_attributes_count(data2, column2, sort2)
                    # Showing extracted statistics:
                    st.header("Extracted statistics")                    
                    st.write('Number total of users: ', extract_statistics_user.get_number_id())
                    st.write('Analyzing possible values per attribute: ')
                    number_possible_values_df = extract_statistics_user.get_number_possible_values_by_attribute()
                    avg_possible_values_df = extract_statistics_user.get_avg_possible_values_by_attribute()
                    sd_possible_values_df = extract_statistics_user.get_sd_possible_values_by_attribute()                                        
                    extracted_statistics_df = pd.concat([number_possible_values_df, avg_possible_values_df, sd_possible_values_df])                    
                    # Insert the new column at index 0:
                    label_column_list = ['count', 'average', 'standard deviation']                    
                    extracted_statistics_df.insert(loc=0, column='possible values', value=label_column_list)                  
                    if extracted_statistics_df.isnull().values.any():
                        st.warning('If there are <NA> values, it is because these attributes have Nan or string values.')
                    st.dataframe(extracted_statistics_df)                    
                    # Showing more details:
                    with st.expander('More details'):
                        statistics = extract_statistics_user.statistics_by_attribute()
                        util.print_statistics_by_attribute(statistics)          
                    # Showing correlation between attributes:
                    st.header("Correlation between attributes")
                    corr_matrix = util.correlation_matrix(df=user_df, label='user')                    
                    if not corr_matrix.empty:                        
                        fig, ax = plt.subplots(figsize=(10, 10))                    
                        sns.heatmap(corr_matrix, vmin=-1, vmax=1, center=0, cmap='coolwarm', annot=True, fmt=".2f", ax=ax)
                        st.pyplot(fig)      
                except Exception as e:
                    st.error(f"Make sure the user dataset is in the right format. {e}")
            else:
                st.warning("The user file (user.csv) has not been uploaded.")
        # Items tab:
        with item_tab:
            if not item_df.empty:
                try:
                    # Item dataframe:
                    st.header("Item file")
                    st.dataframe(item_df)
                    # Extracted statistics:
                    extract_statistics_item = ExtractStatisticsUIC(item_df)
                    # Missing values:
                    st.header("Missing values")
                    missing_values3 = extract_statistics_item.count_missing_values(replace_values={"NULL":np.nan,-1:np.nan})                    
                    st.table(missing_values3)                    
                    # Attributes, data types and value ranges:
                    st.header("Attributes, data types and value ranges")
                    table3 = extract_statistics_item.get_attributes_and_ranges()
                    st.table(pd.DataFrame(table3, columns=["Attribute name", "Data type", "Value ranges"]))
                    # Showing one figure by attribute:
                    st.header("Analysis by attribute")
                    col1, col2 = st.columns(2)
                    with col1:                        
                        item_attribute_list = item_df.columns.tolist()
                        item_attribute_list.remove('item_id')
                        column3 = st.selectbox("Select an attribute", item_attribute_list, key='column3')
                    with col2:
                        sort3 = st.selectbox('Sort', ['none', 'asc', 'desc'], key='sort3')
                    data3 = extract_statistics_item.column_attributes_count(column3)
                    util.plot_column_attributes_count(data3, column3, sort3)
                    # Showing extracted statistics:
                    st.header("Extracted statistics")                    
                    st.write('Number total of items: ', extract_statistics_item.get_number_id())
                    st.write('Analyzing possible values per attribute: ')
                    number_possible_values_df = extract_statistics_item.get_number_possible_values_by_attribute()
                    avg_possible_values_df = extract_statistics_item.get_avg_possible_values_by_attribute()
                    sd_possible_values_df = extract_statistics_item.get_sd_possible_values_by_attribute()                                        
                    extracted_statistics_df = pd.concat([number_possible_values_df, avg_possible_values_df, sd_possible_values_df])                    
                    # Insert the new column at index 0:
                    label_column_list = ['count', 'average', 'standard deviation']                    
                    extracted_statistics_df.insert(loc=0, column='possible values', value=label_column_list)                  
                    if extracted_statistics_df.isnull().values.any():
                        st.warning('If there are <NA> values, it is because these attributes have Nan or string values.')
                    st.dataframe(extracted_statistics_df) 
                    # Showing more details:
                    with st.expander('More details'):                        
                        statistics = extract_statistics_item.statistics_by_attribute()
                        util.print_statistics_by_attribute(statistics)                        
                    # Showing correlation between attributes:
                    st.header("Correlation between attributes")
                    corr_matrix = util.correlation_matrix(df=item_df, label='item')
                    if not corr_matrix.empty:                        
                        fig, ax = plt.subplots(figsize=(10, 10))                    
                        sns.heatmap(corr_matrix, vmin=-1, vmax=1, center=0, cmap='coolwarm', annot=True, fmt=".2f", ax=ax)
                        st.pyplot(fig)                        
                except Exception as e:
                    st.error(f"Make sure the item dataset is in the right format. {e}")
            else:
                st.warning("The item file (item.csv) has not been uploaded.")
        # Contexts tab:
        if with_context:
            with context_tab:
                if not context_df.empty:
                    try:
                        # Context dataframe:
                        st.header("Context file")
                        st.dataframe(context_df)
                        # Extracted statistics:
                        extract_statistics_context = ExtractStatisticsUIC(context_df)
                        # Missing values:
                        st.header("Missing values")
                        missing_values4 = extract_statistics_context.count_missing_values(replace_values={"NULL":np.nan,-1:np.nan})                        
                        st.table(missing_values4)
                        # Attributes, data types and value ranges:
                        st.header("Attributes, data types and value ranges")
                        table4 = extract_statistics_context.get_attributes_and_ranges()
                        st.table(pd.DataFrame(table4, columns=["Attribute name", "Data type", "Value ranges"]))
                        # Showing one figure by attribute:
                        st.header("Analysis by attribute")                        
                        col1, col2 = st.columns(2)
                        with col1:
                            context_attribute_list = context_df.columns.tolist()
                            context_attribute_list.remove('context_id')
                            column4 = st.selectbox("Select an attribute", context_attribute_list, key='column4')
                        with col2:
                            sort4 = st.selectbox('Sort', ['none', 'asc', 'desc'], key='sort4')
                        data4 = extract_statistics_context.column_attributes_count(column4)
                        util.plot_column_attributes_count(data4, column4, sort4)
                        # Showing extracted statistics:
                        st.header("Extracted statistics")                    
                        st.write('Number total of contexts: ', extract_statistics_context.get_number_id())
                        st.write('Analyzing possible values per attribute: ')
                        number_possible_values_df = extract_statistics_context.get_number_possible_values_by_attribute()
                        avg_possible_values_df = extract_statistics_context.get_avg_possible_values_by_attribute()
                        sd_possible_values_df = extract_statistics_context.get_sd_possible_values_by_attribute()                                        
                        extracted_statistics_df = pd.concat([number_possible_values_df, avg_possible_values_df, sd_possible_values_df])                    
                        # Insert the new column at index 0:
                        label_column_list = ['count', 'average', 'standard deviation']                    
                        extracted_statistics_df.insert(loc=0, column='possible values', value=label_column_list)                  
                        if extracted_statistics_df.isnull().values.any():
                            st.warning('If there are <NA> values, it is because these attributes have Nan or string values.')
                        st.dataframe(extracted_statistics_df)
                        # Showing more details:
                        with st.expander('More details'):
                            statistics = extract_statistics_context.statistics_by_attribute()
                            util.print_statistics_by_attribute(statistics)       
                        # Showing correlation between attributes:
                        st.header("Correlation between attributes")
                        corr_matrix = util.correlation_matrix(df=context_df, label='context')
                        if not corr_matrix.empty:                        
                            fig, ax = plt.subplots(figsize=(10, 10))                    
                            sns.heatmap(corr_matrix, vmin=-1, vmax=1, center=0, cmap='coolwarm', annot=True, fmt=".2f", ax=ax)
                            st.pyplot(fig)         
                    except Exception as e:
                        st.error(f"Make sure the context dataset is in the right format. {e}")
                else:
                    st.warning("The context file (context.csv) has not been uploaded.")
        # Ratings tab:
        with rating_tab:
            if not rating_df.empty:
                try:
                    # Rating dataframe:
                    st.header("Rating file")          
                    st.dataframe(rating_df)
                    # Extracted statistics:
                    extract_statistics_rating = ExtractStatisticsRating(rating_df=rating_df)                    
                    # General statistics:
                    st.header("General statistics")
                    unique_users = extract_statistics_rating.get_number_users()
                    unique_items = extract_statistics_rating.get_number_items()
                    unique_counts = {"Users": unique_users, "Items": unique_items}
                    if with_context:
                        unique_contexts = extract_statistics_rating.get_number_contexts()
                        unique_counts["Contexts"] = unique_contexts
                    unique_ratings = extract_statistics_rating.get_number_ratings()
                    unique_counts["Ratings"] = unique_ratings
                    unique_counts_df = pd.DataFrame.from_dict(unique_counts, orient='index', columns=['Count'])
                    unique_counts_df.reset_index(inplace=True)
                    unique_counts_df.rename(columns={"index": "Attribute name"}, inplace=True)                    
                    st.table(unique_counts_df)               
                    # Attributes, data types and value ranges:
                    st.header("Attributes, data types and value ranges")
                    table5 = extract_statistics_rating.get_attributes_and_ranges()
                    st.table(pd.DataFrame(table5, columns=["Attribute name", "Data type", "Value ranges"]))
                    # Histogram of ratings:
                    st.header("Histogram of ratings")
                    counts = np.bincount(rating_df['rating'])[np.nonzero(np.bincount(rating_df['rating']))] #Count the frequency of each rating
                    df5 = pd.DataFrame({'Type of ratings': np.arange(1, len(counts) + 1), 'Number of ratings': counts})
                    chart5 = alt.Chart(df5).mark_bar(color='#0099CC').encode(
                        x=alt.X('Type of ratings:O', axis=alt.Axis(title='Type of ratings')),
                        y=alt.Y('Number of ratings:Q', axis=alt.Axis(title='Number of ratings')),
                        tooltip=['Type of ratings', 'Number of ratings']
                    ).properties(
                        title={
                            'text': 'Histogram of ratings',
                            'fontSize': 16,
                        }
                    )                    
                    st.altair_chart(chart5, use_container_width=True)
                    # Statistics per user:
                    st.header("Statistics per user")
                    users = list(rating_df['user_id'].unique())                    
                    selected_user = st.selectbox("Select a user:", users, key="selected_user_tab5")   
                    # Items per user:
                    st.markdown("*Items*")                           
                    counts_items, unique_items, total_count = extract_statistics_rating.get_number_items_from_user(selected_user)
                    df = pd.DataFrame({'Type of items': counts_items.index, 'Number of items': counts_items.values})                    
                    counts_items = pd.Series(counts_items, name='Number of items').reset_index()
                    counts_items = counts_items.rename(columns={'index': 'Type of items'})
                    chart = alt.Chart(counts_items).mark_bar(color="#0099CC").encode(
                        x=alt.X('Type of items:O', axis=alt.Axis(labelExpr='datum.value', title='Type of items')),
                        y=alt.Y('Number of items:Q', axis=alt.Axis(title='Number of items')),
                        tooltip=['Type of items', 'Number of items']
                    ).properties(
                        title={
                        "text": [f"Histogram of items rated per user {str(selected_user)} (total={total_count})"],
                        "fontSize": 16,
                        }
                    )                    
                    st.altair_chart(chart, use_container_width=True) 
                    # Statistics of items:
                    item_statistics_dict = {}         
                    # Number of items by user:           
                    number_items_df = extract_statistics_rating.get_number_ratings_by_user()
                    number_items = number_items_df.loc[number_items_df['user_id'] == selected_user, 'count_ratings'].iloc[0]
                    # Percentage of items by user:
                    percentage_items_df = extract_statistics_rating.get_percentage_ratings_by_user()                    
                    percentage_items = percentage_items_df.loc[percentage_items_df['user_id'] == selected_user, 'percentage_ratings'].iloc[0]
                    # Average of items by user:    
                    avg_items_df = extract_statistics_rating.get_avg_items_by_user()
                    avg_items = avg_items_df.loc[avg_items_df['user_id'] == selected_user, 'avg_items'].iloc[0]
                    # Variance of items by user:
                    variance_items_df = extract_statistics_rating.get_variance_items_by_user()
                    variance_items = variance_items_df.loc[variance_items_df['user_id'] == selected_user, 'variance_items'].iloc[0]                    
                    # Standard deviation of items by user:
                    sd_items_df = extract_statistics_rating.get_sd_items_by_user()                    
                    sd_items = sd_items_df.loc[sd_items_df['user_id'] == selected_user, 'sd_items'].iloc[0]                    
                    # Number of not repeated items by user:                    
                    number_not_repeated_items_df = extract_statistics_rating.get_number_not_repeated_items_by_user()
                    number_not_repeated_items = number_not_repeated_items_df.loc[number_not_repeated_items_df['user_id'] == selected_user, 'not_repeated_items'].iloc[0]
                    # Percentage of not repeated items by user:                    
                    percentage_not_repeated_items_df = extract_statistics_rating.get_percentage_not_repeated_items_by_user()
                    percentage_not_repeated_items = percentage_not_repeated_items_df.loc[percentage_not_repeated_items_df['user_id'] == selected_user, 'percentage_not_repeated_items'].iloc[0]
                    # Percentage of not repeated items by user:                    
                    percentage_repeated_items_df = extract_statistics_rating.get_percentage_repeated_items_by_user()
                    percentage_repeated_items = percentage_repeated_items_df.loc[percentage_repeated_items_df['user_id'] == selected_user, 'porcentage_repeated_items'].iloc[0]
                    item_statistics_dict['user_id'] = [selected_user]
                    item_statistics_dict['count'] = [number_items]
                    item_statistics_dict['percentage'] = [percentage_items]
                    item_statistics_dict['average'] = [avg_items]                  
                    item_statistics_dict['variance'] = [variance_items]                  
                    item_statistics_dict['standard deviation'] = [sd_items]      
                    item_statistics_dict['not repeated items'] = [number_not_repeated_items]
                    item_statistics_dict['percentage not repeated items'] = [percentage_not_repeated_items]
                    item_statistics_dict['percentage repeated items'] = [percentage_repeated_items]
                    item_statistics_df = pd.DataFrame(item_statistics_dict)
                    st.dataframe(item_statistics_df)   
                    if with_context:
                        # Contexts per user:                    
                        st.markdown("*Contexts*")
                        # Statistics of contexts:
                        context_statistics_dict = {}         
                        # Number of contexts by user:           
                        number_contexts_df = extract_statistics_rating.get_number_ratings_by_user()
                        number_contexts = number_contexts_df.loc[number_contexts_df['user_id'] == selected_user, 'count_ratings'].iloc[0]
                        # Percentage of contexts by user:
                        percentage_contexts_df = extract_statistics_rating.get_percentage_ratings_by_user()
                        percentage_contexts = percentage_contexts_df.loc[percentage_contexts_df['user_id'] == selected_user, 'percentage_ratings'].iloc[0]
                        # Average of contexts by user:    
                        avg_contexts_df = extract_statistics_rating.get_avg_contexts_by_user()
                        avg_contexts = avg_contexts_df.loc[avg_contexts_df['user_id'] == selected_user, 'avg_contexts'].iloc[0]
                        # Variance of contexts by user:
                        variance_contexts_df = extract_statistics_rating.get_variance_contexts_by_user()
                        variance_contexts = variance_contexts_df.loc[variance_contexts_df['user_id'] == selected_user, 'variance_contexts'].iloc[0]
                        # Standard deviation of contexts by user:
                        sd_contexts_df = extract_statistics_rating.get_sd_contexts_by_user()                    
                        sd_contexts = sd_contexts_df.loc[sd_contexts_df['user_id'] == selected_user, 'sd_contexts'].iloc[0]                    
                        # Number of not repeated contexts by user:                    
                        number_not_repeated_contexts_df = extract_statistics_rating.get_number_not_repeated_contexts_by_user()
                        number_not_repeated_contexts = number_not_repeated_contexts_df.loc[number_not_repeated_contexts_df['user_id'] == selected_user, 'not_repeated_contexts'].iloc[0]
                        # Percentage of not repeated contexts by user:                    
                        percentage_not_repeated_contexts_df = extract_statistics_rating.get_percentage_not_repeated_contexts_by_user()
                        percentage_not_repeated_contexts = percentage_not_repeated_contexts_df.loc[percentage_not_repeated_contexts_df['user_id'] == selected_user, 'percentage_not_repeated_contexts'].iloc[0]
                        # Percentage of not repeated contexts by user:                    
                        percentage_repeated_contexts_df = extract_statistics_rating.get_percentage_repeated_contexts_by_user()
                        percentage_repeated_contexts = percentage_repeated_contexts_df.loc[percentage_repeated_contexts_df['user_id'] == selected_user, 'porcentage_repeated_contexts'].iloc[0]
                        context_statistics_dict['user_id'] = [selected_user]
                        context_statistics_dict['count'] = [number_contexts]
                        context_statistics_dict['percentage'] = [percentage_contexts]
                        context_statistics_dict['average'] = [avg_contexts]                  
                        context_statistics_dict['variance'] = [variance_contexts]                  
                        context_statistics_dict['standard deviation'] = [sd_contexts] 
                        context_statistics_dict['not repeated contexts'] = [number_not_repeated_contexts]
                        context_statistics_dict['percentage not repeated contexts'] = [percentage_not_repeated_contexts]
                        context_statistics_dict['percentage repeated contexts'] = [percentage_repeated_contexts]     
                        context_statistics_df = pd.DataFrame(context_statistics_dict)
                        st.dataframe(context_statistics_df)    
                    # Ratings per user:                    
                    st.markdown("*Ratings*")                  
                    rating_statistics_dict = {}         
                    # Number of ratings by user:           
                    number_ratings_df = extract_statistics_rating.get_number_ratings_by_user()
                    number_ratings = number_ratings_df.loc[number_ratings_df['user_id'] == selected_user, 'count_ratings'].iloc[0]
                    # Percentage of ratings by user:
                    percentage_ratings_df = extract_statistics_rating.get_percentage_ratings_by_user()                    
                    percentage_ratings = percentage_ratings_df.loc[percentage_ratings_df['user_id'] == selected_user, 'percentage_ratings'].iloc[0]
                    # Average of ratings by user:    
                    avg_ratings_df = extract_statistics_rating.get_avg_ratings_by_user()
                    avg_ratings = avg_ratings_df.loc[avg_ratings_df['user_id'] == selected_user, 'avg_ratings'].iloc[0]
                    # Variance of ratings by user:
                    variance_ratings_df = extract_statistics_rating.get_variance_ratings_by_user()
                    variance_ratings = variance_ratings_df.loc[variance_ratings_df['user_id'] == selected_user, 'variance_ratings'].iloc[0]
                    # Standard deviation of ratings by user:
                    sd_ratings_df = extract_statistics_rating.get_sd_items_by_user()                    
                    sd_ratings = sd_ratings_df.loc[sd_ratings_df['user_id'] == selected_user, 'sd_items'].iloc[0]                    
                    rating_statistics_dict['user_id'] = [selected_user]
                    rating_statistics_dict['count'] = [number_ratings]
                    rating_statistics_dict['percentage'] = [percentage_ratings]  
                    rating_statistics_dict['average'] = [avg_ratings]                  
                    rating_statistics_dict['variance'] = [variance_ratings]                  
                    rating_statistics_dict['standard deviation'] = [sd_ratings]      
                    rating_statistics_df = pd.DataFrame(rating_statistics_dict)
                    st.dataframe(rating_statistics_df)                  
                except Exception as e:
                    st.error(f"Make sure the rating dataset is in the right format. {e}")
            else:
                st.warning("The rating file (rating.csv) has not been uploaded.")
    # EVALUATION:    
    elif is_analysis == 'Evaluation':
        st.header('Evaluation')  
        # CARS Evaluation:        
        if with_context:
            if (not rating_df.empty) and (not item_df.empty) and (not context_df.empty):
                st.sidebar.markdown("""---""")
                # SELECTING PARADIGM TO EVALUATE:
                st.sidebar.markdown('**CARS paradigm selection**')
                paradigm = st.sidebar.selectbox("Select one paradigm", ["Contextual Modeling", "Pre-filtering", "Post-filtering"])
                lars = st.sidebar.checkbox('LARS', value=True)
                st.session_state["lars"] = lars
                if lars:
                    side_lars = st.sidebar.checkbox('SocIal-Distance prEserving', value=True)
                    st.session_state["side_lars"] = side_lars
                st.sidebar.markdown("""---""")
                if paradigm == "Contextual Modeling":
                    # SELECTING CONTEXTUAL FEATURES:
                    st.sidebar.markdown('**Contextual features selection**')
                    item_feature_df = util.select_contextual_features(df=item_df, label="item")                    
                    context_feature_df = util.select_contextual_features(df=context_df, label="context")
                    # Building knowledge base:                    
                    try:
                        merged_df = rating_df.merge(item_feature_df, on='item_id').merge(context_feature_df, on='context_id')
                        merged_df.drop('context_id', axis=1, inplace=True)
                    except KeyError as e:
                        st.error(f"The rating, user, item and context datasets do not have '_id' columns in common. {e}")                    
                    st.sidebar.markdown("""---""")
                    # SELECTING CLASSIFIER:
                    st.sidebar.markdown('**Classifier selection**')
                    classifier_name_list = st.sidebar.multiselect("Select one or more classifiers", ["KNeighborsClassifier", "SVC", "GaussianNB", "RandomForestClassifier", "KMeans", "HistGradientBoostingClassifier"], default="KNeighborsClassifier")
                    # Replacing some values and building classifiers.
                    classifier_list = []
                    st.sidebar.write("-0.5 values will be replaced with None")
                    # Help information:
                    with st.expander(label='Help information'): 
                        for classifier_name in classifier_name_list:
                            classifier_params = util.replace_with_none(util.select_params_contextual(classifier_name))
                            if classifier_name == 'KNeighborsClassifier':
                                st.markdown("""- ``` KNeighborsClassifier ```: Classifier implementing the k-nearest neighbors vote.""")
                            if classifier_name == 'SVC':
                                st.markdown("""- ``` SVC ```: C-Support Vector Classification. The implementation is based on libsvm.""")
                            if classifier_name == 'GaussianNB':
                                st.markdown("""- ``` GaussianNB ```: Gaussian Naive Bayes.""")
                            if classifier_name == 'RandomForestClassifier':
                                st.markdown("""- ``` RandomForestClassifier ```: A random forest classifier. A random forest is a meta estimator that fits a number of decision tree classifiers on various sub-samples of the dataset and uses averaging to improve the predictive accuracy and control over-fitting.""")
                            if classifier_name == 'KMeans':
                                st.markdown("""- ``` KMeans ```: K-Means clustering.""")
                            if classifier_name == 'HistGradientBoostingClassifier':
                                st.markdown("""- ``` HistGradientBoostingClassifier ```: Histogram-based Gradient Boosting Classification Tree. This estimator has native support for missing values (NaNs).""")
                            st.markdown("""These algorithms are implemented in the [scikit-learn](https://scikit-learn.org/stable/supervised_learning.html#supervised-learning) python library.""")                                             
                            # PARAMETER SETTINGS:                            
                            classifier_instance = sklearn_helpers.create_algorithm(classifier_name, classifier_params)
                            classifier_list.append(classifier_instance)
                            st.sidebar.markdown("""---""")
                    # CROSS VALIDATION:
                    st.sidebar.markdown('**Split strategy selection**')
                    strategy = st.sidebar.selectbox("Select a strategy", ["KFold", "ShuffleSplit", "LeaveOneOut"]) # , "PredefinedKFold", "train_test_split", "RepeatedKFold", 
                    strategy_params = util.select_split_strategy_contextual(strategy)
                    strategy_instance = sklearn_helpers.create_split_strategy(strategy, strategy_params)
                    st.sidebar.markdown("""---""")
                    # METRICS:
                    st.sidebar.markdown('**Metrics selection**')  
                    metrics = st.sidebar.multiselect("Select one or more metrics", config.SCIKIT_LEARN_METRICS, default="Precision")
                    st.sidebar.markdown("""---""")
                    # EVALUATION:
                    st.sidebar.markdown('**Target user**')
                    # Extract unique user_ids and add "All users" option
                    user_ids = sorted(rating_df['user_id'].unique().tolist())
                    user_options = ["All users"] + user_ids
                    selected_users = st.sidebar.multiselect("Select one or more users or 'All users'", options=user_options, default="All users")
                    if st.sidebar.button("Evaluate"):
                        if "All users" in selected_users:
                            target_user_ids = None
                        else:
                            target_user_ids = selected_users                            
                        fold_results_df = sklearn_helpers.evaluate(merged_df, classifier_list, strategy_instance, metrics, target_user_ids)
                        st.session_state["fold_results"] = fold_results_df #Save the results dataframe in the session state
                    # RESULTS:
                    if "fold_results" in st.session_state:
                        # Results (folds):
                        fold_results_df = st.session_state["fold_results"]
                        st.subheader("Detailed evaluation results (folds and means)")
                        st.dataframe(fold_results_df)                    
                        link_fold_result = f'<a href="data:file/csv;base64,{base64.b64encode(fold_results_df.to_csv(index=False).encode()).decode()}" download="fold_evaluation_results.csv">Download results</a>'
                        st.markdown(link_fold_result, unsafe_allow_html=True)
                        # Results (means):
                        metric_list = fold_results_df.columns[3:].tolist()                 
                        mean_results_df = fold_results_df.groupby(['User','Algorithm'])[metric_list].mean().reset_index()
                        st.dataframe(mean_results_df)                    
                        link_mean_result = f'<a href="data:file/csv;base64,{base64.b64encode(mean_results_df.to_csv(index=False).encode()).decode()}" download="mean_evaluation_results.csv">Download results</a>'
                        st.markdown(link_mean_result, unsafe_allow_html=True)
                        # Evaluation figures:
                        st.subheader("Evaluation graphs (folds and means)")
                        with_fold = st.selectbox(label="Select one option to plot", options=['Means', 'Folds']) 
                        col_algorithm, col_metric, col_user = st.columns(3)
                        with col_algorithm:
                            st.session_state['selected_algorithm_list'] = st.multiselect(label="Select an algorithm", options=fold_results_df["Algorithm"].unique().tolist())
                        with col_metric:                            
                            st.session_state['selected_metric_list'] = st.multiselect(label="Select a metric", options=metric_list)
                        with col_user:                                                        
                            st.session_state['selected_users_list'] = st.multiselect(label="Select a user", options=selected_users)  
                        # Increasing the maximum value of the Y-axis:
                        increment_yaxis = st.number_input("How to increment the maximum value of the Y-axis", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
                        # Plotting the graph (by using the "Means" option):
                        if with_fold == 'Means':                             
                            # Showing graph:               
                            if st.button(label='Show graph'):
                                util.visualize_graph_mean_cars(fold_results_df, st.session_state['selected_algorithm_list'], st.session_state['selected_metric_list'], st.session_state['selected_users_list'], increment_yaxis)
                                # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:
                                df = mean_results_df.loc[mean_results_df['Algorithm'].isin(st.session_state['selected_algorithm_list']), ['User', 'Algorithm']+st.session_state['selected_metric_list']]
                                with st.expander(label='Data to plot in the graphic'):
                                    st.dataframe(df)
                        elif with_fold == 'Folds': # Plotting the graph (by using the "Folds" option):                            
                            # Showing graph:               
                            if st.button(label='Show graph'):                                
                                util.visualize_graph_fold_cars(fold_results_df, st.session_state['selected_algorithm_list'], st.session_state['selected_metric_list'], st.session_state['selected_users_list'], increment_yaxis)
                                # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:                                
                                df = fold_results_df.loc[fold_results_df['Algorithm'].isin(st.session_state['selected_algorithm_list']), ['User', 'Fold', 'Algorithm']+st.session_state['selected_metric_list']]
                                with st.expander(label='Data to plot in the graphic'):
                                    st.dataframe(df)
                elif paradigm == "Post-filtering":
                    if side_lars and (not user_df.empty) and (not item_df.empty) and (not context_df.empty) and (not rating_df.empty) and (not behavior_df.empty):
                        st.sidebar.header("Algorithm selection")
                        algorithms = st.sidebar.multiselect("Select one or more algorithms", ["KNNBasic", "KNNWithMeans", "KNNWithZScore", "KNNBaseline"], default="KNNBasic")
                        algo_list = []
                        for algorithm in algorithms:
                            algo_params = util.select_params(algorithm)
                            algo_instance = surprise_helpers.create_algorithm(algorithm, algo_params)
                            algo_list.append(algo_instance)
                            st.sidebar.markdown("""---""")
                        st.sidebar.header("Split strategy selection")
                        strategy = st.sidebar.selectbox("Select a strategy", ["KFold", "RepeatedKFold", "ShuffleSplit", "LeaveOneOut", "PredefinedKFold", "train_test_split"])
                        strategy_params = util.select_split_strategy(strategy)
                        strategy_instance = surprise_helpers.create_split_strategy(strategy, strategy_params)
                        data = surprise_helpers.convert_to_surprise_dataset(rating_df)
                        st.sidebar.header("Metrics selection")
                        if binary_ratings.is_binary_rating(rating_df):
                            metrics = st.sidebar.multiselect("Select one or more cross validation binary metrics", ["Precision", "Recall", "F1_Score", "AUC_ROC"], default="Precision")
                        else:
                            metrics = st.sidebar.multiselect("Select one or more cross validation non-binary metrics", ["RMSE", "MSE", "MAE", "FCP", "Precision", "Recall", "F1_Score", "MAP", "NDCG"], default="MAE")
                        # min_social_distance = st.sidebar.number_input("Minimum social distance", min_value=0, max_value=100, value=2, step=1)
                        # k_recommendations = st.sidebar.number_input("Number of recommendations", min_value=1, max_value=100, value=3, step=1)
                        # EVALUATION:
                        if st.sidebar.button("Evaluate"):
                            fold_results_df = util.evaluate_algo(algo_list, strategy_instance, metrics, data)
                            st.session_state["fold_results"] = fold_results_df #Save the results dataframe in the session state
                        # RESULTS:
                        if "fold_results" in st.session_state:
                            # Results (folds):
                            fold_results_df = st.session_state["fold_results"]
                            st.subheader("Detailed evaluation results (folds and means)")
                            st.dataframe(fold_results_df)                    
                            link_fold_result = f'<a href="data:file/csv;base64,{base64.b64encode(fold_results_df.to_csv(index=False).encode()).decode()}" download="fold_evaluation_results.csv">Download results</a>'
                            st.markdown(link_fold_result, unsafe_allow_html=True)
                            # Results (means):
                            metric_list = fold_results_df.columns[2:].tolist()
                            mean_results_df = fold_results_df.groupby('Algorithm')[metric_list].mean().reset_index()
                            st.dataframe(mean_results_df)                    
                            link_mean_result = f'<a href="data:file/csv;base64,{base64.b64encode(mean_results_df.to_csv(index=False).encode()).decode()}" download="mean_evaluation_results.csv">Download results</a>'
                            st.markdown(link_mean_result, unsafe_allow_html=True)
                            # Evaluation figures:
                            st.subheader("Evaluation graphs (folds and means)")
                            with_fold = st.selectbox(label="Select one option to plot", options=['Means', 'Folds'])  
                            algorithm_list = fold_results_df["Algorithm"].unique().tolist()                  
                            selected_algorithm_list = st.multiselect(label="Select one or more algorithms to plot", options=algorithm_list, default=algorithm_list)
                            
                            # Plotting the graph (by using the "Means" option):
                            if with_fold == 'Means':
                                selected_metric_list = st.multiselect(label="Select one or more metrics to plot", options=metric_list, default=metric_list)
                                # Increasing the maximum value of the Y-axis:
                                increment_yaxis = st.number_input("How to increment the maximum value of the Y-axis", min_value=0.0, max_value=10.0, value=0.5, step=0.1)     
                                # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:
                                df = mean_results_df.loc[mean_results_df['Algorithm'].isin(selected_algorithm_list), ['Algorithm']+selected_metric_list]
                                # Showing graph:               
                                if st.button(label='Show graph'):
                                    util.visualize_graph_mean_rs(df, increment_yaxis)
                                    with st.expander(label='Data to plot in the graphic'):
                                        st.dataframe(df)
                            elif with_fold == 'Folds': # Plotting the graph (by using the "Folds" option):
                                selected_metric = st.selectbox(label="Select one or more metrics to plot", options=metric_list)
                                # Increasing the maximum value of the Y-axis:
                                increment_yaxis = st.number_input("How to increment the maximum value of the Y-axis", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
                                # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:
                                df = fold_results_df.loc[fold_results_df['Algorithm'].isin(selected_algorithm_list), ['Fold', 'Algorithm']+[selected_metric]]                        
                                # Showing graph:               
                                if st.button(label='Show graph'):
                                    util.visualize_graph_fold_rs(df, selected_metric, increment_yaxis)
                                    with st.expander(label='Data to plot in the graphic'):
                                        st.dataframe(df)
                    else:
                        st.error(st.warning("The user, item, context, rating and behavior files have not been uploaded."))
                else:
                    st.write("TODO: pre-filtering")
            else:
                st.warning("The item, context and rating files have not been uploaded.")
        else:
            # Traditional RS Evaluation:
            if not rating_df.empty:
                st.sidebar.markdown("""---""")
                # SELECTING RS TO EVALUATE:                
                st.sidebar.markdown('**Recommendation Systems selection**')
                recommender_name_list = []
                # Basic Recommenders:
                basic_recommender_name = st.sidebar.multiselect(label='Basic Recommenders:', options=['BaselineOnly', 'NormalPredictor'])
                recommender_name_list.extend(basic_recommender_name)
                # Collaborative Filtering Recommenders:
                cf_recommender_name = st.sidebar.multiselect(label='Collaborative Filtering Recommenders:', options=['KNNBasic', 'KNNWithMeans', 'KNNWithZScore', 'KNNBaseline', 'SVD', 'SVDpp', 'NMF', 'SlopeOne', 'CoClustering'])
                recommender_name_list.extend(cf_recommender_name)
                # Content-Based Recommenders:
                cb_recommender_type = st.sidebar.multiselect(label='Content-Based Recommenders:', options=['PENDING TODO'])
                # recommender_name_list.extend(cb_recommender_type)
                # Help information:
                with st.expander(label='Help information'):                    
                    for recommender_name in recommender_name_list:                        
                        if recommender_name == 'BaselineOnly':
                            st.markdown("""- ``` BaselineOnly ```: Algorithm predicting the baseline estimate for given user and item.""")
                        if recommender_name == 'NormalPredictor':
                            st.markdown("""- ``` NormalPredictor ```: Algorithm predicting a random rating based on the distribution of the training set, which is assumed to be normal.""")
                        if recommender_name == 'KNNBasic':
                            st.markdown("""- ``` KNNBasic ```: A basic collaborative filtering algorithm derived from a basic nearest neighbors approach.""")
                        if recommender_name == 'KNNWithMeans':
                            st.markdown("""- ``` KNNWithMeans ```: A basic collaborative filtering algorithm, taking into account the mean ratings of each user.""")
                        if recommender_name == 'KNNWithZScore':
                            st.markdown("""- ``` KNNWithZScore ```: A basic collaborative filtering algorithm, taking into account the z-score normalization of each user.""")
                        if recommender_name == 'KNNBaseline':
                            st.markdown("""- ``` KNNBaseline ```: A basic collaborative filtering algorithm taking into account a baseline rating.""")
                        if recommender_name == 'SVD':
                            st.markdown("""- ``` SVD ```: The famous SVD algorithm, as popularized by Simon Funk during the Netflix Prize. When baselines are not used, this is equivalent to Probabilistic Matrix Factorization""")
                        if recommender_name == 'SVDpp':
                            st.markdown("""- ``` SVDpp ```: The SVD++ algorithm, an extension of SVD taking into account implicit ratings.""")
                        if recommender_name == 'NMF':
                            st.markdown("""- ``` NMF ```:  A collaborative filtering algorithm based on Non-negative Matrix Factorization.""")
                        if recommender_name == 'SlopeOne':
                            st.markdown("""- ``` SlopeOne ```: A simple yet accurate collaborative filtering algorithm. This is a straightforward implementation of the SlopeOne algorithm [LM07]. [LM07] Daniel Lemire and Anna Maclachlan. [Slope one predictors for online rating-based collaborative filtering](https://arxiv.org/abs/cs/0702144). 2007.""")
                        if recommender_name == 'CoClustering':
                            st.markdown("""- ``` CoClustering ```: A collaborative filtering algorithm based on co-clustering. This is a straightforward implementation of [GM05]. [GM05] Thomas George and Srujana Merugu. [A scalable collaborative filtering framework based on co-clustering](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.113.6458&rep=rep1&type=pdf). 2005.""")
                    st.markdown("""These algorithms are implemented in the [surprise](https://github.com/NicolasHug/Surprise) python library.""")                                             
                # PARAMETER SETTINGS:
                algo_list = []
                for algorithm in recommender_name_list:                                  
                    algo_params = util.select_params(algorithm)                        
                    algo_instance = surprise_helpers.create_algorithm(algorithm, algo_params)
                    algo_list.append(algo_instance)
                st.sidebar.markdown("""---""")            
                # CROSS VALIDATION:
                st.sidebar.markdown('**Split strategy selection**')
                strategy = st.sidebar.selectbox("Select a strategy", ["KFold", "RepeatedKFold", "ShuffleSplit", "LeaveOneOut"]) # , "PredefinedKFold", "train_test_split"
                strategy_params = util.select_split_strategy(strategy)
                strategy_instance = surprise_helpers.create_split_strategy(strategy, strategy_params)
                data = surprise_helpers.convert_to_surprise_dataset(rating_df)
                st.sidebar.markdown("""---""")
                # METRICS:
                st.sidebar.markdown('**Metrics selection**')                
                if binary_ratings.is_binary_rating(rating_df):
                    metrics = st.sidebar.multiselect("Select one or more binary metrics", ["Precision", "Recall", "F1_Score", "AUC_ROC"], default=["Precision", "Recall", "F1_Score"])
                else:
                    metrics = st.sidebar.multiselect("Select one or more non-binary metrics", ["MAE", "Precision", "Recall", "F1_Score", "RMSE", "MSE", "FCP", "MAP", "NDCG"], default=["MAE", "Precision", "Recall", "F1_Score"])
                # EVALUATION:
                if st.sidebar.button("Evaluate"):
                    fold_results_df = util.evaluate_algo(algo_list, strategy_instance, metrics, data)
                    st.session_state["fold_results"] = fold_results_df #Save the results dataframe in the session state
                # RESULTS:
                if "fold_results" in st.session_state:
                    # Results (folds):
                    fold_results_df = st.session_state["fold_results"]
                    st.subheader("Detailed evaluation results (folds and means)")
                    st.dataframe(fold_results_df)                    
                    link_fold_result = f'<a href="data:file/csv;base64,{base64.b64encode(fold_results_df.to_csv(index=False).encode()).decode()}" download="fold_evaluation_results.csv">Download results</a>'
                    st.markdown(link_fold_result, unsafe_allow_html=True)
                    # Results (means):
                    metric_list = fold_results_df.columns[2:].tolist()
                    mean_results_df = fold_results_df.groupby('Algorithm')[metric_list].mean().reset_index()
                    st.dataframe(mean_results_df)                    
                    link_mean_result = f'<a href="data:file/csv;base64,{base64.b64encode(mean_results_df.to_csv(index=False).encode()).decode()}" download="mean_evaluation_results.csv">Download results</a>'
                    st.markdown(link_mean_result, unsafe_allow_html=True)
                    # Evaluation figures:
                    st.subheader("Evaluation graphs (folds and means)")
                    with_fold = st.selectbox(label="Select one option to plot", options=['Means', 'Folds'])  
                    algorithm_list = fold_results_df["Algorithm"].unique().tolist()                  
                    selected_algorithm_list = st.multiselect(label="Select one or more algorithms to plot", options=algorithm_list, default=algorithm_list)
                    
                    # Plotting the graph (by using the "Means" option):
                    if with_fold == 'Means':
                        selected_metric_list = st.multiselect(label="Select one or more metrics to plot", options=metric_list, default=metric_list)
                        # Increasing the maximum value of the Y-axis:
                        increment_yaxis = st.number_input("How to increment the maximum value of the Y-axis", min_value=0.0, max_value=10.0, value=0.5, step=0.1)     
                        # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:
                        df = mean_results_df.loc[mean_results_df['Algorithm'].isin(selected_algorithm_list), ['Algorithm']+selected_metric_list]
                        # Showing graph:               
                        if st.button(label='Show graph'):
                            util.visualize_graph_mean_rs(df, increment_yaxis)
                            with st.expander(label='Data to plot in the graphic'):
                                st.dataframe(df)
                    elif with_fold == 'Folds': # Plotting the graph (by using the "Folds" option):
                        selected_metric = st.selectbox(label="Select one or more metrics to plot", options=metric_list)
                        # Increasing the maximum value of the Y-axis:
                        increment_yaxis = st.number_input("How to increment the maximum value of the Y-axis", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
                        # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:
                        df = fold_results_df.loc[fold_results_df['Algorithm'].isin(selected_algorithm_list), ['Fold', 'Algorithm']+[selected_metric]]                        
                        # Showing graph:               
                        if st.button(label='Show graph'):
                            util.visualize_graph_fold_rs(df, selected_metric, increment_yaxis)
                            with st.expander(label='Data to plot in the graphic'):
                                st.dataframe(df)
            else:
                st.error(st.warning("The rating file has not been uploaded."))
