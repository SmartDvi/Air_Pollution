import dash_mantine_components as dmc
from dash import register_page, html, Input, Output, Dash, dcc, callback
import pandas as pd
import dash_ag_grid as dag
import dash_daq as daq
import plotly.express as px

from utils import categorize_pm25, aqi_data

from utils import merged_df

Average_trnd = merged_df['PM2.5'].mean()


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
# PM2.5 Gauge indicator with dynamic color
# PM2.5 Gauge indicator with both static and dynamic ranges
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
            get_color_by_pm25_level(Average_trnd): [Average_trnd, Average_trnd],  # Highlight current PM2.5 level
        }
    },
    min=0,  
    max=500,  # Ensure max is high enough to show the full range
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
        data=merged_df.to_dict('records'),
        dataKey={'x': 'City', 'y': 'PM2.5'},
        series=series_data,
        xAxisLabel="City",
        yAxisLabel="PM2.5",
        withTooltip=True,
        withXAxis={'type': 'category', 'label': {'display': True, 'text': "Year"}, 'tickInterval': 1},
        legendProps={'verticalAlign': 'top', 'height': 50},
        withLegend=True,
        h=250
    )

# Line chart for yearly PM2.5 trend
def yr_trend():
    yearly_data = merged_df.groupby("Year")["PM2.5"].mean().reset_index()
    
    # Dynamic color based on PM2.5 levels
    series_data = [
        {
            "name": "PM2.5",
            "data": yearly_data.to_dict("records"),
            "color": get_color_by_pm25_level(yearly_data.iloc[i]["PM2.5"]),
        }
        for i in range(len(yearly_data))
    ]

    return dmc.LineChart(
        id='yr_trend',
        h=150,
        data=yearly_data.to_dict('records'),
        dataKey={'x': 'Year', 'y': 'PM2.5'},
        tooltipAnimationDuration=10,
        referenceLines=[{'y': Average_trnd, 'label': 'Average PM2.5', 'color': 'blue'}],
        series=series_data,
        xAxisLabel="Year",
        yAxisLabel="PM2.5",
        withDots=True,
        withTooltip=True,
        withXAxis={'type': 'category', 'label': {'display': True, 'text': "Year"}, 'tickInterval': 1}
    )

# Mapbox scatter plot for AQI levels
def mapbox():
    return px.scatter_mapbox(
        merged_df,
        lat='Latitude', 
        lon='Longitude',
        color=get_color_by_pm25_level,
        size='PM2.5', 
        hover_name='City',
        zoom=0.08,
        hover_data={'Latitude': False, 'Longitude': False, 'PM2.5_Pct_Change': True, 'Yearly_Avg_PM2.5': True},
        mapbox_style='open-street-map'
    )
def create_aqi_tabs():
    tabs = ['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous']
    tab_contents = {tab: PM_level(tab) for tab in tabs}


def filter_data_by_aqi_level(level):
    for level in merged_df['AQI_Level']:
        if level == 'Good':
            return create_aqi_tabs

color_map = {
        'Good': 'green',
        'Hazardous': 'red',
        'Moderate': 'yellow',
        'Unhealthy': 'orange',
        'Unhealthy for Sensitive Groups': 'purple',
        'Others': 'gray'
    }



def PM_level(tabs):


    for i in merged_df['PM2.5'] <= 12:
        if tabs == "1":
            return dmc.BarChart(
                 id='pm_scatter',
                orientation="vertical",
                unit='pm2.5',
                data=merged_df.to_dict('records'),
                dataKey={'x': 'City', 'y': 'PM2.5'},
                xAxisLabel="City",
                yAxisLabel="PM2.5",
                withTooltip=True,
                withXAxis={'type': 'category', 'label': {'display': True, 'text': "Year"}, 'tickInterval': 1},
                legendProps={'verticalAlign': 'top', 'height': 50},
                withLegend=True,
                h=250
            )
        
# Function to create donut chart with a label
def create_donut_chart_with_label(aqi_level):
     # Calculate total PM2.5 from the dataset (sum of all AQI level values)
    total_pm25 = sum(aqi_data[level]['value'] for level in aqi_data)
    
    # Get the specific AQI level's value
    aqi_value = aqi_data[aqi_level]['value']
    
    # Calculate the percentage of this AQI level relative to total PM2.5
    percentage_value = (aqi_value / total_pm25) * 100
    data = [
        {'name': aqi_level, 'value': aqi_data[aqi_level]['value'], 'color':  color_map[aqi_level]},
        {'name': 'Others', 'value': aqi_data[aqi_level]['others'], 'color': 'gray'}
    ]
    
  
    return html.Div(
        [
             html.Div(
                aqi_level,  # Chart label below the donut char
                style={"textAlign": "center","fontWeight": "bold"}
            ),
            dmc.DonutChart(
                id='pm_gauge',
                data=data,
                size=123,
                thickness=18,
                withTooltip=True,
                mx='auto',
                chartLabel=f"{percentage_value:.1f}%",
                startAngle=180,
                endAngle=0
            ),
           
        ]
    )

# Group of Donut Charts for different AQI levels
def donut_charts_group():
    return dmc.Group(
        [
            
            create_donut_chart_with_label('Good'),
            create_donut_chart_with_label('Hazardous'),
            create_donut_chart_with_label('Moderate'),
            create_donut_chart_with_label('Unhealthy'),
            create_donut_chart_with_label('Unhealthy for Sensitive Groups')
        ],
        justify="center",
        gap=10,
        grow=True
    )


def create_aqi_tab(aqi_level):
    # Filter the data for the selected AQI level
    filtered_data = merged_df[merged_df['AQI_Level'] == aqi_level]

    # Prepare data for the BarChart
    data_for_chart = filtered_data.groupby('City')['PM2.5'].sum().reset_index()

    # Convert the DataFrame to a JSON-serializable format
    data_for_chart_dict = data_for_chart.to_dict(orient='records')  # Use 'records' to convert to a list of dictionaries
    
    # Define the series for the BarChart
    series_data = [
        {
            "name": "PM2.5 Levels",
            "data": data_for_chart['PM2.5'].tolist(),  # PM2.5 values
            "color": "blue",  # Color of the bars
        }
    ]

    # Create and return the BarChart
    return dmc.BarChart(
        h=250,
        dataKey="City",  # Use 'City' to align with your data
        data=data_for_chart_dict,  
        orientation="vertical",
        yAxisProps={"width": 80},
        series=series_data  # Pass the series data
    )



def tabs():
    return dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.TabsTab('Gd', value='Good'),
                    dmc.TabsTab('ME', value='Moderate'),
                    dmc.TabsTab('Unhy', value='Unhealthy'),
                    dmc.TabsTab('UfG', value='Unhealthy for Sensitive Groups'),
                    dmc.TabsTab('Hds', value='Hazardous')
                ]
            ),
            
            dmc.TabsPanel(create_aqi_tab('Good'), value='Good'),
            dmc.TabsPanel(create_aqi_tab('Moderate'), value='Moderate'),
            dmc.TabsPanel(create_aqi_tab('Unhealthy'), value='Unhealthy'),
            dmc.TabsPanel(create_aqi_tab('Unhealthy for Sensitive Groups'), value='Unhealthy for Sensitive Groups'),
            dmc.TabsPanel(create_aqi_tab('Hazardous'), value='Hazardous'),
                
            
        ],
        value=merged_df['PM2.5'],
    )

