# sourcery skip: use-fstring-for-concatenation
import streamlit as st
import pandas as pd
import numpy as np
import datetime
# from PIL import Image
import config

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
    context = None
    if is_context := st.sidebar.checkbox('With context', value=True):        
        context = True
        tab_generation, tab_user, tab_item, tab_context  = st.tabs(['Generation', 'Users', 'Items', 'Contexts'])
    else:
        context = False        
        tab_generation, tab_user, tab_item = st.tabs(['Generation', 'Users', 'Items'])  

    # GENERATION SETTINGS:
    with tab_generation:
        st.header('Generation')
        value = ''
        if is_upload_generation := st.checkbox('Upload generation file', value=True):
            if generation_config_file := st.file_uploader(label='Choose the generation file:', key='generation_config_file'):
                value = generation_config_file.getvalue().decode("utf-8")
        else:
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
            # st.write('Dates of the ratings to generate (years only):')
            # rating_min = st.number_input(label='From:', value=1980)
            # rating_max = st.number_input(label='Until:', value=2020)                
            rating_value += ('number_rating=' + str(rating_count) + '\n' +
                             'minimum_value_rating=' + str(rating_min) + '\n' +
                             'maximum_value_rating=' + str(rating_max) + '\n' + 
                             'percentage_rating_variation=' + str(rating_impact) + '\n' +
                             'gaussian_distribution=' + str(rating_distribution) + '\n')
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
            value = dimension_value + '\n' + rating_value + '\n' + item_profile_value                         

    # USER SETTINGS:
    with tab_user:        
        st.header('Users')
        schema_type = 'user'
    # ITEM SETTINGS:
    with tab_item:
        st.header('Items')
        schema_type = 'item'
    # CONTEXT SETTINGS:
    if context:
        with tab_context:
            st.header('Contexts')
            schema_type = 'context'

    if is_upload_schema := st.checkbox('Upload schema file', value=True):
        if schema_file := st.file_uploader(label='Choose the schema file:', key='schema_file'):
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
            value += '[attribute'+str(position)+']'+'\n'
            # name_attribute:     
            attribute_name = st.text_input(label="Attribute's name:", key='attribute_name_'+str(position))
            value += 'name_attribute_'+str(position)+'='+attribute_name+'\n'
            # generator_type_attribute:
            generator_type = st.selectbox(label='Generator type:', options=['Random', 'Fixed', 'URL', 'Address', 'Date', 'BooleanArrayList'],  key='generator_type_'+str(position))
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
                    area_column, button_column = st.columns(2)
                    with area_column:
                        string_text_area = st.text_area(label='Introduce new values to the list (split by comma):', value='rainy, cloudy, sunny', key='string_text_area_'+str(position))  
                        str_possible_value_list = string_text_area.split(',')
                        number_possible_value = len(str_possible_value_list)
                        for i in range(number_possible_value):
                            value += 'posible_value_'+str(i+1)+'attribute_'+str(position)+'='+str_possible_value_list[i]+'\n'
                        value += 'number_posible_values_attribute_'+str(position)+'='+str(number_possible_value)+'\n'                    
                    with button_column:                        
                        export_button = st.download_button(label='Export list', data=string_text_area, file_name='str_possible_value_list.csv', key='export_button_'+str(position)) 
                        if import_file := st.file_uploader(label='Import list', key='import_file'):                            
                            string_text_area = st.text_area(label='Introduce new values to the list (split by comma):', value=import_file.getvalue().decode("utf-8"), key='import_button_'+str(position))                          
                elif attribute_type == 'Boolean':
                    # Boolean:                 
                    boolean_possible_value_list = ['True', 'False']
                    boolean_text_area = st.text_area(label='Introduce new values to the list (split by comma):', value='True, False', key='boolean_text_area_'+str(position))  
            elif generator_type == 'Fixed':                    
                attribute_type = st.selectbox(label='Attribute type:', options=['Integer', 'String', 'Boolean'], key='attribute_type_'+str(position)+'_'+generator_type)
                fixed_input = st.text_input(label='Imput the fixed value:', key='fixed_input_'+str(position))
                value += 'input_parameter_attribute_'+str(position)+'='+str(fixed_input)+'\n'
            elif generator_type == 'URL':                    
                attribute_type = st.selectbox(label='Attribute type:', options=['AttributeComposite'], key='attribute_type_'+str(position)+'_'+generator_type)
            elif generator_type == 'Address':                    
                attribute_type = st.selectbox(label='Attribute type:', options=['AttributeComposite'], key='attribute_type_'+str(position)+'_'+generator_type)
                address_area_column, address_button_column = st.columns(2)
                with address_area_column:
                    st.write('Add this address')
                    street_address = st.text_input(label='Street:', key='street_address_'+str(position))
                    number_address = st.number_input(label='Number:', value=0, key='number_address_'+str(position))
                    zip_code_address = st.number_input(label='Zip Code:', value=0, key='zip_code_address_'+str(position))
                    latitude_address = st.text_input(label='Latitude:', key='latitude_address_'+str(position))
                    longitude_address = st.text_input(label='Latitude:', key='longitude_address_'+str(position))
                    poi_address = st.text_input(label='Place of Interest (e.g., restaurant):', key='poi_address_'+str(position))                    
                with address_button_column:                                                        
                    if add_button := st.button(label='Add', key='add_button_'+str(position)):
                        address_value = f'{street_address};{number_address};{zip_code_address};{latitude_address};{longitude_address}'
                        address_list = st.text_area(label='Introduce new addresses to the list (split by comma):', value=address_value, key='address_list_'+str(position))                    
                    if search_button := st.button(label='Search', key='search_button_'+str(position)):
                        st.write('TODO')
                    if address_export_button := st.button(label='Export list', key='address_export_button_'+str(position)):
                        st.write('TODO')
                    if address_import_button := st.button(label='Import list', key='address_import_button_'+str(position)):
                        st.write('TODO')
            elif generator_type == 'Date':                    
                attribute_type = st.selectbox(label='Attribute type:', options=['Integer'], key='attribute_type_'+str(position)+'_'+generator_type)
                st.write('Imput the range of dates (years only):')
                date_min = st.number_input(label='From:', value=1980, key='date_min_'+str(position))
                value += 'minimum_value_attribute_'+str(position)+'='+str(date_min)+'\n'
                date_max = st.number_input(label='Until:', value=2020, key='date_max_'+str(position))
                value += 'maximum_value_attribute_'+str(position)+'='+str(date_max)+'\n'
            elif generator_type == 'BooleanArrayList':                    
                attribute_type = st.selectbox(label='Attribute type:', options=['ArrayList'], key='attribute_type_'+str(position)+'_'+generator_type)
                boolean_list = st.text_area(label='Introduce boolean values to the list (split by comma):', value='True, False, True', key='boolean_list_'+str(position))                
            value += 'type_attribute_'+str(position)+'='+attribute_type+'\n'                                                                                                                             
            # distribution_type = st.selectbox(label='Distribution type:', options=['Uniform', 'Gaussian'], key='distribution_type_'+str(position))
            # with_correlation = st.checkbox('Attribute with correlation', value=True)
            value += '\n'
            st.markdown("""---""")  

    if edit_schema := st.checkbox(label='Edit file?'):
        user_schema_text_area = st.text_area(label='Current file:', value=value, height=500)
    else:
        user_schema_text_area = st.text_area(label='Current file:', value=value, height=500, disabled=True)
    st.download_button(label='Download', data=user_schema_text_area, file_name=schema_type+'_schema.conf')  

