import base64
import io

import config
import console
import pandas as pd
import requests
import streamlit as st
from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.rating_explicit import RatingExplicit
from streamlit_app import help_information
from streamlit_app.workflow_graph import workflow_image


def generate_synthtetic_dataset(with_context):     
    # Help information:
    help_information.help_explicit_rating_wf()

    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='GenerateSyntheticDataset(Explicit_ratings)', init_step='True', with_context=with_context, optional_value_list=[("UP", "Manual")])
    
    # Loading available tabs:
    if with_context:        
        tab_generation, tab_user, tab_item, tab_context, tab_user_profile, tab_run  = st.tabs(['Generation', 'Users', 'Items', 'Contexts', 'User profile', 'Run'])
    else:        
        tab_generation, tab_user, tab_item, tab_user_profile, tab_run = st.tabs(['Generation', 'Users', 'Items', 'User profile', 'Run'])
    
    # Initializing global variables:
    generation_config_schema = ''
    user_schema = ''
    item_schema = ''
    item_profile = ''
    context_schema = ''
    user_profile = pd.DataFrame()    

    # TAB --> Generation config:    
    with tab_generation:
        st.header('Generation')
        # Uploading the file: "generation_config.conf"        
        if st.checkbox('Upload the data generation configuration file', value=True, key=f'is_upload_{config.GENERATION_CONFIG_SCHEMA_NAME}_file'):
            schema_value = upload_schema_file(schema_file_name=config.GENERATION_CONFIG_SCHEMA_NAME)
        else:
            # Generating the schema file: "generation_config.conf"
            schema_value = get_generation_config_file(with_context)
        # Editing schema:
        generation_config_schema = edit_schema_file(schema_file_name=config.GENERATION_CONFIG_SCHEMA_NAME, schema_value=schema_value)
        # Saving schema:
        save_file(file_name=config.GENERATION_CONFIG_SCHEMA_NAME, file_value=generation_config_schema, extension='conf')
    # TAB --> User:
    with tab_user:        
        st.header('Users')
        # Uploading the file: "user_schema.conf"        
        if st.checkbox(f'Upload the data {config.USER_TYPE} schema file', value=True, key=f'is_upload_{config.USER_SCHEMA_NAME}_file'):
            schema_value = upload_schema_file(schema_file_name=config.USER_SCHEMA_NAME)
        else:
            # Generating the schema file: "user_schema.conf"
            schema_value = get_schema_file(schema_type=config.USER_TYPE)
        # Editing schema:
        user_schema = edit_schema_file(schema_file_name=config.USER_SCHEMA_NAME, schema_value=schema_value)
        # Saving schema:
        save_file(file_name=config.USER_SCHEMA_NAME, file_value=user_schema, extension='conf')
    # TAB --> Item and Item Profile:
    with tab_item:
        st.header('Items')
        # Uploading the file: "item_schema.conf"
        if st.checkbox(f'Upload the data {config.ITEM_TYPE} schema file', value=True, key=f'is_upload_{config.ITEM_SCHEMA_NAME}_file'):
            schema_value = upload_schema_file(schema_file_name=config.ITEM_SCHEMA_NAME)
        else:
            # Generating the schema file: "item_schema.conf"
            schema_value = get_schema_file(schema_type=config.ITEM_TYPE)
        # Editing schema:
        item_schema = edit_schema_file(schema_file_name=config.ITEM_SCHEMA_NAME, schema_value=schema_value)
        # Saving schema:
        save_file(file_name=config.ITEM_SCHEMA_NAME, file_value=item_schema, extension='conf')
        st.markdown("""---""")

        # Uploading the file: "item_profile.conf"
        if st.checkbox(f'Upload the data {config.ITEM_PROFILE_TYPE} schema file', value=True, key=f'is_upload_{config.ITEM_PROFILE_SCHEMA_NAME}_file'):
            item_profile_value = upload_schema_file(schema_file_name=config.ITEM_PROFILE_SCHEMA_NAME)
        else:
            # Generating the schema file: "item_profile.conf"
            item_profile_value = get_item_profile_file()
        # Editing schema:
        item_profile = edit_schema_file(schema_file_name=config.ITEM_PROFILE_SCHEMA_NAME, schema_value=item_profile_value)
        # Saving schema:
        save_file(file_name=config.ITEM_PROFILE_SCHEMA_NAME, file_value=item_profile, extension='conf')             
    # TAB --> Context:
    if with_context:
        with tab_context:
            st.header('Contexts')
            # Uploading the file: "context_schema.conf"        
            if st.checkbox(f'Upload the data {config.CONTEXT_TYPE} schema file', value=True, key=f'is_upload_{config.CONTEXT_SCHEMA_NAME}_file'):
                schema_value = upload_schema_file(schema_file_name=config.CONTEXT_SCHEMA_NAME)
            else:
                # Generating the schema file: "context_schema.conf"
                schema_value = get_schema_file(schema_type=config.CONTEXT_TYPE)
            # Editing schema:
            context_schema = edit_schema_file(schema_file_name=config.CONTEXT_SCHEMA_NAME, schema_value=schema_value)
            # Saving schema:
            save_file(file_name=config.CONTEXT_SCHEMA_NAME, file_value=context_schema, extension='conf')
    # TAB --> User Profile:    
    with tab_user_profile:
        st.header('User profile')  
        # Uploading the file: "user_profile.csv"        
        if st.checkbox(f'Upload the data {config.USER_PROFILE_TYPE} file', value=True, key=f'is_upload_{config.USER_PROFILE_SCHEMA_NAME}_file'):
            user_profile = upload_user_profile_file()
        else:
            # Generating the schema file: "user_profile.csv"
            if with_context:
                user_profile = get_user_profile_file(user_schema, item_schema, context_schema)
            else:
                user_profile = get_user_profile_file(user_schema, item_schema)
    # TAB --> Run:
    with tab_run:        
        if with_context:
            run(generation_config_schema=generation_config_schema, user_schema=user_schema, user_profile=user_profile, item_schema=item_schema, item_profile=item_profile, with_context=with_context, context_schema=context_schema)
        else:
            run(generation_config_schema=generation_config_schema, user_schema=user_schema, user_profile=user_profile, item_schema=item_schema, item_profile=item_profile)
        
