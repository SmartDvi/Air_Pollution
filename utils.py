import pandas as pd
from geopy.geocoders import Nominatim
import random
import os
import time

def load_data():
    df = pd.read_csv('C:\\Users\\Moritus Peters\\Downloads\\air-pollution.csv')
    df1 = pd.read_csv('C:\\Users\\Moritus Peters\\Downloads\\air-poplution-extraction-data.csv')
    #df = pd.read_csv('https://raw.githubusercontent.com/SmartDvi/Air_Pollution/main/air-pollution.csv')
    #df1 = pd.read_csv('https://raw.githubusercontent.com/SmartDvi/Air_Pollution/main/air-poplution-extraction-data.csv')
    
    df_melted = df.melt(id_vars=['Year'], var_name='City', value_name='PM2.5')
    df_melted[['City', 'Country']] = df_melted['City'].str.split(', ', expand=True, n=1)
    df_melted['Country'] = df_melted['Country'].fillna('Singapore')
    
    # Categorize PM2.5 values
    df_melted['AQI_Level'] = df_melted['PM2.5'].apply(categorize_pm25)

    # Merge the two datasets
    merged_df = pd.merge(df_melted, df1, on='City', how='left')

    # Calculate yearly averages and anomalies
    yearly_avg = merged_df.groupby('Year')['PM2.5'].mean().reset_index()
    yearly_avg.columns = ['Year', 'Yearly_Avg_PM2.5']
    merged_df = merged_df.merge(yearly_avg, on='Year', how='left')
    merged_df['PM2.5_Anomaly'] = merged_df['PM2.5'] - merged_df['Yearly_Avg_PM2.5']
    
    # Calculate percentage change in PM2.5
    merged_df.sort_values(by=['City', 'Year'], inplace=True)
    merged_df['PM2.5_Pct_Change'] = merged_df.groupby('City')['PM2.5'].pct_change() * 100

    # Convert Year to string for dropdown use
    merged_df['Year'] = merged_df['Year'].astype(str)

    return merged_df

def categorize_pm25(value):
    if value <= 9.0:
        return "Good"
    elif 9.1 <= value <= 35.4:
        return "Moderate"
    elif 35.5 <= value <= 55.4:
        return "Unhealthy for Sensitive Groups"
    elif 55.5 <= value <= 150.4:
        return "Unhealthy"
    elif 150.5 <= value <= 225.4:
        return "Very Unhealthy"
    else:
        return "Hazardous"

def group_aqi_level(aqi_level, specific_level):
    """
    Function to group AQI levels into specific categories or 'Others'
    """
    if aqi_level == specific_level:
        return specific_level
    else:
        return 'Others'

def prepare_aqi_data(merged_df):
    """
    Grouping the AQI level data for a donuts chart
    """
    aqi_levels = ['Good', 'Moderate', 'Unhealthy', 'Unhealthy for Sensitive Groups', 'Hazardous']
    aqi_data = {}

    for level in aqi_levels:
        merged_df['group_AQI'] = merged_df['AQI_Level'].apply(lambda x: group_aqi_level(x, level))
        group_data = merged_df.groupby('group_AQI')['PM2.5'].sum().reset_index()

        # Fetch the value for the specific AQI level and 'Others'
        specific_value = group_data.loc[group_data['group_AQI'] == level, 'PM2.5'].values
        others_value = group_data.loc[group_data['group_AQI'] == 'Others', 'PM2.5'].sum()

        aqi_data[level] = {
            'value': specific_value[0] if len(specific_value) > 0 else 0,
            'others': others_value
        }

    return aqi_data

# Load the data and prepare AQI data
merged_df = load_data()
aqi_data = prepare_aqi_data(merged_df)

# Output a summary of AQI data (for debugging)
aqi_data


