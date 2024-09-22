import dash_bootstrap_components as dbc
import pandas as pd 
import dash
from dash import dcc, html, State, Input, Output

#df = pd.read_csv('https://raw.githubusercontent.com/SmartDvi/Air_Pollution/main/air-pollution.csv')
#df1 = pd.read_csv('https://raw.githubusercontent.com/SmartDvi/Air_Pollution/main/air-poplution-extraction-data.csv')
df=pd.read_csv('C:\\Users\\Moritus Peters\\Downloads\\air-pollution.csv')

df1 = pd.read_csv('C:\\Users\\Moritus Peters\\Downloads\\air-poplution-extraction-data.csv')

df_melted = df.melt(id_vars=['Year'], var_name='City', value_name='PM2.5')

# Handle cases where the 'City' column may not have a valid 'City, Country' format
df_melted[['City', 'Country']] = df_melted['City'].str.split(', ', expand=True, n=1)

# Fill missing values in 'Country' with an empty string or a placeholder if necessary
df_melted['Country'] = df_melted['Country'].fillna('Singapore')

# Define the categorize_pm25 function
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

# Apply the categorize_pm25 function to the 'PM2.5' column and create a new 'AQI_Level' column
df_melted['AQI_Level'] = df_melted['PM2.5'].apply(categorize_pm25)

# merged the both datast to get a processed dataframe
merged_df = pd.merge(df_melted, df1, on='City', how='left')

yearly_avg = merged_df.groupby('Year')['PM2.5'].mean().reset_index()
yearly_avg.columns = ['Year', 'Yearly_Avg_PM2.5']

# Merge the yearly average into the main DataFrame
merged_df = merged_df.merge(yearly_avg, on='Year', how='left')

# Calculate the anomaly as the difference from the yearly average
merged_df['PM2.5_Anomaly'] = merged_df['PM2.5'] - merged_df['Yearly_Avg_PM2.5']

# Calculate the percentage change in PM2.5 year-over-year
merged_df.sort_values(by=['City', 'Year'], inplace=True)  # Ensure data is sorted
merged_df['PM2.5_Pct_Change'] = merged_df.groupby('City')['PM2.5'].pct_change() * 100

# converting the year column to string to be used for the dropdown
merged_df['Year'] = merged_df['Year'].astype(str)


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        html








    ]
)





if __name__ =="__main__":
    app.run(debug=True, port=6030)