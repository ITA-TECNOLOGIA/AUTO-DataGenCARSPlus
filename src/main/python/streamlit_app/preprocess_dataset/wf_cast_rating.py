import console
import pandas as pd
import streamlit as st
from datagencars.existing_dataset.cast_rating.cast_rating import CastRating
from streamlit_app import config, help_information
from streamlit_app.preprocess_dataset import wf_util
from streamlit_app.workflow_graph import workflow_image


def generate():
    """
    Processes and converts different types of ratings (binary or preferencial) in a DataFrame.
    :return: The modified rating DataFrame after the Cast Ratings workflow.
    """
    # WF --> Cast Ratings:
    st.header('Workflow: Cast Ratings')
    # Help information:
    help_information.help_cast_rating_wf()
    # Showing the initial image of the WF:
    workflow_image.show_wf(wf_name='CastRating', init_step=True)

    # Loading dataset:
    st.write('Upload the following files: ')    
    __, __, __, rating_df, __ = wf_util.load_dataset(file_type_list=['rating'], wf_type='wf_rating_to_binary')
    st.markdown("""---""")

    # Transforming ratings to binary values:
    output = st.empty() 
    new_rating_df = pd.DataFrame()  
    with console.st_log(output.code):   
        if not rating_df.empty:
            generator = CastRating(rating_df=rating_df)
            if generator.is_binary_rating():  
                print('The dataset has rating values of binary type (0 or 1).')
                scale = st.number_input("Enter the maximum value of the rating.", value=5)
                threshold_binary = st.number_input(f"Binary threshold (range from 1 to {scale})", value=3)
                print('Casting the rating value in the rating.csv file.')
                new_rating_df = generator.rating_binary_to_preferencial(scale, threshold=threshold_binary)
                print('The casting process has finished.')
                with st.expander(label=f'Show the modified rating file: {config.RATING_TYPE}.csv'):                
                    # Showing the replicated rating file:
                    st.dataframe(new_rating_df)    
                    # Saving the replicated rating file:
                    wf_util.save_df(df_name='rating', df_value=new_rating_df, extension='csv') 
            elif generator.is_preferencial_rating():
                min_rating = rating_df['rating'].min()
                max_rating = rating_df['rating'].max()
                print(f'The dataset has rating values of preferencial type in the range [{min_rating}, {max_rating}].')
                threshold_preferencial = st.number_input(f"Binary threshold (range from {min_rating} to {max_rating})", value=3)
                print('Casting the rating value in the rating.csv file.')
                new_rating_df = generator.rating_preferencial_to_binary(threshold=threshold_preferencial)
                print('The casting process has finished.')
                if st.checkbox(label="Do you want to change the vote label (e.g. 1 to 'like' and 0 to 'dislike')?", value=False, key='binary_set_rating_label'):
                    label_1 = st.text_input(label='Enter a label for the rating value 1:', value='like', key='text_input_label_1')
                    label_0 = st.text_input(label='Enter a label for the rating value 0:', value='dislike', key='text_input_label_0')
                    print(f'Changing the binary numeric rating value to a string label: 1 to {label_1} and 0 to {label_0}.')
                    new_rating_df = generator.set_binary_rating_label(label_1, label_0)
                    print('The rating value has been changed to a label.')
                with st.expander(label=f'Show the modified rating file: {config.RATING_TYPE}.csv'):                
                    # Showing the replicated rating file:
                    st.dataframe(new_rating_df)    
                    # Saving the replicated rating file:
                    wf_util.save_df(df_name='rating', df_value=new_rating_df, extension='csv')            
        else:            
            st.warning("The rating file has not been uploaded.")
    return new_rating_df
       