import io
from datagencars.synthetic_dataset.generator.generator_output_file.generator_explicit_rating_file import GeneratorExplicitRatingFile

from streamlit_app import config
import console
import pandas as pd
import requests
import streamlit as st
from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from streamlit_app import help_information
from streamlit_app.preprocess_dataset import wf_generate_user_profile
from streamlit_app.preprocess_dataset.wf_util import save_df, save_file
from streamlit_app.workflow_graph import workflow_image
from datagencars.synthetic_dataset.generator.generator_output_file.generator_user_file import GeneratorUserFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_item_file import GeneratorItemFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_context_file import GeneratorContextFile
from streamlit_app.preprocess_dataset import wf_util


def generate_synthtetic_dataset(with_context):
    """
    Generates a synthetic dataset with explicit ratings.
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    """ 
    # Help information:
    help_information.help_explicit_rating_wf()

    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='GenerateSyntheticDataset(Explicit_ratings)', init_step='True', with_context=with_context, optional_value_list=[("UP", "Manual")])
    
    # Loading available tabs:
    if with_context:        
        tab_user, tab_item, tab_context, tab_rating  = st.tabs(config.CONTEXT_TAB_LIST)
    else:        
        tab_user, tab_item, tab_rating = st.tabs(config.WITHOUT_CONTEXT_TAB_LIST)
             
    # TAB --> User:
    with tab_user:
        # Generating or uploading the configuration shema file (generation_config.conf):
        generation_config_schema = get_general_settings(with_context, tab_type='tab_user')        
        # Generating or uploading the user schema file (user_schema.conf):
        st.header('Users')        
        if st.checkbox(f'Upload the data {config.USER_TYPE} schema file', value=True, key=f'is_upload_{config.USER_SCHEMA_NAME}_file'):
            # Uploading the file ("user_schema.conf"):
            schema_value = upload_schema_file(schema_file_name=config.USER_SCHEMA_NAME, tab_type='tab_user')
        else:
            # Generating the schema file ("user_schema.conf"):
            schema_value = get_schema_file(schema_type=config.USER_TYPE)        
        # Editing schema:
        user_schema = edit_schema_file(schema_file_name=config.USER_SCHEMA_NAME, schema_value=schema_value, tab_type='tab_user')        
        # Generating the user file (user.csv):
        generate_user_file(generation_config=generation_config_schema, user_schema=user_schema)
    # TAB --> Item and Item Profile:
    with tab_item:
        # Generating or uploading the configuration shema file (generation_config.conf):
        generation_config_schema = get_general_settings(with_context, tab_type='tab_item')        
        # Generating or uploading the item schema file (item_schema.conf):
        st.header('Items')        
        if st.checkbox(f'Upload the data {config.ITEM_TYPE} schema file', value=True, key=f'is_upload_{config.ITEM_SCHEMA_NAME}_file'):
            # Uploading the file ("item_schema.conf"):
            schema_value = upload_schema_file(schema_file_name=config.ITEM_SCHEMA_NAME, tab_type='tab_item')
        else:
            # Generating the schema file ("item_schema.conf"):
            schema_value = get_schema_file(schema_type=config.ITEM_TYPE)
        # Editing schema:
        item_schema = edit_schema_file(schema_file_name=config.ITEM_SCHEMA_NAME, schema_value=schema_value, tab_type='tab_item')
        
        # Generating the item file (item.csv):
        with_correlation = st.checkbox(f'Apply correlation between item attributes?', value=False, key=f'is_with_correlation_{config.ITEM_PROFILE_SCHEMA_NAME}_file')
        # Generating or uploading the item profile schema file (item_profile.conf):
        if with_correlation:
            # Uploading the file ("item_profile.conf"):
            if st.checkbox(f'Upload the data {config.ITEM_PROFILE_TYPE} schema file', value=True, key=f'is_upload_{config.ITEM_PROFILE_SCHEMA_NAME}_file'):
                item_profile_value = upload_schema_file(schema_file_name=config.ITEM_PROFILE_SCHEMA_NAME, tab_type='tab_item')
            else:
                # Generating the file ("item_profile.conf"):
                item_profile_value = get_item_profile_file()
            # Editing schema:
            item_profile = edit_schema_file(schema_file_name=config.ITEM_PROFILE_SCHEMA_NAME, schema_value=item_profile_value, tab_type='tab_item')        
            # Generating the item file (item.csv) with correlation:
            generate_item_file(generation_config=generation_config_schema, item_schema=schema_value, item_profile=item_profile)
        else:
            # Generating the item file (item.csv) without correlation:
            generate_item_file(generation_config=generation_config_schema, item_schema=schema_value)
    # TAB --> Context:
    if with_context:
        with tab_context:
            # Generating or uploading the configuration shema file (generation_config.conf):
            generation_config_schema = get_general_settings(with_context, tab_type='tab_context')        
            # Generating or uploading the context schema file (context_schema.conf):
            st.header('Contexts')                 
            if st.checkbox(f'Upload the data {config.CONTEXT_TYPE} schema file', value=True, key=f'is_upload_{config.CONTEXT_SCHEMA_NAME}_file'):
                # Uploading the file ("context_schema.conf"):
                schema_value = upload_schema_file(schema_file_name=config.CONTEXT_SCHEMA_NAME, tab_type='tab_context')
            else:
                # Generating the schema file ("context_schema.conf"):
                schema_value = get_schema_file(schema_type=config.CONTEXT_TYPE)
            # Editing schema:
            context_schema = edit_schema_file(schema_file_name=config.CONTEXT_SCHEMA_NAME, schema_value=schema_value, tab_type='tab_context')
            # Generating the context file (context.csv):
            generate_context_file(generation_config=generation_config_schema, context_schema=schema_value)
    # TAB --> Rating:
    with tab_rating:        
        # Initializing files:
        generation_config=item_schema=context_schema=''
        user_df=user_profile_df=item_df=context_df= pd.DataFrame()

        ###### Generation config #####: 
        # Generating or uploading the configuration shema file (generation_config.conf):        
        generation_config = get_general_settings(with_context, tab_type='tab_rating')        
        
        ###### User, Item and Context #####:
        if with_context:
            st.header('User, Item and Context data')
        else:
            st.header('User and Item data')
        # Uploading the user file (user.csv):        
        user_df = wf_util.load_one_file(file_type='user', wf_type='wf_generate_explicit_rating')     
        ###### Item #####:        
        # Uploading the item file (user.csv):
        item_df = wf_util.load_one_file(file_type='item', wf_type='wf_generate_explicit_rating')
        ###### Context #####:        
        if with_context:
            # Uploading the context file (user.csv):
            context_df = wf_util.load_one_file(file_type='context', wf_type='wf_generate_explicit_rating')
        
        ###### User profile #####:
        st.header('User profile')
        # Generating or uploading the user profile file (user_profile.csv):
        if st.checkbox(f'Upload the data {config.USER_PROFILE_SCHEMA_NAME} file', value=True, key=f'is_upload_{config.USER_PROFILE_SCHEMA_NAME}_file'):
            # Uploading the file ("user_profile.csv"):
            user_profile_df = upload_user_profile_file(tab_type='tab_up')
        else:
            # Generating the file ("user_profile.csv"):
            if with_context:
                user_profile_df = get_user_profile_file(user_schema, item_schema, context_schema)
            else:
                user_profile_df = get_user_profile_file(user_schema, item_schema)        

        ###### Item and Context schemas #####:                 
        if with_context:
            st.header('Item and Context schema files (optionals)')
        else:
            st.header('Item schema file (optional)')
        # Uploading the item schema file (item_schema.conf): optional
        item_schema_value = upload_schema_file(schema_file_name=config.ITEM_SCHEMA_NAME, tab_type='tab_rating')
        # Editing schema:
        item_schema = edit_schema_file(schema_file_name=config.ITEM_SCHEMA_NAME, schema_value=item_schema_value, tab_type='tab_rating')
        if with_context:
            # Uploading the context schema file (context_schema.conf): optional     
            context_schema_value = upload_schema_file(schema_file_name=config.CONTEXT_SCHEMA_NAME, tab_type='tab_rating')
            # Editing schema:
            context_schema = edit_schema_file(schema_file_name=config.CONTEXT_SCHEMA_NAME, schema_value=context_schema_value, tab_type='tab_rating')
        
        # Generating the rating file (rating.csv):
        generate_rating_file(with_context=with_context, generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df, item_schema=item_schema, context_df=context_df, context_schema=context_schema)
        
