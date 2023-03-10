# sourcery skip: use-fstring-for-concatenation
import io
import streamlit as st
import config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import console
from datagencars.synthetic_dataset.generate_synthetic_dataset import GenerateSyntheticDataset
from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

from datagencars.synthetic_dataset.generator.generator_output_file.generator_rating import GeneratorRatingFile


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

        with col_stop:
            button_stop = st.button(label='Stop', key='button_stop')
        
        generator = GenerateSyntheticDataset(generation_config=generation_config_value)
        output = st.empty()    
        with console.st_log(output.code):
            if button_run:
                print('Starting execution')
                # Check if all the files required for the synthetic data generation exist.                    
                # Checking the existence of the file: "user_schema.conf"            
                if user_schema_value:
                    st.write('user.csv')
                    print('Generating user.csv')           
                    user_file_df = generator.generate_user_file(user_schema=user_schema_value)                           
                    st.dataframe(user_file_df)
                    st.download_button(label='Download user.csv', data=user_file_df.to_csv(index=False).encode('utf-8'), file_name='user.csv', key='user_button')                  
                else:
                    st.warning('The user schema file (user_schema.conf) is required.')
                
                # Checking the existence of the file: "item_schema.conf"            
                if item_schema_value:
                    st.write('item.csv')
                    print('Generating item.csv')                    
                    item_file_df = generator.generate_item_file(item_schema=item_schema_value, item_profile=item_profile_value, with_correlation=with_correlation_checkbox)
                    st.dataframe(item_file_df)                    
                    st.download_button(label='Download item.csv', data=item_file_df.to_csv(index=False).encode('utf-8'), file_name='item.csv', key='item_button')         
                else:
                    st.warning('The item schema file (item_schema.conf) is required.')
                
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
                                
                # Checking the existence of the file: "generation_config.conf"             
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

