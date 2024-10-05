import dash
import dash_mantine_components as dmc
import pandas as pd
import dash_ag_grid as dag
from dash import html, dcc, Input, Output, State, register_page
import dash_bootstrap_components as dbc

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

[data Source]()

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

dash.register_page(__name__,
path='/',
title='Introducto and Dataset Details',
description= 'Belief Intoduction to the project and Dateset details',
order=0)




# Retrive column names
columns = merged_df.columns

# Generate column definition for AG Grid
def data_detail():
    grid = dag.AgGrid(
        id='table',
        rowData=merged_df.to_dict("records"),  # Convert dataframe to dictionary format
        columnDefs=[
            {'field': 'City', 'headerName': 'City'},
            {'field': 'Country', 'headerName': 'Country'},
            {
                'field': 'PM2.5', 
                'headerName': 'PM2.5',
                'cellStyle': {
                    'function': """(params) => {
                        if (params.data.AQI_Level === 'Good') {
                            return { backgroundColor: 'green', color: 'white' };
                        } else if (params.data.AQI_Level === 'Moderate') {
                            return { backgroundColor: 'yellow', color: 'black' };
                        } else if (params.data.AQI_Level === 'Unhealthy for Sensitive Groups') {
                            return { backgroundColor: 'orange', color: 'black' };
                        } else if (params.data.AQI_Level === 'Unhealthy') {
                            return { backgroundColor: 'red', color: 'white' };
                        } else if (params.data.AQI_Level === 'Very Unhealthy') {
                            return { backgroundColor: 'purple', color: 'white' };
                        } else if (params.data.AQI_Level === 'Hazardous') {
                            return { backgroundColor: 'brown', color: 'white' };
                        }
                        return null;
                    }"""
                },
                'valueFormatter': {"function": "d3.format('.2f')(params.value)"}, 
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
                'headerName': 'Yearly Avg PM2.5',
                'valueFormatter': {"function": "d3.format('.2f')(params.value)"},  # Format to two decimal places
                'type': 'rightAligned'
            }
        ],
        defaultColDef={"filter": True, "floatingFilter": True},  # Enable filters
        columnSize='autoSize',  # Automatically size columns
        dashGridOptions={"suppressColumnVirtualisation": True}  # Avoid column virtualization for better performance
    )
    return grid

# developing app layout
layout = dmc.MantineProvider(
    [
         dmc.Box([
            dmc.Text("INTRODUCTION", ta='center'),
            dcc.Markdown(task, style={"maxWidth": 800}),
            dcc.Markdown(introduction, style={"maxWidth": 800}),
    ]),
        dmc.Grid([
            dmc.GridCol([
                # Bottom section with data table
        dmc.Paper([
            dmc.Text('Data Details'),
            data_detail()
        ], px="md", withBorder=True, style={"marginTop": "20px"}),

            ])
        ])
    ]
)