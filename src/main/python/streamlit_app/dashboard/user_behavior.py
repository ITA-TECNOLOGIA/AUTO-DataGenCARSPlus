import warnings

import streamlit as st
from geopy.geocoders import Nominatim

warnings.filterwarnings("ignore")
st.set_option('deprecation.showPyplotGlobalUse', False)


def show_user_map(df):    
    # Inicializar el geocodificador de Nominatim
    geolocator = Nominatim(user_agent="MyGeo")
    
    def geocode_country(country):
        """
        Función para geocodificar un país y obtener sus coordenadas
        """
        try:
            location = geolocator.geocode(country)
            if location:
                return location.latitude, location.longitude
            else:
                return None, None
        except Exception as e:
            return None, None

    # Aplicar la función para obtener las coordenadas de cada país en la columna "Country"
    df['latitude'], df['longitude'] = zip(*df['Country'].apply(geocode_country))        
    # Crear un mapa en Streamlit
    st.header('Map of countries using AUTO-DataGenCARS')
    data = df.loc[:, ['latitude', 'longitude']]        
    st.map(data)  

    with st.expander(label='Show details'):
        # Calculate the frequency of values in the "country" column
        country_frequency_df = df['Country'].value_counts().reset_index()
        country_frequency_df.columns = ['Country', 'Frequency']
        st.dataframe(country_frequency_df)