elif general_option == 'Analysis an existing dataset':
    is_analysis = st.sidebar.radio(label='Analysis an existing dataset', options=['Data visualization', 'Replicate dataset', 'Extend dataset', 'Recalculate ratings', 'Replace NULL values', 'Generate user profile'])
    if is_analysis == 'Data visualization':  
        tab1, tab2, tab3, tab4, tab5 = st.tabs(['Upload dataset', 'Users', 'Items', 'Contexts', 'Ratings'])
        def replace_count_missing_values(dataframe, replace_values=None):
            """
            Count missing values in the dataframe.
            """
            if replace_values is None:
                replace_values = {}
            for k,v in replace_values.items():
                dataframe.replace(k, np.nan, inplace=True)
            missing_values = dataframe.isnull().sum()
            missing_values = pd.DataFrame(missing_values, columns=["Count"])
            missing_values.reset_index(inplace=True)
            missing_values.rename(columns={"index": "Attribute name"}, inplace=True)
            st.dataframe(dataframe)
            st.write("Missing values:")
            st.table(missing_values)
        def list_attributes_and_ranges(dataframe):
            """
            List attributes, data types, and value ranges of the dataframe.
            """
            st.write("Attributes, data types and value ranges:")
            table = []
            for column in dataframe.columns:
                if dataframe[column].dtype in ['int64', 'float64']:
                    table.append([column, dataframe[column].dtype, f"{dataframe[column].min()} - {dataframe[column].max()}"])
                elif dataframe[column].dtype == 'object':
                    try:
                        dataframe[column] = pd.to_datetime(dataframe[column])
                        table.append([column, dataframe[column].dtype, f"{dataframe[column].min().strftime('%Y-%m-%d')} - {dataframe[column].max().strftime('%Y-%m-%d')}"])
                    except ValueError:
                        unique_values = dataframe[column].dropna().unique()
                        unique_values_str = ', '.join([str(value) for value in unique_values])
                        table.append([column, dataframe[column].dtype, unique_values_str])
                else:
                    table.append([column, dataframe[column].dtype, "unsupported data type"])
            st.table(pd.DataFrame(table, columns=["Attribute name", "Data type", "Value ranges"]))
        with tab1:
            option = st.selectbox('Choose between uploading multiple files or a single file:', ('Multiple files', 'Single file'))
            if option == 'Multiple files':
                upload_context = st.checkbox("With context", value=True, key='with_comtext')
                data = {} #Dictionary with the dataframes
                for file_type in ["user", "item", "context", "rating"]:
                    if file_type == "context":
                        if not upload_context:
                            continue
                    with st.expander(f"Upload your {file_type}.csv file"):
                        uploaded_file = st.file_uploader(f"Select {file_type}.csv file", type="csv")
                        separator = st.text_input(f"Enter the separator for your {file_type}.csv file (default is ';')", ";")
                        if uploaded_file is not None:
                            if not separator:
                                st.error('Please provide a separator.')
                            else:
                                try:
                                    data[file_type] = pd.read_csv(uploaded_file, sep=separator)
                                    st.dataframe(data[file_type].head())
                                except Exception as e:
                                    st.error(f"An error occurred while reading the {file_type} file: {str(e)}")
                                    data[file_type] = None
            elif option == 'Single file':
                data = {} # Dictionary with the dataframes
                data_file = st.file_uploader("Select Data_STS.csv file", type="csv")
                separator = st.text_input("Enter the separator for your Data_STS.csv file (default is '	')", "	")
                if data_file is not None:
                    if not separator:
                        st.error('Please provide a separator.')
                    else:
                        try:
                            df = pd.read_csv(data_file, sep=separator)
                            st.dataframe(df.head())
                            def create_dataframe(label, df, new_df_name):
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
                replace_count_missing_values(data['user'],replace_values={"NULL":np.nan,-1:np.nan})
                list_attributes_and_ranges(data['user'])
            else:
                st.error("User dataset not found.")
        with tab3:
            if 'item' in data and data['item'] is not None:
                replace_count_missing_values(data['item'],replace_values={"NULL":np.nan,-1:np.nan})
                list_attributes_and_ranges(data['item'])
            else:
                st.error("Item dataset not found.")
        with tab4:
            if 'context' in data and data['context'] is not None:
                replace_count_missing_values(data['context'],replace_values={"NULL":np.nan,-1:np.nan})
                list_attributes_and_ranges(data['context'])
            else:
                st.error("Context dataset not found.")
        with tab5:
            if 'rating' in data and data['rating'] is not None:
                # Replace missing values
                for k,v in {"NULL":np.nan,-1:np.nan}.items():
                    data['rating'].replace(k, np.nan, inplace=True)

                st.dataframe(data['rating'])

                # Count unique users, items and contexts
                unique_users = data['rating']["userID"].nunique()
                unique_items = data['rating']["itemID"].nunique()
                unique_contexts = data['rating']["contextID"].nunique()
                unique_ratings = data['rating']["rating"].nunique()
                unique_counts = {"Users": unique_users, "Items": unique_items, "Contexts": unique_contexts, "Ratings": unique_ratings} # Create a dictionary of the unique counts
                unique_counts_df = pd.DataFrame.from_dict(unique_counts, orient='index', columns=['Count']) # Create a DataFrame from the dictionary
                unique_counts_df.reset_index(inplace=True)
                unique_counts_df.rename(columns={"index": "Attribute name"}, inplace=True)
                st.write("General statistics:")
                st.table(unique_counts_df)
                
                list_attributes_and_ranges(data['rating'])

                font = {'family': 'serif', 'color':  'black', 'weight': 'normal', 'size': 12}
                grid = {'visible':True, 'color':'gray', 'linestyle':'-.', 'linewidth':0.5}

                fig, ax = plt.subplots()
                ax.set_title("Distribution of ratings", fontdict={'size': 16, **font})
                ax.set_xlabel("Rating", fontdict=font)
                ax.set_ylabel("Frequency", fontdict=font)
                ax.grid(**grid)
                counts = np.bincount(data['rating']["rating"]) # Count the frequency of each rating
                for i in range(5):
                    ax.bar(i+1, counts[i+1], color="#0099CC")
                    ax.text(i+1, counts[i+1]+1, str(counts[i+1]), ha='center')
                st.pyplot(fig, clear_figure=True)

                user_options = data['rating'].groupby("userID")["itemID"].nunique().index
                selected_user = st.selectbox("Select a user:", user_options)
                filtered_ratings_df = data['rating'][data['rating']['userID'] == selected_user]
                total_count = len(filtered_ratings_df["itemID"])
                fig, ax = plt.subplots()
                ax.set_title(f"Number of items voted by user {str(selected_user)} (total={total_count})", fontdict={'size': 16, **font})
                ax.set_xlabel("Items", fontdict=font)
                ax.set_ylabel("Frequency", fontdict=font)
                ax.grid(**grid)
                counts_items = filtered_ratings_df.groupby("itemID").size()
                ax.bar(counts_items.index, counts_items.values, color="#0099CC")
                unique_items = np.unique(filtered_ratings_df["itemID"]) #Obtain the unique values and convert them to list
                ax.set_xticks(unique_items)
                counts_items = filtered_ratings_df["itemID"].value_counts()
                for item, count in counts_items.items(): #Add the count of each item to the plot
                    ax.text(item, count, str(count), ha='center', va='bottom')
                st.pyplot(fig)
            else:
                st.error("Ratings dataset not found.")
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

elif general_option == 'Evaluation of a dataset':
    st.sidebar.write('Evaluation of a dataset')
