def generate():
    # Loading dataset:
    file_selectibox = st.selectbox(label='Files available:', options=['user', 'item', 'context'])        
    file = 'F'
    num2cat = 'T'
    init_step = 'True'
    if file_selectibox == 'user':
        df, _, _, _ = util.load_dataset(file_type_list=['user'])
        file = 'U'
    elif file_selectibox == 'item':
        _, df, _, _ = util.load_dataset(file_type_list=['item'])
        file = 'I'
    elif file_selectibox == 'context':
        _, _, df, _ = util.load_dataset(file_type_list=['context'])   
        file = 'C'

    # WF --> Mapping categorization:
    st.header('Workflow: Mapping categorization')
    # Help information:
    help_information.help_mapping_categorization_wf()
    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='MappingCategorization', init_step=init_step, with_context=True, optional_value_list=[('Num2Cat', num2cat), ('file', file)])
        
    option = st.radio(options=['From numerical to categorical', 'From categorical to numerical'], label='Select an option')
    if not df.empty:
        if option == 'From numerical to categorical':
            # Showing the image of the WF:
            init_step = 'False'
            num2cat = 'True'
            workflow_image.show_wf(wf_name='MappingCategorization', init_step=init_step, with_context=with_context, optional_value_list=[('Num2Cat', num2cat), ('file', file)])                
            st.header("Category Encoding")
            # Help information:
            help_information.help_mapping_categorization_num2cat() 

            include_nan = st.checkbox("Include NaN values")
            mappings = {}
            for col in df.columns:
                with st.expander(col):
                    if 'id' not in col.lower() and not pd.api.types.is_datetime64_dtype(df[col]) and not pd.api.types.is_object_dtype(df[col]): # Ignore ID, object and datetime columns
                        unique_values = sorted(df[col].unique())
                        st.write(f"Unique values: {', '.join(map(str, unique_values))}")
                        col_mappings = {}
                        for val in unique_values:
                            if not include_nan and pd.isna(val):
                                col_mappings[val] = np.nan
                                continue
                            else:
                                mapping = st.text_input(f"Mapping for {val}", "", key=f"{col}_{val}")                                    
                                if mapping:
                                    col_mappings[val] = mapping
                                else:
                                    col_mappings[val] = val                                
                        st.write(col_mappings)
                        mappings[col] = col_mappings                
            if st.button("Generate mapping"):
                categorized_df = mapping_categorization.apply_mappings(df, mappings)
                st.header("Categorized dataset:")
                st.dataframe(categorized_df)
                link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(categorized_df.to_csv(index=False).encode()).decode()}" download="{file_selectibox}.csv">Download</a>'
                st.markdown(link_rating, unsafe_allow_html=True)
        else:
            # Showing the image of the WF:
            num2cat = 'False'
            init_step = 'False'
            workflow_image.show_wf(wf_name='MappingCategorization', init_step=init_step, with_context=with_context, optional_value_list=[('Num2Cat', num2cat), ('file', file)])
            
            st.header("Label Encoding")
            # Help information:
            help_information.help_mapping_categorization_cat2num()
                            
            categorical_cols = [col for col in df.select_dtypes(exclude=[np.number]) if 'id' not in col.lower()]
            if categorical_cols:
                selected_cols = st.multiselect("Select categorical columns to label encode:", categorical_cols)
                if selected_cols:
                    if st.button("Encode categorical columns"):
                        encoded_df = label_encoding.apply_label_encoder(df, selected_cols)
                        st.header("Encoded dataset:")
                        st.write(encoded_df)
                        link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(encoded_df.to_csv(index=False).encode()).decode()}" download="{file_selectibox}.csv">Download</a>'
                        st.markdown(link_rating, unsafe_allow_html=True)
            else:
                st.write("No categorical columns found.")
    else:
        st.warning("The user, item or context file has not been uploaded.")