import dash
import dash_mantine_component as dmc
import pandas as pd
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc


task = """
Air quality around the globe has gone through significant ups and downs since the Industrial Revolution. Many factors affect the air that we breath such as the usage of coal power plants, clean air legislation, and automobile congestion.

`Week 36 of Figure-Friday` will dive into this topic with data 5 from the Air Quality Stripes project, which shows the concentration of particulate matter air pollution (PM2.5) in cities around the world.

##### Things to consider:
    - can you replicate the sample graph with Plotly?
    - can you improve the sample graph built?
    - would a different figure tell the data story better?
    - are you able to replicate or improve the app 3 built by the Air Quality Stripes project?





    """



app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# developing app layout
app.layout = dbc.Container(
    dbc.Col(
        [
            dash.page_container
        ]
    )
)
