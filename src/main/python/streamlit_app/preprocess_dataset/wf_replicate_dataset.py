import streamlit as st
from streamlit_app import help_information
from streamlit_app.workflow_graph import workflow_image
import pandas as pd


def generate(with_context):    
    # Loading dataset:
    st.header('Load dataset')     
    if with_context:
        user_df, item_df, context_df, rating_df = wf_util.load_dataset(file_type_list=['user', 'item', 'context', 'rating'])
    else:
        user_df, item_df, __, rating_df = wf_util.load_dataset(file_type_list=['user', 'item', 'rating'])   

    # WF --> Replicate dataset:
    st.header('Workflow: Replicate dataset')    

    # Help information:
    help_information.help_replicate_dataset_wf()
    
    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='ReplicateDataset', init_step='True', with_context=True, optional_value_list=[('NULLValues', 'True'), ('NULLValuesC', 'True'), ('NULLValuesI', 'True')])
        
    # Options tab:
    tab_replace_null_values, tab_generate_user_profile, tab_replicate_dataset  = st.tabs(['Replace NULL values', 'Generate user profile', 'Replicate dataset'])
    # REPLACE NULL VALUES TAB:
    new_item_df = pd.DataFrame()
    new_context_df = pd.DataFrame()     
    with tab_replace_null_values:
        if with_context:
            null_values_c, null_values_i, new_item_df, new_context_df = util.tab_logic_replace_null('ReplicateDataset', with_context, item_df, context_df)
        else:
            _, null_values_i, new_item_df, _ = util.tab_logic_replace_null('ReplicateDataset', with_context, item_df)
            null_values_c = False
    # USER PROFILE TAB:
    with tab_generate_user_profile:
        optional_value_list = [('NULLValues', str(null_values_c & null_values_i)), ('NULLValuesC', str(null_values_c)), ('NULLValuesI', str(null_values_i))]
        if not null_values_i:
            new_item_df = item_df
        if not null_values_c and with_context:
            new_context_df = context_df
        if with_context:
            user_profile_df = util.tab_logic_generate_up('ReplicateDataset', with_context, optional_value_list, rating_df, new_item_df, new_context_df)         
        else:    
            user_profile_df = util.tab_logic_generate_up('ReplicateDataset', with_context, optional_value_list, rating_df, new_item_df)             
    # REPLICATE TAB:        
    with tab_replicate_dataset:
        new_rating_df = pd.DataFrame()
        # Showing the current image of the WF:
        workflow_image.show_wf(wf_name='ReplicateDataset', init_step='False', with_context=with_context, optional_value_list=[('NULLValues', str(null_values_c or null_values_i)), ('NULLValuesC', str(null_values_c)), ('NULLValuesI', str(null_values_i))])
        percentage_rating_variation = st.number_input(label='Percentage of rating variation:', value=25, key='percentage_rating_variation_rs')
        output = st.empty()  
        replicate_button = st.button(label='Replicate', key = 'replicate_cars', on_click=util.replicate_task, args=(with_context, rating_df, user_profile_df, new_item_df, new_context_df,percentage_rating_variation, output, st))   

    if os.path.exists('new_ratings.csv'):
        new_rating_df = pd.read_csv('new_ratings.csv')
        with st.expander(label='Show the replicated file: rating.csv'):
            st.dataframe(new_rating_df)
            link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(new_rating_df.to_csv(index=False).encode()).decode()}" download="rating.csv">Download</a>'
            st.markdown(link_rating, unsafe_allow_html=True)    
        os.remove('new_ratings.csv')