def get_general_settings(with_context, tab_type):
    """
    Display and manage general settings for data generation.
    :param with_context: Boolean indicating whether to include context data.
    :param tab_type: Type of tab or section in the GUI.
    :return: The edited data generation configuration schema.
    """
    st.header('General settings')    
    if st.checkbox('Upload the data generation configuration file', value=True, key=f'is_upload_{config.GENERATION_CONFIG_SCHEMA_NAME}_{tab_type}_file'):
        # Uploading the file ("generation_config.conf"):
        schema_value = upload_schema_file(schema_file_name=config.GENERATION_CONFIG_SCHEMA_NAME, tab_type=tab_type)
    else:
        # Generating the schema file ("generation_config.conf"):
        schema_value = get_generation_config_file(with_context)
    # Editing schema:
    return edit_schema_file(schema_file_name=config.GENERATION_CONFIG_SCHEMA_NAME, schema_value=schema_value, tab_type=tab_type)   

def upload_schema_file(schema_file_name, tab_type):
    """
    Upload schema from file.
    :param schema_file_name: The name of the schema file.
    :return: The content of the schema file.
    """
    schema_file_value = ''
    with st.expander(f"Upload {schema_file_name}.conf"):
        if schema_file := st.file_uploader(label='Choose the file:', key=f"{schema_file_name}_file_{tab_type}"):
            schema_file_value = schema_file.getvalue().decode("utf-8")
    return schema_file_value