def upload_schema_file(schema_file_name):
    """
    Upload schema from file.
    :param schema_file_name: The name of the schema file.
    :return: The content of the schema file.
    """
    schema_file_value = ''
    with st.expander(f"Upload {schema_file_name}.conf"):
        if schema_file := st.file_uploader(label='Choose the file:', key=f"{schema_file_name}_file"):
            schema_file_value = schema_file.getvalue().decode("utf-8")
    return schema_file_value

def upload_user_profile_file():
    """
    Upload an existing user profile.
    :return: A dataframe with the user profile content.
    """
    user_profile_df = pd.DataFrame()
    with st.expander(label=f'Upload {config.USER_PROFILE_SCHEMA_NAME}.csv'):
        if user_profile_file := st.file_uploader(label='Choose the file:', key=f'{config.USER_PROFILE_SCHEMA_NAME}_file'):
            user_profile_value = user_profile_file.getvalue().decode("utf-8")
            user_profile_df = pd.read_csv(io.StringIO(user_profile_value))  
            st.dataframe(user_profile_df)
    return user_profile_df

def get_generation_config_file(with_context):
    """
    Generate the schema file "generating_config.conf".
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    :return: The content of the "generating_config.conf" schema.
    """
    # [dimension]
    st.write('General configuration')
    dimension_value = '[dimension] \n'
    user_count = st.number_input(label='Number of users to generate:', value=0)
    item_count = st.number_input(label='Number of items to generate:', value=0)
    if with_context:
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
    # Generating the text of the file "generation_config.conf":
    generation_config_schema = dimension_value + '\n' + rating_value + '\n' + item_profile_value
    return generation_config_schema