elif general_option == 'Analysis an existing dataset':
    is_analysis = st.sidebar.radio(label='Analysis an existing dataset', options=['Data visualization', 'Replicate dataset', 'Extend dataset', 'Recalculate ratings', 'Replace NULL values', 'Generate user profile'])
    if is_analysis == 'Data visualization':  
        tab1, tab2, tab3, tab4, tab5 = st.tabs(['Upload dataset', 'Users', 'Items', 'Contexts', 'Ratings'])
        def replace_count_missing_values(dataframe, replace_values={}):
            """
            Count missing values in the dataframe.
            """
            for k,v in replace_values.items():
                dataframe.replace(k, np.nan, inplace=True)
            missing_values = dataframe.isnull().sum()
            st.dataframe(dataframe)
            st.write("Missing values:")
            st.table(missing_values)
        def list_attributes_and_ranges(dataframe):
            """
            List attributes and ranges of the dataframe.
            """
            st.write(f"Attributes and value ranges:")
            for column in dataframe.columns:
                if dataframe[column].dtype in ['int64', 'float64']:
                    st.write(f"{column}: {dataframe[column].min()} - {dataframe[column].max()}")
                elif dataframe[column].dtype == 'object':
                    try:
                        dataframe[column] = pd.to_datetime(dataframe[column])
                        st.write(f"{column}: {dataframe[column].min().strftime('%Y-%m-%d')} - {dataframe[column].max().strftime('%Y-%m-%d')}")
                    except ValueError:
                        unique_values = dataframe[column].dropna().unique()
                        unique_values_str = ', '.join([str(value) for value in unique_values])
                        st.write(f"{column}: {unique_values_str}")
                else:
                    st.write(f"{column} has an unsupported data type")
        with tab1:
            option = st.selectbox('Choose between uploading multiple datasets or a single dataset:', ('Multiple datasets', 'Single dataset'))
            if option == 'Multiple datasets':
                data = {} #Dictionary with the dataframes
                for file_type in ["user", "item", "context", "rating"]:
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
            elif option == 'Single dataset':
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
                            @st.cache
                            def create_dataframe(label, df, new_df_name):
                                columns = st.multiselect(label=label, options=df.columns) #Column name selection
                                if not columns:
                                    st.error('Please select at least one column')
                                else:
                                    # Create a new dataframe with the selected columns
                                    new_df = df[columns]
                                    st.dataframe(new_df.head())
                                    return new_df
                            data = {'user': create_dataframe('Select the columns for the user dataframe:', df, 'user_df'),
                                    'item': create_dataframe('Select the columns for the item dataframe:', df, 'item_df'),
                                    'context': create_dataframe('Select the columns for the context dataframe:', df, 'context_df'),
                                    'rating': create_dataframe('Select the columns for the rating dataframe:', df, 'rating_df')}
                        except Exception as e:
                            st.error(f"An error occurred while reading the file: {str(e)}")
        with tab2:
            if 'user' in data:
                replace_count_missing_values(data['user'],replace_values={"NULL":np.nan,-1:np.nan})
                list_attributes_and_ranges(data['user'])
            else:
                st.error("User dataset not found.")
        with tab3:
            if 'item' in data:
                replace_count_missing_values(data['item'],replace_values={"NULL":np.nan,-1:np.nan})
                list_attributes_and_ranges(data['item'])
            else:
                st.error("Item dataset not found.")
        with tab4:
            if 'context' in data:
                replace_count_missing_values(data['context'],replace_values={"NULL":np.nan,-1:np.nan})
                list_attributes_and_ranges(data['context'])
            else:
                st.error("Context dataset not found.")
        with tab5:
            st.write("TODO")
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
