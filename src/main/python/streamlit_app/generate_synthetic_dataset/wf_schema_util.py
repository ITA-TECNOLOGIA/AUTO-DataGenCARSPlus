import io

import pandas as pd
import requests
import streamlit as st
from streamlit_app import config, help_information
from streamlit_app.preprocess_dataset.wf_util import save_file


def upload_schema_file(schema_file_name, tab_type):
    """
    Upload schema from file.
    :param schema_file_name: The name of the schema file.
    :return: The content of the schema file.
    """
    schema_file_value = ''
    with st.expander(f"Upload {schema_file_name}.conf"):
        if schema_file := st.file_uploader(label='Choose the file:', key=f"upload_{schema_file_name}_{tab_type}"):
            schema_file_value = schema_file.getvalue().decode("utf-8")
    return schema_file_value

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

def get_schema_file(schema_type):    
    """
    Generate a schema file: "user_schema.conf", "item_schema.conf" or "context_schema.conf".
    :param schema_type: The type of schema (user, item or context).
    :return: The content of the schema file.
    """
    # Help information:
    help_information.help_schema_file()
    
    with st.expander(f"Generate {schema_type}.conf"):
        # [global]   
        value = '[global]'+'\n'
        value += 'type='+schema_type+'\n'
        number_attribute = st.number_input(label='Number of attributes to generate:', value=1, key='number_attribute_'+schema_type) 
        if schema_type == 'user':
            value += 'number_attributes='+str(number_attribute+1)+'\n' # +1 to incorporate the user_profile attribute.
        else:
            value += 'number_attributes='+str(number_attribute)+'\n'
        value += '\n'        
        # [attribute]
        for position in range(1, number_attribute+1):
            st.markdown("""---""")
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
                    string_text_area = str_text_area.text_area(label='Introduce new values to the list (split by comma): rainy, cloudy, sunny', key='string_text_area_'+str(position)+schema_type)                                                            
                    # Buttons: export and import values
                    export_button_column, import_area_column = st.columns(2)
                    with export_button_column:
                        file_name = 'str_'+attribute_name+'_possible_value_list.csv'
                        if st.download_button(label='Export list', data=string_text_area, file_name=file_name, key='export_button_'+str(position)+schema_type):
                            if len(string_text_area) == 0:                                 
                                st.warning('The file to be exported must not be empty.')
                            else:
                                st.success('The file has been saved with the name: '+file_name)
                    with import_area_column:
                        if import_file := st.file_uploader(label='Import list', key='import_file'+str(position)+schema_type):
                            string_text_area = str_text_area.text_area(label='Introduce new values to the list (split by comma):', value=import_file.getvalue().decode("utf-8"), key='import_button_'+str(position)+schema_type)
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
        if schema_type == config.USER_SCHEMA_NAME:
            st.markdown("""---""")
            number_user_profile = st.number_input(label='Number of user profiles to generate:', value=4, key='number_user_profile_'+schema_type) 
            position = number_attribute + 1
            value += '[attribute'+str(position)+']'+'\n'
            value += 'name_attribute_'+str(position)+'=user_profile_id'+'\n'        
            value += 'generator_type_attribute_'+str(position)+'='+'RandomAttributeGenerator'+'\n'
            value += 'type_attribute_'+str(position)+'='+'Integer'+'\n'   
            value += 'number_posible_values_attribute_'+str(position)+'='+str(2)+'\n'             
            value += 'minimum_value_attribute_'+str(position)+'='+str(1)+'\n'
            value += 'maximum_value_attribute_'+str(position)+'='+str(number_user_profile)+'\n'        
            value += 'important_weight_attribute_'+str(position)+'='+str(False)+'\n'
        value += '\n'
        return value
