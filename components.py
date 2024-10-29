import dash_mantine_components as dmc
from dash import register_page, html, Input, Output, Dash, dcc, callback
import pandas as pd
import dash_ag_grid as dag
import dash_daq as daq
import plotly.express as px

from utils import categorize_pm25, aqi_data

from utils import merged_df

Average_trnd = merged_df['PM2.5'].sum()


# Calculate average PM2.5
Average_trnd = merged_df['PM2.5'].mean()

# Function to get color based on PM2.5 levels
def get_color_by_pm25_level(pm_value):
    if pm_value <= 12.0:
        return 'green'
    elif 12.1 <= pm_value <= 35.4:
        return 'yellow'
    elif 35.5 <= pm_value <= 55.4:
        return 'orange'
    elif 55.5 <= pm_value <= 150.4:
        return 'red'
    elif 150.5 <= pm_value <= 250.4:
        return 'purple'
    else:
        return 'brown'
    
merged_df['Colors'] = merged_df['PM2.5'].apply(get_color_by_pm25_level)

# Dropdown for year selection
yr_dropdown = dmc.Select(
    id="year-dropdown",
    label='Select Year',
    data=[{'label': year, 'value': year} for year in merged_df['Year'].unique()],
    value='2021'
)

# Dropdown for country selection
country_dropdown = dmc.Select(
    id="country-dropdown",
    label='Select Country',
    data=[{'label': country, 'value': country} for country in merged_df['Country'].unique()],
    value=merged_df['Country'][0]
)

# PM2.5 Gauge indicator
pm_indicator = daq.Gauge(
    id='indicator',
    color={
        'gradient': False,
        'ranges': {
            "green": [0, 12],
            "yellow": [12.1, 35.4],
            "orange": [35.5, 55.4],
            "red": [55.5, 150.4],
            "purple": [150.5, 250.4],
            "brown": [250.5, 500],
            get_color_by_pm25_level(Average_trnd): [Average_trnd, Average_trnd],  
        }
    },
    min=0,  
    max=500,  
    showCurrentValue=True,
    units="PM2.5",
    value=Average_trnd,  
    size=150,  
    label="PM2.5 Indicator",  
    scale={'start': 0, 'interval': 25}
)

# Scatter chart for PM2.5 data
def create_pm25_fig():
    yearly_data = merged_df.groupby("City")["PM2.5"].mean().reset_index()
    
    # Dynamic color based on PM2.5 levels
    series_data = [
        {
            "name": "PM2.5",
            "data": yearly_data.to_dict("records"),
            "color": get_color_by_pm25_level(yearly_data.iloc[i]["PM2.5"]),
        }
        for i in range(len(yearly_data))
    ]
    return dmc.BarChart(
        id='pm_scatter',
        orientation="vertical",
        unit='pm2.5',
        data=yearly_data.to_dict('records'),
        dataKey='City',
        series=series_data,
        xAxisLabel="City",
        yAxisLabel="PM2.5",
        withTooltip=True,
        withXAxis={'type': 'category', 'label': {'display': True, 'text': "Year"}, 'tickInterval': 1},
        legendProps={'verticalAlign': 'top', 'height': 50},
        withLegend=True,
        h=250
    )


color_map = {
        'Good': 'green',
        'Hazardous': 'red',
        'Moderate': 'yellow',
        'Unhealthy': 'orange',
        'Unhealthy for Sensitive Groups': 'purple',
        'Others': 'gray'
    }




def create_aqi_tab(aqi_level, data):
    # Filter the data for the selected AQI level
    data = merged_df[merged_df['AQI_Level'] == aqi_level]

    # Prepare data for the BarChart
    data_for_chart = data.groupby('City')['PM2.5'].sum().reset_index()

    # Get top 10 and bottom 10 PM2.5 values by City
    top_10 = data_for_chart.nlargest(10, 'PM2.5')
    least_10 = data_for_chart.nsmallest(10, 'PM2.5')


    comb = pd.concat([top_10, least_10])


    # Define the series for the BarChart
    series_data = [
        {
            "name": "PM2.5",
            "data": comb['PM2.5'].tolist(), 
            "color": "blue",  
        }
    ]

    # Create and return the BarChart
    return dmc.BarChart(
        id='aqi_tab',
        h=180,
        dataKey="City", 
        data=comb.to_dict('records'),
        orientation="vertical",
        yAxisProps={"width": 80},
        series=series_data  
    )



def tabs(year):
    return dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.TabsTab('Gd', value='Good'),
                    dmc.TabsTab('ME', value='Moderate'),
                    dmc.TabsTab('Unhy', value='Unhealthy'),
                    dmc.TabsTab('UfG', value='Unhealthy for Sensitive Groups'),
                    dmc.TabsTab('Hds', value='Hazardous')
                ], grow =True
            ),
            
            dmc.TabsPanel(create_aqi_tab('Good', year), value='Good'),
            dmc.TabsPanel(create_aqi_tab('Moderate', year), value='Moderate'),
            dmc.TabsPanel(create_aqi_tab('Unhealthy', year), value='Unhealthy'),
            dmc.TabsPanel(create_aqi_tab('Unhealthy for Sensitive Groups', year), value='Unhealthy for Sensitive Groups'),
            dmc.TabsPanel(create_aqi_tab('Hazardous', year), value='Hazardous'),
                
            
        ],
        value='Good',
        id='return_tabs'
        
    )

