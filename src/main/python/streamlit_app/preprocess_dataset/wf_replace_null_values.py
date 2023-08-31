import base64
import io

import pandas as pd
import requests
import streamlit as st
from datagencars.existing_dataset.replace_null_values import ReplaceNullValues
from streamlit_app import config, console, help_information
from streamlit_app.preprocess_dataset import wf_util
from streamlit_app.workflow_graph import workflow_image

def generate(with_context, tab_replace_null_values_item, tab_replace_null_values_context=None):
    """
    Replaces NULL values in the item or context files.
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    :param tab_replace_null_values_item: The tab related to the replacement of NULL values in the item file.
    :param tab_replace_null_values_context: The tab related to the replacement of NULL values in the context file.
    :return: The item and context files with replaced NULL values.
    """
    new_item_df = pd.DataFrame()
    new_context_df = pd.DataFrame()
    if with_context:
        # Replacing NULL values in context.csv:
        with tab_replace_null_values_context:
            new_context_df = generate_context(with_context)
    # Replacing NULL values in item.csv:
    with tab_replace_null_values_item:
        new_item_df = generate_item(with_context)
    return new_item_df, new_context_df
        
def generate_item(with_context):
    """
    Replaces NULL values in the item schema files.
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    """
    # WF --> Replace NULL values:
    st.header(f'Workflow: Replace NULL values')
    # Help information:
    help_information.help_replace_nulls_wf()
    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='ReplaceNULLValues', init_step="True", with_context="True", optional_value_list=[('NULLValuesC', str(True)), ('NULLValuesI', str(True))])
    st.markdown("""---""")
    
    # Showing progress messages in console:
    output = st.empty()  
    with console.st_log(output.code):
        # Replacing NULL values in item.csv:
        replace_null_item = st.checkbox(f"Do you want to replace the null values in {config.ITEM_TYPE}.csv file?", value=False)
        new_item_df = pd.DataFrame()
        if replace_null_item:            
            # Showing the WF image, by replacing null values in item.csv:
            workflow_image.show_wf(wf_name='ReplaceNULLValues', init_step="False", with_context=with_context, optional_value_list=[('NULLValuesC', str(False)), ('NULLValuesI', str(True))])
            # Loading item.csv file:
            __, item_df, __, __, __ = wf_util.load_dataset(file_type_list=['item'], wf_type='wf_replace_nulls')
            # Infering context schema from item.csv:
            item_schema = infer_schema(df=item_df)
            # Showing the inferred schema:
            wf_util.show_schema_file(schema_file_name=config.ITEM_TYPE, schema_value=item_schema)        
            # Replacing null values:
            new_item_df = button_replace_null_values(schema_type=config.ITEM_TYPE, df=item_df, schema=item_schema)      
    return new_item_df

def generate_context(with_context):
    """
    Replaces NULL values in the context schema files.
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    """
    # WF --> Replace NULL values:
    st.header(f'Workflow: Replace NULL values')
    # Help information:
    help_information.help_replace_nulls_wf()
    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='ReplaceNULLValues', init_step="True", with_context="True", optional_value_list=[('NULLValuesC', str(True)), ('NULLValuesI', str(True))])
    st.markdown("""---""")
    
    # Replacing NULL values in context.csv:
    new_context_df = pd.DataFrame()
    if with_context:
        # Showing progress messages in console:
        output = st.empty()  
        with console.st_log(output.code):
            replace_null_context = st.checkbox(f"Do you want to replace the null values in {config.CONTEXT_TYPE}.csv file?", value=False)                    
            if replace_null_context:                
                # Showing the WF image, by replacing null values in context.csv:
                workflow_image.show_wf(wf_name='ReplaceNULLValues', init_step="False", with_context=with_context, optional_value_list=[('NULLValuesC', str(True)), ('NULLValuesI', str(False))])            
                # Loading context.csv file:        
                __, __, context_df, __, __ = wf_util.load_dataset(file_type_list=['context'], wf_type='wf_replace_nulls')
                # Infering context schema from context.csv:
                context_schema = infer_schema(df=context_df)
                # Showing the inferred schema:
                wf_util.show_schema_file(schema_file_name=config.CONTEXT_TYPE, schema_value=context_schema)            
                # Replacing null values:
                new_context_df = button_replace_null_values(schema_type=config.CONTEXT_TYPE, df=context_df, schema=context_schema)                   
    return new_context_df   