def get_schema_file(schema_type):    
    """
    Generate a schema file: "user_schema.conf", "item_schema.conf" or "context_schema.conf".
    :param schema_type: The type of schema (user, item or context).
    :return: The content of the schema file.
    """
    # [global]   
    value = '[global]'+'\n'
    value += 'type='+config.USER_TYPE+'\n'
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
        generator_type = st.selectbox(label='Generator type:', options=['Categorical', 'Numerical', 'Fixed', 'Date', 'URL', 'Address', 'BooleanList', 'Position', 'Device'],  key=schema_type+'_generator_type_'+str(position))            
        # type_attribute:
        attribute_type = None
        # String and Boolean:
        if generator_type == 'Categorical':                        
            distribution_type = st.selectbox(label='Distribution type:', options=['Random', 'Gaussian'],  key=schema_type+'_distribution_type_'+str(position)) 
            value += 'generator_type_attribute_'+str(position)+'='+f'{distribution_type}AttributeGenerator'+'\n'
            attribute_type = st.selectbox(label='Attribute type:', options=['String', 'Boolean'], key=schema_type+'_attribute_type_'+str(position)) 
            value += 'type_attribute_'+str(position)+'='+f'{attribute_type}'+'\n'
            # String:
            if attribute_type == 'String':                
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
            # Boolean:
            elif attribute_type == 'Boolean':
                bool_possible_value_list = ['True', 'False']
                number_possible_value = len(bool_possible_value_list)
                value += 'number_posible_values_attribute_'+str(position)+'='+str(number_possible_value)+'\n'
                for i, bool_value in enumerate(bool_possible_value_list):
                    value += 'posible_value_'+str(i+1)+'_attribute_'+str(position)+'='+str(bool_value)+'\n'
                st.write(bool_possible_value_list)
        elif generator_type == 'Numerical':                  
            distribution_type = st.selectbox(label='Distribution type:', options=['Random', 'Gaussian'],  key=schema_type+'_distribution_type_'+str(position))             
            value += 'generator_type_attribute_'+str(position)+'='+f'{distribution_type}AttributeGenerator'+'\n'
            attribute_type = st.selectbox(label='Attribute type:', options=['Integer', 'Float'], key=schema_type+'_attribute_type_'+str(position)) 
            value += 'type_attribute_'+str(position)+'='+f'{attribute_type}'+'\n'
            # Integer:
            if attribute_type == 'Integer':                
                integer_min = st.number_input(label='Minimum value of the attribute', value=0, key=schema_type+'_integer_min_'+str(position)) 
                value += 'minimum_value_attribute_'+str(position)+'='+str(integer_min)+'\n'
                integer_max = st.number_input(label='Maximum value of the ratings', value=0, key=schema_type+'_integer_max_'+str(position)) 
                value += 'maximum_value_attribute_'+str(position)+'='+str(integer_max)+'\n'
            # Float:
            elif attribute_type == 'Float':                
                float_min = float(st.number_input(label='Minimum value of the attribute', value=0.0, key=schema_type+'_float_min_'+str(position))) 
                value += 'minimum_value_attribute_'+str(position)+'='+str(float_min)+'\n'
                float_max = float(st.number_input(label='Maximum value of the ratings', value=0.0, key=schema_type+'_float_max_'+str(position))) 
                value += 'maximum_value_attribute_'+str(position)+'='+str(float_max)+'\n'                                
        elif generator_type == 'Fixed':     
            value += 'generator_type_attribute_'+str(position)+'=FixedAttributeGenerator'+'\n' 
            attribute_type = st.selectbox(label='Attribute type:', options=['Integer', 'String', 'Boolean'], key='attribute_type_'+str(position)+'_'+generator_type)
            fixed_input = st.text_input(label='Imput the fixed value:', key='fixed_input_'+str(position))
            value += 'input_parameter_attribute_'+str(position)+'='+str(fixed_input)+'\n'
        elif generator_type == 'Date':    
            value += 'generator_type_attribute_'+str(position)+'=DateAttributeGenerator'+'\n'                 
            attribute_type = st.selectbox(label='Attribute type:', options=['String'], key='attribute_type_'+str(position)+'_'+generator_type)
            value += 'type_attribute_'+str(position)+'='+f'{attribute_type}'+'\n'
            st.write('Imput the range of dates (years only):')
            date_min = st.number_input(label='From:', value=1980, key='date_min_'+str(position))
            value += 'minimum_value_attribute_'+str(position)+'='+str(date_min)+'\n'
            date_max = st.number_input(label='Until:', value=2020, key='date_max_'+str(position))
            value += 'maximum_value_attribute_'+str(position)+'='+str(date_max)+'\n'
        elif generator_type == 'BooleanList':       
            value += 'generator_type_attribute_'+str(position)+'=BooleanListAttributeGenerator'+'\n'              
            attribute_type = st.selectbox(label='Attribute type:', options=['List'], key='attribute_type_'+str(position)+'_'+generator_type)
            component_list = st.text_area(label='Introduce component values to the list (split by comma): monday, tuesday, wednesday, thursday, friday', key='component_list_'+str(position)).split(',')
            value += 'number_maximum_component_attribute_'+str(position)+'='+str(len(component_list))+'\n'
            value += 'type_component_attribute_'+str(position)+'=Boolean'+'\n'
            for idx, component in enumerate(component_list):
                value += 'component_'+str(idx+1)+'_attribute_'+str(position)+'='+str(component).strip()+'\n'
            component_input_parameter = st.number_input(label='Number of boolean values to generate for these components:', value=1, key='component_input_parameter_'+str(position))
            value += 'input_parameter_attribute_'+str(position)+'='+str(component_input_parameter)+'\n'
        elif generator_type == 'URL':    
            value += 'generator_type_attribute_'+str(position)+'=URLAttributeGenerator'+'\n'                  
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
            input_parameter_list = input_parameter_df['place'].astype(str).values.tolist()
            value += 'input_parameter_attribute_'+str(position)+'='+str(input_parameter_list)+'\n'
            # Unique value?
            unique_value = st.checkbox(label='Unique value?', value=True, key='unique_value_'+str(position)+'_'+generator_type)
            if unique_value:
                value += 'unique_value_attribute_'+str(position)+'=True'+'\n'
            else:
                value += 'unique_value_attribute_'+str(position)+'=False'+'\n'
        elif generator_type == 'Address':     
            value += 'generator_type_attribute_'+str(position)+'=AddressAttributeGenerator'+'\n'                     
            attribute_type = st.selectbox(label='Attribute type:', options=['AttributeComposite'], key='attribute_type_'+str(position)+'_'+generator_type)
            address_complete_type = st.selectbox(label='Address complete type:', options=['Manually', 'Upload file', 'Search Address'], key='address_complete_type')
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
            if address_complete_type == 'Manually':
                input_parameter_text_area = ip_text_area.text_area(label='Introduce address values (line by line), keeping the header: <street;number;zp;latitude;longitude>', value='street,number,zp,latitude,longitude', key='address_ip_text_area_'+str(position))   
                input_parameter_df=pd.read_csv(io.StringIO(input_parameter_text_area), sep=",")                                                 
                input_parameter_list = input_parameter_df.astype(str).values.tolist()
                value += 'input_parameter_attribute_'+str(position)+'='+str(input_parameter_list)+'\n'
            if address_complete_type == 'Upload file':
                input_parameter_text_area = None
                input_parameter_list = []
                import_split = st.text_input(label='Specifies the type of separator to read the file (; , # tab)', key='import_split')
                if import_file := st.file_uploader(label='Import list', key='import_file'+str(position)):                            
                    input_parameter_text_area = ip_text_area.text_area(label='Introduce address values below <street,number,zp,latitude,longitude> (line by line):', value=import_file.getvalue().decode("utf-8"), key='import_address_ip_text_area_'+str(position))                            
                    input_parameter_df=pd.read_csv(io.StringIO(input_parameter_text_area), sep=import_split)                                                 
                    input_parameter_list = input_parameter_df.astype(str).values.tolist()                        
                value += 'input_parameter_attribute_'+str(position)+'='+str(input_parameter_list)+'\n'
            if address_complete_type == 'Search Address':
                # Input through a text area:
                input_parameter_text_area = ip_text_area.text_area(label="Introduce place_name to search address, for example: McDonald's, 50017, keeping header: place, postalcode", value='place, zipcode', key='address_ip_text_area_'+str(position))   
                # Buttons: export and import values  
                export_button_column, import_area_column = st.columns(2)
                # Export a file:
                with export_button_column:
                    file_name = attribute_name+'_search_places.csv'
                    if st.download_button(label='Export list', data=input_parameter_text_area, file_name=file_name, key='search_export_button_'+str(position)):
                        if len(input_parameter_text_area) == 0:                                 
                            st.warning('The file to be exported must not be empty.')
                        else:
                            st.success('The file has been saved with the name: '+file_name)
                # Import a file:
                with import_area_column:                        
                    # Input through an uploaded file:
                    if import_file := st.file_uploader(label='Import place_name list, keeping header: place', key='import_file'+str(position)):                            
                        input_parameter_text_area = ip_text_area.text_area(label="Introduce place_name to search address, for example: McDonald's, 50017, keeping header: place, postalcode", value=import_file.getvalue().decode("utf-8"), key='import_address_ip_text_area_'+str(position))                            
                # Searching places:
                places_list = []
                places_str = 'street;number;zp;latitude;longitude\n'
                input_parameter_df=pd.read_csv(io.StringIO(input_parameter_text_area))                    
                input_parameter_list = input_parameter_df.astype(str).values.tolist()                                     
                if st.button(label="Search", key="button_search_place"):
                    for place in input_parameter_list:
                        # Construct the API endpoint URL
                        if place[1] == '':
                            url = f"https://nominatim.openstreetmap.org/search?q={place[0]}&format=json&limit=1000"
                        else:
                            url = f"https://nominatim.openstreetmap.org/search?q={place[0]}, {place[1]}&format=json&limit=1000"
                        # Send a GET request to the API endpoint
                        response = requests.get(url).json()                        
                        # If more than one result, return the first one
                        location = response[0]
                        # Extract the latitude and longitude coordinates from the first result
                        lat = location['lat']
                        lon = location['lon']
                        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
                        response = requests.get(url)
                        # Extract the JSON response as a dictionary
                        location2 = response.json()                                                     
                        if location2 == None:
                            st.write(str(place[0]) +' not found.')
                            places_str = places_str + 'None;None;None;None;None\n'
                        else:
                            item_info=[]
                            try:                                    
                                name = str(location2['display_name'].split(',')[0])
                                if name.lower() == place[0].lower():                                        
                                    street = location2['address']['road'] 
                                    try:
                                        number = location2['address']['house_number']
                                    except: 
                                        number = 'S/N'
                                    zp = location2['address']['postcode']
                                    item_info.append(street)
                                    item_info.append(number)
                                    item_info.append(zp)
                                    item_info.append(lat)
                                    item_info.append(lon)
                                    places_list.append(item_info)                                                                             
                                    places_str = places_str + item_info[0] + '; ' + item_info[1] + '; ' + item_info[2] + '; ' + str(item_info[3]) + '; ' + str(item_info[4]) + '\n'                                        
                                else:
                                    places_str = places_str + 'None;None;None;None;None\n' 
                                    st.write(str(place[0]) +' not found.')
                            except Exception as ex:
                                print(ex)
                                pass                            
                    # Showing results:                                    
                    ip_text_area_2 = st.empty()
                    input_parameter_text_area_2 = ip_text_area_2.text_area(label='Search results:', value=places_str, key='address_ip_text_area_2_'+str(position))   
                    value += 'input_parameter_attribute_'+str(position)+'='+str(places_list)+'\n'            
                    input_parameter_text_area = places_str
                    # Buttons: export and import values  
                    file_name = attribute_name+'_input_parameter_list'
                    if input_parameter_text_area != None or len(input_parameter_text_area) != 0:
                        save_file(file_name=file_name, file_value=input_parameter_text_area, extension='csv')
                    else:
                        st.warning('The file to be exported must not be empty.')
        elif generator_type == 'Device': # Marcos REVIEW!!!
            attribute_type = st.selectbox(label='Attribute type:', options=['List'], key=schema_type+'_attribute_type_'+str(position)) 
            # List:
            if attribute_type == 'List':
                value += 'generator_type_attribute_'+str(position)+'='+f'{generator_type}AttributeGenerator'+'\n'
                number_maximum_subattribute = st.number_input(label='Number of subattributes to generate:', value=5, key='number_maximum_subattribute_'+schema_type+'_'+str(position))
                value += 'number_maximum_subattribute_attribute_'+str(position)+'='+str(number_maximum_subattribute)+'\n'
                for subattribute in range(1, number_maximum_subattribute+1):
                    subattribute_name = st.text_input(label="Subattribute's name:", key=schema_type+'_subattribute_name_'+str(position)+'_'+str(subattribute)) 
                    value += 'name_subattribute_'+str(subattribute)+'_attribute_'+str(position)+'='+subattribute_name+'\n'
                    subattribute_type = st.selectbox(label='Subattribute type:', options=['String'], key=schema_type+'_subattribute_type_'+str(position)+'_'+str(subattribute)) 
                    value += 'type_subattribute_'+str(subattribute)+'_attribute_'+str(position)+'='+subattribute_type+'\n'
                    subattribute_input = st.text_area(label="Subattribute's input parameter:", key=schema_type+'_subattribute_input_'+str(position)+'_'+str(subattribute)) 
                    value += 'input_parameter_subattribute_'+str(subattribute)+'_attribute_'+str(position)+'='+subattribute_input+'\n'        
        elif generator_type == 'Position': # Marcos REVIEW!!!
            attribute_type = st.selectbox(label='Attribute type:', options=['AttributeComposite'], key=schema_type+'_attribute_type_'+str(position)) 
            # AttributeComposite: 
            if attribute_type == 'AttributeComposite':            
                value += 'generator_type_attribute_'+str(position)+'='+f'Object{generator_type}AttributeGenerator'+'\n'
                number_maximum_subattribute = st.number_input(label='Number of subattributes to generate:', value=3, key='number_maximum_subattribute_'+schema_type+'_'+str(position))
                value += 'number_maximum_subattribute_attribute_'+str(position)+'='+str(number_maximum_subattribute)+'\n'
                for subattribute in range(1, number_maximum_subattribute+1):
                    subattribute_name = st.text_input(label="Subattribute's name:", key=schema_type+'_subattribute_name_'+str(position)+'_'+str(subattribute)) 
                    value += 'name_subattribute_'+str(subattribute)+'_attribute_'+str(position)+'='+subattribute_name+'\n'
                    subattribute_type = st.selectbox(label='Subattribute type:', options=['float'], key=schema_type+'_subattribute_type_'+str(position)+'_'+str(subattribute)) 
                    value += 'type_subattribute_'+str(subattribute)+'_attribute_'+str(position)+'='+subattribute_type+'\n'
                input_parameter = st.text_area(label="Attribute's input parameter:", key=schema_type+'_input_parameter_'+str(position)) 
                value += 'input_parameter_attribute_'+str(position)+'='+input_parameter+'\n'

        # Important attributes:                
        is_important_attribute = st.checkbox(label=f'Is {attribute_name} an important attribute to include in the user profile?', value=False, key=schema_type+'_is_important_attribute_'+str(position)) 
        value += 'important_weight_attribute_'+str(position)+'='+str(is_important_attribute)+'\n'
        if is_important_attribute:
            # Ranking order:
            help_information.help_important_attribute_ranking_order()            
            ranking_order_original = st.selectbox(label='Select an order of importance?', options=['ascending', 'descending', 'neutral'], key="important_order_"+str(position))
            ranking_order = 'neut'
            if ranking_order_original == 'ascending':
                ranking_order = 'asc'
            elif ranking_order_original == 'descending':
                ranking_order = 'desc'
            value += 'ranking_order_by_attribute_'+str(position)+'='+ranking_order+'\n'
        value += '\n'
        st.markdown("""---""")
    return value

