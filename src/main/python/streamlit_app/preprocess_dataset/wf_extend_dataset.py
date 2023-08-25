def generate():
    # Loading dataset:
    init_step = 'True'
    user_df, item_df, context_df, rating_df = util.load_dataset(file_type_list=['user', 'item', 'context', 'rating'])
    
    # WF --> Extend dataset:
    st.header('Apply workflow: Extend dataset')
    # Help information:
    help_information.help_extend_dataset_wf()
    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='ExtendDataset', init_step=init_step, with_context=True, optional_value_list=[('NULLValues', 'True'), ('NULLValuesC', 'True'), ('NULLValuesI', 'True')])   

    # Options tab:
    tab_replace_null_values, tab_generate_user_profile, tab_extend_dataset  = st.tabs(['Replace NULL values', 'Generate user profile', 'Extend dataset'])     
    # REPLACE NULL VALUES TAB:
    new_item_df = pd.DataFrame()
    new_context_df = pd.DataFrame()        
    with tab_replace_null_values:
        # null_values_c, null_values_i, new_item_df, new_context_df = util.tab_logic_replace_null('ExtendDataset', with_context, item_df, context_df)
        if with_context:
            null_values_c, null_values_i, new_item_df, new_context_df = util.tab_logic_replace_null('ExtendDataset', with_context, item_df, context_df)
        else:
            _, null_values_i, new_item_df, _ = util.tab_logic_replace_null('ExtendDataset', with_context, item_df)
            null_values_c = False
    with tab_generate_user_profile:
        user_profile = util.generate_user_profile_automatic(rating_df, item_df, context_df) # Old way
        optional_value_list = [('NULLValues', str(null_values_c & null_values_i)), ('NULLValuesC', str(null_values_c)), ('NULLValuesI', str(null_values_i))]
        if not null_values_i:
            new_item_df = item_df
        if not null_values_c and with_context:
            new_context_df = context_df
        if with_context:
            user_profile = util.tab_logic_generate_up('ExtendDataset', with_context, optional_value_list, rating_df, new_item_df, new_context_df)         
        else:    
            user_profile = util.tab_logic_generate_up('ExtendDataset', with_context, optional_value_list, rating_df, new_item_df) 
    with tab_extend_dataset:
        # Showing the current image of the WF:
        workflow_image.show_wf(wf_name='ExtendDataset', init_step='False', with_context=with_context, optional_value_list=[('NULLValues', str(null_values_c or null_values_i)), ('NULLValuesC', str(null_values_c)), ('NULLValuesI', str(null_values_i))])
        inc_rating = IncreaseRating(rating_df=rating_df, item_df=item_df, user_df=user_df, context_df=context_df, user_profile=user_profile)
        option = st.selectbox('How would you like to extend the dataset?',('K ratings for all users', 'K ratings for N users'))
        if option == 'K ratings for all users':
            number_ratings = st.number_input('Enter the number of ratings to generate for each user:', min_value=1, step=1, value=1)
            percentage_rating_variation = st.number_input('Enter the percentage rating variation:', min_value=0, max_value=100, step=1, value=25)
            k = st.number_input('Enter the k ratings to take in the past:', min_value=1, step=1, value=10)
            
            if st.button('Generate Ratings'):
                result_df = inc_rating.incremental_rating_random(number_ratings=number_ratings, percentage_rating_variation=percentage_rating_variation, k=k)
                st.write("Generated Ratings:")
                st.write(result_df)

        elif option == 'K ratings for N users':
            selected_users = st.multiselect('Select users:', user_df['user_id'])
            number_ratings = st.number_input('Enter the number of ratings to generate for each user:', min_value=1, step=1)
            percentage_rating_variation = st.number_input('Enter the percentage rating variation:', min_value=0, max_value=100, step=1)
            k = st.number_input('Enter the k ratings to take in the past:', min_value=1, step=1)
            
            if st.button('Generate Ratings'):
                result_df = inc_rating.incremental_rating_by_user(user_ids=selected_users, number_ratings=number_ratings, percentage_rating_variation=percentage_rating_variation, k=k)
                st.write("Generated Ratings:")
                st.write(result_df)