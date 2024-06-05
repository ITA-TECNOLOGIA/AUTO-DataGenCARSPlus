import console
import pandas as pd
import streamlit as st
from datagencars.existing_dataset.generate_null_values.generate_null_values import GenerateNullValues
from streamlit_app import config, help_information
from streamlit_app.preprocess_dataset import wf_util
from streamlit_app.workflow_graph import workflow_image


def generate(with_context, tab_generate_null_values_item, tab_generate_null_values_context=None):
    """
    Generates new data frames for items and contexts with the potential inclusion of NULL values.

    Parameters:
    - with_context (bool): A flag indicating whether context data should be included in the generation process.
    - tab_generate_null_values_item (context manager): A context manager that handles the generation of NULL values within the 'item' data frame.
    - tab_generate_null_values_context (context manager, optional): A context manager that handles the generation of NULL values within the 'context' data frame if 'with_context' is True.

    The function works by initially creating empty data frames for items and contexts. If the 'with_context' flag is True, it uses the 'tab_generate_null_values_context' context manager to generate a new context data frame with NULL values by invoking the 'generate_context' method. Independently, it generates a new item data frame with NULL values using the 'tab_generate_null_values_item' context manager and the 'generate_item' method.

    Returns:
    - new_item_df (DataFrame): The newly generated data frame for items, potentially containing NULL values.
    - new_context_df (DataFrame): The newly generated data frame for contexts, potentially containing NULL values if 'with_context' is True; otherwise, it remains an empty data frame.
    """
    new_item_df = pd.DataFrame()
    new_context_df = pd.DataFrame()    
    if with_context:
        # Generating NULL values in context.csv:
        with tab_generate_null_values_context:
            new_context_df = generate_context(with_context)
    # Generating NULL values in item.csv:
    with tab_generate_null_values_item:
        new_item_df = generate_item(with_context)
    return new_item_df, new_context_df

def generate_item(with_context):
    """
    Generates a new item data frame with the option to insert NULL values, allowing user interaction to define the method and extent of NULL value insertion.

    Parameters:
    - with_context (bool): Indicates whether the context information affects the generation workflow (e.g., showing different initial workflow images).

    This function provides a user interface for configuring the generation of NULL values in an 'item' data frame. It starts by displaying workflow information and help resources. Depending on the 'with_context' flag, it adjusts the initial display of the workflow. The user can then choose between global or attribute-specific strategies for NULL generation, and configure the extent of NULLs using input widgets. The process is interactive, with real-time log messages about the progress.

    - For the 'Global' strategy, users can specify a percentage of NULL values across all attributes.
    - For the 'By Attribute' strategy, users can specify a percentage for each attribute.

    After configuration, the function triggers the generation process upon user command and displays the resulting data frame with NULL values, along with statistics about the NULL values. It also provides options to save the modified data frame.

    Returns:
    - new_item_df (DataFrame): The newly generated data frame with specified NULL values, which may be empty if no data file is loaded initially or if generation is not triggered.
    """
    # WF --> Generate NULL values:
    st.header(f'Workflow: Generate NULL values')        
    # Showing the initial image of the WF:
    if with_context:
        help_information.help_generate_nulls_wf_item_cars()
        workflow_image.show_wf(wf_name='GenerateNULLValues', init_step="True", with_context="True", optional_value_list=[('NULLValuesC', str(True)), ('NULLValuesI', str(True))])
    else:
        # Help information:
        help_information.help_generate_nulls_wf_item_rs()
        workflow_image.show_wf(wf_name='GenerateNULLValues', init_step="False", with_context="False", optional_value_list=[('NULLValuesI', str(True))])
    st.markdown("""---""")
    
    # Showing progress messages in console:
    output = st.empty()  
    generate_null_value = GenerateNullValues()
    new_item_df = pd.DataFrame()  
    with console.st_log(output.code):
        __, item_df, __, __, __, __ = wf_util.load_dataset(file_type_list=['item'], wf_type='wf_generate_null_values')  
        if not item_df.empty:            
            null_value_strategy = st.selectbox(label='Strategy for generating null values', options=config.NULL_VALUES_GENERATE_OPTIONS, key='null_value_strategy_item_selectbox')            
            if null_value_strategy == 'Global':
                percentage_null_value_global = st.number_input("Percentage of null values", min_value=1, max_value=100, value=20, key='number_input_percentage_nulls_item')
                if st.button(label='Generate', key='button_generate_null_values_global_item'):            
                    new_item_df = generate_null_value.generate_null_value_global(file_df=item_df, percentage_null=percentage_null_value_global)
                    with st.expander(label=f'Show the {config.ITEM_TYPE}.csv file with null values:'):
                        # Showing statistics:                        
                        generate_null_value.display_null_statistics(file_df=new_item_df)
                        # Showing the generated file:
                        st.markdown("""**Resulting file:**""")
                        st.dataframe(new_item_df)    
                        # Saving the generated file:
                        wf_util.save_df(df_name=config.ITEM_TYPE+f'_null_values_global', df_value=new_item_df, extension='csv')
            elif null_value_strategy == 'By Attribute':                
                attribute_list = item_df.columns.tolist()[1:]
                percentage_null_value_attribute_list = []
                for attribute in attribute_list:
                    percentage_null_value = st.text_input(label=attribute, value=0, key=f'{attribute}_text_input')
                    percentage_null_value_attribute_list.append(percentage_null_value)
                if st.button(label='Generate', key='button_generate_null_values_by_attribute_item'):            
                    new_item_df = generate_null_value.generate_null_value_attribute(file_df=item_df, percentage_null_value_attribute_list=percentage_null_value_attribute_list)
                    with st.expander(label=f'Show the {config.ITEM_TYPE}.csv file with null values:'):
                        # Showing statistics:                            
                        generate_null_value.display_null_statistics(file_df=new_item_df)
                        # Showing the generated file:
                        st.markdown("""**Resulting file:**""")
                        st.dataframe(new_item_df)    
                        # Saving the generated file:
                        wf_util.save_df(df_name=config.ITEM_TYPE+f'__null_values_by_attribute', df_value=new_item_df, extension='csv')                
        else:
            st.warning("The item file must be uploaded.")
    return new_item_df

