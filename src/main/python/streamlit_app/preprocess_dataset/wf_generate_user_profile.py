def generate():
    # Loading dataset:
    init_step = 'True'
    if with_context:
        user_df, item_df, context_df, rating_df = util.load_dataset(file_type_list=['user', 'item', 'context', 'rating'])
    else:
        user_df, item_df, __, rating_df = util.load_dataset(file_type_list=['user', 'item', 'rating'])

    # WF --> Generate user profile:
    st.header('Apply workflow: Generate user profile')
    # Help information:
    help_information.help_user_profile_wf()
    # Worflow image:
    optional_value_list = [('NULLValues', str(True)), ('NULLValuesC', str(True)), ('NULLValuesI', str(True)), ('UPManual', 'True'), ('UPAutomatic', 'True')]
    workflow_image.show_wf(wf_name='GenerateUserProfile', init_step=init_step, with_context=True, optional_value_list=optional_value_list)

    # Workflow:
    st.header('User profile')
    # Choosing user profile generation options (manual or automatic):
    up_option = st.selectbox(label='Choose an option to generate the user profile:', options=['Manual', 'Automatic'])    
    tab_replace_null_values, tab_generate_user_profile = st.tabs(['Replace NULL values', 'Generate user profile'])
    # REPLACE NULL VALUES TAB:
    new_item_df = pd.DataFrame()
    new_context_df = pd.DataFrame()        
    with tab_replace_null_values:
        if up_option == 'Manual':
            upauto = False
            upmanual = True
        else:
            upauto = True
            upmanual = False
        if with_context:
            null_values_c, null_values_i, new_item_df, new_context_df = util.tab_logic_replace_null('GenerateUserProfile', with_context, item_df, context_df, [('UPAutomatic', str(upauto)), ('UPManual', str(upmanual))])
        else:
            _, null_values_i, new_item_df, _ = util.tab_logic_replace_null('GenerateUserProfile', with_context, item_df, None, [('UPAutomatic', str(upauto)), ('UPManual', str(upmanual))])
    # USER PROFILE TAB:
    user_profile_df = pd.DataFrame()
    with tab_generate_user_profile:
        # Generating the user profile manually:
        if up_option == 'Manual':  
            # Help information:
            help_information.help_user_profile_manual()                     
            if with_context:           
                if not item_df.empty and not context_df.empty:
                    # Adding column "id":
                    attribute_column_list = ['user_profile_id']  
                    # Adding relevant item attribute columns:        
                    item_access = AccessItem(item_df)
                    item_attribute_name_list = item_access.get_item_attribute_list()                
                    attribute_column_list.extend(item_attribute_name_list)   
                    item_possible_value_map = {}     
                    for item_attribute_name in item_attribute_name_list:
                        item_possible_value_map[item_attribute_name] = item_access.get_item_possible_value_list_from_attributte(attribute_name=item_attribute_name)
                    # Adding relevant context attribute columns:    
                    context_access = AccessContext(context_df)
                    context_attribute_name_list = context_access.get_context_attribute_list()                    
                    attribute_column_list.extend(context_attribute_name_list)
                    context_possible_value_map = {}
                    for context_attribute_name in context_attribute_name_list:
                        context_possible_value_map[context_attribute_name] = context_access.get_context_possible_value_list_from_attributte(attribute_name=context_attribute_name)
                    # Adding column "other":
                    attribute_column_list.extend(['other'])
                    # Introducing the number of user profiles to generate:   
                    number_user_profile = st.number_input(label='Number of user profiles', value=4)
                    # Generate user profile manual (with context):              
                    user_profile_df = util.generate_user_profile_manual(number_user_profile, attribute_column_list, item_possible_value_map, context_possible_value_map)
                else:
                    st.warning("The item and context files have not been uploaded.")
            else:              
                if not item_df.empty:
                    # Adding column "id":
                    attribute_column_list = ['user_profile_id']  
                    # Adding relevant item attribute columns:        
                    item_access = AccessItem(item_df)
                    item_attribute_name_list = item_access.get_item_attribute_list()                
                    attribute_column_list.extend(item_attribute_name_list)   
                    item_possible_value_map = {}     
                    for item_attribute_name in item_attribute_name_list:
                        item_possible_value_map[item_attribute_name] = item_access.get_item_possible_value_list_from_attributte(attribute_name=item_attribute_name)
                    # Adding column "other":
                    attribute_column_list.extend(['other'])
                    # Introducing the number of user profiles to generate:   
                    number_user_profile = st.number_input(label='Number of user profiles', value=4)
                    # Generate user profile manual (not context):                 
                    user_profile_df = util.generate_user_profile_manual(number_user_profile, attribute_column_list, item_possible_value_map)
                else:
                    st.warning("The item file has not been uploaded.")
        elif up_option == 'Automatic':
            # Help information:
            help_information.help_user_profile_automatic()            
            if with_context:
                # Generate user profile automatic (with context):               
                if (not item_df.empty) and (not context_df.empty) and (not rating_df.empty):
                    user_profile_df = util.generate_user_profile_automatic(rating_df, item_df, context_df)
                else:
                    st.warning("The item, context and rating files have not been uploaded.")
            else:
                # Generate user profile automatic (not context):                     
                if (not item_df.empty) and (not rating_df.empty):
                    user_profile_df = util.generate_user_profile_automatic(rating_df, item_df)
                else:
                    st.warning("The item and rating files have not been uploaded.")