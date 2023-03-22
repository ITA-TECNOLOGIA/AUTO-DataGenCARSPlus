# sourcery skip: use-fstring-for-concatenation
import io
import sys
import streamlit as st
import config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import altair as alt
import seaborn as sns
from pathlib import Path
import console
from datagencars.synthetic_dataset.generate_synthetic_dataset import GenerateSyntheticDataset
from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
sys.path.append("src/main/python")
import datagencars.evaluation.rs_surprise.surprise_helpers as surprise_helpers
import datagencars.evaluation.rs_surprise.evaluation as evaluation
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_rating import ExtractStatisticsRating as extract_statistics_rating
from datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_uic import ExtractStatisticsUIC as extract_statistics_uic
import datagencars.existing_dataset.label_encoding as label_encoding
import datagencars.existing_dataset.mapping_categorization as mapping_categorization
import datagencars.existing_dataset.binary_ratings as binary_ratings

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
    st.title('AUTO-DataGenCARS')
    # Description:
    st.write('DataGenCARS is a complete Java-based synthetic dataset generator for the evaluation of Context-Aware Recommendation Systems (CARS) to obtain the required datasets for any type of scenario desired.')
with col2:    
    # Icon:
    st.image(image=config.AUTO_DATAGENCARS_ICON, use_column_width=False, output_format="auto") # width=200, 
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
        st.download_button(label='Download', data=schema_text_area, file_name=schema_type+'_schema.conf')
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
        st.download_button(label='Download', data=config_file_text_area, file_name='generation_config.conf')  
                               
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
        st.download_button(label='Download', data=item_profile_text_area, file_name='item_profile.conf')
      
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
            st.download_button(label='Download', data=user_profile_df.to_csv(index=False).encode('utf-8'), file_name='user_profile.csv')

    # RUN:
    with tab_run:                   
        col_run, col_stop = st.columns(2)        
        with col_run:
            button_run = st.button(label='Run', key='button_run')
            spinner = st.spinner(text = 'Generating data')

        with col_stop:
            button_stop = st.button(label='Stop', key='button_stop')
        
        generator = GenerateSyntheticDataset(generation_config=generation_config_value)
        output = st.empty()    
        with console.st_log(output.code):
            if button_run:
                    if context:
                        steps = 4
                    else: 
                        steps = 3
                    current_step = 1
                    print('Starting execution')
                    # Check if all the files required for the synthetic data generation exist.                    
                    # Checking the existence of the file: "user_schema.conf"  
                    progress_text = f'Generating data .....step {current_step} from {steps}'
                    my_bar = st.progress(0, text=progress_text)
                    if user_schema_value:
                        st.write('user.csv')
                        print('Generating user.csv')           
                        user_file_df = generator.generate_user_file(user_schema=user_schema_value)                           
                        st.dataframe(user_file_df)
                        st.download_button(label='Download user.csv', data=user_file_df.to_csv(index=False).encode('utf-8'), file_name='user.csv', key='user_button')                  
                    else:
                        st.warning('The user schema file (user_schema.conf) is required.')
                    current_step = current_step + 1
                    # Checking the existence of the file: "item_schema.conf"            
                    my_bar.progress(int(100/steps), f'Generating data Step {current_step} from {steps}: ')
                    if item_schema_value:
                        st.write('item.csv')
                        print('Generating item.csv')                    
                        item_file_df = generator.generate_item_file(item_schema=item_schema_value, item_profile=item_profile_value, with_correlation=with_correlation_checkbox)
                        st.dataframe(item_file_df)                    
                        st.download_button(label='Download item.csv', data=item_file_df.to_csv(index=False).encode('utf-8'), file_name='item.csv', key='item_button')         
                    else:
                        st.warning('The item schema file (item_schema.conf) is required.')
                    current_step = current_step + 1
                    my_bar.progress(int(100/steps*2), f'Generating data Step {current_step} from {steps}: ')
                    if context:
                        # Checking the existence of the file: "context_schema.conf"                             
                        if context_schema_value:
                            st.write('context.csv')
                            print('Generating context.csv')                        
                            context_file_df = generator.generate_context_file(context_schema=context_schema_value)
                            st.dataframe(context_file_df)
                            st.download_button(label='Download context.csv', data=context_file_df.to_csv(index=False).encode('utf-8'), file_name='context.csv', key='context_button')         
                        else:
                            st.warning('The context schema file (context_schema.conf) is required.')
                        current_step = current_step + 1                
                    # Checking the existence of the file: "generation_config.conf" 
                    my_bar.progress(int(100/steps*3), f'Generating data Step {current_step} from {steps}: ')
                    if config_file_text_area:
                        st.write('rating.csv')
                        print('Generating rating.csv')           
                        if with_context:
                            rating_file_df = generator.generate_rating_file(user_df=user_file_df, user_profile_df=user_profile_df, item_df=item_file_df, item_schema=item_schema_value, with_context=with_context, context_df=context_file_df, context_schema=context_schema_value)        
                        else:
                            rating_file_df = generator.generate_rating_file(user_df=user_file_df, user_profile_df=user_profile_df, item_df=item_file_df, item_schema=item_schema_value)
                        st.dataframe(rating_file_df)
                        st.download_button(label='Download rating.csv', data=rating_file_df.to_csv(index=False).encode('utf-8'), file_name='rating.csv', key='rating_button') 
                    else:
                        st.warning('The configuration file (generation_config.conf) is required.')
                    print('Synthetic data generation has finished.')   
                    my_bar.progress(100, 'Synthetic data generation has finished.')

