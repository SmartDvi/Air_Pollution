import pandas as pd
from geopy.geocoders import Nominatim
import random
import os
import time

df=pd.read_csv('C:\\Users\\Moritus Peters\\Downloads\\air-pollution.csv')

# Initialize geocoder
geolocator = Nominatim(user_agent="geoapiExercises")


# Function to extract or fetch the latitude and longitude for each city
def get_lat_lon(city, country):
    try:
        location = geolocator.geocode(f"{city}, {country}")
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error geocoding {city}, {country}: {e}")
        return None, None

# function to apply rate limiting
def rate_limited_geocode(row, delay=1):
    lat, lon = get_lat_lon(row['City'], row['Country'])
    time.sleep(delay) # sleep to comply with rate limits
    return pd.Series([lat, lon])

# melting the dataset to be analysizable
melted_df =  df.melt(id_vars=['Year'], var_name='Country_City', var_name='PM 2.5')

# spliting the country city column to be seperate columns
melted_df[['City', 'Country']] = melted_df['Country_City'].str.split(', ', expand=True, n=1)

# exploring the dataset only Singapore has a singe  name 
melted_df['Country']=melted_df['Country'].fillna('Singapore')

# categorizing the PM 2.5 level for better analysis
def categorize_pm25(value):
    if value <= 9.0:
        return 'Good'
    elif 9.1 <= value <= 35.4:
        return 'Moderate'
    elif 35.5 <= value <= 55.4:
        return 'Unhealthy for Sensitive Groups'
    elif 55.5 <= value <= 225.4:
        return "Unhealthy"
    elif 150.5 <= value <=225.4:
        return 'Very Unhealthy'
    else:
        return 'Hazardous'

# Apply the categorized PM 2.5 to the melt_df DataFrame
melted_df['AQI_Level'] = melted_df['PM 2.5'].apply(categorize_pm25)

# fetch latitude and longitude for each city with rate limiting
melted_df[['Latitude', 'Longitude']] = melted_df.apply(
    lambda row: rate_limited_geocode(row), axis=1
)

# saving the Dataframe as Csv
melted_df.to_csv('processed_air_quality_data.csv', index=False)