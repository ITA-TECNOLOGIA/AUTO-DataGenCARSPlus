import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from datetime import date
import plotly.graph_objs as go
import datagencars.evaluation.rs_surprise.evaluation as evaluation
import base64
import io
import requests
import config
from datagencars.existing_dataset.generate_user_profile.generate_user_profile_dataset import GenerateUserProfileDataset
from datagencars.existing_dataset.replace_null_values import ReplaceNullValues
from datagencars.existing_dataset.replicate_dataset.replicate_dataset import ReplicateDataset
import console
from streamlit_app import workflow_image

####### Generate a synthetic dataset ######
def generate_schema_file(schema_type):
    """
    Generates schema files from streamlit.
    :param schema_type: The schema type (user_schema.conf, item_schema.conf, context_schema.conf or generation_config.conf).
    :return: A text area with the generated schema.
    """
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
            generator_type = st.selectbox(label='Generator type:', options=['Integer/Float/String/Boolean (following a distribution)', 'Fixed', 'URL', 'Address', 'Date', 'BooleanList', 'RandomAttributeGenerator', 'DeviceGenerator', 'ObjectPositionAttributeGenerator', 'FixedAttributeGenerator'],  key=schema_type+'_generator_type_'+str(position))            
            # type_attribute:
            attribute_type = None
            if generator_type=='RandomAttributeGenerator' or generator_type=='DeviceGenerator' or generator_type=='ObjectPositionAttributeGenerator' or generator_type=='FixedAttributeGenerator':
                attribute_type = st.selectbox(label='Attribute type:', options=['String', 'List', 'AttributeComposite'], key=schema_type+'_attribute_type_'+str(position)) 
                if attribute_type == 'String' and generator_type == 'RandomAttributeGenerator':
                    value += 'generator_type_attribute_'+str(position)+'='+generator_type+'\n'
                    str_text_area = st.empty()                        
                    string_text_area = str_text_area.text_area(label='Introduce new values to the list (split by comma): Poster, Sphere, Screen, NPC, Button', key='string_text_area_'+str(position))                                                            
                    str_possible_value_list = string_text_area.split(',')
                    number_possible_value = len(str_possible_value_list)
                    value += 'number_posible_values_attribute_'+str(position)+'='+str(number_possible_value)+'\n'
                    for i in range(number_possible_value):
                        value += 'posible_value_'+str(i+1)+'_attribute_'+str(position)+'='+str(str_possible_value_list[i]).strip()+'\n'
                elif (attribute_type == 'List' and generator_type == 'DeviceGenerator') or attribute_type == 'List' and generator_type == 'FixedAttributeGenerator':
                    value += 'generator_type_attribute_'+str(position)+'='+generator_type+'\n'
                    number_maximum_subattribute = st.number_input(label='Number of subattributes to generate:', value=5, key='number_maximum_subattribute_'+schema_type+'_'+str(position))
                    value += 'number_maximum_subattribute_attribute_'+str(position)+'='+str(number_maximum_subattribute)+'\n'
                    for subattribute in range(1, number_maximum_subattribute+1):
                        subattribute_name = st.text_input(label="Subattribute's name:", key=schema_type+'_subattribute_name_'+str(position)+'_'+str(subattribute)) 
                        value += 'name_subattribute_'+str(subattribute)+'_attribute_'+str(position)+'='+subattribute_name+'\n'
                        subattribute_type = st.selectbox(label='Subattribute type:', options=['String'], key=schema_type+'_subattribute_type_'+str(position)+'_'+str(subattribute)) 
                        value += 'type_subattribute_'+str(subattribute)+'_attribute_'+str(position)+'='+subattribute_type+'\n'
                        subattribute_input = st.text_area(label="Subattribute's input parameter:", key=schema_type+'_subattribute_input_'+str(position)+'_'+str(subattribute)) 
                        value += 'input_parameter_subattribute_'+str(subattribute)+'_attribute_'+str(position)+'='+subattribute_input+'\n'
                elif attribute_type == 'AttributeComposite' and generator_type == 'ObjectPositionAttributeGenerator':
                    value += 'generator_type_attribute_'+str(position)+'='+generator_type+'\n'
                    number_maximum_subattribute = st.number_input(label='Number of subattributes to generate:', value=3, key='number_maximum_subattribute_'+schema_type+'_'+str(position))
                    value += 'number_maximum_subattribute_attribute_'+str(position)+'='+str(number_maximum_subattribute)+'\n'
                    for subattribute in range(1, number_maximum_subattribute+1):
                        subattribute_name = st.text_input(label="Subattribute's name:", key=schema_type+'_subattribute_name_'+str(position)+'_'+str(subattribute)) 
                        value += 'name_subattribute_'+str(subattribute)+'_attribute_'+str(position)+'='+subattribute_name+'\n'
                        subattribute_type = st.selectbox(label='Subattribute type:', options=['float'], key=schema_type+'_subattribute_type_'+str(position)+'_'+str(subattribute)) 
                        value += 'type_subattribute_'+str(subattribute)+'_attribute_'+str(position)+'='+subattribute_type+'\n'
                    input_parameter = st.text_area(label="Attribute's input parameter:", key=schema_type+'_input_parameter_'+str(position)) 
                    value += 'input_parameter_attribute_'+str(position)+'='+input_parameter+'\n'
                else:
                    st.write('This combination of generator type and attribute type is not supported in this script.')
            elif generator_type == 'Integer/Float/String/Boolean (following a distribution)':
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
                value += 'generator_type_attribute_'+str(position)+'=FixedAttributeGenerator'+'\n' 
                attribute_type = st.selectbox(label='Attribute type:', options=['Integer', 'String', 'Boolean'], key='attribute_type_'+str(position)+'_'+generator_type)
                fixed_input = st.text_input(label='Imput the fixed value:', key='fixed_input_'+str(position))
                value += 'input_parameter_attribute_'+str(position)+'='+str(fixed_input)+'\n'
            elif generator_type == 'Date':                    
                attribute_type = st.selectbox(label='Attribute type:', options=['Integer'], key='attribute_type_'+str(position)+'_'+generator_type)
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
                unique_value = st.checkbox(label='Unique value?:', value=True, key='unique_value_'+str(position)+'_'+generator_type)
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
                    input_parameter_text_area = ip_text_area.text_area(label='Introduce address values (line by line), keeping the header: <street,number,zp,latitude,longitude>', value='street,number,zp,latitude,longitude', key='address_ip_text_area_'+str(position))   
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
                    places_list = []
                    places_str = 'street,number,zp,latitude,longitude\n'
                    input_parameter_text_area = ip_text_area.text_area(label="Introduce place_name to search address ex. McDonald's, 50017, keeping header: place, postalcode", value='place, zipcode', key='address_ip_text_area_'+str(position))   
                    if import_file := st.file_uploader(label='Import place_name list, keeping header: place', key='import_file'+str(position)):                            
                        input_parameter_text_area = ip_text_area.text_area(label="Introduce place_name to search address ex. McDonald's, 50017, keeping header: place, postalcode", value=import_file.getvalue().decode("utf-8"), key='import_address_ip_text_area_'+str(position))                            
                    input_parameter_df=pd.read_csv(io.StringIO(input_parameter_text_area))     
                    input_parameter_list = input_parameter_df.astype(str).values.tolist()
                    # print(input_parameter_text_area)
                    for place in input_parameter_list:   
                        # print(place)
                        # Construct the API endpoint URL
                        if place[1] == '':
                            url = f"https://nominatim.openstreetmap.org/search?q={place[0]}&format=json&limit=1000"
                        else:
                            url = f"https://nominatim.openstreetmap.org/search?q={place[0]}, {place[1]}&format=json&limit=1000"

                        # Send a GET request to the API endpoint
                        response = requests.get(url).json()
                        # print(response)

                        # If more than one result, return the first one
                        location = response[0]

                        # Extract the latitude and longitude coordinates from the first result
                        lat = location['lat']
                        lon = location['lon']

                        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
                        response = requests.get(url)
                        # Extract the JSON response as a dictionary
                        location2 = response.json()
                        #print(location2)
                        if location2 == None:
                            st.write(str(place[0]) +' not found.')
                        else:
                            item_info=[]
                            try:
                                #zp = location2['address']['postcode']
                                #print(location)
                                name = str(location2['display_name'].split(',')[0])
                                if name.lower() == place[0].lower():
                                    # print('IF')
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
                                    # print(places_list)
                                    places_str = places_str + item_info[0] + ', ' + item_info[1] + ', ' + item_info[2] + ', ' + str(item_info[3]) + ', ' + str(item_info[4]) + '\n'
                                    # print(places_str)
                            except Exception as ex:
                                print(ex)
                                pass
                    
                    ip_text_area_2 = st.empty()
                    input_parameter_text_area_2 = ip_text_area_2.text_area(label='Address values generated', value=places_str, key='address_ip_text_area_2_'+str(position))   
                    value += 'input_parameter_attribute_'+str(position)+'='+str(places_list)+'\n'            
                    input_parameter_text_area = places_str
                # Buttons: export and import values  
                file_name = attribute_name+'_input_parameter_list.csv'
                if input_parameter_text_area != None:
                    link_address_values = f'<a href="data:file/csv;base64,{base64.b64encode(input_parameter_text_area.encode()).decode()}" download={file_name}> Download </a>'
                    if st.markdown(link_address_values, unsafe_allow_html=True):
                    #if st.download_button(label='Export list', data=input_parameter_text_area, file_name=file_name, key='address_ip_export_button_'+str(position)):
                        if len(input_parameter_text_area) == 0:                                 
                            st.warning('The file to be exported must not be empty.')
                        else:
                            st.success('The file has been saved with the name: '+file_name)
            value += 'type_attribute_'+str(position)+'='+str(attribute_type)+'\n'
            # Important attributes:                
            is_important_attribute = st.checkbox(label=f'Is {attribute_name} an important attribute to include in the user profile?', value=False, key=schema_type+'_is_important_attribute_'+str(position)) 
            value += 'important_weight_attribute_'+str(position)+'='+str(is_important_attribute)+'\n'
            if is_important_attribute:
                # Ranking order:
                st.write('Examples of importance order:')
                st.markdown("""- ascending: ``` quality food=[bad, normal, good], global_rating=[1, 5] ``` """)
                st.markdown("""- descending: ``` quality food=[good, normal, bad], global_rating=[5, 1] ``` """)
                st.markdown("""- neutral (no important order): ``` quality food=[chinese, italian, vegetarian, international] ``` """)
                ranking_order_original = st.selectbox(label='Select an order of importance?', options=['ascending', 'descending', 'neutral'], key="important_order_"+str(position))
                ranking_order = 'neut'
                if ranking_order_original == 'ascending':
                    ranking_order = 'asc'
                elif ranking_order_original == 'descending':
                    ranking_order = 'desc'
                value += 'ranking_order_by_attribute_'+str(position)+'='+ranking_order+'\n'
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

