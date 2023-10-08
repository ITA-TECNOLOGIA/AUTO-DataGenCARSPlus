import console
import streamlit as st
from streamlit_app import config, help_information
from streamlit_app.analysis_dataset.evaluation import (st_evaluation_cars_cm,
                                                       st_evaluation_cars_post,
                                                       st_evaluation_cars_pre)
from streamlit_app.preprocess_dataset import wf_util


def generate(rating_df):
    """
    Evaluating Context-Aware Recommendation Systems.
    """
    output = st.empty() 
    with console.st_log(output.code):         
        if not rating_df.empty:
            print('The rating file has been uploaded.')   
            
            # SELECTING PARADIGM TO EVALUATE:
            st.sidebar.markdown("""---""")
            with st.sidebar.expander(label='**CARS paradigm selection**'):
                paradigm = st.selectbox(label="Select one paradigm:", options=config.PARDIGM_OTPIONS)
            print(f'The paradigm ({paradigm}) has been selected.')
            st.header(f'Evaluation of CARS: {paradigm}')                

            # CONTEXTUAL MODELING:
            if paradigm == "Contextual Modeling":                
                help_information.help_contextual_modeling_paradigm()
                st_evaluation_cars_cm.evaluate_cm_paradigm(rating_df)
            # POST-FILTERING:
            elif paradigm == "Post-filtering":            
                help_information.help_postfiltering_paradigm()
                st_evaluation_cars_post.evaluate_postfiltering_paradigm(rating_df)
                # print('The pre-filtering paradigm has been evaluated.')
            # PRE-FILTERING:
            else:
                help_information.help_prefiltering_paradigm()
                st_evaluation_cars_pre.evaluate_prefiltering_paradigm(rating_df)
                # print('The post-filtering paradigm has been evaluated.')        
        else:
            st.warning("The rating file has not been uploaded.")
