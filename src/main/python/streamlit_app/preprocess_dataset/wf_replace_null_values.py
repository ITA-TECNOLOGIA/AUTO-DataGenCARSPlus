import pandas as pd
import streamlit as st
from datagencars.existing_dataset.replace_null_values.replace_null_values import ReplaceNullValues
from dateutil.parser import parse
from streamlit_app import config, console, help_information
from streamlit_app.generate_synthetic_dataset import wf_schema_util
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
    # Showing the initial image of the WF:
    if with_context:
        # Help information:
        help_information.help_replace_nulls_wf_item_cars()
        workflow_image.show_wf(wf_name='ReplaceNULLValues', init_step="True", with_context="True", optional_value_list=[('NULLValuesC', str(True)), ('NULLValuesI', str(True))])
    else:
        # Help information:
        help_information.help_replace_nulls_wf_item_rs()
        workflow_image.show_wf(wf_name='ReplaceNULLValues', init_step="False", with_context="False", optional_value_list=[('NULLValuesI', str(True))])
    st.markdown("""---""")
    
    # Showing progress messages in console:
    output = st.empty()  
    with console.st_log(output.code):
        # Replacing NULL values in item.csv:
        st.session_state['replace_item']=False
        replace_null_item = st.checkbox(f"Do you want to replace the null values in {config.ITEM_TYPE}.csv file?", value=False)
        new_item_df = pd.DataFrame()
        if replace_null_item:   
            st.session_state['replace_item']=True
            # Showing the WF image, by replacing null values in item.csv:
            workflow_image.show_wf(wf_name='ReplaceNULLValues', init_step="False", with_context=with_context, optional_value_list=[('NULLValuesC', str(False)), ('NULLValuesI', str(True))])
            # Loading item.csv file:
            __, item_df, __, __, __, __ = wf_util.load_dataset(file_type_list=['item'], wf_type='wf_replace_nulls')
            # Infering context schema from item.csv:
            item_schema = infer_schema(df=item_df, file_type=config.ITEM_TYPE)
            # Showing and editing the inferred schema:
            item_schema = wf_schema_util.edit_schema_file(schema_file_name=config.ITEM_TYPE, schema_value=item_schema, tab_type='null_values')           
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
    help_information.help_replace_nulls_wf_context_cars()
    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='ReplaceNULLValues', init_step="True", with_context="True", optional_value_list=[('NULLValuesC', str(True)), ('NULLValuesI', str(True))])
    st.markdown("""---""")
    
    # Replacing NULL values in context.csv:
    new_context_df = pd.DataFrame()
    if with_context:
        # Showing progress messages in console:
        output = st.empty()  
        with console.st_log(output.code):
            st.session_state['replace_context']=False            
            replace_null_context = st.checkbox(f"Do you want to replace the null values in {config.CONTEXT_TYPE}.csv file?", value=False)                    
            if replace_null_context:  
                st.session_state['replace_context']=True                              
                # Showing the WF image, by replacing null values in context.csv:
                workflow_image.show_wf(wf_name='ReplaceNULLValues', init_step="False", with_context=with_context, optional_value_list=[('NULLValuesC', str(True)), ('NULLValuesI', str(False))])            
                # Loading context.csv file:        
                __, __, context_df, __, __, __ = wf_util.load_dataset(file_type_list=['context'], wf_type='wf_replace_nulls')
                # Infering context schema from context.csv:
                context_schema = infer_schema(df=context_df, file_type=config.CONTEXT_TYPE)
                # Showing and editing the inferred schema:
                context_schema = wf_schema_util.edit_schema_file(schema_file_name=config.CONTEXT_TYPE, schema_value=context_schema, tab_type='null_values')                
                # Replacing null values:
                new_context_df = button_replace_null_values(schema_type=config.CONTEXT_TYPE, df=context_df, schema=context_schema)                   
    return new_context_df

