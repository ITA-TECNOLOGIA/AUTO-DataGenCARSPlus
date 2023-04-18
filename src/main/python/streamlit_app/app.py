# sourcery skip: use-fstring-for-concatenation
import io
import sys
import streamlit as st
import config
import pandas as pd
import altair as alt
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import seaborn as sns
from pathlib import Path
import console
import base64
from datagencars.synthetic_dataset.generate_synthetic_dataset import GenerateSyntheticDataset
from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
sys.path.append("src/main/python")
import datagencars.evaluation.rs_surprise.surprise_helpers as surprise_helpers
import datagencars.evaluation.sklearn_helpers as sklearn_helpers
import datagencars.evaluation.rs_surprise.evaluation as evaluation
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_rating import ExtractStatisticsRating
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_uic import ExtractStatisticsUIC
import datagencars.existing_dataset.label_encoding as label_encoding
import datagencars.existing_dataset.mapping_categorization as mapping_categorization
import datagencars.existing_dataset.binary_ratings as binary_ratings
from streamlit_app import util


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
    st.image(image=config.AUTO_DATAGENCARS_ICON, use_column_width=False, output_format="auto", width=180) # width=200, 
st.markdown("""---""")

# Tool bar:
general_option = st.sidebar.selectbox(label='**Options available:**', options=['Select one option', 'Generate a synthetic dataset', 'Analysis an existing dataset', 'Evaluation of a dataset'])

