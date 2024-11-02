import dash
import dash_mantine_components as dmc
import pandas as pd
import dash_ag_grid as dag
from dash import html, dcc, Input, Output, State, register_page
import dash_bootstrap_components as dbc



register_page(__name__,
path='/',
title='Introducto and Dataset Details',
description= 'Belief Intoduction to the project and Dateset details',
order=0)

from utils import merged_df


task = """

### Project Task
Air quality around the globe has gone through significant ups and downs since the Industrial Revolution. Many factors affect the air that we breath such as the usage of coal power plants, clean air legislation, and automobile congestion.

`Week 36 of Figure-Friday` will dive into this topic with data 5 from the Air Quality Stripes project, which shows the concentration of particulate matter air pollution (PM2.5) in cities around the world.

##### Things to consider:
    - can you replicate the sample graph with Plotly?
    - can you improve the sample graph built?
    - would a different figure tell the data story better?
    - are you able to replicate or improve the app 3 built by the Air Quality Stripes project?

[data Source](https://github.com/plotly/Figure-Friday/tree/main/2024/week-36)

    """


introduction = """
### Overview
This application is designed to provide comprehensive insights into Global air quality by analyzing PM2.5 (particulate matter with a diameter of less than 2.5 microns) levels across various cities and countries over multiple years. PM2.5 is a critical air pollutant that affects public health, and understanding its distribution and trends is essential for making informed decisions regarding environmental policies, public safety, and health regulations.

#### Key Features:
1. **Year and Country Selection**: Use the dropdowns to select specific years and countries, allowing for a focused view of air quality data in different regions.
2. **PM2.5 Gauge Indicator**: The dashboard features a real-time gauge that reflects the average PM2.5 concentration for the selected year, helping to quickly assess air quality levels.
3. **PM2.5 Scatter Chart**: Visualizes the PM2.5 concentrations across cities, allowing for city-to-city comparison in a given year.
4. **Yearly Trend Analysis**: The line chart tracks PM2.5 levels over time, with colors that change dynamically based on air quality levels. The average trend line gives a quick snapshot of whether air quality is improving or worsening.
5. **Mapbox Integration**: This feature allows for geographical visualization of PM2.5 levels and AQI categories across different cities. Users can see the spatial distribution of air quality, with city markers varying in size based on PM2.5 concentrations.

This dashboard combines visual data exploration with interactive components, making it an essential tool for environmental scientists, policymakers, and the public to monitor air quality trends, identify high-risk areas, and track progress toward cleaner air.




"""


date_obj = "d3.timeParse('%Y')(params.merged_df.Year)"

columnDefs=[
    {'field': 'City', 'headerName': 'City'},
    {'field': 'Country', 'headerName': 'Country'},
    {
        'field': 'PM2.5', 
        'headerName': 'PM2.5',
        'valueFormatter': {"function": "d3.format('.2f')(params.value)"}, 
        'type': 'rightAligned',
       
    },
    {
        'field': 'Year',
        'headerName': 'Year',
        
        "valueFormatter": {"function": "d3.format('')(params.value)"},  # Format to two decimal places
        'type': 'rightAligned'
    },
    {
        'field': 'PM2.5_Anomaly',
        'headerName': 'PM2.5 Anomaly',
        'valueFormatter': {"function": "d3.format('.2f')(params.value)"},  # Format to two decimal places
        'type': 'rightAligned'
    },
    {
        'field': 'PM2.5_Pct_Change',
        'headerName': 'PM2.5 % Change',
        'valueFormatter': {"function": "d3.format('.1f')(params.value) + '%'"},
        'type': 'rightAligned'
    },
    {
        'field': 'Yearly_Avg_PM2.5',
        'headerName': 'Yearly_Avg_PM2.5',
        'valueFormatter': {"function": "value"},  # Format to two decimal places
        'type': 'rightAligned'
    }
]

grid = html.Div([
    html.H1('Detail Table'),
    dag.AgGrid(
        id='grid_id',
        columnDefs=columnDefs,
        columnSize="autoSize",
        rowData=merged_df.to_dict('records'),
        defaultColDef={'editable': True, "filter": True, "floatingFilter": True},
        dashGridOptions = {"suppressFieldDotNotation": True}

    ),

]) 
# Full layout of the page
layout = html.Div(
    [
        html.H2('INTRODUCTION', style={'textAlign': 'center', 'marginTop': '20px'}),
        dcc.Markdown(task, style={"maxWidth": 800, "margin": "20px auto", "padding": "20px" }),
        dcc.Markdown(introduction, style={"maxWidth": 800, "margin": "20px auto", "padding": "20px"}),
        grid
    ],
    style={'fontFamily': 'Arial, sans-serif'}
)
