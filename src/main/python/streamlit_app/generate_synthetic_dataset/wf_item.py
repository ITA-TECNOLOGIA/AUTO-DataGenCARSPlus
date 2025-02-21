import console
import pandas as pd
import streamlit as st
from datagencars.synthetic_dataset.generator.generator_output_file.generator_item_file import GeneratorItemFile
from streamlit_app import config, help_information
from streamlit_app.generate_synthetic_dataset import wf_schema_util
from streamlit_app.preprocess_dataset import wf_util


def get_generation_config_schema():
    """
    Get the schema <generating_config_item.conf> for the generation of the item file.    
    :return: The edited content of the <generating_config_item.conf> schema.
    """
    st.header('General Settings')
    if st.checkbox('Upload the user data generation configuration file', value=True, key=f'is_upload_{config.GENERATION_CONFIG_ITEM_SCHEMA_NAME}'):
        # Uploading the schema <"generation_config_item.conf">:
        schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.GENERATION_CONFIG_ITEM_SCHEMA_NAME, tab_type='tab_item')
    else:
        # Generating the schema <"generation_config_item.conf">:
        schema_value = generate_generation_config_schema()

    # Editing schema:
    return wf_schema_util.edit_schema_file(schema_file_name=config.GENERATION_CONFIG_ITEM_SCHEMA_NAME, schema_value=schema_value, tab_type='tab_item')

def generate_generation_config_schema():
    """
    Generate the schema <generating_config_item.conf> for the generation of the item file.    
    :return: The content of the <generating_config_item.conf> schema.
    """    
    with st.expander(f"Generate generating_config_item.conf"):        
        # [dimension]        
        dimension_value = '[dimension] \n'
        item_count = st.number_input(label='Number of items to generate:', value=0)      
        dimension_value += 'number_item=' + str(item_count) + '\n'        
        
        st.markdown("""---""")
        
        # [null values]     
        generation_config_item_schema = ''   
        generation_config_item_schema += '[null values] \n'        
        if st.checkbox(label='Generate null values?', value=False, key='checkbox_null_value_item'):
            null_value_option = st.selectbox(label='', options=['Null percentage in the complete file', 'Null percentage per attribute'], key='selectbox_null_value_item')
            if null_value_option == 'Null percentage in the complete file':
                percentage_null_user = st.number_input(label='Null percentage in the complete file:', value=1, min_value=1, max_value=100, key='input_null_value_item')
                generation_config_item_schema += 'percentage_null_value_global=' + str(percentage_null_user) + '\n'            
            elif null_value_option == 'Null percentage per attribute':
                percentage_null_user_list = [int(number) for number in st.text_area(label='Null percentage per attribute: Provide a list detailing the percentage of null values for each attribute.', value='40, 0, 10, 97', key='textarea_null_value_item').split(',')]
                generation_config_item_schema += 'percentage_null_value_attribute=' + str(percentage_null_user_list) + '\n' 
        else:            
            generation_config_item_schema += 'percentage_null_value_global=0' + '\n'
        
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
        # Generating the text of the file <generation_config.conf>:
        generation_config_item_schema = dimension_value + '\n' + generation_config_item_schema + '\n' + item_profile_value        
    return generation_config_item_schema

def get_item_schema(n):
    """
    Get the schema <item_schema.conf>.
    :return: The edited item schema content.
    """
    st.header('Item Schema')        
    if st.checkbox(f'Upload the data {config.ITEM_TYPE} schema file', value=True, key=f'is_upload_{config.ITEM_SCHEMA_NAME}_file_{n}'):
        # Uploading the schema <"item_schema.conf">:
        schema_value = wf_schema_util.upload_schema_file(schema_file_name=config.ITEM_SCHEMA_NAME, tab_type=f'tab_item_{n}')
    else:
        # Generating the schema <"item_schema.conf">:
        schema_value = wf_schema_util.get_schema_file(schema_type=config.ITEM_SCHEMA_NAME)
    # Editing schema:
    return wf_schema_util.edit_schema_file(schema_file_name=config.ITEM_SCHEMA_NAME, schema_value=schema_value, tab_type=f'tab_item_{n}')

def get_item_profile_schema():
    """
    Get the schema <item_profile.conf>.
    :return: The edited schema <item_profile.conf> content.
    """
    # Uploading the schema <"item_profile.conf">:
    if st.checkbox(f'Upload the data {config.ITEM_PROFILE_TYPE} schema file', value=True, key=f'is_upload_{config.ITEM_PROFILE_SCHEMA_NAME}'):
        item_profile_value = wf_schema_util.upload_schema_file(schema_file_name=config.ITEM_PROFILE_SCHEMA_NAME, tab_type='tab_item')
    else:
        # Generating the schema <"item_profile.conf">:
        item_profile_value = generate_item_profile_schema()
    # Editing schema:
    return wf_schema_util.edit_schema_file(schema_file_name=config.ITEM_PROFILE_SCHEMA_NAME, schema_value=item_profile_value, tab_type='tab_item')   

def generate_item_profile_schema():
    """
    Generate the schema <item_profile.conf>.
    :return: The item profile content.
    """
    with st.expander(f"Generate item_profile.conf"):
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

def generate_item_file(generation_config, item_schema, item_profile=None):
    """
    Generates the item file from item_schema. 
    :param generation_config: The configuration file.
    :param item_schema: The item schema. It should contain information about items.
    :param item_profile: The item profile <optional>.    
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
                    wf_util.save_df(df_name=config.ITEM_TYPE, df_value=item_file_df, extension='csv')
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
                    wf_util.save_df(df_name=config.ITEM_TYPE, df_value=item_file_df, extension='csv')
        else:            
            st.warning(f'The item schema (item_schema.conf) and general setting (general_config.conf) files are required. The item profile schema (item_profile.conf) file should only be uploaded if you want to generate correlated item attributes ("check "with correlation" and upload the item profile").')
    return item_file_df