if general_option == 'Generate a synthetic dataset':
    def generate_schema_file(schema_type):
        value = ''
        schema_text_area = ''     
        attribute_name = ''   
        if is_upload_schema := st.checkbox(f'Upload the {schema_type} schema file', value=True, key='is_upload_schema_'+schema_type):
            with st.expander(f"Upload {schema_type}_schema.conf"):
                if schema_file := st.file_uploader(label='Choose the file:', key=schema_type+'_schema_file'):
                    value = schema_file.getvalue().decode("utf-8")        
        else:
            # [global]   
            value = '[global]'+'\n'
            value += 'type='+schema_type+'\n'
            number_attribute = st.number_input(label='Number of attributes to generate:', value=1, key='number_attribute_'+schema_type)
            value += 'number_attributes='+str(number_attribute)+'\n'
            value += '\n'
            st.markdown("""---""")       

            # [attribute]
            for position in range(1, number_attribute+1):
                st.write('__[attribute'+str(position)+']__')
                value += '[attribute'+str(position)+']'+'\n'
                # name_attribute:     
                attribute_name = st.text_input(label="Attribute's name:", key=schema_type+'_attribute_name_'+str(position))
                value += 'name_attribute_'+str(position)+'='+attribute_name+'\n'
                # generator_type_attribute:
                generator_type = st.selectbox(label='Generator type:', options=['Integer/Float/String/Boolean (following a distribution)', 'Fixed', 'URL', 'Address', 'Date', 'BooleanList'],  key=schema_type+'_generator_type_'+str(position))                
                # type_attribute:
                attribute_type = None
                if generator_type == 'Integer/Float/String/Boolean (following a distribution)':
                    distribution_type = ''             
                    distribution_type = st.selectbox(label='Distribution type:', options=['Random', 'Gaussian'],  key=schema_type+'_distribution_type_'+str(position))
                    value += 'generator_type_attribute_'+str(position)+'='+distribution_type+'AttributeGenerator'+'\n'                              
                    attribute_type = st.selectbox(label='Attribute type:', options=['Integer', 'Float', 'String', 'Boolean'], key=schema_type+'_attribute_type_'+str(position))
                    if attribute_type == 'Integer':
                        # Integer:
                        integer_min = st.number_input(label='Minimum value of the attribute', value=0, key=schema_type+'_integer_min_'+str(position))
                        value += 'minimum_value_attribute_'+str(position)+'='+str(integer_min)+'\n'
                        integer_max = st.number_input(label='Maximum value of the ratings', value=0, key=schema_type+'_integer_max_'+str(position))
                        value += 'maximum_value_attribute_'+str(position)+'='+str(integer_max)+'\n'
                    elif attribute_type == 'Float':
                        # Float:
                        float_min = float(st.number_input(label='Minimum value of the attribute', value=0.0, key=schema_type+'_float_min_'+str(position)))
                        value += 'minimum_value_attribute_'+str(position)+'='+str(float_min)+'\n'
                        float_max = float(st.number_input(label='Maximum value of the ratings', value=0.0, key=schema_type+'_float_max_'+str(position)))
                        value += 'maximum_value_attribute_'+str(position)+'='+str(float_max)+'\n'
                    elif attribute_type == 'String':
                        # String:                        
                        str_text_area = st.empty()                        
                        string_text_area = str_text_area.text_area(label='Introduce new values to the list (split by comma): rainy, cloudy, sunny', key='string_text_area_'+str(position))                                                            
                        # Buttons: export and import values
                        export_button_column, import_area_column = st.columns(2)
                        with export_button_column:
                            file_name = 'str_'+attribute_name+'_possible_value_list.csv'
                            if st.download_button(label='Export list', data=string_text_area, file_name=file_name, key='export_button_'+str(position)):
                                if len(string_text_area) == 0:                                 
                                    st.warning('The file to be exported must not be empty.')
                                else:
                                    st.success('The file has been saved with the name: '+file_name)
                        with import_area_column:
                            if import_file := st.file_uploader(label='Import list', key='import_file'+str(position)):
                                string_text_area = str_text_area.text_area(label='Introduce new values to the list (split by comma):', value=import_file.getvalue().decode("utf-8"), key='import_button_'+str(position))
                        str_possible_value_list = string_text_area.split(',')
                        number_possible_value = len(str_possible_value_list)
                        value += 'number_posible_values_attribute_'+str(position)+'='+str(number_possible_value)+'\n'
                        for i in range(number_possible_value):
                            value += 'posible_value_'+str(i+1)+'_attribute_'+str(position)+'='+str(str_possible_value_list[i]).strip()+'\n'                    
                elif generator_type == 'Fixed':                    
                    attribute_type = st.selectbox(label='Attribute type:', options=['Integer', 'String', 'Boolean'], key='attribute_type_'+str(position)+'_'+generator_type)
                    fixed_input = st.text_input(label='Imput the fixed value:', key='fixed_input_'+str(position))
                    value += 'input_parameter_attribute_'+str(position)+'='+str(fixed_input)+'\n'
                elif generator_type == 'URL':                    
                    attribute_type = st.selectbox(label='Attribute type:', options=['AttributeComposite'], key='attribute_type_'+str(position)+'_'+generator_type)  
                    number_maximum_subattribute = 2
                    value += 'number_maximum_subattribute_attribute_'+str(position)+'='+str(number_maximum_subattribute)+'\n'
                    value += 'name_subattribute_1'+'_attribute_'+str(position)+'=name'+'\n'
                    value += 'name_subattribute_2'+'_attribute_'+str(position)+'=url'+'\n'
                    for idx in range(number_maximum_subattribute):
                        value += 'type_subattribute_'+str(idx+1)+'_attribute_'+str(position)+'=String'+'\n'                    
                    # Generate input parameter file: input_parameter_attribute_1=name_restaurant.csv
                    ip_text_area = st.empty()
                    input_parameter_text_area = ip_text_area.text_area(label='Introduce values (a value by line), keeping the header: <place>', value='place', key='url_ip_text_area_'+str(position))   
                    # Buttons: export and import values  
                    export_button_column, import_area_column = st.columns(2)
                    with export_button_column:
                        file_name = attribute_name+'_input_parameter_list.csv'
                        if st.download_button(label='Export list', data=input_parameter_text_area, file_name=file_name, key='ip_export_button_'+str(position)):
                            if len(input_parameter_text_area) == 0:                                 
                                st.warning('The file to be exported must not be empty.')
                            else:
                                st.success('The file has been saved with the name: '+file_name)
                    with import_area_column:
                        input_parameter_list = []
                        if import_file := st.file_uploader(label='Import list', key='import_file'+str(position)):                                
                            input_parameter_text_area = ip_text_area.text_area(label='Introduce values (a value by line), keeping the header: <place>', value=import_file.getvalue().decode("utf-8"), key='import_url_ip_text_area_'+str(position))                    
                            input_parameter_df=pd.read_csv(io.StringIO(input_parameter_text_area))
                            input_parameter_list = input_parameter_df.astype(str).values.tolist()
                    value += 'input_parameter_attribute_'+str(position)+'='+str(input_parameter_list)+'\n'
                    # Unique value?
                    unique_value = st.checkbox(label='Unique value?:', value=True, key='unique_value_'+str(position)+'_'+generator_type)
                    if unique_value:
                        value += 'unique_value_attribute_'+str(position)+'=True'+'\n'
                    else:
                        value += 'unique_value_attribute_'+str(position)+'=False'+'\n'
                elif generator_type == 'Address':                    
                    attribute_type = st.selectbox(label='Attribute type:', options=['AttributeComposite'], key='attribute_type_'+str(position)+'_'+generator_type)
                    number_maximum_subattribute = 5
                    value += 'number_maximum_subattribute_attribute_'+str(position)+'='+str(number_maximum_subattribute)+'\n'
                    value += 'name_subattribute_1'+'_attribute_'+str(position)+'=street'+'\n'
                    value += 'name_subattribute_2'+'_attribute_'+str(position)+'=number'+'\n'
                    value += 'name_subattribute_3'+'_attribute_'+str(position)+'=zp'+'\n'
                    value += 'name_subattribute_4'+'_attribute_'+str(position)+'=latitude'+'\n'
                    value += 'name_subattribute_5'+'_attribute_'+str(position)+'=longitude'+'\n'
                    for idx in range(number_maximum_subattribute):
                        value += 'type_subattribute_'+str(idx+1)+'_attribute_'+str(position)+'=String'+'\n'                         
                    # Generate input parameter file: input_parameter_attribute_1=name_restaurant.csv
                    ip_text_area = st.empty()
                    input_parameter_text_area = ip_text_area.text_area(label='Introduce address values (line by line), keeping the header: <street,number,zp,latitude,longitude>', value='street,number,zp,latitude,longitude', key='address_ip_text_area_'+str(position))   
                    # Buttons: export and import values  
                    export_button_column, import_area_column = st.columns(2)
                    with export_button_column:
                        file_name = attribute_name+'_input_parameter_list.csv'
                        if st.download_button(label='Export list', data=input_parameter_text_area, file_name=file_name, key='address_ip_export_button_'+str(position)):
                            if len(input_parameter_text_area) == 0:                                 
                                st.warning('The file to be exported must not be empty.')
                            else:
                                st.success('The file has been saved with the name: '+file_name)
                    with import_area_column:
                        input_parameter_list = []
                        import_split = st.text_input(label='Specifies the type of separator to read the file (; , # tab)', key='import_split')
                        if import_file := st.file_uploader(label='Import list', key='import_file'+str(position)):                            
                            input_parameter_text_area = ip_text_area.text_area(label='Introduce address values below <street,number,zp,latitude,longitude> (line by line):', value=import_file.getvalue().decode("utf-8"), key='import_address_ip_text_area_'+str(position))                            
                            input_parameter_df=pd.read_csv(io.StringIO(input_parameter_text_area), sep=import_split)                                                 
                            input_parameter_list = input_parameter_df.astype(str).values.tolist()                        
                    value += 'input_parameter_attribute_'+str(position)+'='+str(input_parameter_list)+'\n'
                elif generator_type == 'Date':                    
                    attribute_type = st.selectbox(label='Attribute type:', options=['Integer'], key='attribute_type_'+str(position)+'_'+generator_type)
                    st.write('Imput the range of dates (years only):')
                    date_min = st.number_input(label='From:', value=1980, key='date_min_'+str(position))
                    value += 'minimum_value_attribute_'+str(position)+'='+str(date_min)+'\n'
                    date_max = st.number_input(label='Until:', value=2020, key='date_max_'+str(position))
                    value += 'maximum_value_attribute_'+str(position)+'='+str(date_max)+'\n'
                elif generator_type == 'BooleanList':                    
                    attribute_type = st.selectbox(label='Attribute type:', options=['List'], key='attribute_type_'+str(position)+'_'+generator_type)
                    component_list = st.text_area(label='Introduce component values to the list (split by comma): monday, tuesday, wednesday, thursday, friday', key='component_list_'+str(position)).split(',')
                    value += 'number_maximum_component_attribute_'+str(position)+'='+str(len(component_list))+'\n'
                    value += 'type_component_attribute_'+str(position)+'=Boolean'+'\n'
                    for idx, component in enumerate(component_list):
                        value += 'component_'+str(idx+1)+'_attribute_'+str(position)+'='+str(component).strip()+'\n'
                    component_input_parameter = st.number_input(label='Number of boolean values to generate for these components:', value=1, key='component_input_parameter')
                    value += 'input_parameter_attribute_'+str(position)+'='+str(component_input_parameter)+'\n'

                value += 'type_attribute_'+str(position)+'='+str(attribute_type)+'\n'
                # Important attributes:                
                is_important_attribute = st.checkbox(label=f'Is {attribute_name} an important attribute to include in the user profile?', value=False, key=schema_type+'_is_important_attribute_'+str(position))
                value += 'important_profile_attribute_'+str(position)+'='+str(is_important_attribute)+'\n'
                if is_important_attribute:
                    # Ranking order:
                    st.write('Examples of importance order:')
                    st.markdown("""- ascending: ``` quality food=[bad, normal, good], global_rating=[1, 5] ``` """)
                    st.markdown("""- descending: ``` quality food=[good, normal, bad], global_rating=[5, 1] ``` """)
                    st.markdown("""- neutral: ``` quality food=[chinese, italian, vegetarian, international] ``` """)
                    ranking_order_original = st.selectbox(label='Select an order of importance?', options=['ascending', 'descending', 'neutral'])
                    ranking_order = 'neut'
                    if ranking_order_original == 'ascending':
                        ranking_order = 'asc'
                    elif ranking_order_original == 'descending':
                        ranking_order = 'desc'
                    value += 'ranking_order_by_attribute_'+str(position)+'='+ranking_order+'\n'
                    value += 'important_weight_attribute_'+str(position)+'=True'+'\n'
                value += '\n'
                st.markdown("""---""")                    
        # Show generated schema file:
        with st.expander(f"Show {schema_type}_schema.conf"):
            sch_text_area = st.empty()
            if st.checkbox(label='Edit file?', key='edit_schema_'+schema_type):
                schema_text_area = sch_text_area.text_area(label='Current file:', value=value, height=500, key=schema_type+'_schema_text_area')
            else:
                schema_text_area = sch_text_area.text_area(label='Current file:', value=value, height=500, disabled=True, key=schema_type+'_schema_text_area')
        link_schema_file = f'<a href="data:text/plain;base64,{base64.b64encode(schema_text_area.encode()).decode()}" download="{schema_type}_schema.conf">Download</a>'
        st.markdown(link_schema_file, unsafe_allow_html=True) 
        return schema_text_area

    context = None
    if with_context := st.sidebar.checkbox('With context', value=True):
        context = True
        tab_generation, tab_user, tab_item, tab_context, tab_user_profile, tab_run  = st.tabs(['Generation', 'Users', 'Items', 'Contexts', 'User profile', 'Run'])
    else:
        context = False
        tab_generation, tab_user, tab_item, tab_user_profile, tab_run = st.tabs(['Generation', 'Users', 'Items', 'User profile', 'Run'])

    # GENERATION SETTINGS:
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
                rating_value += ('minimum_year_timestamp='+str(min_year_ts)+'\n' +
                                'maximum_year_timestamp='+str(max_year_ts)+'\n')            
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
                               
    # USER SETTINGS:
    with tab_user:        
        st.header('Users')
        schema_type = 'user'
        user_schema_value = generate_schema_file(schema_type)

    # ITEM SETTINGS:
    with tab_item:
        st.header('Items')
        schema_type = 'item'
        item_schema_value = generate_schema_file(schema_type)
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
        
    # CONTEXT SETTINGS:
    if context:
        with tab_context:
            st.header('Contexts')
            schema_type = 'context'
            context_schema_value = generate_schema_file(schema_type)

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
                # user_profile_id_list = list(range(1, number_user_profile+1))
                # df['user_profile_id'] = user_profile_id_list
                return df
            
            user_profile_df = get_dataframe()
            # Create row, column, and value inputs:
            col_row, col_col, col_val = st.columns(3)
            with col_row:
                # Choosing the row index:
                row = st.number_input('row (profile)', max_value=user_profile_df.shape[0]) #, value=1
            with col_col:
                # Choosing the column index:
                selected_attribute = st.selectbox(label='column (attribute)', options=attribute_column_list)
                attribute_position = attribute_column_list.index(selected_attribute)                           
                col = attribute_position
                # Getting possible values, in order to facilitate the importance ranking:
                item_possible_value_list = item_access_schema.get_possible_values_attribute_list_from_name(attribute_name=selected_attribute)                
                if with_context:
                    context_possible_value_list = context_access_schema.get_possible_values_attribute_list_from_name(attribute_name=selected_attribute)
                    if (selected_attribute != 'user_profile_id') and (selected_attribute != 'other'):                                 
                        if (len(item_possible_value_list) != 0) and (len(context_possible_value_list) == 0):
                            st.warning(item_possible_value_list)
                        elif (len(item_possible_value_list) == 0) and (len(context_possible_value_list) != 0):
                            st.warning(context_possible_value_list)                   
                else:
                    if (len(item_possible_value_list) != 0):
                        st.warning(item_possible_value_list)                    
            with col_val:   
                # Inserting weight value:
                value = st.text_input(label='weight (with range [0-1])', value=1)                
                # Validating weight values:
                if len(value) == 0:
                    if (selected_attribute == 'user_profile_id'):
                        st.warning('You must insert an ```integer``` value, starting with  ```1```.')
                    else:
                        st.warning('You must insert an ```weight``` value in the range ```[0-1]```.')
                else:
                    # Checking user_profile_id:      
                    if (selected_attribute == 'user_profile_id'):                    
                        # Float number:
                        if ('.' in value) or (',' in value):
                            st.warning('The value of ```user_profile_id``` must not be of type ```float```.')
                        # Negative or Zero numbers:
                        elif (int(value) < 0) or (int(value) == 0):
                            st.warning('The ```user_profile_id``` value must be an ```integer``` and greater than zero (e.g., 1, 2, 3, ...).')  
                        # First value:
                        elif (int(value) > 1 and row == 0):
                            st.warning('The first value of ```user_profile_id``` must start at ```1```.')                    
                    else:
                        # Checking attribute weights:                    
                        # Float number:
                        if ('.' in value) or (',' in value):
                            # Negative number:
                            if float(value) < 0:
                                st.warning('The ```weight``` must be a positive value.')  
                            else:
                                # Range [0-1]:
                                if float(value) > 1.0:
                                    st.warning('The ```weight``` value must be in the range ```[0-1]```.')  
                        else:
                            # Negative number:
                            if int(value) < 0:
                                st.warning('The ```weight``` must be a positive value.')  
                            else:
                                # Range [0-1]:
                                if (int(value) > 1):
                                    st.warning('The ```weight``` value must be positive and in the range ```[0-1]```.')  

            # Change the entry at (row, col) to the given weight value:
            user_profile_df.values[row][col] = str(value)
            # Show the user profile dataframe:
            st.markdown(""" Please, note that the ```user_profile_id``` column must start at ```1```, while the rest of values must be in the range ```[0-1]```.""")
            st.dataframe(user_profile_df)
            # Downloading user_profile.csv:
            link_user_profile = f'<a href="data:file/csv;base64,{base64.b64encode(user_profile_df.to_csv(index=False).encode()).decode()}" download="user_profile.csv">Download</a>'
            st.markdown(link_user_profile, unsafe_allow_html=True)  

    # RUN:
    with tab_run:                   
        col_run, col_stop = st.columns(2)        
        with col_run:
            button_run = st.button(label='Run', key='button_run')
        with col_stop:
            button_stop = st.button(label='Stop', key='button_stop')
        
        generator = GenerateSyntheticDataset(generation_config=generation_config_value)
        output = st.empty()    
        with console.st_log(output.code):
            if button_run:
                    df_zip = []
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
               
