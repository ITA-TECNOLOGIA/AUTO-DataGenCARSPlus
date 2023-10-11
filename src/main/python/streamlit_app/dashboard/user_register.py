import os

import pandas as pd
import requests
from streamlit_app import config
from streamlit_javascript import st_javascript


def generate_implicit():
    """    
    Loads a user database, checks if the user's IP address is already in the database, 
    and appends information about the user's location to the database if it's not present. 
    It then saves the updated user database to a CSV file.
    """
    user_database_df = load_user_database()
    user_ip = get_user_ip()
    if user_ip not in user_database_df[config.IP_LABEL].values:
        country, city, region, loc, timezone = get_country_from_ip(user_ip)        
        # Append the new instance to the DataFrame:
        selected_data_dict = {config.IP_LABEL: user_ip, config.COUNTRY_LABEL: country, config.CITY_LABEL: city, config.REGION_LABEL: region, config.LOC_LABEL: loc, config.TIMEZONE_LABEL: timezone}
        user_database_df = user_database_df.append(selected_data_dict, ignore_index=True)        
        # Save the selected data to a CSV file:
        user_database_df.to_csv(config.USER_INFORMATION_LOG_PATH, index=False)

def get_user_ip():
    """
    Retrieve the user's IP address using an external API.
    This function sends an HTTP request to 'https://api.ipify.org?format=json' to obtain the user's IP address.
    The IP address is extracted from the API response and returned.
    :return: The user's IP address if it is successfully obtained, or None if there's an error.
    """
    url = 'https://api.ipify.org?format=json'
    script = (f'await fetch("{url}").then('
                'function(response) {'
                    'return response.json();'
                '})')

    try:
        result = st_javascript(script)
        if isinstance(result, dict) and 'ip' in result:
            return result['ip']
    except:
        pass

def get_country_from_ip(user_ip):
    """
    Retrieve location information (country, city, region, coordinates, and timezone)
    based on the user's IP address using an IP geolocation API.
    This function makes an HTTP request to the 'ipinfo.io' API to obtain location information
    for the given user's IP address. It extracts and returns the country, city, region,
    coordinates (latitude and longitude), and timezone information as strings. If any of
    this information is not available, it defaults to 'N/A' (Not Available).    
    :param user_ip: The IP address for which location information is to be retrieved.
    :return: A tuple containing the following location information: Country, City, Region/State, 
    Coordinates (latitude and longitude), Timezone.
    """
    country=city=region=loc=timezone = None    
    try:
        response = requests.get(f"https://ipinfo.io/{user_ip}/json")
        data = response.json()
        country = data.get("country", None)
        city = data.get("city", None)
        region = data.get("region", None)
        loc = data.get("loc", None)
        timezone = data.get("timezone", None)        
    except Exception as e:
        print(f"Error: {e}")        
    return country, city, region, loc, timezone

def load_user_database():
    """
    Load or create a user information database stored in a CSV file.
    This function checks if the specified CSV file (defined in the 'config' module) exists.
    If the file exists, it loads the data into a Pandas DataFrame. If the file does not
    exist, it creates an empty DataFrame with predefined columns for storing user
    information, such as IP addresses, countries, cities, regions, coordinates, and timezones.
    :return: A DataFrame containing user information, loaded from the CSV file
    if it exists, or an empty DataFrame with predefined columns if the file does not exist.    
    """
     # Check if the CSV file exists:
    if os.path.exists(config.USER_INFORMATION_LOG_PATH):
        # Load the existing DataFrame from the file:
        user_information_log_df = pd.read_csv(config.USER_INFORMATION_LOG_PATH)
    else:
        # Create an empty DataFrame if the file doesn't exist:
        user_information_log_df = pd.DataFrame(columns=[config.IP_LABEL, config.COUNTRY_LABEL, config.CITY_LABEL, config.REGION_LABEL, config.LOC_LABEL, config.TIMEZONE_LABEL])
    return user_information_log_df
