
def generate():
     # Loading dataset:
    init_step = 'True' 
    _, item_df, context_df, rating_df = util.load_dataset(file_type_list=['item', 'context', 'rating'])

    # WF --> Recalculate ratings:
    st.header('Workflow: Recalculate ratings')
    # Help information:
    help_information.help_recalculate_ratings_wf()
    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='RecalculateRatings', init_step='True', with_context=True, optional_value_list=[('NULLValues', str(True)), ('NULLValuesC', str(True)), ('NULLValuesI', str(True))])

    # Options tab:
    tab_replace_null_values, tab_generate_user_profile, tab_extend_dataset  = st.tabs(['Replace NULL values', 'Generate user profile', 'Extend dataset'])     
    # REPLACE NULL VALUES TAB:
    new_item_df = pd.DataFrame()
    new_context_df = pd.DataFrame()        
    with tab_replace_null_values:
        null_values_c, null_values_i, new_item_df, new_context_df = util.tab_logic_replace_null('RecalculateRatings', with_context, item_df, context_df)
    with tab_generate_user_profile:
        optional_value_list = [('NULLValues', str(null_values_c & null_values_i)), ('NULLValuesC', str(null_values_c)), ('NULLValuesI', str(null_values_i))]
        if with_context:
            user_profile_df = util.tab_logic_generate_up('ExtendDataset', with_context, optional_value_list, rating_df, new_item_df, new_context_df)         
        else:    
            user_profile_df = util.tab_logic_generate_up('ExtendDataset', with_context, optional_value_list, rating_df, new_item_df) 
    with tab_extend_dataset:
        # Showing the current image of the WF:
        workflow_image.show_wf(wf_name='ExtendDataset', init_step='False', with_context=with_context, optional_value_list=[('NULLValues', str(null_values_c or null_values_i)), ('NULLValuesC', str(null_values_c)), ('NULLValuesI', str(null_values_i))])
    st.write('TODO')