elif general_option == 'Analysis an existing dataset':
    is_analysis = st.sidebar.radio(label='Analysis an existing dataset', options=['Data visualization', 'Replicate dataset', 'Extend dataset', 'Recalculate ratings', 'Replace NULL values', 'Generate user profile', 'Ratings to binary', 'Mapping categorization'])
    is_context = st.sidebar.checkbox('With context', value=True)
    
    if is_analysis == 'Data visualization':
        if is_context:
            tab1, tab2, tab3, tab4, tab5 = st.tabs(['Upload dataset', 'Users', 'Items', 'Contexts', 'Ratings'])
        else:
            tab1, tab2, tab3, tab5 = st.tabs(['Upload dataset', 'Users', 'Items', 'Ratings'])                        
        # Upload dataset tab:
        with tab1:
            # Uploading a dataset:
            user_df = util.load_one_file(file_type='user')
            item_df = util.load_one_file(file_type='item')
            if is_context:
                context_df = util.load_one_file(file_type='context')
            rating_df = util.load_one_file(file_type='rating')              
        # Users tab:
        with tab2:
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
                st.warning("The user file (user.csv) has not been uploaded in the 'Uploaded dataset' tab.")
        # Items tab:
        with tab3:
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
                st.warning("The item file (item.csv) has not been uploaded in the 'Uploaded dataset' tab.")
        # Contexts tab:
        if is_context:
            with tab4:
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
                    st.warning("The context file (context.csv) has not been uploaded in the 'Uploaded dataset' tab.")
        # Ratings tab:
        with tab5:
            if not rating_df.empty:
                # try:
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
                    if is_context:
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
                # except Exception as e:
                #     st.error(f"Make sure the rating dataset is in the right format. {e}")
            else:
                st.warning("The rating file (rating.csv) has not been uploaded in the 'Uploaded dataset' tab.")
    elif is_analysis == 'Replicate dataset':
        st.write('TODO')
        # tab1 = st.tabs(['Upload dataset']) 
        # option = st.selectbox('Choose between uploading multiple files or a single file:', ('Multiple files', 'Single file'))
        # if option == 'Multiple files':
        #     data = {} #Dictionary with the dataframes
        #     for file_type in ["user", "item", "context", "rating"]:
        #         if file_type == "context":
        #             if not is_context:
        #                 continue
        #         with st.expander(f"Upload your {file_type}.csv file"):
        #             separator = st.text_input(f"Enter the separator for your {file_type}.csv file (default is ';')", ";")
        #             uploaded_file = st.file_uploader(f"Select {file_type}.csv file", type="csv")
        #             if uploaded_file is not None:
        #                 if not separator:
        #                     st.error('Please provide a separator.')
        #                 else:
        #                     try:
        #                         data = read_uploaded_file(uploaded_file, data, file_type, separator)
        #                         st.dataframe(data[file_type].head())
        #                     except Exception as e:
        #                         st.error(f"An error occurred while reading the {file_type} file: {str(e)}")
        #                         data[file_type] = None
        # elif option == 'Single file':
        #     data = {} #Dictionary with the dataframes
        #     data_file = st.file_uploader("Select the single file", type="csv")
        #     separator = st.text_input("Enter the separator for your single file (default is '	')", "	")
        #     if data_file is not None:
        #         if not separator:
        #             st.error('Please provide a separator.')
        #         else:
        #             try:
        #                 df = pd.read_csv(data_file, sep=separator)
        #                 st.dataframe(df.head())
        #                 def create_dataframe(label, df):
        #                     if columns := st.multiselect(label=f"Select the columns for the {label} dataframe:", options=df.columns):
        #                         # Create a new dataframe with the selected columns
        #                         new_df = df[columns]
        #                         st.dataframe(new_df.head())
        #                         st.session_state[label] = new_df #Save the label dataframe in the session state
        #                         st.download_button(
        #                             label=f"Download {label} dataset CSV",
        #                             data=new_df.to_csv(index=False),
        #                             file_name=f"{label}.csv",
        #                             mime='text/csv'
        #                         )
        #                         return new_df
        #                 data = {'user': create_dataframe('user', df),
        #                         'item': create_dataframe('item', df),
        #                         'rating': create_dataframe('rating', df)}
        #                 if is_context:
        #                     data['context'] = create_dataframe('context', df)
        #             except Exception as e:
        #                 st.error(f"An error occurred while reading the file: {str(e)}")
    elif is_analysis == 'Extend dataset':
        st.write('TODO')
    elif is_analysis == 'Recalculate ratings':
        st.write('TODO')
    elif is_analysis == 'Replace NULL values':
        st.write('TODO')
    elif is_analysis == 'Generate user profile':
        st.write('TODO')
    elif is_analysis == 'Ratings to binary':
        st.title("Rating Binarization")
        with st.expander(label='Help information'):
            st.write('This tool allows you to convert ratings to binary values. For example, if you have a dataset with ratings from 1 to 5, you can convert them to 0 and 1, where 0 represents a negative rating and 1 a positive one.')
            st.write('The tool will convert the ratings to binary values using a threshold. For example, if you set the threshold to 3, all ratings equal or greater than 3 will be converted to 1, and all ratings less than 3 will be converted to 0.')
        def ratings_to_binary(df, threshold=3):
            def binary_rating(rating):
                return 1 if rating >= threshold else 0
            df['rating'] = df['rating'].apply(binary_rating)
            return df
        st.write("Upload a CSV file containing ratings to convert them to binary values.")
        delimiter = st.text_input("CSV delimiter", ";")
        uploaded_file = st.file_uploader("Choose a file")

        if uploaded_file is not None:
            df_ratings = pd.read_csv(uploaded_file, delimiter=delimiter)
            min_rating = df_ratings['rating'].min()
            max_rating = df_ratings['rating'].max()
            threshold = st.number_input(f"Binary threshold (range from {min_rating} to {max_rating})", min_value=min_rating, max_value=max_rating, value=3)
            df_binary = ratings_to_binary(df_ratings, threshold)
            st.write("Converted ratings:")
            st.write(df_binary)
            st.download_button(
                label="Download binary ratings CSV",
                data=df_binary.to_csv(index=False),
                file_name=Path(uploaded_file.name).stem + "_binary.csv",
                mime='text/csv'
            )
    elif is_analysis == 'Mapping categorization':
        option = st.radio(options=['From numerical to categorical', 'From categorical to numerical'], label='Select an option')
        if option == 'From numerical to categorical':
            st.title("Category Encoding")
            with st.expander(label='Help information'):
                st.write("This tool allows you to convert numerical values to categorical values. For example, you can convert the numerical values of a rating scale to the corresponding categories of the scale (e.g. 1-2 -> Bad, 3-4 -> Average, 5 -> Good).")
                st.write("To use this tool, you need to upload a CSV file containing the numerical values to convert. Then, you need to specify the mapping for each numerical value. For example, you could to specify the following mappings: numerical values 1, 2, 3, 4 and 5 to categories Bad, Average, Good, Very good and Excellent, respectively.")
                st.write("Objects and datetime values are ignored.")
            st.write("Upload a CSV file containing numerical values to convert them to categorical values.")
            uploaded_file = st.file_uploader("Choose a file")
            delimiter = st.text_input("CSV delimiter", '\t')
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file, delimiter=delimiter)
                include_nan = st.checkbox("Include NaN values")
                mappings = {}
                for col in df.columns:
                    if 'id' not in col.lower() and not pd.api.types.is_datetime64_dtype(df[col]) and not pd.api.types.is_object_dtype(df[col]): # Ignore ID, object and datetime columns
                        unique_values = sorted(df[col].unique())
                        st.write(f"Unique values in {col}: {', '.join(map(str, unique_values))}")
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
                        mappings[col] = col_mappings
                st.markdown("""---""")
                st.write("Mappings:", mappings)
                if st.button("Generate categorized dataframe"):
                    categorized_df = mapping_categorization.apply_mappings(df, mappings)
                    st.header("Categorized dataset:")
                    st.write(categorized_df)
                    st.download_button(
                        label="Download categorized dataset CSV",
                        data=categorized_df.to_csv(index=False),
                        file_name=Path(uploaded_file.name).stem + "_categorized.csv",
                        mime='text/csv'
                    )
        else:
            st.title("Label Encoding")
            with st.expander(label='Help information'):
                st.write("Label encoding is a process of transforming categorical values into numerical values.")
                st.write("For example, you can convert the categorical values of a rating scale to the corresponding numerical values of the scale (e.g. Bad -> 1, Average -> 2, Good -> 3, Very good -> 4, Excellent -> 5).")
                st.write("To use this tool, you need to upload a CSV file containing the categorical values to convert. Then, you need to select the categorical columns to convert.")
            st.write("Upload a CSV file containing categorical values to convert them to numerical values.")
            uploaded_file = st.file_uploader("Choose a file")
            delimiter = st.text_input("CSV delimiter", '\t')
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file, delimiter=delimiter)
                categorical_cols = [col for col in df.select_dtypes(exclude=[np.number]) if 'id' not in col.lower()]
                if categorical_cols:
                    selected_cols = st.multiselect("Select categorical columns to label encode:", categorical_cols)
                    if selected_cols:
                        if st.button("Encode categorical columns"):
                            encoded_df = label_encoding.apply_label_encoder(df, selected_cols)
                            st.header("Encoded dataset:")
                            st.write(encoded_df)
                            st.download_button(
                                label="Download encoded dataset CSV",
                                data=encoded_df.to_csv(index=False),
                                file_name=Path(uploaded_file.name).stem + "_encoded.csv",
                                mime='text/csv'
                            )
                else:
                    st.write("No categorical columns found.")