def generation_settings(tab_generation):
    # GENERATION SETTING TAB:
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
            user_count = st.number_input(label='Number of users to generate:', value=250)
            item_count = st.number_input(label='Number of items to generate:', value=100)
            context_count = st.number_input(label='Number of contexts to generate:', value=10)

            dimension_value += ('number_user=' + str(user_count) + '\n' +
                                'number_item=' + str(item_count) + '\n' +
                                'number_context=' + str(context_count) + '\n')
            st.markdown("""---""")

            # [behavior]
            st.write('Behavior configuration')
            behavior_value = '[behavior] \n'
            number_behavior = st.number_input(label='Number of behaviors:', value=1000)
            session_time = st.number_input(label='Session time (seconds):', value=3600)
            min_interval_behavior = st.number_input(label='Minimum interval between behaviors (seconds):', value=1)
            max_interval_behavior = st.number_input(label='Maximum interval between behaviors (seconds):', value=300)
            min_radius = st.number_input(label='Minimum radius:', value=1)
            max_radius = st.number_input(label='Maximum radius:', value=5)
            door = st.text_input(label='Door: (format exaple: x, y, z)', value='0, 5, 5')
            interaction_threshold = st.number_input(label='Interaction threshold:', value=2.5)

            behavior_value += ('number_behavior=' + str(number_behavior) + '\n' +
                            'session_time=' + str(session_time) + '\n' +
                            'minimum_interval_behavior=' + str(min_interval_behavior) + '\n' +
                            'maximum_interval_behavior=' + str(max_interval_behavior) + '\n' +
                            'minimum_radius=' + str(min_radius) + '\n' +
                            'maximum_radius=' + str(max_radius) + '\n' +
                            'door=[' + door + ']\n' +
                            'interaction_threshold=' + str(interaction_threshold) + '\n')
            st.markdown("""---""")

            # [rating]
            st.write('Rating configuration')
            rating_value = '[rating] \n'
            rating_min = st.number_input(label='Minimum value of the ratings:', value=0)
            rating_max = st.number_input(label='Maximum value of the ratings:', value=1)
            min_year_ts = st.date_input(label='From:', value=date(2023, 1, 1))
            max_year_ts = st.date_input(label='Until:', value=date(2023, 4, 1))
            rating_value += ('minimum_value_rating=' + str(rating_min) + '\n' +
                            'maximum_value_rating=' + str(rating_max) + '\n' +
                            'minimum_date_timestamp=' + str(min_year_ts) + '\n' +
                            'maximum_date_timestamp=' + str(max_year_ts) + '\n')
            # Rules
            st.write('Rules configuration')
            num_rules = st.number_input(label="Number of rules (format example: {'action': 'Click', 'rating': 1}):", min_value=0, value=0)
            rules = []
            for i in range(num_rules):
                rule = st.text_input(label=f"Rule {i + 1}:", value="")
                rules.append(rule)
            for i, rule in enumerate(rules):
                rating_value += f'rule_{i + 1}=' + rule + '\n'
            st.markdown("""---""")

            # [item profile]
            st.write('Item profile configuration')
            item_profile_value = '[item profile] \n'
            probability_percentage_profile_1 = st.number_input(label='Profile probability percentage 1:', value=10)
            probability_percentage_profile_2 = st.number_input(label='Profile probability percentage 2:', value=30)
            probability_percentage_profile_3 = st.number_input(label='Profile probability percentage 3:', value=60)
            noise_percentage_profile_1 = st.number_input(label='Profile noise percentage 1:', value=20)
            noise_percentage_profile_2 = st.number_input(label='Profile noise percentage2:', value=20)
            noise_percentage_profile_3 = st.number_input(label='Profile noise percentage 3:', value=20)

            item_profile_value += ('probability_percentage_profile_1=' + str(probability_percentage_profile_1) + '\n' +
            'probability_percentage_profile_2=' + str(probability_percentage_profile_2) + '\n' +
            'probability_percentage_profile_3=' + str(probability_percentage_profile_3) + '\n' +
            'noise_percentage_profile_1=' + str(noise_percentage_profile_1) + '\n' +
            'noise_percentage_profile_2=' + str(noise_percentage_profile_2) + '\n' +
            'noise_percentage_profile_3=' + str(noise_percentage_profile_3) + '\n')
            st.markdown("""---""")

            # Generate the configuration file
            generation_config_value = dimension_value + '\n' + behavior_value + '\n' + rating_value + '\n' + item_profile_value
        # Edit file:
        with st.expander(f"Show generation_config.conf"):
            if edit_config_file := st.checkbox(label='Edit file?', key='edit_config_file'):
                config_file_text_area = st.text_area(label='Current file:', value=generation_config_value, height=500)
            else:               
                config_file_text_area = st.text_area(label='Current file:', value=generation_config_value, height=500, disabled=True)    
        link_generation_config = f'<a href="data:text/plain;base64,{base64.b64encode(config_file_text_area.encode()).decode()}" download="generation_config.conf">Download</a>'
        st.markdown(link_generation_config, unsafe_allow_html=True)

        return generation_config_value

