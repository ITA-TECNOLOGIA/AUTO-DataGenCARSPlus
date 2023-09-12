import streamlit as st
import pandas as pd
from streamlit_app import config
from streamlit_app.analysis_dataset.evaluation import st_evaluation_rs


def evaluate_postfiltering_paradigm(rating_df):
    """
    Evaluates the post-filtering paradigm.
    :param rating_df: The rating dataframe.    
    """     
    # Step 1: Builds a new dataset that ignores the contextual information of the CARS dataset (like a 2D database: problem of traditional RS).
    rs_rating_df = build_knowledge_base(rating_df)

    # Step 2: Evaluate a traditional RS.
    st_evaluation_rs.generate(rating_df=rs_rating_df)
    
    # Step 3: The resulting set of recommendations is adjusted (contextualized) for each user by using contextual information.
    # TODO

def build_knowledge_base(rating_df):
    """    
    Builds a 2D dataset where the contextual information of the CARS dataset (rating_df) is initially ignored and 
    the ratings are predicted using any conventional 2D recommendation system, taking all the potential items to 
    recommend into account.
    :param rating_df: The rating dataframe.
    :return: A 2D dataframe (traditional RS).
    """    
    # Loading item and context files:
    st.markdown("""---""")
    st.header('Ignore the context dimension')
    # Reducing the dimensions of the CARS dataset:
    rs_rating_df = pd.DataFrame()
    if not rating_df.empty:        
        if 'context_id' not in rating_df.columns:
            st.error(f'The uploaded {config.RATING_TYPE} file must contain contextual information (context_id).')
        else:
            rs_rating_df = rating_df.drop(f'{config.CONTEXT_TYPE}_id', axis=1)
            rs_rating_df = rs_rating_df.drop_duplicates()
            print(f'The {config.RATING_TYPE} file (CARS) has been reduced to 2D (traditional RS).')   
        # Showing the knowledge base built:
        with st.expander(label='Show the 2D dataset built'):
            st.dataframe(rs_rating_df)
    else:
        st.warning(f'The {config.RATING_TYPE} file has not been uploaded.')
    return rs_rating_df