elif general_option == 'Evaluation of a dataset':
    def select_params(algorithm):
        if algorithm == "SVD":
            return {"n_factors": st.sidebar.number_input("Number of factors", min_value=1, max_value=1000, value=100, key='n_factors_svd'),
                    "n_epochs": st.sidebar.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_svd'),
                    "lr_all": st.sidebar.number_input("Learning rate for all parameters", min_value=0.0001, max_value=1.00, value=0.005, step=0.0001, key='lr_all_svd'),
                    "reg_all": st.sidebar.number_input("Regularization term for all parameters", min_value=0.0001, max_value=1.00, value=0.02, key='reg_all_svd')}
        if algorithm == "KNNBasic":
            return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnbasic'),
                    "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["cosine", "msd", "pearson"], key='sim_options_knnbasic'),
                                    "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnbasic')}}
        if algorithm == "BaselineOnly":
            return {"bsl_options": {"method": st.sidebar.selectbox("Baseline method", ["als", "sgd"], key='method_baselineonly'),
                                    "reg_i": st.sidebar.number_input("Regularization term for item parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_i_baselineonly'),
                                    "reg_u": st.sidebar.number_input("Regularization term for user parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_u_baselineonly')}}
        if algorithm == "CoClustering":
            return {"n_cltr_u": st.sidebar.number_input("Number of clusters for users", min_value=1, max_value=1000, value=5),
                    "n_cltr_i": st.sidebar.number_input("Number of clusters for items", min_value=1, max_value=1000, value=5)}
        if algorithm == "KNNBaseline":
            return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnbaseline'),
                    "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["cosine", "msd", "pearson"], key='sim_options_knnbaseline'),
                                    "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnbaseline')},
                    "bsl_options": {"method": st.sidebar.selectbox("Baseline method", ["als", "sgd"], key='method_knnbaseline'),
                                    "reg_i": st.sidebar.number_input("Regularization term for item parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_i_knnbaseline'),
                                    "reg_u": st.sidebar.number_input("Regularization term for user parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_u_knnbaseline')}}
        if algorithm == "KNNWithMeans":
            return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnwithmeans'),
                    "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["cosine", "msd", "pearson"], key='sim_options_knnwithmeans'),
                                    "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnwithmeans')}}
        if algorithm == "NMF":
            return {"n_factors": st.sidebar.number_input("Number of factors", min_value=1, max_value=1000, value=100, key='n_factors_nmf'),
                    "n_epochs": st.sidebar.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_nmf'),
                    "reg_pu": st.sidebar.number_input("Regularization term for user factors", min_value=0.0001, max_value=1.0, value=0.02),
                    "reg_qi": st.sidebar.number_input("Regularization term for item factors", min_value=0.0001, max_value=1.0, value=0.02)}
        if algorithm == "NormalPredictor":
            return {}
        if algorithm == "SlopeOne":
            return {}
        if algorithm == "SVDpp":
            return {"n_factors": st.sidebar.number_input("Number of factors", min_value=1, max_value=1000, value=100, key='n_factors_svdpp'),
                    "n_epochs": st.sidebar.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_svdpp'),
                    "lr_all": st.sidebar.number_input("Learning rate for all parameters", min_value=0.0001, max_value=1.0, value=0.005, key='lr_all_svdpp'),
                    "reg_all": st.sidebar.number_input("Regularization term for all parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_all_svdpp')}

    def select_params_contextual(algorithm):
        if algorithm == "KNeighborsClassifier":
            return {"n_neighbors": st.sidebar.number_input("Number of neighbors", min_value=1, max_value=1000, value=5, key='n_neighbors_kneighborsclassifier'),
                    "weights": st.sidebar.selectbox("Weights", ["uniform", "distance"], key='weights_kneighborsclassifier'),
                    "algorithm": st.sidebar.selectbox("Algorithm", ["auto", "ball_tree", "kd_tree", "brute"], key='algorithm_kneighborsclassifier'),
                    "leaf_size": st.sidebar.number_input("Leaf size", min_value=1, max_value=1000, value=30, key='leaf_size_kneighborsclassifier'),
                    "p": st.sidebar.number_input("P", min_value=1, max_value=1000, value=2, key='p_kneighborsclassifier'),
                    "metric": st.sidebar.selectbox("Metric", ["minkowski", "euclidean", "manhattan", "chebyshev", "seuclidean", "mahalanobis", "wminkowski", "haversine"], key='metric_kneighborsclassifier'),
                    "n_jobs": st.sidebar.number_input("Number of jobs", min_value=1, max_value=1000, value=1, key='n_jobs_kneighborsclassifier')}
        elif algorithm == "SVC":
            return {"C": st.sidebar.number_input("C", min_value=0.0001, max_value=1000.0, value=1.0, key='C_svc'),
                    "kernel": st.sidebar.selectbox("Kernel", ["linear", "poly", "rbf", "sigmoid", "precomputed"], key='kernel_svc'),
                    "degree": st.sidebar.number_input("Degree", min_value=1, max_value=1000, value=3, key='degree_svc'),
                    "gamma": st.sidebar.selectbox("Gamma", ["scale", "auto"], key='gamma_svc'),
                    "coef0": st.sidebar.number_input("Coef0", min_value=0.0, max_value=1000.0, value=0.0, key='coef0_svc'),
                    "shrinking": st.sidebar.checkbox("Shrinking?", key='shrinking_svc'),
                    "probability": st.sidebar.checkbox("Probability?", key='probability_svc'),
                    "tol": st.sidebar.number_input("Tol", min_value=0.0001, max_value=1000.0, value=0.001, key='tol_svc'),
                    "cache_size": st.sidebar.number_input("Cache size", min_value=0.0001, max_value=1000.0000, value=200.0000, key='cache_size_svc'),
                    "class_weight": st.sidebar.selectbox("Class weight", ["balanced", None], key='class_weight_svc'),
                    "verbose": st.sidebar.checkbox("Verbose?", key='verbose_svc'),
                    "max_iter": st.sidebar.number_input("Maximum iterations", min_value=-1, max_value=1000, value=-1, key='max_iter_svc'),
                    "decision_function_shape": st.sidebar.selectbox("Decision function shape", ["ovo", "ovr"], key='decision_function_shape_svc'),
                    "random_state": st.sidebar.number_input("Random state", min_value=-0.5, max_value=1000.0, value=-0.5, key='random_state_svc'),
                    "break_ties": st.sidebar.checkbox("Break ties?", key='break_ties_svc')}
        elif algorithm == "GaussianNB":
            return {}
        elif algorithm == "RandomForestClassifier":
            return {"n_estimators": st.sidebar.number_input("Number of estimators", min_value=1, max_value=1000, value=100, key='n_estimators_randomforestclassifier'),
                    "criterion": st.sidebar.selectbox("Criterion", ["gini", "entropy"], key='criterion_randomforestclassifier'),
                    "max_depth": st.sidebar.number_input("Maximum depth", min_value=-0.5, max_value=1000.0, value=-0.5, key='max_depth_randomforestclassifier'),
                    "min_samples_split": st.sidebar.number_input("Minimum samples split", min_value=1, max_value=1000, value=2, key='min_samples_split_randomforestclassifier'),
                    "min_samples_leaf": st.sidebar.number_input("Minimum samples leaf", min_value=1, max_value=1000, value=1, key='min_samples_leaf_randomforestclassifier'),
                    "min_weight_fraction_leaf": st.sidebar.number_input("Minimum weight fraction leaf", min_value=0.0001, max_value=1.0, value=0.01, key='min_weight_fraction_leaf_randomforestclassifier'),
                    "max_features": st.sidebar.selectbox("Maximum features", ["auto", "sqrt", "log2", None], key='max_features_randomforestclassifier'),
                    "max_leaf_nodes": st.sidebar.number_input("Maximum leaf nodes", min_value=-0.5, max_value=1000.0, value=-0.5, key='max_leaf_nodes_randomforestclassifier'),
                    "min_impurity_decrease": st.sidebar.number_input("Minimum impurity decrease", min_value=0.0001, max_value=1.0, value=0.01, key='min_impurity_decrease_randomforestclassifier'),
                    "bootstrap": st.sidebar.checkbox("Bootstrap?", key='bootstrap_randomforestclassifier'),
                    "oob_score": st.sidebar.checkbox("OOB score?", key='oob_score_randomforestclassifier'),
                    "n_jobs": st.sidebar.number_input("Number of jobs", min_value=-0.5, max_value=1000.0, value=-0.5, key='n_jobs_randomforestclassifier'),
                    "random_state": st.sidebar.number_input("Random state", min_value=-0.5, max_value=1000.0, value=-0.5, key='random_state_randomforestclassifier'),
                    "verbose": st.sidebar.number_input("Verbose", min_value=0, max_value=1000, value=0, key='verbose_randomforestclassifier'),
                    "ccp_alpha": st.sidebar.number_input("CCP alpha", min_value=0.0001, max_value=1.0, value=0.01, key='ccp_alpha_randomforestclassifier'),
                    "class_weight": st.sidebar.selectbox("Class weight", ["balanced", "balanced_subsample", None], key='class_weight_randomforestclassifier'),
                    "max_samples": st.sidebar.number_input("Maximum samples", min_value=-0.5, max_value=1.0, value=-0.5, key='max_samples_randomforestclassifier'),
                    "warm_start": st.sidebar.checkbox("Warm start?", key='warm_start_randomforestclassifier')}
        elif algorithm == "KMeans":
            return {"n_clusters": st.sidebar.number_input("Number of clusters", min_value=1, max_value=1000, value=5, key='n_clusters_kmeans'),
                    "init": st.sidebar.selectbox("Initialization method", ["k-means++", "random"], key='init_kmeans'),
                    "n_init": st.sidebar.number_input("Number of initializations", min_value=1, max_value=1000, value=10, key='n_init_kmeans'),
                    "max_iter": st.sidebar.number_input("Maximum number of iterations", min_value=1, max_value=1000, value=300, key='max_iter_kmeans'),
                    "tol": st.sidebar.number_input("Tolerance", min_value=0.0001, max_value=1.0, value=0.0001, key='tol_kmeans')}
        elif algorithm == "HistGradientBoostingClassifier":
            return {"learning_rate": st.sidebar.slider("Learning rate", 0.01, 1.0, 0.1, step=0.01),
                    "max_iter": st.sidebar.slider("Max number of iterations", 10, 1000, 100, step=10),
                    "max_leaf_nodes": st.sidebar.slider("Max leaf nodes", 10, 200, 31, step=1),
                    "max_depth": st.sidebar.slider("Max depth", 1, 50, 15, step=1),
                    "l2_regularization": st.sidebar.slider("L2 regularization", 0.0, 1.0, 0.0, step=0.01)}
        
    def select_split_strategy(strategy):
        if strategy == "KFold":
            return {"n_splits": st.sidebar.number_input("Number of splits", min_value=2, max_value=10, value=5),
                    "shuffle": st.sidebar.checkbox("Shuffle?")}
        elif strategy == "RepeatedKFold":
            return {"n_splits": st.sidebar.number_input("Number of splits", min_value=2, max_value=10, value=5),
                    "n_repeats": st.sidebar.number_input("Number of repeats", min_value=1, max_value=10, value=1),
                    "shuffle": st.sidebar.checkbox("Shuffle?")}
        elif strategy == "ShuffleSplit":
            return {"n_splits": st.sidebar.number_input("Number of splits", min_value=2, max_value=10, value=5),
                    "test_size": st.sidebar.number_input("Test size", min_value=0.1, max_value=0.9, step=0.1, value=0.2),
                    "random_state": st.sidebar.number_input("Random state", min_value=0, max_value=100, value=42)}
        elif strategy == "LeaveOneOut":
            return {}
        elif strategy == "PredefinedKFold":
            return {"folds_file": st.sidebar.file_uploader("Upload folds file")}
        elif strategy == "train_test_split":
            return {"test_size": st.sidebar.number_input("Test size", min_value=0.1, max_value=0.9, step=0.1, value=0.2),
                    "random_state": st.sidebar.number_input("Random state", min_value=0, max_value=100, value=42)}
        
    def select_split_strategy_contextual(strategy):
        if strategy == "ShuffleSplit":
            n_splits = st.sidebar.number_input("Number of splits", 2, 100, 10)
            train_size = st.sidebar.slider("Train set size (0.0 to 1.0)", 0.01, 1.0, 0.2, step=0.01)
            random_state = st.sidebar.number_input("Random state", 0, 100, 42)
            return {"n_splits": n_splits, "train_size": train_size, "random_state": random_state}
        elif strategy == "KFold":
            n_splits = st.sidebar.number_input("Number of folds", 2, 100, 5)
            random_state = st.sidebar.number_input("Random state (KFold)", 0, 100, 42)
            return {"n_splits": n_splits, "random_state": random_state}
        elif strategy == "LeaveOneOut":
            return {}
        elif strategy == "RepeatedKFold":
            n_splits = st.sidebar.number_input("Number of folds (RepeatedKFold)", 2, 100, 5)
            n_repeats = st.sidebar.number_input("Number of repetitions", 1, 100, 10)
            random_state = st.sidebar.number_input("Random state (RepeatedKFold)", 0, 100, 42)
            return {"n_splits": n_splits, "n_repeats": n_repeats, "random_state": random_state}
        elif strategy == "train_test_split":
            test_size = st.sidebar.slider("Test set size (train_test_split, 0.0 to 1.0)", 0.01, 1.0, 0.2, step=0.01)
            random_state = st.sidebar.number_input("Random state (train_test_split)", 0, 100, 42)
            return {"test_size": test_size, "random_state": random_state}

    def evaluate_algo(algo_list, strategy_instance, metrics, data):
        results = []
        fold_counter = {} # To count the number of folds for each algorithm
        fold_count = 0
        with st.spinner("Evaluating algorithms..."):
            for algo in algo_list:
                fold_count += 1
                cross_validate_results = evaluation.cross_validate(algo, data, measures=metrics, cv=strategy_instance)
                for i in range(strategy_instance.n_splits):
                    row = {}
                    algo_name = type(algo).__name__
                    row["Algorithm"] = algo_name

                    # Modify the name of the metrics to be more readable
                    for key, value in cross_validate_results.items():
                        if key == "fit_time":
                            row["Time (train)"] = value[i]
                        elif key == "test_time":
                            row["Time (test)"] = value[i]
                        elif key == "test_f1_score":
                            row["F1_Score"] = value[i]
                        elif key == "test_recall":
                            row["Recall"] = value[i]
                        elif key == "test_precision":
                            row["Precision"] = value[i]
                        elif key == "test_auc_roc":
                            row["AUC-ROC"] = value[i]
                        else:
                            row[key.replace("test_", "").upper()] = value[i]
                        
                    if algo_name in fold_counter:
                        fold_counter[algo_name] += 1
                    else:
                        fold_counter[algo_name] = 1
                    row["Fold"] = fold_counter[algo_name]

                    results.append(row)
        df = pd.DataFrame(results)
        cols = ["Fold"] + [col for col in df.columns if col != "Fold"] # Move the "Fold" column to the first position
        df = df[cols]
        return df

    def visualize_results_algo(df, algorithm):
        # Show the mean of the metrics for the chosen algorithm
        df_algo = df[df["Algorithm"] == algorithm].drop(["Algorithm", "Fold"], axis=1)
        st.write(f"**{algorithm}** mean")
        st.write(df_algo.mean())

        # Filter the dataframe for the chosen algorithm
        filtered_df = df[df["Algorithm"] == algorithm]

        # Create the line chart
        fig = go.Figure()
        for metric in [col for col in df.columns if col not in ["Algorithm", "Fold", "Time (train)", "Time (test)"]]:
            # Create a trace for the current metric
            fig.add_trace(go.Scatter(
                x=filtered_df["Fold"],
                y=filtered_df[metric],
                name=metric
            ))

        fig.update_layout(
            xaxis_title="Fold",
            yaxis_title="Value",
            legend=dict(title="Metrics")
        )
        st.plotly_chart(fig, use_container_width=True)

    def visualize_results_metric(df, metric):
        # Show the mean of the metrics for each algorithm
        df_metric = df.pivot(index="Fold", columns="Algorithm", values=metric)
        st.write(f"**{metric} mean**")
        st.write(df_metric.mean())

        algorithms = df["Algorithm"].unique()
        fig = go.Figure()
        for algorithm in algorithms:
            # Filter the dataframe for the current algorithm
            filtered_df = df[df["Algorithm"] == algorithm]

            # Create the line chart for the current metric
            fig.add_trace(go.Scatter(
                x=filtered_df["Fold"],
                y=filtered_df[metric],
                name=algorithm
            ))
        fig.update_layout(
            xaxis_title="Fold",
            yaxis_title="Value",
            legend=dict(title="Algorithms")
        )
        st.plotly_chart(fig, use_container_width=True)

    def visualize_results_combined(df, algorithms, metrics, selected_users):
        filtered_df = df[df["Algorithm"].isin(algorithms)]
        fig = go.Figure()
        for algorithm in algorithms:
            for metric in metrics:
                if "All users" in selected_users:
                    users = df["User"].unique()
                    algo_filtered_df = filtered_df[(filtered_df["Algorithm"] == algorithm) & (filtered_df["User"].isin(users))]
                    mean_values = []
                    for fold in algo_filtered_df["Fold"].unique():
                        fold_filtered_df = algo_filtered_df[algo_filtered_df["Fold"] == fold]
                        mean_value = fold_filtered_df[metric].mean()
                        mean_values.append(mean_value)
                    fig.add_trace(go.Scatter(
                        x=algo_filtered_df["Fold"].unique(),
                        y=mean_values,
                        name=f"{algorithm} - {metric} - All users",
                        mode="markers+lines"
                    ))
                else:
                    for user in selected_users:
                        algo_user_filtered_df = filtered_df[(filtered_df["Algorithm"] == algorithm) & (filtered_df["User"] == user)]
                        fig.add_trace(go.Scatter(
                            x=algo_user_filtered_df["Fold"],
                            y=algo_user_filtered_df[metric],
                            name=f"{algorithm} - {metric} - User {user}",
                            mode="markers+lines"
                        ))
        fig.update_layout(
            xaxis=dict(
                title="Fold",
                dtick=1,
                tickmode='linear'
            ),
            yaxis_title="Performance",
            legend=dict(title="Measures of performance")
        )
        st.plotly_chart(fig, use_container_width=True)

    def visualize_mean_evaluation_bar(df, algorithms, metrics, selected_users):
        fig = go.Figure()
        for algorithm in algorithms:
            filtered_df = df[df["Algorithm"] == algorithm]
            for metric in metrics:
                if "All users" in selected_users:
                    users = df["User"].unique()
                    user_label = "All users"
                    user_filtered_df = filtered_df[filtered_df["User"].isin(users)]
                    mean_value = user_filtered_df[metric].mean()
                    fig.add_trace(go.Bar(
                        x=[f"{metric}"],
                        y=[mean_value],
                        name=f"{algorithm} - {user_label}",
                        legendgroup=f"{algorithm} - {user_label}"
                    ))
                else:
                    for user in selected_users:
                        user_filtered_df = filtered_df[filtered_df["User"] == user]
                        mean_value = user_filtered_df[metric].mean()
                        fig.add_trace(go.Bar(
                            x=[f"{metric}"],
                            y=[mean_value],
                            name=f"{algorithm} - User {user}",
                            legendgroup=f"{algorithm} - User {user}"
                        ))
        fig.update_layout(
            xaxis_title="Measures of performance",
            yaxis_title="Performance",
            legend=dict(title="Algorithms & Users"),
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)

    def select_columns(df, label):
        column_names = df.columns.tolist()
        selected_columns = st.sidebar.multiselect(f'Select features ({label}):', column_names, column_names)
        if selected_columns:
            return df[selected_columns]
        
    def replace_with_none(params):
        for key, value in params.items():
            if value == -0.5:
                params[key] = None
        return params

    st.sidebar.title('Evaluation of a dataset')
    # Load the user, item, context rating files from streamlit session state
    if "rating" in st.session_state:
        rating_df = st.session_state["rating"]
    if "item" in st.session_state:
        item_df = st.session_state["item"]
    if "context" in st.session_state:
        context_df = st.session_state["context"]

    if st.sidebar.checkbox("With context", value=True):
        if "rating" in st.session_state and "item" in st.session_state and "context" in st.session_state:
            st.sidebar.header("Paradigm selection")
            paradigm = st.sidebar.selectbox("Select one paradigm", ["Contextual Modeling", "Pre-filtering", "Post-filtering"])
            if paradigm == "Contextual Modeling":
                st.sidebar.header("Features selection")
                features_item = select_columns(item_df, "item")
                features_context = select_columns(context_df, "context")
                try:
                    merged_df = rating_df.merge(features_item, on='item_id').merge(features_context, on='context_id')
                except KeyError as e:
                    st.error(f"The rating, user, item and context datasets don´t have '_id' columns in common. {e}")
                st.sidebar.header("Algorithm selection")
                algorithms = st.sidebar.multiselect("Select one or more algorithms", ["KNeighborsClassifier", "SVC", "GaussianNB", "RandomForestClassifier", "KMeans", "HistGradientBoostingClassifier"], default="KNeighborsClassifier")

                algo_list = []
                st.sidebar.write("-0.5 values will be replaced with None")
                for algorithm in algorithms:
                    algo_params = replace_with_none(select_params_contextual(algorithm))
                    algo_instance = sklearn_helpers.create_algorithm(algorithm, algo_params)
                    algo_list.append(algo_instance)
                    st.sidebar.markdown("""---""")
                st.sidebar.header("Split strategy selection")
                strategy = st.sidebar.selectbox("Select a strategy", ["ShuffleSplit", "KFold", "LeaveOneOut", "RepeatedKFold", "train_test_split"])
                strategy_params = select_split_strategy_contextual(strategy)
                strategy_instance = sklearn_helpers.create_split_strategy(strategy, strategy_params)
                st.sidebar.header("Metrics selection")
                metrics = st.sidebar.multiselect("Select the metrics to calculate", config.SCIKIT_LEARN_METRICS, default="Precision")
                st.sidebar.header("Target user")
                # Extract unique user_ids and add "All users" option
                user_ids = sorted(rating_df['user_id'].unique())
                user_options = ["All users"] + user_ids
                selected_users = st.sidebar.multiselect("Select one or more users or 'All users'", options=user_options, default="All users")

                if st.sidebar.button("Evaluate"):
                    if "All users" in selected_users:
                        target_user_ids = None
                    else:
                        target_user_ids = selected_users
                    results_contextual_df = sklearn_helpers.evaluate(merged_df, algo_list, strategy_instance, metrics, target_user_ids)
                    st.session_state["results_contextual"] = results_contextual_df #Save the results dataframe in the session state
                if "results_contextual" in st.session_state:
                    results_contextual = st.session_state["results_contextual"]
                    st.header("Evaluation Results")
                    
                    st.subheader("Mean evaluation results")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        algorithms = results_contextual["Algorithm"].unique()
                        selected_algorithm = st.multiselect("Select an algorithm", algorithms)
                    with col2:
                        metrics = results_contextual.columns[3:]
                        selected_metric = st.multiselect("Select a metric", metrics)
                    with col3:
                        users = results_contextual["User"].unique().tolist()  # Convert numpy array to a Python list
                        users.insert(0, "All users")  # Insert "All users" at the beginning of the list
                        selected_users_1 = st.multiselect("Select a user", users)
                    
                    visualize_mean_evaluation_bar(results_contextual, selected_algorithm, selected_metric, selected_users_1)
                    mean_df = results_contextual.copy()
                    mean_df.drop(columns=[col for col in ['Fold'] if col in mean_df.columns], inplace=True) #Delete the 'Fold' column if it exists in the DataFrame
                    mean_df = mean_df.groupby(['Algorithm', 'User'], as_index=False).mean()  # Calculate the mean value of the metrics for each classification algorithm and user separately
                    st.write("Detailed results:")
                    st.dataframe(mean_df)
                    link_results_mean = f'<a href="data:file/csv;base64,{base64.b64encode(mean_df.to_csv(index=False).encode()).decode()}" download="results_contextual_mean.csv">Download</a>'
                    st.markdown(link_results_mean, unsafe_allow_html=True)

                    st.subheader("Fold evaluation results")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        algorithms = results_contextual["Algorithm"].unique()
                        selected_algorithms = st.multiselect("Select algorithms to plot", algorithms)
                    with col2:
                        metrics = results_contextual.columns[3:]
                        selected_metrics = st.multiselect("Select metrics to plot", metrics)
                    with col3:
                        users = results_contextual["User"].unique().tolist()  # Convert numpy array to a Python list
                        users.insert(0, "All users")  # Insert "All users" at the beginning of the list
                        selected_users2 = st.multiselect("Select users to filter", users)
                    
                    visualize_results_combined(results_contextual, selected_algorithms, selected_metrics, selected_users2)
                    st.write("Detailed results:")
                    st.dataframe(results_contextual)
                    link_results_contextual = f'<a href="data:file/csv;base64,{base64.b64encode(results_contextual.to_csv(index=False).encode()).decode()}" download="results_contextual.csv">Download</a>'
                    st.markdown(link_results_contextual, unsafe_allow_html=True)
            else:
                st.write("TODO: pre-filtering and post-filtering")
        else:
            st.error("No rating, item or context datasets loaded.")
    else:
        if "rating" in st.session_state:
            st.sidebar.header("Algorithm selection")
            algorithms = st.sidebar.multiselect("Select one or more algorithms", ["BaselineOnly", "CoClustering", "KNNBaseline", "KNNBasic", "KNNWithMeans", "NMF", "NormalPredictor", "SlopeOne", "SVD", "SVDpp"], default="SVD")
            algo_list = []
            for algorithm in algorithms:
                algo_params = select_params(algorithm)
                algo_instance = surprise_helpers.create_algorithm(algorithm, algo_params)
                algo_list.append(algo_instance)
                st.sidebar.markdown("""---""")

            st.sidebar.header("Split strategy selection")
            strategy = st.sidebar.selectbox("Select a strategy", ["KFold", "RepeatedKFold", "ShuffleSplit", "LeaveOneOut", "PredefinedKFold", "train_test_split"])
            strategy_params = select_split_strategy(strategy)
            strategy_instance = surprise_helpers.create_split_strategy(strategy, strategy_params)

            data = surprise_helpers.convert_to_surprise_dataset(rating_df)

            st.sidebar.header("Metrics selection")
            if binary_ratings.is_binary_rating(rating_df):
                metrics = st.sidebar.multiselect("Select one or more cross validation binary metrics", ["Precision", "Recall", "F1_Score", "AUC_ROC"], default="Precision")
            else:
                metrics = st.sidebar.multiselect("Select one or more cross validation non-binary metrics", ["RMSE", "MSE", "MAE", "FCP", "Precision", "Recall", "F1_Score", "MAP", "NDCG"], default="MAE")

            if st.sidebar.button("Evaluate"):
                results_df = evaluate_algo(algo_list, strategy_instance, metrics, data)
                st.session_state["results"] = results_df #Save the results dataframe in the session state

            if "results" in st.session_state:
                results_df = st.session_state["results"]
                st.subheader("Detailed results")

                st.dataframe(results_df)
                st.download_button(
                    label="Download results",
                    data=results_df.to_csv(index=False),
                    file_name="results.csv",
                    mime="text/csv"
                )

                st.header("Evaluation Results")
                st.subheader("Algorithm evaluation results")
                algorithms = results_df["Algorithm"].unique()
                algorithm = st.selectbox("Select an algorithm to plot", algorithms)
                visualize_results_algo(results_df, algorithm)

                st.subheader("Metric evaluation results")
                metrics = results_df.columns[2:]
                metric = st.selectbox("Select a metric to plot", metrics)
                visualize_results_metric(results_df, metric)
        else:
            st.error("No rating dataset loaded.")
