import warnings

import pandas as pd
import streamlit as st

warnings.filterwarnings("ignore")
st.set_option('deprecation.showPyplotGlobalUse', False)


def show_user_map(df):
    """
    Display a map of countries using user data with latitude and longitude coordinates.
    :param df: A DataFrame containing user data, including 'loc' column with location coordinates in the format 'latitude, longitude'.       
    """    
    if not df.empty:
        # Split the 'loc' column into 'latitude' and 'longitude' columns
        df[['latitude', 'longitude']] = df['loc'].str.split(',', expand=True)
        # Convert 'latitude' and 'longitude' columns to numeric (handle non-numeric values)
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')    
        # Remove rows with NaN values in 'latitude' or 'longitude' columns
        df = df.dropna(subset=['latitude', 'longitude'])                          
        with st.expander(label='Show Map'):
            # Check if there are any rows left to plot
            if df.empty:
                st.warning("No valid data for plotting.")
            else: 
                # Create a map in Streamlit            
                data = df.loc[:, ['latitude', 'longitude']]
                st.map(data)
                # Calculate the frequency of values in the "country" column
                country_frequency_df = df['country'].value_counts().reset_index()
                country_frequency_df.columns = ['country', 'frequency']
                st.dataframe(country_frequency_df)
    else:
        st.warning('No data available to display the map.')
