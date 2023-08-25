def generate():
    # Loading dataset:
    init_step = 'True'
    _, _, _, rating_df = util.load_dataset(file_type_list=['rating'])

    # WF --> Ratings to binary:
    st.header('Apply workflow: Ratings to binary')
    # Help information:
    help_information.help_ratings_to_binary_wf()        
    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='RatingsToBinary', init_step=init_step)

    if not rating_df.empty:            
        min_rating = rating_df['rating'].min()
        max_rating = rating_df['rating'].max()
        threshold = st.number_input(f"Binary threshold (range from {min_rating} to {max_rating})", value=3)
        df_binary = util.ratings_to_binary(rating_df, threshold)
        st.write("Converted ratings:")
        st.dataframe(df_binary.head())
        link_rating = f'<a href="data:file/csv;base64,{base64.b64encode(df_binary.to_csv(index=False).encode()).decode()}" download="rating.csv">Download rating CSV</a>'
        st.markdown(link_rating, unsafe_allow_html=True)
    else:            
        st.warning("The rating file has not been uploaded.")