def get_item_profile_file():
    """
    Generate the item profile file (item_profile.conf).
    :return: The content of the item profile file.
    """
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
    help_information.help_important_attribute_ranking_order()
    ranking_order_original = st.selectbox(label='Select an order of importance?', options=['descending', 'ascending', 'neutral'], key="ip_important_order")
    ranking_order = 'neut'
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
    help_information.help_overlapping_attribute_values()    
    item_profile_value += 'overlap_midpoint_left_profile='+str(overlap_midpoint_left_profile)+'\n'
    item_profile_value += 'overlap_midpoint_right_profile='+str(overlap_midpoint_right_profile)+'\n'
    item_profile_value += '\n' 

def get_user_profile_file(user_schema, item_schema, context_schema=None):
    """
    Generate the user profile file (user_profile.csv).
    :param user_schema: The content of the user schema file.
    :param item_schema: The content of the item schema file.
    :param context_schema: The content of the context schema file.
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
    number_user_profile = st.number_input(label='Number of user profiles', value=initial_value)
                            
    # Generate user profile manual:                
    user_profile_df = generate_user_profile_manual(number_user_profile, attribute_column_list, item_possible_value_map, context_possible_value_map)                  
    return user_profile_df

def generate_user_profile_manual(number_user_profile, attribute_column_list, item_possible_value_map, context_possible_value_map=None):
    """
    Generate manually a user profile.
    :param number_user_profile:
    :param attribute_column_list:
    :param item_possible_value_map:
    :param context_possible_value_map:
    :return: 
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
    help_information.help_user_profile_id()
    st.dataframe(user_profile_df)   
    # Downloading user_profile.csv:
    if not inconsistent:
        save_df(df_name=config.USER_PROFILE_SCHEMA_NAME, df_value=export_df, extension='csv')        
    return user_profile_df

