def generation_synthtetic_dataset():
    if with_context:
        lars = st.sidebar.checkbox('LARS', value=True)
        if lars:
            side_lars = st.sidebar.checkbox('SocIal-Distance prEserving', value=True)
    feedback = 'implicit'
    init_step = 'True'
    # Help information:
    help_information.help_implicit_rating_wf()
    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='GenerateSyntheticDataset(Implicit_ratings)', init_step=init_step, with_context=with_context)
    
    inconsistent = False
    # AVAILABLE TABS:
    if with_context and lars and side_lars:
        context = True
        tab_generation, tab_user, tab_item, tab_context, tab_behavior, tab_run  = st.tabs(['Generation', 'Users', 'Items', 'Contexts', 'Behavior', 'Run'])
        # GENERATION SETTING TAB:
        generation_config_value = util.generation_settings(tab_generation)
        with_correlation_checkbox = False
        # USER TAB:
        with tab_user:        
            st.header('Users')
            schema_type = 'user'
            user_schema_value = util.generate_schema_file(schema_type)
        # ITEM TAB:
        with tab_item:
            st.header('Items')
            schema_type = 'item'
            item_schema_value = util.generate_schema_file(schema_type)
            st.markdown("""---""")
            # Item profile:
            item_profile_value = ''
            item_profile_text_area = ''  
            if is_upload_item_profile := st.checkbox('Upload the item profile file', value=True, key='is_upload_item_profile'):
                with st.expander("Upload item_profile.conf"):
                    if item_profile_file := st.file_uploader(label='Choose the file:', key='item_profile_file'):
                        item_profile_value = item_profile_file.getvalue().decode("utf-8")
            else:
                # [global]   
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
                st.write('Examples of importance order:')
                st.markdown("""- ascending: ``` quality food=[bad, normal, good] ``` """)
                st.markdown("""- descending: ``` quality food=[good, normal, bad] ``` """)
                ranking_order_original = st.selectbox(label='Select an order of importance?', options=['descending', 'ascending'])
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
                st.markdown(
                """ 
                ```python
                # Example 1: overlapping at the midpoint on the left and the right
                item_profile_names = ['bad', 'normal', 'good'] 
                overlap_midpoint_left_profile = 0 
                overlap_midpoint_right_profile = 0 
                good_profile =   ['good'] 
                normal_profile =   ['normal'] 
                bad_profile =   ['bad'] 
                ``` 
                """)
                st.markdown(""" 
                ```python
                # Example 2: overlapping at the midpoint on the left and the right
                item_profile_names = ['bad', 'normal', 'good']
                overlap_midpoint_left_profile = 1
                overlap_midpoint_right_profile = 1
                good_item_profile =   ['good']
                normal_item_profile =   ['bad', 'normal', 'good']
                bad_item_profile =   ['bad']
                ``` 
                """)
                item_profile_value += 'overlap_midpoint_left_profile='+str(overlap_midpoint_left_profile)+'\n'
                item_profile_value += 'overlap_midpoint_right_profile='+str(overlap_midpoint_right_profile)+'\n'
                item_profile_value += '\n'            
            # Show generated schema file:
            with st.expander("Show item_profile.conf"):
                iprof_text_area = st.empty()
                if st.checkbox(label='Edit file?', key='edit_item_profile'):
                    item_profile_text_area = iprof_text_area.text_area(label='Current file:', value=item_profile_value, height=500, key='item_profile_text_area')
                else:
                    item_profile_text_area = iprof_text_area.text_area(label='Current file:', value=item_profile_value, height=500, disabled=True, key='item_profile_text_area')
            link_item_profile = f'<a href="data:text/plain;base64,{base64.b64encode(item_profile_text_area.encode()).decode()}" download="item_profile.conf">Download</a>'
            st.markdown(link_item_profile, unsafe_allow_html=True)
        # CONTEXT TAB:
        if with_context:
            with tab_context:
                st.header('Contexts')
                schema_type = 'context'
                context_schema_value = util.generate_schema_file(schema_type) 
        # BEHAVIOR TAB:
        with tab_behavior:
            st.header('Behaviors')
            schema_type = 'behavior'
            behavior_schema_value = util.generate_schema_file(schema_type) 
        # RUN TAB:
        with tab_run:                   
            col_run, col_stop = st.columns(2)        
            with col_run:
                button_run = st.button(label='Run', key='button_run')
            with col_stop:
                button_stop = st.button(label='Stop', key='button_stop')        
            generator = RatingImplicit(generation_config=generation_config_value)
            output = st.empty()
            with console.st_log(output.code):
                if not inconsistent:
                    if button_run:
                        if context:
                            steps = 4
                            if side_lars:
                                steps = 5
                        else: 
                            steps = 3
                        current_step = 0
                        print('Starting execution')
                        # Check if all the files required for the synthetic data generation exist.                    
                        # Checking the existence of the file: "user_schema.conf"  
                        progress_text = f'Generating data .....step {current_step + 1} from {steps}'
                        my_bar = st.progress(0, text=progress_text)
                        if user_schema_value:
                            st.write('user.csv')
                            print('Generating user.csv')           
                            user_file_df = generator.generate_user_file(user_schema=user_schema_value)                           
                            st.dataframe(user_file_df)
                            link_user = f'<a href="data:file/csv;base64,{base64.b64encode(user_file_df.to_csv(index=False).encode()).decode()}" download="user.csv">Download user CSV</a>'
                            st.markdown(link_user, unsafe_allow_html=True)              
                        else:
                            st.warning('The user schema file (user_schema.conf) is required.')
                        current_step = current_step + 1
                        if button_stop:
                            st.experimental_rerun()
                        else:
                            # Checking the existence of the file: "item_schema.conf"            
                            my_bar.progress(int(100/steps)*current_step, f'Generating data Step {current_step + 1} from {steps}: ')
                            if item_schema_value:
                                st.write('item.csv')
                                print('Generating item.csv')                    
                                item_file_df = generator.generate_item_file(item_schema=item_schema_value, item_profile=item_profile_value, with_correlation=with_correlation_checkbox)
                                st.dataframe(item_file_df)
                                link_item = f'<a href="data:file/csv;base64,{base64.b64encode(item_file_df.to_csv(index=False).encode()).decode()}" download="item.csv">Download item CSV</a>'
                                st.markdown(link_item, unsafe_allow_html=True)
                                current_step = current_step + 1
                            else:
                                st.warning('The item schema file (item_schema.conf) is required.')
                            my_bar.progress(int(100/steps*current_step), f'Generating data Step {current_step + 1} from {steps}: ')
                            if button_stop:
                                st.experimental_rerun()
                            else:
                                if context:
                                    # Checking the existence of the file: "context_schema.conf"                             
                                    if context_schema_value:
                                        st.write('context.csv')
                                        print('Generating context.csv')                        
                                        context_file_df = generator.generate_context_file(context_schema=context_schema_value)
                                        st.dataframe(context_file_df)
                                        link_context = f'<a href="data:file/csv;base64,{base64.b64encode(context_file_df.to_csv(index=False).encode()).decode()}" download="context.csv">Download context CSV</a>'
                                        st.markdown(link_context, unsafe_allow_html=True)
                                        current_step = current_step + 1
                                    else:
                                        st.warning('The context schema file (context_schema.conf) is required.')
                                # Checking the existence of the file: "generation_config.conf" 
                                my_bar.progress(int(100/steps*current_step), f'Generating data Step {current_step + 1} from {steps}: ')
                                if button_stop:
                                    st.experimental_rerun()
                                else:
                                    if behavior_schema_value:
                                        st.write('behavior.csv')
                                        print('Generating behavior.csv')
                                        behavior_file_df = generator.generate_behavior_file(behavior_schema=behavior_schema_value, item_df=item_file_df, item_schema=item_schema_value)
                                        st.dataframe(behavior_file_df)
                                        link_behavior = f'<a href="data:file/csv;base64,{base64.b64encode(behavior_file_df.to_csv(index=False).encode()).decode()}" download="behavior.csv">Download behavior CSV</a>'
                                        st.markdown(link_behavior, unsafe_allow_html=True)
                                        current_step = current_step + 1
                                        my_bar.progress(int(100/steps*current_step), f'Generating data Step {current_step + 1} from {steps}: ')
                                        if button_stop:
                                            st.experimental_rerun()
                                        else:
                                            if generation_config_value:
                                                st.write('rating.csv')
                                                print('Generating rating.csv')  
                                                print('Generating instances by context.')         
                                                if with_context:
                                                    rating_file_df = generator.generate_rating_file(item_df=item_file_df, behavior_df=behavior_file_df, with_context=with_context, context_df=context_file_df)  
                                                else:
                                                    rating_file_df = generator.generate_rating_file(item_df=item_file_df, behavior_df=behavior_file_df, with_context=with_context, context_df=None)
                                                st.dataframe(rating_file_df)
                                                link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(rating_file_df.to_csv(index=False).encode()).decode()}" download="rating.csv">Download rating CSV</a>'
                                                st.markdown(link_rating, unsafe_allow_html=True)
                                            else:
                                                st.warning('The configuration file (generation_config.conf) is required.')
                                    else:
                                        st.warning('The behavior schema file (behavior_schema.conf) is required.')
                                    print('Synthetic data generation has finished.')   
                                    my_bar.progress(100, 'Synthetic data generation has finished.')    
                else:
                    st.warning('Before generating data ensure all files are correctly generated.')
    