def infer_data_type(attribute_value_list):
    """
    Infers the generator type and attribute type for a given list of attribute values.
    :param attribute_value_list: A list containing attribute values to infer the data type for.
    :return: A tuple containing the inferred generator type, attribute type, type component, and type subattribute.
    """
    generator_type = 'Unknown'            
    attribute_type = 'Unknown'
    type_component = 'Unknown'
    type_subattribute = 'Unknown'
    
    data_type = type(attribute_value_list[0])    
    # String:
    if data_type == str:
        # Categorical:
        generator_type = 'RandomAttributeGenerator'    
        attribute_type= 'String'
        # URL:
        if 'www.' in attribute_value_list[0]:
            generator_type = 'URLAttributeGenerator'
            attribute_type= 'AttributeComposite'       
            type_subattribute = 'String'     
        # Fixed:
        elif len(attribute_value_list) == 1:
            generator_type = 'FixedAttributeGenerator'  
            attribute_type= 'String'  
        # Address:
        elif '[' in attribute_value_list[0]:
            address_list = eval(attribute_value_list[0])
            attribute_type = type(address_list)
            if len(address_list) == 5:
                street_type = type(address_list[0])
                number_type = type(eval(address_list[1]))
                zp_type = type(eval(address_list[2]))
                lat_type = type(eval(address_list[3]))
                long_type = type(eval(address_list[4]))
                if (street_type == str) and (number_type == int) and (zp_type == int) and (lat_type == float) and (long_type == float):
                    generator_type = 'AddressAttributeGenerator'
                    attribute_type= 'AttributeComposite'
                    type_subattribute = 'String'
                # BooleanList:
                else:
                    generator_type = 'BooleanListAttributeGenerator'
                    attribute_type= 'List'  
                    type_component = 'Boolean'
            # BooleanList:
            else:                
                generator_type = 'BooleanListAttributeGenerator'
                attribute_type= 'List'  
                type_component = 'Boolean'
        elif is_valid_date(date_string=attribute_value_list[0]):
            generator_type = 'DateAttributeGenerator'
            attribute_type= 'String'

    # Boolean:
    elif data_type == bool:
        # Categorical:
        generator_type = 'RandomAttributeGenerator'
        attribute_type= 'Boolean'
        # Fixed:
        if len(attribute_value_list) == 1:
            generator_type = 'FixedAttributeGenerator'  
            attribute_type= 'Boolean' 

    # Integer:
    elif data_type == int:
        # Numerical:
        generator_type = 'RandomAttributeGenerator'
        attribute_type= 'Integer'
        # Fixed:
        if len(attribute_value_list) == 1:
            generator_type = 'FixedAttributeGenerator'  
            attribute_type= 'Integer' 
    # Float:
    elif data_type == float:
        # Numerical:
        generator_type = 'RandomAttributeGenerator'
        attribute_type= 'Float'
        # Fixed:
        if len(attribute_value_list) == 1:
            generator_type = 'FixedAttributeGenerator'  
            attribute_type= 'Float' 
    return generator_type, attribute_type, type_component, type_subattribute

def is_valid_date(date_string):
    """
    Determines whether a given string can be successfully parsed as a valid date.
    :param date_string: A string representation of a date.
    :return: True if the string is a valid date; False otherwise.
    """
    try:
        # Try to parse the string as a date
        parse(date_string)
        return True
    except ValueError:
        return False