def run(generation_config_schema, user_schema, user_profile, item_schema, item_profile, with_context=False, context_schema=None):
    """
    Runs the workflow related to generating a synthetic dataset with explicit ratings.
    """
    with_correlation_checkbox = False
    inconsistent = False                
    col_run, col_stop = st.columns(2)
    with col_run:
        button_run = st.button(label='Run', key='button_run')
    with col_stop:
        button_stop = st.button(label='Stop', key='button_stop')
    generator = RatingExplicit(generation_config=generation_config_schema)
    output = st.empty()
    with console.st_log(output.code):
        if not inconsistent:
            if button_run:
                if with_context:
                    steps = 4
                else: 
                    steps = 3
                current_step = 0
                print('Starting execution')
                # Check if all the files required for the synthetic data generation exist:
                # Checking the existence of the file: "user_schema.conf"  
                progress_text = f'Generating data .....step {current_step + 1} from {steps}'
                my_bar = st.progress(0, text=progress_text)                
                if len(user_schema) != 0:
                    st.write(f'{config.USER_TYPE}.csv')
                    print('Generating user.csv')
                    user_file_df = generator.generate_user_file(user_schema=user_schema)
                    st.dataframe(user_file_df)
                    save_df(df_name=config.USER_TYPE, df_value=user_file_df, extension='csv')
                else:
                    st.warning('The user schema file (user_schema.conf) is required.')
                current_step = current_step + 1
                if button_stop:
                    st.experimental_rerun()
                else:
                    # Checking the existence of the file: "item_schema.conf"            
                    my_bar.progress(int(100/steps)*current_step, f'Generating data Step {current_step + 1} from {steps}: ')
                    if len(item_schema) != 0:
                        st.write(f'{config.ITEM_TYPE}.csv')
                        print('Generating item.csv')                    
                        item_file_df = generator.generate_item_file(item_schema=item_schema, item_profile=item_profile, with_correlation=with_correlation_checkbox)
                        st.dataframe(item_file_df)   
                        save_df(df_name=config.ITEM_TYPE, df_value=item_file_df, extension='csv')
                        current_step = current_step + 1
                    else:
                        st.warning('The item schema file (item_schema.conf) is required.')
                    my_bar.progress(int(100/steps*current_step), f'Generating data Step {current_step + 1} from {steps}: ')
                    if button_stop:
                        st.experimental_rerun()
                    else:                        
                        # Checking the existence of the file: "context_schema.conf"  
                        if with_context:                           
                            if context_schema:
                                st.write(f'{config.CONTEXT_TYPE}.csv')
                                print('Generating context.csv')                        
                                context_file_df = generator.generate_context_file(context_schema=context_schema)
                                st.dataframe(context_file_df)
                                save_df(df_name=config.CONTEXT_TYPE, df_value=context_file_df, extension='csv')
                                current_step = current_step + 1
                            else:
                                st.warning('The context schema file (context_schema.conf) is required.')               
                        # Checking the existence of the file: "generation_config.conf" 
                        my_bar.progress(int(100/steps*current_step), f'Generating data Step {current_step + 1} from {steps}: ')
                        if button_stop:
                            st.experimental_rerun()
                        else:
                            if len(generation_config_schema) != 0:
                                st.write('rating.csv')
                                if with_context:                                                  
                                    if context_schema:
                                        rating_file_df = generator.generate_rating_file(user_df=user_file_df, user_profile_df=user_profile, item_df=item_file_df, item_schema=item_schema, with_context=True, context_df=context_file_df, context_schema=context_schema)
                                    else:
                                        st.warning('The context schema file (context_schema.conf) is required.')
                                else:
                                    rating_file_df = generator.generate_rating_file(user_df=user_file_df, user_profile_df=user_profile, item_df=item_file_df, item_schema=item_schema)
                                st.dataframe(rating_file_df)
                                save_df(df_name='rating', df_value=rating_file_df, extension='csv')
                                                                                                        
                            else:
                                st.warning('The configuration file (generation_config.conf) is required.')
                            print('Synthetic data generation has finished.')   
                            my_bar.progress(100, 'Synthetic data generation has finished.')    
        else:
            st.warning('Before generating data ensure all files are correctly generated.')
            
