import os

import pandas as pd
import streamlit as st
from streamlit_app import config


def generate():
    if 'button_save' not in st.session_state:
        st.session_state['button_save'] = False
    user_database_df = load_user_database() 
    with st.expander("User registration"):                
        st.write("In order to use AUTO-DataGenCARS, it is necessary to provide the following information:")
        email = st.text_input(label=config.EMAIL_LABEL, key='email_textinput')
        organization = st.text_input(label=config.ORGANIZATION_LABEL, key='organization_textinput')
        country = st.selectbox(label=config.COUNTRY_LABEL, options=config.COUNTRY_LIST, key='country_selectbox')
        purpose = st.selectbox(label=config.PURPOSE_LABEL, options=config.PURPOSE_LIST, key='purpose_selectbox')  
        if st.button(label='save', key='save_button'):
            st.session_state['button_save'] = True      
            if email not in user_database_df[config.EMAIL_LABEL].values:
                # Append the new instance to the DataFrame:
                selected_data_dict = {config.EMAIL_LABEL: email, config.ORGANIZATION_LABEL: organization, config.COUNTRY_LABEL: country, config.PURPOSE_LABEL: purpose}
                user_database_df = user_database_df.append(selected_data_dict, ignore_index=True)        
                # Save the selected data to a CSV file:        
                user_database_df.to_csv(config.USER_INFORMATION_LOG_PATH, index=False)
                st.success('User registration has been successfully completed!')
            else:
                st.success("The user is already registered.")

def load_user_database():
     # Check if the CSV file exists:
    if os.path.exists(config.USER_INFORMATION_LOG_PATH):
        # Load the existing DataFrame from the file
        user_information_log_df = pd.read_csv(config.USER_INFORMATION_LOG_PATH)
    else:
        # Create an empty DataFrame if the file doesn't exist
        user_information_log_df = pd.DataFrame(columns=[config.EMAIL_LABEL, config.ORGANIZATION_LABEL, config.COUNTRY_LABEL, config.PURPOSE_LABEL])
    return user_information_log_df