def infer_schema(df, file_type):
    """
    Infers the content of the schema file.
    :param df: The item or context dataframe that will be used to infer its schema.
    :return: The inferred schema.
    """    
    schema_str=''
    schema_str += '[global]'+'\n'
    schema_str += f'type={file_type}'+'\n'
    attribute_name_list = df.columns[1:]   
    schema_str += f'number_attributes={len(attribute_name_list)}'+'\n'         
    for id_idx, attribute_name in enumerate(attribute_name_list, start=1):
        attribute_value_list = list(set(df[attribute_name].drop_duplicates().dropna()))
        # Infering types:
        generator_type, attribute_type, type_component, type_subattribute = infer_data_type(attribute_value_list)
        # Schema:                   
        schema_str += '\n'
        schema_str += f'[attribute{id_idx}]'+'\n'
        schema_str += f'name_attribute_{id_idx}={attribute_name}'+'\n'
        schema_str += f'generator_type_attribute_{id_idx}={generator_type}'+'\n'
        schema_str += f'type_attribute_{id_idx}={attribute_type}'+'\n'
        # URLAttributeGenerator-AttributeComposite-String:
        if generator_type == 'URLAttributeGenerator':            
            schema_str += f'number_maximum_subattribute_attribute_{id_idx}=2'+'\n'
            schema_str += f'name_subattribute_1_attribute_{id_idx}=name'+'\n'
            schema_str += f'name_subattribute_2_attribute_{id_idx}=url'+'\n'
            for i in range(1, 3):
                schema_str += f'type_subattribute_{i}_attribute_{id_idx}={type_subattribute}'+'\n'            
            name_list = []
            for attribute_value in attribute_value_list:
                name = attribute_value.replace('http', '').replace(':', '').replace('//', '').replace('www.', '').replace('.com', '')
                name_list.append(name)
            schema_str += f'input_parameter_attribute_{id_idx}={name_list}'+'\n'
            if len(name_list) == 1:
                schema_str += f'unique_value_attribute_{id_idx}=True'+'\n'
            else:
                schema_str += f'unique_value_attribute_{id_idx}=False'+'\n'            
        # AddressAttributeGenerator-AttributeComposite-String:
        elif generator_type == 'AddressAttributeGenerator':            
            schema_str += f'number_maximum_subattribute_attribute_{id_idx}=5'+'\n'
            schema_str += f'name_subattribute_1_attribute_{id_idx}=street'+'\n'
            schema_str += f'name_subattribute_2_attribute_{id_idx}=number'+'\n'
            schema_str += f'name_subattribute_3_attribute_{id_idx}=zp'+'\n'
            schema_str += f'name_subattribute_4_attribute_{id_idx}=latitude'+'\n'
            schema_str += f'name_subattribute_5_attribute_{id_idx}=longitude'+'\n'
            for i in range(1, 6):                
                schema_str += f'type_subattribute_{i}_attribute_{id_idx}={type_subattribute}'+'\n'
            address_value_list = []
            for attribute_value in attribute_value_list:
                address_value_list.append(eval(attribute_value))
            schema_str += f'input_parameter_attribute_{id_idx}={address_value_list}'+'\n'            
        # FixedAttributeGenerator-String/Integer/Boolean:
        elif generator_type == 'FixedAttributeGenerator':                      
            schema_str += f'input_parameter_attribute_{id_idx}={attribute_value_list[0]}'+'\n'            
        # RandomAttributeGenerator-Integer/Float/String/Boolean:
        elif generator_type == 'RandomAttributeGenerator':            
            if (attribute_type == 'Integer') or (attribute_type == 'Float'):
                schema_str += f'minimum_value_attribute_{id_idx}={min(attribute_value_list)}'+'\n'   
                schema_str += f'maximum_value_attribute_{id_idx}={max(attribute_value_list)}'+'\n'            
            elif attribute_type == 'String':
                schema_str += f'number_posible_values_attribute_{id_idx}={len(attribute_value_list)}'+'\n'  
                for i, attribute_value in enumerate(attribute_value_list, start=1):
                    schema_str += f'posible_value_{i}_attribute_{id_idx}={attribute_value}'+'\n'   
                schema_str += f'ranking_order_by_attribute_{id_idx}=neut'+'\n'
            elif attribute_type == 'Boolean':
                schema_str += f'number_posible_values_attribute_{id_idx}=2'+'\n'                  
                schema_str += f'posible_value_{1}_attribute_{id_idx}=True'+'\n'   
                schema_str += f'posible_value_{2}_attribute_{id_idx}=False'+'\n'  
                schema_str += f'ranking_order_by_attribute_{id_idx}=desc'+'\n'            
        # BooleanListAttributeGenerator-List-Boolean:
        elif generator_type == 'BooleanListAttributeGenerator':            
            schema_str += f'number_maximum_component_attribute_{id_idx}={len(attribute_value_list)}'+'\n'  
            schema_str += f'type_component_attribute_{id_idx}={type_component}'+'\n'  
            unique_attribute_value_set = set()
            for attribute_value in attribute_value_list:
                unique_attribute_value_set.update(eval(attribute_value))
            unique_attribute_value_list = list(unique_attribute_value_set)            
            for i, attribute_value in enumerate(unique_attribute_value_list, start=1):
                schema_str += f'component_{i}_attribute_{id_idx}={attribute_value}'+'\n'   
            schema_str += f'ranking_order_by_attribute_{id_idx}=neut'+'\n'
            schema_str += f'input_parameter_attribute_{id_idx}=1'+'\n'         
        # DateAttributeGenerator-String:
        elif generator_type == 'DateAttributeGenerator':            
            min_year = max_year = int(attribute_value_list[0].split('-')[2])
            for date_string in attribute_value_list:
                year = int(date_string.split('-')[2])
                if year < min_year:
                    min_year = year
                elif year > max_year:
                    max_year = year
            schema_str += f'minimum_value_attribute_{id_idx}={min_year}'+'\n'   
            schema_str += f'minimum_value_attribute_{id_idx}={max_year}'+'\n'
        schema_str += f'important_weight_attribute_{id_idx}=True'+'\n'
    schema_str += '\n'
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
        if st.button(label='Replace', key=f'button_replace_nulls_{schema_type}'):
            print('Replacing NULL Values')
            replace_null_values = ReplaceNullValues(file_df=df)         
            if schema_type == 'item':
                new_df = replace_null_values.regenerate_item_file(item_schema=schema)
                df_name = config.ITEM_TYPE
            elif schema_type == 'context':
                new_df = replace_null_values.regenerate_context_file(context_schema=schema)
                df_name = config.CONTEXT_TYPE
            if new_df.equals(df):
                st.warning(f'There are no Nulls values in the {schema_type} file. Below is the original {schema_type} file (without being transformed).')
            else:
                st.success(f'In the {schema_type} file, null values have been replaced successfully.')
            with st.expander(label=f'Show the replaced file: {schema_type}.csv'):
                # Show the new item schema file with replaced null values:    
                st.dataframe(new_df)
                # Downloading new item.csv:
                wf_util.save_df(df_name=df_name, df_value=new_df, extension='csv')          
    else:
        st.warning(f"The {schema_type} schema file have not been uploaded.")
    return new_df