def edit_schema_file(schema_file_name, schema_value):
    """
    Edit the content of a schema file.
    :param schema_file_name: The name of the schema file.
    :param schema_value: The content of the schema file.
    :return: The content of the edited schema file.
    """    
    with st.expander(f"Show {schema_file_name}.conf"):
        if st.checkbox(label='Edit file?', key=f"edit_{schema_file_name}"):
            schema_text_area = st.text_area(label='Current file:', value=schema_value, height=500, key=f'true_edit_{schema_file_name}')
        else:               
            schema_text_area = st.text_area(label='Current file:', value=schema_value, height=500, disabled=True, key=f'false_edit_{schema_file_name}')
    return schema_text_area

def save_file(file_name, file_value, extension):
    """
    Save a schema file.
    :param file_name: The name of the schema file.
    :param file_value: The content of the schema file.
    :param extension: The file extension ('*.conf' or '*.csv').
    """
    if extension == 'conf':
        link_file = f'<a href="data:text/plain;base64,{base64.b64encode(file_value.encode()).decode()}" download="{file_name}.{extension}">Download</a>'
    elif extension == 'csv':
        link_file = f'<a href="data:file/csv;base64,{base64.b64encode(file_value.encode()).decode()}" download="{file_name}.{extension}">Download</a>'
    st.markdown(link_file, unsafe_allow_html=True)    

def save_df(df_name, df_value, extension):
    """
    Save a df file.
    :param df_name: The name of the df file.
    :param df_value: The content of the df file.
    :param extension: The file extension ('*.csv').
    """
    link_df = f'<a href="data:file/csv;base64,{base64.b64encode(df_value.to_csv(index=False).encode()).decode()}" download="{df_name}.{extension}">Download</a>'
    st.markdown(link_df, unsafe_allow_html=True)    