def upload_user_profile_file(tab_type):
    """
    Upload an existing user profile.
    :return: A dataframe with the user profile content.
    """
    user_profile_df = pd.DataFrame()
    with st.expander(label=f'Upload {config.USER_PROFILE_SCHEMA_NAME}.csv'):
        if user_profile_file := st.file_uploader(label='Choose the file:', key=f'{config.USER_PROFILE_SCHEMA_NAME}_file_{tab_type}'):
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
    # Generating the text of the file "generation_config.conf":
    generation_config_schema = dimension_value + '\n' + rating_value + '\n' + item_profile_value
    return generation_config_schema

def get_schema_file(schema_type):    
    """
    Generate a schema file: "user_schema.conf", "item_schema.conf" or "context_schema.conf".
    :param schema_type: The type of schema (user, item or context).
    :return: The content of the schema file.
    """
    # Help information:
    help_information.help_schema_file()
    
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
                st.text(bool_possible_value_list)
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
            value += 'type_attribute_'+str(position)+'='+f'{attribute_type}'+'\n'
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
            value += 'type_attribute_'+str(position)+'='+f'{attribute_type}'+'\n'
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
            value += 'type_attribute_'+str(position)+'='+f'{attribute_type}'+'\n'
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
            value += 'type_attribute_'+str(position)+'='+f'{attribute_type}'+'\n'
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
            value += 'type_attribute_'+str(position)+'='+f'{attribute_type}'+'\n'
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
            value += 'type_attribute_'+str(position)+'='+f'{attribute_type}'+'\n'
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
    item_profile_value=''
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
    return item_profile_value

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
    number_user_profile = st.number_input(label='Number of user profiles:', value=initial_value, disabled=True)
    st.warning('The number of profiles has been previously defined in the ```user_profile_id``` attribute of the ```user_schema.conf``` file. If you want to change it, you must first modify the ```user_schema.conf``` file.')
                            
    # Generate user profile manual:                
    user_profile_df = wf_generate_user_profile.generate_user_profile_manual(number_user_profile, attribute_column_list, item_possible_value_map, context_possible_value_map)
    return user_profile_df
   