def infer_schema(df):
    """
    Infers the content of the schema file.
    :param df: The item or context dataframe that will be used to infer its schema.
    :return: The inferred schema.
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
        if item_type == 'Integer':
            if len(items) >= 2:
                item_generator = 'Numerical'
                min_val = int(min(items))
                max_val = int(max(items))
            else:
                item_generator = 'Fixed'
                min_val = int(items[0])
                max_val = int(items[0])
        elif item_type == 'Float':
            if len(items) >= 2:
                item_generator = 'Numerical'
                min_val = float(min(items))
                max_val = float(max(items))
            else:
                item_generator = 'Fixed'
                min_val = float(items[0])
                max_val = float(items[0])            
        if item_type == 'String':
            if len(items) >= 2:
                item_generator = 'Categorical'
            else:
                item_generator = 'Fixed'
                fix_val = items[0]
        if item_type == 'Boolean':
            item_generator = 'Categorical'
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
        atrib_generator = st.selectbox(label='Generator type:', options=config.GENERATOR_OPTIONS, key = attribute+'generator', index=config.GENERATOR_OPTIONS.index(row['GeneratorType']))
        atrib_type = st.selectbox(label='Attribute type:', options=config.ATTRITBUTE_OPTIONS, key=attribute+'_attribute_type_', index=config.ATTRITBUTE_OPTIONS.index(row['TypeAttribute']))
        schema_str = schema_str + 'type_attribute_' + str(int(index+1)) + '=' + atrib_type + '\n'
        if atrib_type == 'Float':
            if atrib_generator == 'Fixed':
                schema_str = schema_str + 'generator_type_attribute_' + str((index+1)) + '=FixedAttributeGenerator\n'
                fixed_val = st.number_input(label='Fixed value of the attribute', value=float(row['Min_val']), key=attribute+'_fixed_val')
                schema_str = schema_str + 'input_parameter_attribute_' + str((index+1)) + '=' + str(fixed_val) + '\n'
            else:
                schema_str = schema_str + 'generator_type_attribute_' + str((index+1)) + '=RandomAttributeGenerator\n'
                integer_min = st.number_input(label='Minimum value of the attribute', value=float(row['Min_val']), key=attribute+'_integer_min')
                integer_max = st.number_input(label='Maximum value of the attribute', value=float(row['Max_val']), key=attribute+'_integer_max')
                schema_str = schema_str + 'minimum_value_attribute_' + str((index+1)) + '=' + str((integer_min)) + '\n'
                schema_str = schema_str + 'maximum_value_attribute_' + str((index+1)) + '=' + str((integer_max)) + '\n'
        if atrib_type == 'Integer':
            if atrib_generator == 'Fixed':
                schema_str = schema_str + 'generator_type_attribute_' + str((index+1)) + '=FixedAttributeGenerator\n'
                fixed_val = st.number_input(label='Fixed value of the attribute', value=int(row['Min_val']), key=attribute+'_fixed_val')
                schema_str = schema_str + 'input_parameter_attribute_' + str((index+1)) + '=' + str(fixed_val) + '\n'
            else:
                schema_str = schema_str + 'generator_type_attribute_' + str((index+1)) + '=RandomAttributeGenerator\n'
                integer_min = st.number_input(label='Minimum value of the attribute', value=int(row['Min_val']), key=attribute+'_integer_min')
                integer_max = st.number_input(label='Maximum value of the attribute', value=int(row['Max_val']), key=attribute+'_integer_max')
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
                    input_parameter_text_area = ip_text_area.text_area(label='Introduce address values (line by line), keeping the header: <street;number;zp;latitude;longitude>', value='street,number,zp,latitude,longitude', key='address_ip_text_area_'+str(index+1))   
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
                    input_parameter_text_area = ip_text_area.text_area(label="Introduce place_name to search address, for example: McDonald's, 50017, keeping header: place, postalcode", value='place, zipcode', key='address_ip_text_area_'+str(index+1))   
                    if import_file := st.file_uploader(label='Import place_name list, keeping header: place', key='import_file'+str(index+1)):                            
                        input_parameter_text_area = ip_text_area.text_area(label="Introduce place_name to search address, for example: McDonald's, 50017, keeping header: place, postalcode", value=import_file.getvalue().decode("utf-8"), key='import_address_ip_text_area_'+str(index+1))                            
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
                    input_parameter_text_area_2 = ip_text_area_2.text_area(label='Search results:', value=places_str, key='address_ip_text_area_2_'+str(index+1))   
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
                unique_value = st.checkbox(label='Unique value?', value=True, key='unique_value_'+str(index+1)+'_'+attribute)
                if unique_value:
                    schema_str += 'unique_value_attribute_'+str(index+1)+'=True'+'\n'
                else:
                    schema_str += 'unique_value_attribute_'+str(index+1)+'=False'+'\n'      
        st.markdown("""---""")
        schema_str = schema_str + '\n'
    return schema_str

def button_replace_null_values(schema_type, df, schema):
    """
    Executes a button to replace NULL values in the df entered as parameter (item or context file).
    :param schema_type: The schema type (item or context schema).
    :param df: The item or context dataframe with NULL values.
    :param schema: The item or context schema inferred from item or context dataframe.
    :return: The new item or context dataframe without NULL values.
    """
    new_df = pd.DataFrame()    
    if not df.empty:
        if st.button(label='Replace NULL Values', key=f'button_replace_nulls_{schema_type}'):
            print('Replacing NULL Values')
            replace_null_values = ReplaceNullValues(file_df=df)         
            if schema_type == 'item':
                new_df = replace_null_values.regenerate_item_file(item_schema=schema)
                df_name = config.ITEM_TYPE
            elif schema_type == 'context':
                new_df = replace_null_values.regenerate_context_file(context_schema=schema)
                df_name = config.CONTEXT_TYPE
            with st.expander(label=f'Show the replaced file: {schema_type}.csv'):
                # Show the new item schema file with replaced null values:    
                st.dataframe(new_df)
                # Downloading new item.csv:
                wf_util.save_df(df_name=df_name, df_value=new_df, extension='csv')          
    else:
        st.warning(f"The {schema_type} schema file have not been uploaded.")
    return new_df
