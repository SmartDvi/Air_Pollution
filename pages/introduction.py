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

dash.register_page(__name__,
path='/',
title='Introducto and Dataset Details',
description= 'Belief Intoduction to the project and Dateset details',
order=0)




# Retrive column names
columns = merged_df.columns

# Generate column definition for AG Grid
# Data details table
def data_detail():
    columns = ['City', 'Country', 'Yearly_Avg_PM2.5']
    grid = dag.AgGrid(
        id='table',
        rowData=merged_df.to_dict("records"),
        columnDefs=[
            {'field': 'PM2.5', 'headerName': 'PM2.5',
             'cellStyle': {
                 "function": """(params) => {
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
             "valueFormatter": {"function": "d3.format('.2f')(params.value)"},
             "type": "rightAligned",
            },
            {
                "field": "PM2.5_Anomaly",
                "valueFormatter": {"function": "d3.format('.2f')(params.value)"},
                "type": "rightAligned",
            },
            {
                "field": "PM2.5_Pct_Change",
                "valueFormatter": {"function": "d3.format('.1f')(params.value) + '%'"},
                "type": "rightAligned",
            },
        ] + [{"field": f} for f in columns],
        defaultColDef={"filter": True, "floatingFilter": True},
        columnSize='autoSize',
        dashGridOptions={"suppressColumnVirtualisation": True}
    )
    return grid

# developing app layout
layout = dmc.MantineProvider(
    [
        # Bottom section with data table
        dmc.Paper([
            dmc.Text('Data Details'),
            data_detail()
        ], px="md", withBorder=True, style={"marginTop": "20px"})

    ]
)