def edit_schema_file(schema_file_name, schema_value, tab_type):
    """
    Edit the content of a schema file.
    :param schema_file_name: The name of the schema file.
    :param schema_value: The content of the schema file.
    :return: The content of the edited schema file.
    """
    schema_text_area = schema_value
    with st.expander(f"Show {schema_file_name}.conf"):
        edit_checkbox = st.checkbox(label='Edit file?', value=False, key=f"false_initial_{schema_file_name}_{tab_type}")
        st.warning("If you edit the file and want to save the changes made, you must disable the 'Edit file?' checkbox again.")
        if edit_checkbox:
            schema_text_area = st.text_area(label='Current file:', value=schema_text_area, height=500, disabled=False, key=f'true_edit_{schema_file_name}_{tab_type}')
        else:        
            schema_text_area = st.text_area(label='Current file:', value=schema_text_area, height=500, disabled=True, key=f'true_edit_{schema_file_name}_{tab_type}')            
        # Saving schema:
        save_file(file_name=schema_file_name, file_value=schema_text_area, extension='conf')
    return schema_text_area
    
def generate_user_file(generation_config, user_schema):
    """
    Generates the user file from user_schema. 
    :param generation_config: The configuration file.
    :param user_schema: The user schema. It should contain information about users.    
    :return: The user file generated from the user schema.
    """    
    user_file_df = pd.DataFrame()    
    if st.button(label='Generate user file', key='button_tab_user'):            
        if (len(user_schema) != 0) and (len(generation_config) != 0):
            output = st.empty()
            with console.st_log(output.code): 
                print(f'Generating {config.USER_TYPE}.csv')   
                generator = GeneratorUserFile(generation_config=generation_config, user_schema=user_schema)
                user_file_df = generator.generate_file()
                print('User file generation has finished.')   
                with st.expander(label=f'Show the generated {config.USER_TYPE}.csv file:'):
                    st.dataframe(user_file_df)
                    save_df(df_name=config.USER_TYPE, df_value=user_file_df, extension='csv')
        else:
            st.warning(f'The user schema (user_schema.conf) and general setting (general_config.conf) files are required.')
    return user_file_df

def generate_item_file(generation_config, item_schema, item_profile=None):
    """
    Generates the item file from item_schema. 
    :param generation_config: The configuration file.
    :param item_schema: The item schema. It should contain information about items.
    :param item_profile: The item profile.    
    :return: The item file generated from the item schema.
    """    
    item_file_df = pd.DataFrame()   
    if st.button(label='Generate item file', key='button_tab_item'): 
        # Considering the correlation between attributes (item_profile.csv is required):
        if (len(item_schema) != 0) and (item_profile) and (len(generation_config) != 0):                        
            output = st.empty()
            with console.st_log(output.code):
                print(f'Generating {config.ITEM_TYPE}.csv')
                generator = GeneratorItemFile(generation_config=generation_config, item_schema=item_schema, item_profile=item_profile)
                item_file_df = generator.generate_file()
                print('Item file generation has finished.')   
                with st.expander(label=f'Show the generated {config.ITEM_TYPE}.csv file:'):
                    st.dataframe(item_file_df)
                    save_df(df_name=config.ITEM_TYPE, df_value=item_file_df, extension='csv')
        # Without correlation between attributes (item_profile.csv is not required):
        elif (len(item_schema) != 0) and (not item_profile) and (len(generation_config) != 0):                  
            output = st.empty()
            with console.st_log(output.code):
                print(f'Generating {config.ITEM_TYPE}.csv')
                generator = GeneratorItemFile(generation_config=generation_config, item_schema=item_schema)
                item_file_df = generator.generate_file()
                print('Item file generation has finished.')   
                with st.expander(label=f'Show the generated {config.ITEM_TYPE}.csv file:'):
                    st.dataframe(item_file_df)
                    save_df(df_name=config.ITEM_TYPE, df_value=item_file_df, extension='csv')
        else:            
            st.warning(f'The item schema (item_schema.conf) and general setting (general_config.conf) files are required. The item profile schema (item_profile.conf) file should only be uploaded if you want to generate correlated item attributes ("check "with correlation" and upload the item profile").')
    return item_file_df

