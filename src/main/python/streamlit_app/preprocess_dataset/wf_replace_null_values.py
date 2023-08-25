def generate():
    if with_context:
        file_selectibox = st.selectbox(label='Files available:', options=['item', 'context'])
    else:
        file_selectibox = st.selectbox(label='Files available:', options=['item'])

    # Loading dataset:
    init_step = True
    if file_selectibox == 'item':
        _, df, _, _ = util.load_dataset(file_type_list=['item'])
        schema = util.infer_schema(df)
    elif file_selectibox == 'context':
        _, _, df, _ = util.load_dataset(file_type_list=['context'])
        schema = util.infer_schema(df)
    
    # WF --> Replace NULL values:
    st.header('Apply workflow: Replace NULL values')
    # Help information:
    help_information.help_replace_nulls_wf()
    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='ReplaceNULLValues', init_step="True", with_context="True", optional_value_list=[('NULLValuesC', str(True)), ('NULLValuesI', str(True))])
    tab_replace_null_values = st.tabs(['Replace NULL values'])
    if file_selectibox == 'context':
        workflow_image.show_wf(wf_name='ReplaceNULLValues', init_step="False", with_context=with_context, optional_value_list=[('NULLValuesC', str(True)), ('NULLValuesI', str(False))])
    else:
        workflow_image.show_wf(wf_name='ReplaceNULLValues', init_step="False", with_context=with_context, optional_value_list=[('NULLValuesC', str(False)), ('NULLValuesI', str(True))])
    if not df.empty:
        if st.button(label='Replace NULL Values', key='button_replace_nulls'):
            print('Replacing NULL Values')
            replacenulls = ReplaceNullValues(df)
            if file_selectibox == 'item':
                new_df = replacenulls.regenerate_item_file(schema)
            elif file_selectibox == 'context':
                new_df = replacenulls.regenerate_context_file(schema)
            link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(new_df.to_csv(index=False).encode()).decode()}" download="{file_selectibox}.csv">Download {file_selectibox} CSV</a>'
            st.markdown(link_rating, unsafe_allow_html=True)
    else:
        st.warning("The item file or context file have not been uploaded.")   