def generate_context(with_context):
    """
    Generates a new context data frame with configurable NULL value insertion options, incorporating user interactions for strategy selection and extent configuration.

    Parameters:
    - with_context (bool): Indicates if the context-specific workflow should be affected, primarily influencing the initial workflow image presentation.

    The method begins by setting up the workflow interface, displaying help information and an initial workflow image that varies based on the 'with_context' parameter. Users can select from predefined NULL value generation strategies ('Global' or 'By Attribute') and specify the desired percentage of NULL values either globally or per attribute. The method involves interactive elements like buttons and input fields to collect user preferences.

    The process is outlined as follows:
    - For the 'Global' strategy, a percentage of NULL values is applied across all attributes of the context data frame.
    - For the 'By Attribute' strategy, percentages are applied individually to selected attributes as specified by the user.

    Upon configuration, the function initiates the NULL value generation based on the selected strategy when the user triggers the process. It then displays the modified data frame and statistics regarding the NULL values, and offers an option to save the resultant data frame.

    Returns:
    - new_context_df (DataFrame): The modified context data frame with the specified NULL values, potentially empty if no initial data is available or if no generation process is triggered.
    """
    # WF --> Generate NULL values:
    st.header(f'Workflow: Generate NULL values')
    # Help information:
    help_information.help_generate_nulls_wf_context_cars()
    # Showing the initial image of the WF:
    if with_context:
        workflow_image.show_wf(wf_name='GenerateNULLValues', init_step="True", with_context="True", optional_value_list=[('NULLValuesC', str(True)), ('NULLValuesI', str(True))])
    else:
        workflow_image.show_wf(wf_name='GenerateNULLValues', init_step="False", with_context="False", optional_value_list=[('NULLValuesI', str(True))])
    st.markdown("""---""")
    
    # Showing progress messages in console:
    output = st.empty()  
    generate_null_value = GenerateNullValues()
    new_context_df = pd.DataFrame()  
    with console.st_log(output.code):
        __, __, context_df, __, __, __ = wf_util.load_dataset(file_type_list=['context'], wf_type='wf_generate_null_values')
        if not context_df.empty:            
            null_value_strategy = st.selectbox(label='Strategy for generating null values', options=config.NULL_VALUES_GENERATE_OPTIONS, key='null_value_strategy_context_selectbox')            
            if null_value_strategy == 'Global':
                percentage_null_value_global = st.number_input("Percentage of null values", min_value=1, max_value=100, value=20, key='number_input_percentage_nulls_context')
                if st.button(label='Generate', key='button_generate_null_values_global_context'):            
                    new_context_df = generate_null_value.generate_null_value_global(file_df=context_df, percentage_null=percentage_null_value_global)
                    with st.expander(label=f'Show the {config.CONTEXT_TYPE}.csv file with null values:'):
                        # Showing statistics:                        
                        generate_null_value.display_null_statistics(file_df=new_context_df)
                        # Showing the generated file:
                        st.markdown("""**Resulting file:**""")
                        st.dataframe(new_context_df)    
                        # Saving the generated file:
                        wf_util.save_df(df_name=config.CONTEXT_TYPE+f'_null_values_global', df_value=new_context_df, extension='csv')
            elif null_value_strategy == 'By Attribute':                
                attribute_list = context_df.columns.tolist()[1:]
                percentage_null_value_attribute_list = []
                for attribute in attribute_list:
                    percentage_null_value = st.text_input(label=attribute, value=0, key=f'{attribute}_text_input')
                    percentage_null_value_attribute_list.append(percentage_null_value)
                if st.button(label='Generate', key='button_generate_null_values_by_attribute_context'):            
                    new_context_df = generate_null_value.generate_null_value_attribute(file_df=context_df, percentage_null_value_attribute_list=percentage_null_value_attribute_list)
                    with st.expander(label=f'Show the {config.ITEM_TYPE}.csv file with null values:'):
                        # Showing statistics:                            
                        generate_null_value.display_null_statistics(file_df=new_context_df)
                        # Showing the generated file:
                        st.markdown("""**Resulting file:**""")
                        st.dataframe(new_context_df)    
                        # Saving the generated file:
                        wf_util.save_df(df_name=config.CONTEXT_TYPE+f'__null_values_by_attribute', df_value=new_context_df, extension='csv')                
        else:
            st.warning("The context file must be uploaded.")
    return new_context_df