def generate_context_file(generation_config, context_schema):    
    """
    Generates the context file from context_schema. 
    :param context_schema: The context schema. It should contain information about contexts.
    :param generation_config: The configuration file.
    :return: The context file generated from the context schema.
    """           
    context_file_df = pd.DataFrame()
    if st.button(label='Generate context file', key='button_tab_context'):            
        if (len(context_schema) != 0) and (len(generation_config) != 0):
            output = st.empty()
            with console.st_log(output.code): 
                print(f'Generating {config.CONTEXT_TYPE}.csv')   
                generator = GeneratorContextFile(generation_config=generation_config, context_schema=context_schema)            
                context_file_df = generator.generate_file()
                print('Context file generation has finished.')   
                with st.expander(label=f'Show the generated {config.CONTEXT_TYPE}.csv file:'):
                    st.dataframe(context_file_df)
                    save_df(df_name=config.CONTEXT_TYPE, df_value=context_file_df, extension='csv')
        else:
            st.warning(f'The context schema (context_schema.conf) and general setting (general_config.conf) files are required.')
    return context_file_df

def generate_rating_file(with_context, generation_config, user_df, user_profile_df, item_df, item_schema=None, context_df=None, context_schema=None):
    """
    Generate a rating file based on the provided data and configuration.
    :param generation_config: The configuration for rating file generation.
    :param user_df: The dataFrame with user data.
    :param user_profile: The dataFrame with user profiles.
    :param item_df: The dataFrame with item data.
    :param context_df: The dataFrame with context data (optional).
    :param item_schema: The item schema (optional).
    :param context_schema: The context schema (optional).
    :return: A dataFrame containing the generated rating data.
    """
    generator = None    
    rating_file_df = pd.DataFrame()
    if st.button(label='Generate rating file', key='button_tab_rating'):
        if with_context:  
            # The mandatory files to be uploaded are checked (including contextual information):
            if (len(generation_config) !=0) and (not user_df.empty) and (not user_profile_df.empty) and (not item_df.empty) and (not context_df.empty):
                # All files are uploaded, including item and context schemas:  
                if (len(item_schema) != 0) and (len(context_schema) != 0):
                    generator = GeneratorExplicitRatingFile(generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df, item_schema=item_schema, context_df=context_df, context_schema=context_schema)
                # All files are uploaded, except context schema:
                elif (len(item_schema) != 0) and (len(context_schema) == 0):
                    generator = GeneratorExplicitRatingFile(generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df, item_schema=item_schema, context_df=context_df)
                # All files are uploaded, except item schema:
                elif (len(item_schema) == 0) and (len(context_schema) != 0):
                    generator = GeneratorExplicitRatingFile(generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df, context_df=context_df, context_schema=context_schema)
                # All files are uploaded, except item and context schemas:
                else:                    
                    generator = GeneratorExplicitRatingFile(generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df, context_df=context_df)                        
            else:
                st.warning(f'At least the generation configuration (generation_config.conf), user (user.csv), user profile (user_profile.csv), item (item.csv) and context (context.csv) files must be uploaded. The item and context schema files (item_schema.conf and context_schema.conf) are optionals.')
        else:
            # The mandatory files to be uploaded are checked (without contextual information):
            if (len(generation_config) !=0) and (not user_df.empty) and (not user_profile_df.empty) and (not item_df.empty):
                # All files are uploaded, including the item schema:
                if (len(item_schema) != 0):
                    generator = GeneratorExplicitRatingFile(generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df, item_schema=item_schema)
                # All files are uploaded, except item schema:
                else:
                    generator = GeneratorExplicitRatingFile(generation_config=generation_config, user_df=user_df, user_profile_df=user_profile_df, item_df=item_df)
            else:
                st.warning(f'At least the generation configuration (generation_config.conf), user (user.csv), user profile (user_profile.csv) and item (item.csv) files must be uploaded. The item schema file (item_schema.conf) is optional.')
        # Generating rating file (rating.csv):        
        if generator:
            output = st.empty()
            with console.st_log(output.code):              
                rating_file_df = generator.generate_file()
                print('Rating file generation has finished.')   
                with st.expander(label=f'Show the generated {config.RATING_TYPE}.csv file:'):
                    st.dataframe(rating_file_df)
                    save_df(df_name=config.RATING_TYPE, df_value=rating_file_df, extension='csv')       
    return rating_file_df
