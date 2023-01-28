# sourcery skip: use-fstring-for-concatenation
import streamlit as st
# from PIL import Image
import config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import console
from datagencars.synthetic_dataset.generate_synthetic_dataset import GenerateSyntheticDataset


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
        if is_upload_schema := st.checkbox('Upload schema file', value=True, key='is_upload_schema_'+schema_type):
            if schema_file := st.file_uploader(label='Choose the schema file:', key=schema_type+'_schema_file'):
                value = schema_file.getvalue().decode("utf-8")        
        else:
            # [global]   
            value = '[global]'+'\n'
            value += 'type='+schema_type+'\n'
            number_attribute = st.number_input(label='Number of attributes to generate:', value=1, key='number_attribute_context')
            value += 'number_attributes='+str(number_attribute)+'\n'
            value += '\n'
            st.markdown("""---""")       

            # [attribute]
            for position in range(1, number_attribute+1):
                st.write('__[attribute'+str(position)+']__')
                value += '[attribute'+str(position)+']'+'\n'
                # name_attribute:     
                attribute_name = st.text_input(label="Attribute's name:", key='attribute_name_'+str(position))
                value += 'name_attribute_'+str(position)+'='+attribute_name+'\n'
                # generator_type_attribute:
                generator_type = st.selectbox(label='Generator type:', options=['Random', 'Fixed', 'URL', 'Address', 'Date', 'BooleanList'],  key='generator_type_'+str(position))
                value += 'generator_type_attribute_'+str(position)+'='+generator_type+'AttributeGenerator'+'\n'
                # type_attribute:
                attribute_type = None
                if generator_type == 'Random':                    
                    attribute_type = st.selectbox(label='Attribute type:', options=['Integer', 'String', 'Boolean'], key='attribute_type_'+str(position)+'_'+generator_type)
                    if attribute_type == 'Integer':
                        # Integer:
                        integer_min = st.number_input(label='Minimum value of the attribute', value=0, key='integer_min_'+str(position))
                        value += 'minimum_value_attribute_'+str(position)+'='+str(integer_min)+'\n'
                        integer_max = st.number_input(label='Maximum value of the ratings', value=0, key='integer_max_'+str(position))
                        value += 'maximum_value_attribute_'+str(position)+'='+str(integer_max)+'\n'
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
                            value += 'posible_value_'+str(i+1)+'_attribute_'+str(position)+'='+str_possible_value_list[i]+'\n'
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
                    input_parameter_text_area = ip_text_area.text_area(label='Introduce values below <place> (a value by line):', value='place', key='url_ip_text_area_'+str(position))   
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
                        if import_file := st.file_uploader(label='Import list', key='import_file'+str(position)):                                
                            input_parameter_text_area = ip_text_area.text_area(label='Introduce values below <place> (a value by line):', value=import_file.getvalue().decode("utf-8"), key='import_url_ip_text_area_'+str(position))                        
                    value += 'input_parameter_attribute_'+str(position)+'='+file_name+'\n'
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
                    input_parameter_text_area = ip_text_area.text_area(label='Introduce address values below <street,number,zp,latitude,longitude> (line by line):', value='street,number,zp,latitude,longitude', key='address_ip_text_area_'+str(position))   
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
                        if import_file := st.file_uploader(label='Import list', key='import_file'+str(position)):                                
                            input_parameter_text_area = ip_text_area.text_area(label='Introduce address values below <street,number,zp,latitude,longitude> (line by line):', value=import_file.getvalue().decode("utf-8"), key='import_address_ip_text_area_'+str(position))                        
                    value += 'input_parameter_attribute_'+str(position)+'='+file_name+'\n'
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
                        value += 'component_'+str(idx+1)+'_attribute_'+str(position)+'='+component+'\n'
                    component_input_parameter = st.number_input(label='Number of boolean values to generate for these components:', value=1, key='component_input_parameter')
                    value += 'input_parameter_attribute_'+str(position)+'='+str(component_input_parameter)+'\n'

                value += 'type_attribute_'+str(position)+'='+attribute_type+'\n'
                # Important attributes:                
                is_important_attribute = st.checkbox(label=f'Is {attribute_name} an important attribute to include in the user profile?', value=False)
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
        sch_text_area = st.empty()
        if st.checkbox(label='Edit file?', key='edit_schema_'+schema_type):
            schema_text_area = sch_text_area.text_area(label='Current file:', value=value, height=500, key=schema_type+'_schema_text_area')
        else:
            schema_text_area = sch_text_area.text_area(label='Current file:', value=value, height=500, disabled=True, key=schema_type+'_schema_text_area')
        st.download_button(label='Download', data=schema_text_area, file_name=schema_type+'_schema.conf')
        return schema_text_area

    context = None
    if is_context := st.sidebar.checkbox('With context', value=True):
        context = True
        tab_generation, tab_user, tab_item, tab_context, tab_run  = st.tabs(['Generation', 'Users', 'Items', 'Contexts', 'Run'])
    else:
        context = False
        tab_generation, tab_user, tab_item, tab_run = st.tabs(['Generation', 'Users', 'Items', 'Run'])  

    # GENERATION SETTINGS:
    with tab_generation:
        st.header('Generation')
        # Uploading the file: "generation_config.conf"
        generation_config_value = ''
        if is_upload_generation := st.checkbox('Upload generation file', value=True):            
            if generation_config_file := st.file_uploader(label='Choose the generation file:', key='generation_config_file'):
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
            rating_count = st.number_input(label='Number of ratings to generate:', value=0)
            rating_min = st.number_input(label='Minimum value of the ratings:', value=1, key='rating_min')
            rating_max = st.number_input(label='Maximum value of the ratings:', value=5, key='rating_max')
            rating_impact = st.number_input(label='Impact of user expectatiosn in future ratings (%):', value=25)            
            rating_distribution = st.selectbox(label='Choose a distribution to generate the ratings:', options=['Uniform', 'Gaussian'])                        
            gaussian_distribution = True
            if rating_distribution == 'Uniform':
                gaussian_distribution = False                    
            # st.write('Dates of the ratings to generate (years only):')
            # rating_min = st.number_input(label='From:', value=1980)
            # rating_max = st.number_input(label='Until:', value=2020)                
            rating_value += ('number_rating=' + str(rating_count) + '\n' +
                             'minimum_value_rating=' + str(rating_min) + '\n' +
                             'maximum_value_rating=' + str(rating_max) + '\n' + 
                             'percentage_rating_variation=' + str(rating_impact) + '\n' +
                             'gaussian_distribution=' + str(gaussian_distribution) + '\n')
            st.markdown("""---""")
            # [item profile]
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
        if edit_config_file := st.checkbox(label='Edit file?', key='edit_config_file'):
            config_file_text_area = st.text_area(label='Current file:', value=generation_config_value, height=500)
        else:
            config_file_text_area = st.text_area(label='Current file:', value=generation_config_value, height=500, disabled=True)    
        st.download_button(label='Download', data=config_file_text_area, file_name='generation_config.conf')  
                               
    # USER SETTINGS:
    with tab_user:        
        st.header('Users')
        schema_type = 'user'
        user_schema_text_area = generate_schema_file(schema_type)

    # ITEM SETTINGS:
    with tab_item:
        st.header('Items')
        schema_type = 'item'
        item_schema_text_area = generate_schema_file(schema_type)

    # CONTEXT SETTINGS:
    if context:
        with tab_context:
            st.header('Contexts')
            schema_type = 'context'
            context_schema_text_area = generate_schema_file(schema_type)

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
                if user_schema_text_area:
                    st.write('user.csv')
                    print('Generating user.csv')                
                    user_file_bar = st.progress(value=0)
                    for percent_complete in range(100):
                        time.sleep(0.1)
                        user_file_bar.progress(percent_complete + 1)   
                        if button_stop: 
                            print('Stopping execution')                            
                            user_file_bar.empty()                                               
                    user_file = ''
                    st.download_button(label='Download user.csv', data='', file_name=user_file, key='user_button')                  
                else:
                    st.warning('The user schema file (user_schema.conf) is required.')
                
                # Checking the existence of the file: "item_schema.conf"            
                if item_schema_text_area:
                    st.write('item.csv')
                    print('Generating item.csv')
                    item_file_bar = st.progress(value=0)
                    for percent_complete in range(100):
                        time.sleep(0.1)
                        item_file_bar.progress(percent_complete + 1)   
                        if button_stop: 
                            print('Stopping execution')
                            item_file_bar.empty()                                              
                    item_file = ''
                    st.download_button(label='Download item.csv', data='', file_name=item_file, key='item_button')         
                else:
                    st.warning('The item schema file (item_schema.conf) is required.')
                
                if context:
                    # Checking the existence of the file: "context_schema.conf"                             
                    if context_schema_text_area:
                        st.write('context.csv')
                        print('Generating context.csv')  
                        context_file_bar = st.progress(0)
                        for percent_complete in range(100):
                            time.sleep(0.1)
                            context_file_bar.progress(percent_complete + 1) 
                            if button_stop: 
                                print('Stopping execution')
                                context_file_bar.empty()
                        context_file = ''   
                        st.download_button(label='Download context.csv', data='', file_name=context_file, key='context_button')         
                    else:
                        st.warning('The context schema file (context_schema.conf) is required.')
                                
                # Checking the existence of the file: "generation_config.conf"             
                if config_file_text_area:
                    st.write('rating.csv')
                    print('Generating rating.csv')  
                    rating_file_bar = st.progress(0)
                    for percent_complete in range(100):
                        time.sleep(0.1)
                        rating_file_bar.progress(percent_complete + 1)  
                        if button_stop: 
                            print('Stopping execution')
                            rating_file_bar.empty()          
                    rating_file = ''             
                    st.download_button(label='Download rating.csv', data='', file_name=rating_file, key='rating_button') 
                else:
                    st.warning('The configuration file (generation_config.conf) is required.')                  

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
                upload_context = st.checkbox("With context", value=True)
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