def upload_user_profile_file():
    user_profile_df = pd.DataFrame()
    with st.expander(label='Upload user_profile.csv'):
        if user_profile_file := st.file_uploader(label='Choose the file:', key='user_profile_file'):
            user_profile_value = user_profile_file.getvalue().decode("utf-8")
            user_profile_df = pd.read_csv(io.StringIO(user_profile_value))  
            st.dataframe(user_profile_df)
    return user_profile_df

def generate_user_profile_manual(number_user_profile, attribute_column_list, item_possible_value_map, context_possible_value_map=None):
    """
    
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
    st.markdown(""" Please, note that the ```user_profile_id``` column must start at ```1```, while the rest of values must be in the range ```[-1,1]```.""")
    st.dataframe(user_profile_df)
    # Downloading user_profile.csv:
    if not inconsistent:
        link_user_profile = f'<a href="data:file/csv;base64,{base64.b64encode(export_df.to_csv(index=False).encode()).decode()}" download="user_profile.csv">Download</a>'
        st.markdown(link_user_profile, unsafe_allow_html=True)
    return user_profile_df

def generate_user_profile_automatic(rating_df, item_df, context_df=None):
    """
    """
    try:
        output = st.empty()
        with console.st_log(output.code):
            # Generate user profile, by using an original dataset:
            generate_up_dataset = None
            user_profile_df = pd.DataFrame()                    
            if context_df is not None and not context_df.empty:                     
                # With context:            
                if (not item_df.empty) and (not context_df.empty) and (not rating_df.empty):
                        if st.button(label='Generate', key='button_generate_up_cars'):
                            print('Automatically generating user profiles.')                    
                            generate_up_dataset = GenerateUserProfileDataset(rating_df, item_df, context_df)
                            user_profile_df = generate_up(generate_up_dataset)                                  
                            print('The user profile has been generated.')                                                    
                else:
                    st.warning("The item, context and rating files have not been uploaded.")
            else:
                # Without context:            
                if (not item_df.empty) and (not rating_df.empty): 
                    if st.button(label='Generate', key='button_generate_up_rs'):
                        print('Automatically generating user profiles.')                    
                        generate_up_dataset = GenerateUserProfileDataset(rating_df, item_df)
                        user_profile_df = generate_up(generate_up_dataset)                    
                        print('The user profile has been generated.')
                else:
                    st.warning("The item and rating files have not been uploaded.")
    except Exception:
        # Generate user profile, by using an original dataset:
        generate_up_dataset = None
        user_profile_df = pd.DataFrame()                    
        if context_df is not None and not context_df.empty:                     
            # With context:            
            if (not item_df.empty) and (not context_df.empty) and (not rating_df.empty):
                print('Automatically generating user profiles.')                    
                generate_up_dataset = GenerateUserProfileDataset(rating_df, item_df, context_df)
                user_profile_df = generate_up(generate_up_dataset)                                  
                print('The user profile has been generated.')                                                    
            else:
                print("The item, context and rating files have not been uploaded.")
        else:
            # Without context:            
            if (not item_df.empty) and (not rating_df.empty): 
                    print('Automatically generating user profiles.')                    
                    generate_up_dataset = GenerateUserProfileDataset(rating_df, item_df)
                    user_profile_df = generate_up(generate_up_dataset)                    
                    print('The user profile has been generated.')
            else:
                print("The item and rating files have not been uploaded.")
    return user_profile_df

####### Pre-process a dataset #######
# LOAD DATASET:
def load_dataset(file_type_list):
    """
    Loads dataset files (user.csv, item.csv, context.csv and rating.csv) in dataframes.
    :param file_type_list: List of file types.
    :return: Dataframes related to the uploaded dataset files.
    """
    user_df = pd.DataFrame()
    item_df = pd.DataFrame()
    context_df = pd.DataFrame()
    rating_df = pd.DataFrame()
    # Uploading a dataset:
    if 'user' in file_type_list:
        user_df = load_one_file(file_type='user')
    if 'item' in file_type_list:
        item_df = load_one_file(file_type='item')
    if 'context' in file_type_list:
        context_df = load_one_file(file_type='context')   
    if 'rating' in file_type_list:
        rating_df = load_one_file(file_type='rating')
    return user_df, item_df, context_df, rating_df

def load_one_file(file_type):
    """
    Load only one file (user.csv, item.csv, context.csv or rating.csv).
    :param file_type: The file type.
    :return: A dataframe with the information of uploaded file.
    """
    df = pd.DataFrame()    
    with st.expander(f"Upload your {file_type}.csv file"):
        separator = st.text_input(label=f"Enter the separator for your {file_type}.csv file (default is ';')", value=";", key='text_input_'+file_type)
        uploaded_file = st.file_uploader(label=f"Select {file_type}.csv file", type="csv")
        if uploaded_file is not None:
            if not separator:
                st.error('Please provide a separator.')
            else:
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
                try:                    
                    df = pd.read_csv(uploaded_file, sep=separator, names=column_names)                             
                    st.dataframe(df.head())
                except Exception as e:
                    st.error(f"An error occurred while reading the {file_type} file: {str(e)}")
                    df = None
    return df

# WORKFLOW:
# Replicate dataset:
def generate_up(generate_up):
    """
    Generates user profiles (automatically).
    :param generate_up: The constructor of the user profile generator.
    :return: A dataframe with user profiles.
    """
    user_profile_df = generate_up.generate_user_profile()    
    with st.expander(label=f'Show the generated user profile file.'):
        st.dataframe(user_profile_df)
        link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(user_profile_df.to_csv(index=False).encode()).decode()}" download="user_profile.csv">Download</a>'
        st.markdown(link_rating, unsafe_allow_html=True) 
    return user_profile_df

def replicate_task(with_context, rating_df, user_profile_df, new_item_df, new_context_df,percentage_rating_variation, output, st):
    with console.st_log(output.code):     
        if with_context:      
            print('Extracting statistics.')
            print('Replicating the rating.csv file.')                                
            replicate_cars = ReplicateDataset(rating_df, user_profile_df, new_item_df, new_context_df)
            new_rating_df = replicate_cars.replicate_dataset(percentage_rating_variation)           
            new_rating_df.to_csv("new_ratings.csv", index=False)        
            print('Replicated data generation has finished.')        
        else:            
            # Without context:                    
            st.write(new_item_df)                            
            st.write(rating_df)
            st.write(user_profile_df) 
            print('Extracting statistics.')
            print('Replicating the rating.csv file.')
            replicate_cars = ReplicateDataset(rating_df, user_profile_df, new_item_df)
            new_rating_df = replicate_cars.replicate_dataset(percentage_rating_variation)                        
            with st.expander(label='Show the replicated file: rating.csv'):
                st.dataframe(new_rating_df)
                link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(new_rating_df.to_csv(index=False).encode()).decode()}" download="rating.csv">Download</a>'
                st.markdown(link_rating, unsafe_allow_html=True)
            print('Replicated data generation has finished.')  

# Extend dataset:
# Recalculate ratings:
# Replace NULL values:
def tab_logic_replace_null(wf_name, with_context, item_df, context_df=None, other_opts = None):
    output = st.empty()  
    with console.st_log(output.code):
        null_values_c = True
        if with_context:
            null_values_c = st.checkbox("Do you want to replace the null values in context_file?", value=True)   
        null_values_i = st.checkbox("Do you want to replace the null values in item_file?", value=True)               
        if null_values_i or null_values_c:
            # Showing the current image of the WF:
            optional_value_list = [('NULLValues', str(null_values_c or null_values_i)), ('NULLValuesC', str(null_values_c)), ('NULLValuesI', str(null_values_i))]
            if other_opts != None:
                optional_value_list = optional_value_list + other_opts
            workflow_image.show_wf(wf_name=wf_name, init_step='False', with_context=with_context, optional_value_list=optional_value_list)
            new_item_df = pd.DataFrame()
            new_context_df = pd.DataFrame()                      
            # Replacing NULL values in item or context file.
            if with_context:
                if (not item_df.empty) and (not context_df.empty):                                        
                    if st.button(label='Replace', key='button_replace_item_context'):
                        if null_values_i:
                            # Check if item_df has NaN values:
                            print(f'Checking if item.csv has NaN values.')
                            if item_df.isnull().values.any():        
                                print(f'Replacing NaN values.')
                                replacenulls = ReplaceNullValues(item_df)
                                schema = infer_schema(item_df)
                                new_item_df = replacenulls.regenerate_item_file(schema) 
                                print('The null values have been replaced.')
                                with st.expander(label=f'Show replicated file: item.csv'):
                                    st.dataframe(new_item_df)
                                    link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(new_item_df.to_csv(index=False).encode()).decode()}" download="item.csv">Download</a>'
                                    st.markdown(link_rating, unsafe_allow_html=True)
                            else:
                                st.write('new_item_df = item_df.copy()')
                                new_item_df = item_df.copy()
                                st.warning(f'The item.csv file has no null values.')
                        if null_values_c:
                            # Check if context_df has NaN values:
                            print(f'Checking if context.csv has NaN values')
                            if context_df.isnull().values.any():
                                replacenulls = ReplaceNullValues(context_df)
                                schema = infer_schema(context_df)
                                new_context_df = replacenulls.regenerate_item_file(schema) 
                                print('The null values have been replaced.')
                                with st.expander(label=f'Show replicated file: context.csv'):
                                    st.dataframe(new_context_df)
                                    link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(new_context_df.to_csv(index=False).encode()).decode()}" download="context.csv">Download</a>'
                                    st.markdown(link_rating, unsafe_allow_html=True)
                            else:
                                st.write('new_context_df = context_df.copy()')
                                new_context_df = context_df.copy()                                        
                                st.warning(f'The context.csv file has no null values.')                                        
                else:
                    st.warning("The item and context files have not been uploaded.")
            else:
                if not item_df.empty:                                        
                    if st.button(label='Replace', key='button_replace_item'):
                        # Check if item_df has NaN values:
                        print(f'Checking if item.csv has NaN values')
                        if item_df.isnull().values.any():
                            print(f'Replacing NaN values.')
                            new_item_df = pd.DataFrame() # TODO
                            print('The null values have been replaced.')
                            with st.expander(label=f'Show replicated file: item.csv'):
                                st.dataframe(new_item_df)
                                link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(new_item_df.to_csv(index=False).encode()).decode()}" download="item.csv">Download</a>'
                                st.markdown(link_rating, unsafe_allow_html=True)
                        else:
                            new_item_df = item_df.copy()
                            st.warning(f'The item.csv file has no null values.')                                
                else:
                    st.warning("The item file has not been uploaded.")
        else:   
            optional_value_list = [('NULLValues', str(null_values_c or null_values_i)), ('NULLValuesC', str(null_values_c)), ('NULLValuesI', str(null_values_i))]
            if other_opts != None:
                optional_value_list = optional_value_list + other_opts                 
            workflow_image.show_wf(wf_name=wf_name, init_step='False', with_context=with_context, optional_value_list=optional_value_list)          
            new_item_df = item_df.copy()
            new_context_df = context_df.copy()
    
    return null_values_c, null_values_i, new_item_df, new_context_df

def tab_logic_generate_up(wf_name, with_context, optional_value_list, rating_df, new_item_df, new_context_df=None):
    # Showing the current image of the WF:
    workflow_image.show_wf(wf_name=wf_name, init_step='False', with_context=with_context, optional_value_list=optional_value_list)
    if with_context:                             
        user_profile_df = generate_user_profile_automatic(rating_df=rating_df, item_df=new_item_df, context_df=new_context_df)                
    else:
        user_profile_df = generate_user_profile_automatic(rating_df=rating_df, item_df=new_item_df)   
    
    return user_profile_df

def infer_schema(df):
    """
    :param df: original dataset
    :return: A dataframe with schema information
    """
    possible_types = {int:'Integer', float:'Float', bool:'Boolean', list:'List', str:'String'}
    def infer(items):
        try:
            item_type = possible_types[type(items[0])]
            if item_type == 'String' and len(items[0].replace('[','').replace(']','').split(',')) > 0:
                item = items[0].replace('[','').replace(']','').replace('\'','').replace(' ', '').split(',')
                try:
                    float(item[-1])
                    return 'AttributeComposite'
                except:
                    if 'www.' in items[0]:
                        return 'AttributeComposite'
                    else:
                        return 'List'
            else:
                return item_type
        except Exception as ex:
            print(ex)
            return 'Unknown'
        
    schema = pd.DataFrame()

    attributes = df.columns[1:]
    schema['Attribute'] = attributes
    types = list()
    generator = list()
    min_vals = list()
    max_vals = list()
    fix_vals = list()
    item_vals = list()
    values_list_vals = list()
    for attribute in attributes:
        items = list(set(df[attribute].drop_duplicates().dropna()))
        # Infer types
        item_type = infer(items)
        min_val = 0
        max_val = 0
        fix_val = ''
        values_list2=list()
        # Infer rest of info
        if item_type == 'Integer' or item_type == 'Float':
            if len(items) >= 2:
                item_generator = 'Integer/Float/String/Boolean (following a distribution)'
                min_val = min(items)
                max_val = max(items)
            else:
                item_generator = 'Fixed'
                min_val = items[0]
                max_val = items[0]
        if item_type == 'String':
            if len(items) >= 2:
                item_generator = 'Integer/Float/String/Boolean (following a distribution)'
            else:
                item_generator = 'Fixed'
                fix_val = items[0]
        if item_type == 'Boolean':
            item_generator = 'Integer/Float/String/Boolean (following a distribution)'
        if item_type == 'List':
            values_list=''
            for elem in items:
                values_list += ',' + elem.replace('[', '').replace(']','').replace(' ','').replace('\'','')
            values_list2 = list(set(values_list[1:].split(',')))
            item_generator = 'BooleanList'
        if item_type == 'AttributeComposite':
            if 'www.' in items[0]:
                item_generator = 'URL'
            else:
                item_generator = 'Address'

        types.append(item_type)
        generator.append(item_generator)
        min_vals.append(min_val)
        max_vals.append(max_val)
        fix_vals.append(fix_val)
        item_vals.append(items)
        values_list_vals.append(values_list2)

    schema['TypeAttribute'] = types
    schema['GeneratorType'] = generator
    schema['Min_val'] = min_vals
    schema['Max_val'] = max_vals
    schema['Fix_val'] = fix_vals
    schema['Item_vals'] = item_vals
    schema['Values_list_vals'] = values_list_vals

    schema_str = '[global] \ntype=context \nnumber_attributes=' + str(len(schema)) +'\n'
    for index, row in schema.iterrows():
        schema_str = schema_str + '[attribute' + str(int(index+1)) + ']\n'
        attribute = row['Attribute']
        schema_str = schema_str + 'name_attribute_' + str(int(index+1)) + '=' + attribute + '\n'
        st.write(f'[{attribute}]')
        atrib_generator = st.selectbox(label='Generator type:', options=config.GENERATOR_OPTS, key = attribute+'generator', index=config.GENERATOR_OPTS.index(row['GeneratorType']))
        atrib_type = st.selectbox(label='Attribute type:', options=config.ATR_OPTS, key=attribute+'_attribute_type_', index=config.ATR_OPTS.index(row['TypeAttribute']))
        schema_str = schema_str + 'type_attribute_' + str(int(index+1)) + '=' + atrib_type + '\n'
        if atrib_type == 'Integer' or atrib_type == 'Float':
            if atrib_generator == 'Fixed':
                schema_str = schema_str + 'generator_type_attribute_' + str((index+1)) + '=FixedAttributeGenerator\n'
                fixed_val = st.number_input(label='Fixed value of the attribute', value=row['Min_val'], key=attribute+'_fixed_val')
                schema_str = schema_str + 'input_parameter_attribute_' + str((index+1)) + '=' + str(fixed_val) + '\n'
            else:
                schema_str = schema_str + 'generator_type_attribute_' + str((index+1)) + '=RandomAttributeGenerator\n'
                integer_min = st.number_input(label='Minimum value of the attribute', value=row['Min_val'], key=attribute+'_integer_min')
                integer_max = st.number_input(label='Maximum value of the attribute', value=row['Max_val'], key=attribute+'_integer_max')
                schema_str = schema_str + 'minimum_value_attribute_' + str((index+1)) + '=' + str((integer_min)) + '\n'
                schema_str = schema_str + 'maximum_value_attribute_' + str((index+1)) + '=' + str((integer_max)) + '\n'
        if atrib_type == 'String':
            if atrib_generator == 'Fixed':
                schema_str = schema_str + 'generator_type_attribute_' + str((index+1)) + '=FixedAttributeGenerator\n'
                schema_str = schema_str + 'input_parameter_attribute_' + str(index+1) + '=' + row['Fix_val'] + '\n'
                fixed_val = st.text_input(label='Fixed value of the attribute', value=row['Fix_val'], key=attribute+'_fixed_val')
            else:
                schema_str = schema_str + 'generator_type_attribute_' + str((index+1)) + '=RandomAttributeGenerator\n'
                schema_str = schema_str + 'number_posible_values_attribute_'+ str((index+1)) + '=' + str(len(row['Item_vals'])) + '\n'
                for index2, elem in enumerate(row['Item_vals']):
                    schema_str = schema_str + 'posible_value_' + str(index2+1) + '_attribute_' + str(index+1) + '=' + elem + '\n'
                fixed_val = st.text_input(label="Introduce new values to the list (split by comma): ['rainy', 'cloudy', 'sunny']", value=row['Item_vals'], key=attribute+'_list_val')
        if atrib_type == 'Boolean':
            schema_str = schema_str + 'generator_type_attribute_' + str((index+1)) + '=RandomAttributeGenerator\n'
        if atrib_type == 'List':
            schema_str = schema_str + 'generator_type_attribute_' + str((index+1)) + '=BooleanListAttributeGenerator\n'
            schema_str = schema_str + 'type_component_attribute_' + str(int(index+1)) + '=Boolean\n'
            schema_str = schema_str + 'number_maximum_component_attribute_'+ str((index+1)) + '=' + str(len(row['Item_vals'])) + '\n'
            for index2, elem in enumerate(row['Values_list_vals']):
                schema_str = schema_str + 'component_' + str(index2+1) + '_attribute_' + str(index+1) + '=' + elem + '\n'
            fixed_val = st.text_input(label="Introduce new values to the list (split by comma): ['rainy', 'cloudy', 'sunny']", value=row['Values_list_vals'][:], key=attribute+'_list_val')
            input_parameter_val = st.number_input(label='Number of boolean values to generate for these components', value=1, key=attribute+'_input_param_val')
            schema_str = schema_str + 'input_parameter_attribute_' + str(int(index+1)) + '=' + str(input_parameter_val) + '\n'
        if atrib_type == 'AttributeComposite':
            if atrib_generator == 'Address':
                schema_str = schema_str + 'generator_type_attribute_' + str((index+1)) + '=AddressAttributeGenerator\n'
                schema_str = schema_str + 'number_maximum_subattribute_attribute_'+ str((index+1)) + '=5\n'
                schema_str = schema_str + 'name_subattribute_1_attribute_'+ str((index+1)) + '=street\n'
                schema_str = schema_str + 'name_subattribute_2_attribute_'+ str((index+1)) + '=number\n'
                schema_str = schema_str + 'name_subattribute_3_attribute_'+ str((index+1)) + '=zp\n'
                schema_str = schema_str + 'name_subattribute_4_attribute_'+ str((index+1)) + '=latitude\n'
                schema_str = schema_str + 'name_subattribute_5_attribute_'+ str((index+1)) + '=longitude\n'
                schema_str = schema_str + 'type_subattribute_1_attribute_'+ str((index+1)) + '=String\n'
                schema_str = schema_str + 'type_subattribute_2_attribute_'+ str((index+1)) + '=String\n'
                schema_str = schema_str + 'type_subattribute_3_attribute_'+ str((index+1)) + '=String\n'
                schema_str = schema_str + 'type_subattribute_4_attribute_'+ str((index+1)) + '=String\n'
                schema_str = schema_str + 'type_subattribute_5_attribute_'+ str((index+1)) + '=String\n'
                # Generate input parameter file: input_parameter_attribute_1=name_restaurant.csv
                address_complete_type = st.selectbox(label='Address complete type:', options=['Manually', 'Upload file', 'Search Address'], key='address_complete_type')
                ip_text_area = st.empty()
                if address_complete_type == 'Manually':
                    input_parameter_text_area = ip_text_area.text_area(label='Introduce address values (line by line), keeping the header: <street,number,zp,latitude,longitude>', value='street,number,zp,latitude,longitude', key='address_ip_text_area_'+str(index+1))   
                    input_parameter_df=pd.read_csv(io.StringIO(input_parameter_text_area), sep=",")                                                 
                    input_parameter_list = input_parameter_df.astype(str).values.tolist()
                    schema_str += 'input_parameter_attribute_'+str(index+1)+'='+str(input_parameter_list)+'\n'
                if address_complete_type == 'Upload file':
                    input_parameter_text_area = None
                    input_parameter_list = []
                    import_split = st.text_input(label='Specifies the type of separator to read the file (; , # tab)', key='import_split')
                    if import_file := st.file_uploader(label='Import list', key='import_file'+str(index+1)):                            
                        input_parameter_text_area = ip_text_area.text_area(label='Introduce address values below <street,number,zp,latitude,longitude> (line by line):', value=import_file.getvalue().decode("utf-8"), key='import_address_ip_text_area_'+str(index+1))                            
                        input_parameter_df=pd.read_csv(io.StringIO(input_parameter_text_area), sep=import_split)                                                 
                        input_parameter_list = input_parameter_df.astype(str).values.tolist()                        
                    schema_str += 'input_parameter_attribute_'+str(index+1)+'='+str(input_parameter_list)+'\n'
                if address_complete_type == 'Search Address':
                    places_list = []
                    places_str = 'street,number,zp,latitude,longitude\n'
                    input_parameter_text_area = ip_text_area.text_area(label="Introduce place_name to search address ex. McDonald's, 50017, keeping header: place, postalcode", value='place, zipcode', key='address_ip_text_area_'+str(index+1))   
                    if import_file := st.file_uploader(label='Import place_name list, keeping header: place', key='import_file'+str(index+1)):                            
                        input_parameter_text_area = ip_text_area.text_area(label="Introduce place_name to search address ex. McDonald's, 50017, keeping header: place, postalcode", value=import_file.getvalue().decode("utf-8"), key='import_address_ip_text_area_'+str(index+1))                            
                    input_parameter_df=pd.read_csv(io.StringIO(input_parameter_text_area))     
                    input_parameter_list = input_parameter_df.astype(str).values.tolist()
                    # print(input_parameter_text_area)
                    for place in input_parameter_list:   
                        # print(place)
                        # Construct the API endpoint URL
                        if place[1] == '':
                            url = f"https://nominatim.openstreetmap.org/search?q={place[0]}&format=json&limit=1000"
                        else:
                            url = f"https://nominatim.openstreetmap.org/search?q={place[0]}, {place[1]}&format=json&limit=1000"

                        # Send a GET request to the API endpoint
                        response = requests.get(url).json()
                        # print(response)

                        # If more than one result, return the first one
                        location = response[0]

                        # Extract the latitude and longitude coordinates from the first result
                        lat = location['lat']
                        lon = location['lon']

                        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
                        response = requests.get(url)
                        # Extract the JSON response as a dictionary
                        location2 = response.json()
                        #print(location2)
                        if location2 == None:
                            st.write(str(place[0]) +' not found.')
                        else:
                            item_info=[]
                            try:
                                #zp = location2['address']['postcode']
                                #print(location)
                                name = str(location2['display_name'].split(',')[0])
                                if name.lower() == place[0].lower():
                                    # print('IF')
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
                                    # print(places_list)
                                    places_str = places_str + item_info[0] + ', ' + item_info[1] + ', ' + item_info[2] + ', ' + str(item_info[3]) + ', ' + str(item_info[4]) + '\n'
                                    # print(places_str)
                            except Exception as ex:
                                print(ex)
                                pass
                    
                    ip_text_area_2 = st.empty()
                    input_parameter_text_area_2 = ip_text_area_2.text_area(label='Address values generated', value=places_str, key='address_ip_text_area_2_'+str(index+1))   
                    schema_str += 'input_parameter_attribute_'+str(index+1)+'='+str(places_list)+'\n'            
                    input_parameter_text_area = places_str
                # Buttons: export and import values  
                file_name = attribute+'_input_parameter_list.csv'
                if input_parameter_text_area != None:
                    link_address_values = f'<a href="data:file/csv;base64,{base64.b64encode(input_parameter_text_area.encode()).decode()}" download={file_name}> Download </a>'
                    if st.markdown(link_address_values, unsafe_allow_html=True):
                    #if st.download_button(label='Export list', data=input_parameter_text_area, file_name=file_name, key='address_ip_export_button_'+str(position)):
                        if len(input_parameter_text_area) == 0:                                 
                            st.warning('The file to be exported must not be empty.')
                        else:
                            st.success('The file has been saved with the name: '+file_name)
            elif atrib_generator == 'URL':
                schema_str = schema_str + 'generator_type_attribute_' + str((index+1)) + '=URLAttributeGenerator\n'
                schema_str = schema_str + 'number_maximum_subattribute_attribute_'+ str((index+1)) + '=2\n'
                schema_str = schema_str + 'name_subattribute_1_attribute_'+ str((index+1)) + '=name\n'
                schema_str = schema_str + 'name_subattribute_2_attribute_'+ str((index+1)) + '=url\n'
                schema_str = schema_str + 'type_subattribute_1_attribute_'+ str((index+1)) + '=String\n'
                schema_str = schema_str + 'type_subattribute_2_attribute_'+ str((index+1)) + '=String\n'
                # Generate input parameter file: input_parameter_attribute_1=name_restaurant.csv
                ip_text_area = st.empty()
                input_parameter_text_area = ip_text_area.text_area(label='Introduce values (a value by line), keeping the header: <place>', value='place', key='url_ip_text_area_'+str(index+1))   
                # Buttons: export and import values  
                export_button_column, import_area_column = st.columns(2)
                with export_button_column:
                    file_name = attribute +'_input_parameter_list.csv'
                    if st.download_button(label='Export list', data=input_parameter_text_area, file_name=file_name, key='ip_export_button_'+str(index+1)):
                        if len(input_parameter_text_area) == 0:                                 
                            st.warning('The file to be exported must not be empty.')
                        else:
                            st.success('The file has been saved with the name: '+file_name)
                with import_area_column:
                    input_parameter_list = []
                    if import_file := st.file_uploader(label='Import list', key='import_file'+str(index+1)):                                
                        input_parameter_text_area = ip_text_area.text_area(label='Introduce values (a value by line), keeping the header: <place>', value=import_file.getvalue().decode("utf-8"), key='import_url_ip_text_area_'+str(index+1))                    
                input_parameter_df=pd.read_csv(io.StringIO(input_parameter_text_area))
                input_parameter_list = input_parameter_df['place'].astype(str).values.tolist()
                schema_str += 'input_parameter_attribute_'+str(index+1)+'='+str(input_parameter_list)+'\n'
                unique_value = st.checkbox(label='Unique value?:', value=True, key='unique_value_'+str(index+1)+'_'+attribute)
                if unique_value:
                    schema_str += 'unique_value_attribute_'+str(index+1)+'=True'+'\n'
                else:
                    schema_str += 'unique_value_attribute_'+str(index+1)+'=False'+'\n'
      
        st.markdown("""---""")
        schema_str = schema_str + '\n'
    return schema_str

# Generate user profile:
# Ratings to binary:
def ratings_to_binary(df, threshold=3):
    """
    Transforms ratings based on value ranges (e.g., [1-5]) to binary values (e.g., [0-1]), by applying a threshold.
    :param threshold: The rating threshold.
    :return: A dataframe with binary ratings.
    """
    def binary_rating(rating):
        return 1 if rating >= threshold else 0
    df['rating'] = df['rating'].apply(binary_rating)
    return df
# Mapping categorization:

####### Analysis a dataset #######
# VISUALIZATION:
def plot_column_attributes_count(data, column, sort):
    """
    Plot the number of values by attribute.
    :param data: TODO
    :param column: TODO
    :param sort: TODO
    """
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
    """
    Prints in streamlit statistics by attribute.
    :param statistics: The statistics.    
    """
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

def correlation_matrix(df, label):
    """
    Determines the correlation matrix.
    :param label: TODO
    :param df: TODO
    :return: A correlation matrix.
    """
    corr_matrix = pd.DataFrame()
    columns_id = df.filter(regex='_id$').columns.tolist()
    columns_not_id = [col for col in df.columns if col not in columns_id]
    data_types = []
    for col in columns_not_id:     
        data_types.append({"Attribute": col, "Data Type": str(df[col].dtype)})
        break    
    selected_columns = st.multiselect("Select columns to analyze", columns_not_id, key='cm_'+label)
    method = st.selectbox("Select a method", ['pearson', 'kendall', 'spearman'], key='method_'+label)
    if st.button("Generate correlation matrix", key='button_'+label) and selected_columns:
        with st.spinner("Generating correlation matrix..."):
            merged_df_selected = df[selected_columns].copy()
            # Categorize non-numeric columns using label encoding:
            for col in merged_df_selected.select_dtypes(exclude=[np.number]):
                merged_df_selected[col], _ = merged_df_selected[col].factorize()            
            corr_matrix = merged_df_selected.corr(method=method)     
    return corr_matrix       

# EVALUATION:
def select_params(algorithm):
    """
    Select parameters of the specified recommendation algorithm.
    :param algorithm: A recommendation algorithm.
    :return: A dictionary with parameter values.
    """
    if algorithm == "SVD":
        st.sidebar.markdown(f'**{algorithm} parameter settings:**')          
        return {"n_factors": st.sidebar.number_input("Number of factors", min_value=1, max_value=1000, value=100, key='n_factors_svd'),
                "n_epochs": st.sidebar.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_svd'),
                "lr_all": st.sidebar.number_input("Learning rate for all parameters", min_value=0.0001, max_value=1.00, value=0.005, step=0.0001, key='lr_all_svd'),
                "reg_all": st.sidebar.number_input("Regularization term for all parameters", min_value=0.0001, max_value=1.00, value=0.02, key='reg_all_svd')}
    if algorithm == "BaselineOnly":
        st.sidebar.markdown(f'**{algorithm} parameter settings:**')          
        return {"bsl_options": {"method": st.sidebar.selectbox("Baseline method", ["als", "sgd"], key='method_baselineonly'),
                                "reg_i": st.sidebar.number_input("Regularization term for item parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_i_baselineonly'),
                                "reg_u": st.sidebar.number_input("Regularization term for user parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_u_baselineonly')}}
    if algorithm == "CoClustering":
        st.sidebar.markdown(f'**{algorithm} parameter settings:**')          
        return {"n_cltr_u": st.sidebar.number_input("Number of clusters for users", min_value=1, max_value=1000, value=5),
                "n_cltr_i": st.sidebar.number_input("Number of clusters for items", min_value=1, max_value=1000, value=5)}
    if algorithm == "NMF":
        st.sidebar.markdown(f'**{algorithm} parameter settings:**')          
        return {"n_factors": st.sidebar.number_input("Number of factors", min_value=1, max_value=1000, value=100, key='n_factors_nmf'),
                "n_epochs": st.sidebar.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_nmf'),
                "reg_pu": st.sidebar.number_input("Regularization term for user factors", min_value=0.0001, max_value=1.0, value=0.02),
                "reg_qi": st.sidebar.number_input("Regularization term for item factors", min_value=0.0001, max_value=1.0, value=0.02)}
    if algorithm == "NormalPredictor":
        return {}
    if algorithm == "SlopeOne":
        return {}
    if algorithm == "SVDpp":
        st.sidebar.markdown(f'**{algorithm} parameter settings:**')          
        return {"n_factors": st.sidebar.number_input("Number of factors", min_value=1, max_value=1000, value=100, key='n_factors_svdpp'),
                "n_epochs": st.sidebar.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_svdpp'),
                "lr_all": st.sidebar.number_input("Learning rate for all parameters", min_value=0.0001, max_value=1.0, value=0.005, key='lr_all_svdpp'),
                "reg_all": st.sidebar.number_input("Regularization term for all parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_all_svdpp')}
    if algorithm == "KNNBasic":
        return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnbasic'),
                "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["pearson", "msd", "cosine"], key='sim_options_knnbasic'),
                                "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnbasic')}}
    if algorithm == "KNNWithMeans":
        return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnwithmeans'),
                "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["pearson", "msd", "cosine"], key='sim_options_knnwithmeans'),
                                "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnwithmeans')}}
    if algorithm == "KNNWithZScore":
        return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnwithzscore'),
                "min_k": st.sidebar.number_input("Minimum number of nearest neighbors", min_value=1, max_value=1000, value=1, key='min_k_knnwithzscore'),
                "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["pearson", "msd", "cosine"], key='sim_options_knnwithzscore'),
                                "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnwithzscore')}}
    if algorithm == "KNNBaseline":
        return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnbaseline'),
                "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["pearson", "msd", "cosine"], key='sim_options_knnbaseline'),
                                "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnbaseline')},
                "bsl_options": {"method": st.sidebar.selectbox("Baseline method", ["als", "sgd"], key='method_knnbaseline'),
                                "reg_i": st.sidebar.number_input("Regularization term for item parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_i_knnbaseline'),
                                "reg_u": st.sidebar.number_input("Regularization term for user parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_u_knnbaseline')}}

def select_params_contextual(algorithm):
    """
    Select parameters of the specified context-aware recommendation algorithm.
    :param algorithm: A context-aware recommendation algorithm.
    :return: A dictionary with parameter values.
    """
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
    """
    Select parameters related to the specified split strategy (RS).
    :param strategy: The split strategy.
    :return: A dictionary with parameter values. 
    """
    if strategy == "KFold":
        st.sidebar.markdown("""A basic cross-validation iterator. Each fold is used once as a testset while the k - 1 remaining folds are used for training.""")
        return {"n_splits": st.sidebar.number_input("Number of folds", min_value=2, max_value=10, value=5),
                "shuffle": st.sidebar.checkbox("Shuffle?")}
    elif strategy == "RepeatedKFold":
        st.sidebar.markdown("""Repeats KFold n times with different randomization in each repetition.""")
        return {"n_splits": st.sidebar.number_input("Number of folds", min_value=2, max_value=10, value=5),
                "n_repeats": st.sidebar.number_input("Number of repeats", min_value=1, max_value=10, value=1)}
    elif strategy == "ShuffleSplit":
        st.sidebar.markdown("""A basic cross-validation iterator with random trainsets and testsets. Contrary to other cross-validation strategies, random splits do not guarantee that all folds will be different, although this is still very likely for sizeable datasets.""")
        return {"n_splits": st.sidebar.number_input("Number of folds", min_value=2, max_value=10, value=5),
                "test_size": st.sidebar.number_input("Test size", min_value=0.1, max_value=0.9, step=0.1, value=0.2),
                "shuffle": st.sidebar.checkbox("Shuffle?")}
    elif strategy == "LeaveOneOut":
        st.sidebar.markdown("""Cross-validation iterator where each user has exactly one rating in the testset. Contrary to other cross-validation strategies, LeaveOneOut does not guarantee that all folds will be different, although this is still very likely for sizeable datasets.""")
        return {"n_splits": st.sidebar.number_input("Number of folds", min_value=2, max_value=10, value=5),
                "min_n_ratings": st.sidebar.number_input("Minimum number of ratings for each user (trainset)", min_value=0, max_value=10000, value=0)}
    
def select_split_strategy_contextual(strategy):
    """
    Select parameters related to the specified split strategy (CARS).
    :param strategy: The split strategy.
    :return: A dictionary with parameter values. 
    """
    if strategy == "ShuffleSplit":
        n_splits = st.sidebar.number_input("Number of splits", 2, 100, 10)
        train_size = st.sidebar.slider("Train set size (0.0 to 1.0)", 0.01, 1.0, 0.2, step=0.01)        
        return {"n_splits": n_splits, "train_size": train_size}
    elif strategy == "KFold":
        n_splits = st.sidebar.number_input("Number of folds", 2, 100, 5)             
        return {"n_splits": n_splits, "shuffle": st.sidebar.checkbox("Shuffle?")}
    elif strategy == "LeaveOneOut":
        st.sidebar.markdown("""Cross-validation iterator where each user has exactly one rating in the testset. Contrary to other cross-validation strategies, LeaveOneOut does not guarantee that all folds will be different, although this is still very likely for sizeable datasets.""")
        return {"n_splits": st.sidebar.number_input("Number of folds", min_value=2, max_value=10, value=5),
                "min_n_ratings": st.sidebar.number_input("Minimum number of ratings for each user (trainset)", min_value=0, max_value=10000, value=0)}

def evaluate_algo(algo_list, strategy_instance, metrics, data):
    """
    Evaluates recommendation algorithms.
    :param algo_list: Recommendation algorithms.
    :param strategy_instance: Split strategy.
    :param metrics: The evaluation metrics.
    :param data: Recommendation data.
    :return: A dataframe with evaluation results.
    """
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

def visualize_graph_mean_rs(df, increment_yaxis):
    """
    Visualize mean results of the evaluation of recommendation algorithms.   
    :param df: A dataframe with evaluation mean results.
    :param increment_yaxis: A float value to increase the maximum value of the Y-axis.    
    """
    # Create trace for each column:
    fig = go.Figure()
    for column in df.columns[1:]:
        fig.add_trace(go.Bar(x=df['Algorithm'], y=df[column], name=column))      
    # Create figure:
    selected_metric_list = df.columns[1:].tolist()
    fig.update_layout(title='Performance Comparison of Recommendation Algorithms',
                      xaxis_title='Recommendation Algorithm',
                      yaxis_title='Performance',
                      legend=dict(title="Metrics"),
                      barmode='group',
                      yaxis_range=[0, df[selected_metric_list].max().max()+increment_yaxis])
    # Show plot:                        
    st.plotly_chart(fig, use_container_width=True)

def visualize_graph_fold_rs(df, metric, increment_yaxis):
    """
    Visualize fold results by metric of the evaluation of recommendation algorithms.   
    :param df: A dataframe with evaluation results by fold.
    :param metric: The metric measure.
    :param increment_yaxis: A float value to increase the maximum value of the Y-axis.    
    """
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
        yaxis_title="Performance",
        legend=dict(title="Recommendation algorithms"),
        yaxis_range=[0, df[metric].max().max()+increment_yaxis]
    )
    st.plotly_chart(fig, use_container_width=True)

def visualize_graph_fold_cars(df, algorithms, metrics, selected_users, increment_yaxis):
    """
    Visualize a line graphic with evaluation results considering different algorithms, metrics and users.
    :param df: A dataframe with evaluation results.
    :param algorithms: List of recommendation algorithms.
    :param metrics: List of metrics.
    :param selected_users: List of users.
    """
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
        xaxis=dict(title="Fold", dtick=1, tickmode='linear'),
        yaxis_title="Performance",
        legend=dict(title="Measures of performance"),
        yaxis_range=[0, df[metrics].max().max()+increment_yaxis]
    )
    st.plotly_chart(fig, use_container_width=True)

def visualize_graph_mean_cars(df, algorithms, metrics, selected_users, increment_yaxis):
    """
    Visualize a bar graphic with evaluation results considering different algorithms, metrics and users.
    :param df: A dataframe with evaluation results.
    :param algorithms: List of recommendation algorithms.
    :param metrics: List of metrics.
    :param selected_users: List of users.
    """
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
        barmode='group',
        yaxis_range=[0, df[metrics].max().max()+increment_yaxis]
    )
    st.plotly_chart(fig, use_container_width=True)

def select_contextual_features(df, label):
    """
    Gets a sub-dataframe with the user-selected item or context features (from item_df or context_df, respectively).
    :param df: The item or context dataframe.
    :param label: The item or context label ("item" or "context").
    ;return: A sub-dataframe with the user-selected item or context features.
    """
    column_names = df.columns[1:].tolist() # Excluding the item_id or context_id.    
    selected_columns = st.sidebar.multiselect(label=f'Select {label} features:', options=column_names, default=column_names)
    if selected_columns:
        return df[[label+'_id']+selected_columns]
    
def replace_with_none(params):
    """
    TODO
    :param params: TODO
    :return: TODO
    """
    for key, value in params.items():
        if value == -0.5:
            params[key] = None
    return params