elif general_option == 'Analysis an existing dataset':
    is_analysis = st.sidebar.radio(label='Analysis an existing dataset', options=['Data visualization', 'Replicate dataset', 'Extend dataset', 'Recalculate ratings', 'Replace NULL values', 'Generate user profile', 'Ratings to binary', 'Mapping categorization'])
    if is_analysis == 'Data visualization':
        if is_context := st.sidebar.checkbox('With context', value=True):
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Upload dataset', 'Users', 'Items', 'Contexts', 'Ratings', 'Total'])
        else:
            tab1, tab2, tab3, tab5, tab6 = st.tabs(['Upload dataset', 'Users', 'Items', 'Ratings', 'Total'])
        def read_uploaded_file(uploaded_file, data, file_type, separator):
            # Read the header of the file to determine column names
            header = uploaded_file.readline().decode("utf-8").strip()
            column_names = header.split(separator)

            # Rename columns
            for i, col in enumerate(column_names):
                if "user" in col.lower() and "id" in col.lower() and "profile" not in col.lower():
                    column_names[i] = "user_id"
                elif "item" in col.lower() and "id" in col.lower():
                    column_names[i] = "item_id"
                elif "context" in col.lower() and "id" in col.lower():
                    column_names[i] = "context_id"

            data[file_type] = pd.read_csv(uploaded_file, sep=separator, names=column_names)
            return data

        def plot_column_attributes_count(data, column, sort):
            if sort == 'asc':
                sort_field = alt.EncodingSortField('count', order='ascending')
            elif sort == 'desc':
                sort_field = alt.EncodingSortField('count', order='descending') 
            else:
                sort_field = None
            chart = alt.Chart(data).mark_bar().encode(
                x=alt.X(column + ':O', title='Attribute values', sort=sort_field),
                y=alt.Y('count:Q', title='Count'),
                tooltip=[column, 'count']
            ).interactive()
            st.altair_chart(chart, use_container_width=True)
            
        def print_statistics_by_attribute(statistics):
            st.header("Statistics by attribute")
            for stat in statistics:
                st.subheader(stat[0])
                st.write('Average: ', stat[1])
                st.write('Standard deviation: ', stat[2])
                col1, col2 = st.columns(2)
                with col1:
                    st.write('Frequencies:')
                    st.dataframe(stat[3])
                with col2:
                    st.write('Percentages:')
                    st.dataframe(stat[4])
        with tab1:
            option = st.selectbox('Choose between uploading multiple files or a single file:', ('Multiple files', 'Single file'))
            if option == 'Multiple files':
                data = {} #Dictionary with the dataframes
                for file_type in ["user", "item", "context", "rating"]:
                    if file_type == "context":
                        if not is_context:
                            continue
                    with st.expander(f"Upload your {file_type}.csv file"):
                        separator = st.text_input(f"Enter the separator for your {file_type}.csv file (default is ';')", ";")
                        uploaded_file = st.file_uploader(f"Select {file_type}.csv file", type="csv")
                        if uploaded_file is not None:
                            if not separator:
                                st.error('Please provide a separator.')
                            else:
                                try:
                                    data = read_uploaded_file(uploaded_file, data, file_type, separator)
                                    st.dataframe(data[file_type].head())
                                except Exception as e:
                                    st.error(f"An error occurred while reading the {file_type} file: {str(e)}")
                                    data[file_type] = None
            elif option == 'Single file':
                data = {} #Dictionary with the dataframes
                data_file = st.file_uploader("Select Data_STS.csv file", type="csv")
                separator = st.text_input("Enter the separator for your Data_STS.csv file (default is '	')", "	")
                if data_file is not None:
                    if not separator:
                        st.error('Please provide a separator.')
                    else:
                        try:
                            df = pd.read_csv(data_file, sep=separator)
                            st.dataframe(df.head())
                            def create_dataframe(label, df):
                                if columns := st.multiselect(label=label, options=df.columns):
                                    # Create a new dataframe with the selected columns
                                    new_df = df[columns]
                                    st.dataframe(new_df.head())
                                    return new_df
                                else:
                                    st.error('Please select at least one column')
                            data = {'user': create_dataframe('Select the columns for the user dataframe:', df, 'user_df'),
                                    'item': create_dataframe('Select the columns for the item dataframe:', df, 'item_df'),
                                    'context': create_dataframe('Select the columns for the context dataframe:', df, 'context_df'),
                                    'rating': create_dataframe('Select the columns for the rating dataframe:', df, 'rating_df')}
                        except Exception as e:
                            st.error(f"An error occurred while reading the file: {str(e)}")
        with tab2:
            if 'user' in data and data['user'] is not None:
                st.dataframe(data['user'] )
                missing_values2 = extract_statistics_uic.count_missing_values(data['user'],replace_values={"NULL":np.nan,-1:np.nan})
                st.write("Missing values:")
                st.table(missing_values2)
                
                st.write("Attributes, data types and value ranges:")
                table2 = extract_statistics_uic.list_attributes_and_ranges(data['user'])
                st.table(pd.DataFrame(table2, columns=["Attribute name", "Data type", "Value ranges"]))
                
                col1, col2 = st.columns(2)
                with col1:
                    column2 = st.selectbox("Select an attribute", data['user'].columns)
                with col2:
                    sort2 = st.selectbox('Sort', ['none', 'asc', 'desc'], key='sort2')
                data2 = extract_statistics_uic.column_attributes_count(data['user'], column2)
                plot_column_attributes_count(data2, column2, sort2)

                statistics = extract_statistics_uic.statistics_by_attribute(data['user'])
                print_statistics_by_attribute(statistics)
            else:
                st.error("User dataset not found.")
        with tab3:
            if 'item' in data and data['item'] is not None:
                st.dataframe(data['item'] )
                missing_values3 = extract_statistics_uic.count_missing_values(data['user'],replace_values={"NULL":np.nan,-1:np.nan})
                st.write("Missing values:")
                st.table(missing_values3)
                
                st.write("Attributes, data types and value ranges:")
                table3 = extract_statistics_uic.list_attributes_and_ranges(data['item'])
                st.table(pd.DataFrame(table3, columns=["Attribute name", "Data type", "Value ranges"]))

                col1, col2 = st.columns(2)
                with col1:
                    column3 = st.selectbox("Select an attribute", data['item'].columns)
                with col2:
                    sort3 = st.selectbox('Sort', ['none', 'asc', 'desc'], key='sort3')
                data3 = extract_statistics_uic.column_attributes_count(data['item'], column3)
                plot_column_attributes_count(data3, column3, sort3)

                if 'rating' in data and data['rating'] is not None:
                    merged_df = pd.merge(data['rating'], data['item'], on="item_id")
                    users = merged_df['user_id'].unique()
                    selected_user = st.selectbox("Select a user:", users, key="selected_user_tab3")
                    stats = extract_statistics_uic.statistics_by_user(merged_df, selected_user, "items")
                    st.table(pd.DataFrame([stats]))

                statistics = extract_statistics_uic.statistics_by_attribute(data['item'])
                print_statistics_by_attribute(statistics)
            else:
                st.error("Item dataset not found.")
        if is_context:
            with tab4:
                if 'context' in data and data['context'] is not None:
                    st.dataframe(data['context'] )
                    missing_values4 = extract_statistics_uic.count_missing_values(data['user'],replace_values={"NULL":np.nan,-1:np.nan})
                    st.write("Missing values:")
                    st.table(missing_values4)

                    st.write("Attributes, data types and value ranges:")
                    table4 = extract_statistics_uic.list_attributes_and_ranges(data['context'])
                    st.table(pd.DataFrame(table4, columns=["Attribute name", "Data type", "Value ranges"]))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        column4 = st.selectbox("Select an attribute", data['context'].columns)
                    with col2:
                        sort4 = st.selectbox('Sort', ['none', 'asc', 'desc'], key='sort4')
                    data4 = extract_statistics_uic.column_attributes_count(data['context'], column4)
                    plot_column_attributes_count(data4, column4, sort4)

                    if 'rating' in data and data['rating'] is not None:
                        merged_df = pd.merge(data['rating'], data['context'], on="context_id")
                        users = merged_df['user_id'].unique()
                        selected_user = st.selectbox("Select a user:", users, key="selected_user_tab4")
                        stats = extract_statistics_uic.statistics_by_user(merged_df, selected_user, "contexts")
                        st.table(pd.DataFrame([stats]))

                    statistics = extract_statistics_uic.statistics_by_attribute(data['context'])
                    print_statistics_by_attribute(statistics)
                else:
                    st.error("Context dataset not found.")
        with tab5:
            if 'rating' in data and data['rating'] is not None:
                data['rating'] = extract_statistics_rating.replace_missing_values(data['rating'])
                st.session_state["rating"] = data['rating'] #Save the rating dataframe in the session state

                st.dataframe(data['rating'])

                unique_counts_df = extract_statistics_rating.count_unique(data['rating'])
                st.write("General statistics:")
                st.table(unique_counts_df)
                
                st.write("Attributes, data types and value ranges:")
                table5 = extract_statistics_uic.list_attributes_and_ranges(data['rating'])
                st.table(pd.DataFrame(table5, columns=["Attribute name", "Data type", "Value ranges"]))

                # Plot the distribution of ratings
                counts = np.bincount(data['rating']['rating']) #Count the frequency of each rating
                fig, ax = plt.subplots()
                ax.set_title("Distribution of ratings", fontdict={'size': 16, **config.PLOTS_FONT})
                ax.set_xlabel("Rating", fontdict=config.PLOTS_FONT)
                ax.set_ylabel("Frequency", fontdict=config.PLOTS_FONT)
                ax.grid(**config.PLOTS_GRID)
                ax.set_xticks(range(len(counts)))
                for i in range(len(counts)):
                    if counts[i] > 0:
                        ax.bar(i, counts[i], color="#0099CC")
                        ax.text(i, counts[i], str(counts[i]), ha='center')
                st.pyplot(fig, clear_figure=True)

                # Plot the distribution of the number of items voted by each user
                users = data['rating']['user_id'].unique()
                selected_user = st.selectbox("Select a user:", users, key="selected_user_tab5")
                counts_items, unique_items, total_count, percent_ratings_by_user = extract_statistics_rating.count_items_voted_by_user(data['rating'], selected_user)
                fig, ax = plt.subplots()
                ax.set_title(f"Number of items voted by user {str(selected_user)} (total={total_count}) (percentage={percent_ratings_by_user:.2f}%)", fontdict={'size': 16, **config.PLOTS_FONT})
                ax.set_xlabel("Items", fontdict=config.PLOTS_FONT)
                ax.set_ylabel("Frequency", fontdict=config.PLOTS_FONT)
                ax.grid(**config.PLOTS_GRID)
                ax.bar(counts_items.index, counts_items.values, color="#0099CC")
                ax.set_xticks(unique_items)
                for item, count in counts_items.items(): #Add the count of each item to the plot
                    ax.text(item, count, str(count), ha='center', va='bottom')
                st.pyplot(fig)

                # Show the statistics of the selected user votes
                users = ["All users"] + list(users)
                selected_user = st.selectbox("Select user", users)
                vote_stats = extract_statistics_rating.calculate_vote_stats(data['rating'], selected_user)
                for key, value in vote_stats.items():
                    st.write(f"{key}: {value}")
            else:
                st.error("Ratings dataset not found.")
        with tab6:
            try:
                # Merge the dataframes
                merged_df = data["rating"]
                for key in ["user", "item", "context"]:
                    if key in data:
                        merged_df = pd.merge(merged_df, data[key], on=key+"_id", how="left")

                stats = extract_statistics_uic.general_statistics(merged_df)
                st.table(pd.DataFrame([stats]))
                
                st.header("Correlation matrix")
                columns_not_id = [col for col in merged_df.columns if col not in ['user_id', 'item_id', 'context_id']]
                data_types = []
                for col in columns_not_id:
                    data_types.append({"Attribute": col, "Data Type": str(merged_df[col].dtype), "File Type": "rating" if col in data["rating"].columns else "item" if col in data["item"].columns else "context" if col in data["context"].columns else "user"})
                df_data_types = pd.DataFrame(data_types)
                st.dataframe(df_data_types)
                selected_columns = st.multiselect("Select columns to analyze", columns_not_id)
                method = st.selectbox("Select a method", ['pearson', 'kendall', 'spearman'])
                if st.button("Generate correlation matrix") and selected_columns:
                    with st.spinner("Generating correlation matrix..."):
                        merged_df_selected = merged_df[selected_columns].copy()
                        # Categorize non-numeric columns using label encoding
                        for col in merged_df_selected.select_dtypes(exclude=[np.number]):
                            merged_df_selected[col], _ = merged_df_selected[col].factorize()
                        
                        corr_matrix = merged_df_selected.corr(method=method)
                        
                        fig, ax = plt.subplots(figsize=(10, 10))
                        sns.heatmap(corr_matrix, vmin=-1, vmax=1, center=0, cmap='coolwarm', annot=True, fmt=".2f", ax=ax)
                        st.pyplot(fig)
            except:
                st.error("Ratings, items, contexts or users datasets not found.")
    elif is_analysis == 'Replicate dataset':
        st.write('TODO')
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
                date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%m-%d-%Y", "%Y%m%d"]
                time_formats = ["%H:%M:%S", "%H:%M"]
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
        elif algorithm == "KNNBasic":
            return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnbasic'),
                    "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["cosine", "msd", "pearson"], key='sim_options_knnbasic'),
                                    "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnbasic')}}
        elif algorithm == "BaselineOnly":
            return {"bsl_options": {"method": st.sidebar.selectbox("Baseline method", ["als", "sgd"], key='method_baselineonly'),
                                    "reg_i": st.sidebar.number_input("Regularization term for item parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_i_baselineonly'),
                                    "reg_u": st.sidebar.number_input("Regularization term for user parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_u_baselineonly')}}
        elif algorithm == "CoClustering":
            return {"n_cltr_u": st.sidebar.number_input("Number of clusters for users", min_value=1, max_value=1000, value=5),
                    "n_cltr_i": st.sidebar.number_input("Number of clusters for items", min_value=1, max_value=1000, value=5)}
        elif algorithm == "KNNBaseline":
            return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnbaseline'),
                    "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["cosine", "msd", "pearson"], key='sim_options_knnbaseline'),
                                    "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnbaseline')},
                    "bsl_options": {"method": st.sidebar.selectbox("Baseline method", ["als", "sgd"], key='method_knnbaseline'),
                                    "reg_i": st.sidebar.number_input("Regularization term for item parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_i_knnbaseline'),
                                    "reg_u": st.sidebar.number_input("Regularization term for user parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_u_knnbaseline')}}
        elif algorithm == "KNNWithMeans":
            return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnwithmeans'),
                    "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["cosine", "msd", "pearson"], key='sim_options_knnwithmeans'),
                                    "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnwithmeans')}}
        elif algorithm == "NMF":
            return {"n_factors": st.sidebar.number_input("Number of factors", min_value=1, max_value=1000, value=100, key='n_factors_nmf'),
                    "n_epochs": st.sidebar.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_nmf'),
                    "reg_pu": st.sidebar.number_input("Regularization term for user factors", min_value=0.0001, max_value=1.0, value=0.02),
                    "reg_qi": st.sidebar.number_input("Regularization term for item factors", min_value=0.0001, max_value=1.0, value=0.02)}
        elif algorithm == "NormalPredictor":
            return {}
        elif algorithm == "SlopeOne":
            return {}
        elif algorithm == "SVDpp":
            return {"n_factors": st.sidebar.number_input("Number of factors", min_value=1, max_value=1000, value=100, key='n_factors_svdpp'),
                    "n_epochs": st.sidebar.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_svdpp'),
                    "lr_all": st.sidebar.number_input("Learning rate for all parameters", min_value=0.0001, max_value=1.0, value=0.005, key='lr_all_svdpp'),
                    "reg_all": st.sidebar.number_input("Regularization term for all parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_all_svdpp')}

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

    st.sidebar.title('Evaluation of a dataset')
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
    
    if "rating" in st.session_state:
        rating = st.session_state["rating"]
        data = surprise_helpers.convert_to_surprise_dataset(rating)
    else:
        st.error("No rating dataset loaded")

    st.sidebar.header("Metrics selection")
    if binary_ratings.is_binary_rating(rating):
        metrics = st.sidebar.multiselect("Select one or more cross validation binary metrics", ["Precision", "Recall", "F1_Score", "AUC_ROC"], default="Precision")
    else:
        metrics = st.sidebar.multiselect("Select one or more cross validation non-binary metrics", ["RMSE", "MSE", "MAE", "FCP", "Precision", "Recall", "F1_Score", "MAP", "NDCG"], default="MAE")

    if st.sidebar.button("Evaluate"):
        results_df = evaluate_algo(algo_list, strategy_instance, metrics, data)
        st.subheader("Evaluation Results:")
        st.write(pd.DataFrame(results_df))
        st.session_state["results"] = results_df #Save the results dataframe in the session state

    if "results" in st.session_state:
        results_df = st.session_state["rating"]
    results_df = pd.read_csv("results.csv")
    st.subheader("Algorithm evaluation results")
    algorithm = st.selectbox("Select an algorithm to plot", algorithms)
    visualize_results_algo(results_df, algorithm)
    st.subheader("Metric evaluation results")
    metric = st.selectbox("Select a metric to plot", metrics)
    visualize_results_metric(results_df, metric)
