import dash_mantine_components as dmc
from dash import register_page, html, Input, Output, Dash, dcc, callback
import pandas as pd
import dash_ag_grid as dag
import dash_daq as daq
import plotly.express as px

from utils import merged_df

register_page(__name__, name="Geospatial Analysis", path="/geospatial_Analysis")
# Data processing

Average_trnd = merged_df['PM2.5'].mean()

# Fixing dmc.ScatterChart
def create_pm25_fig():
    return dmc.ScatterChart(
        id='pm_scatter',
        data=merged_df.to_dict('records'),
        dataKey={'x': 'City', 'y': 'PM2.5'},
        xAxisProps={'label': 'City', 'tickAngle': -45},
        yAxisProps={'label': 'PM2.5'},
        legendProps={'verticalAlign': 'top', 'height': 50},
        h=250
    )
def yr_trand():
    return dmc.LineChart(
        id='yr_trend',
        h=250,
        data=merged_df.to_dict('records'),  # Convert the dataframe to records
         dataKey={'x': 'Year', 'y': 'PM2.5'},
        tooltipAnimationDuration=200,
        referenceLines=[
            {'y': Average_trnd, 'label': 'Average PM2.5', 'color': 'Orange'},
        ],
        series=[
            {
                "name": "PM2.5",
                "data": merged_df[["Year", "PM2.5"]].groupby("Year").mean().reset_index().to_dict("records")
            }
        ],
        xAxisLabel="Year",   # Set x-axis label
        yAxisLabel="PM2.5",  # Set y-axis label
        withDots=True,       # Optional: to show dots on the chart
        withTooltip=True     # Show tooltips on hover
    )



# Mapbox scatter plot
mapbox = px.scatter_mapbox(
    merged_df, lat='Latitude', lon='Longitude',
    color='AQI_Level', size='PM2.5', hover_name='City',
    hover_data={'Latitude': False, 'Longitude': False, 'PM2.5_Pct_Change': True, 'Yearly_Avg_PM2.5': True},
    mapbox_style='open-street-map',
)

# Layout
# Layout section
layout = dmc.MantineProvider([  # MantineProvider wrapping the layout
    dmc.Container([
        dmc.Grid([  # Main grid for Mapbox and scatter plot
            dmc.GridCol([
                dmc.Paper([
                    dmc.Text('Mapbox Scatter Plot'),
                    dmc.LoadingOverlay(
                        [dcc.Graph(figure=mapbox)],
                        loaderProps={"type": "bars", "color": "orange", "size": "md"},
                        overlayProps={"radius": "sm", "blur": 2},
                        visible=True
                    ),
                ], px="md", withBorder=True)
            ], span=6),
            dmc.GridCol([
                dmc.Paper([
                    dmc.Text('PM2.5 Levels Scatter Plot'),
                    create_pm25_fig()
                ], px="md", withBorder=True)
            ], span=6),
        ], gutter="xl"),
        # PM2.5 Trend section
        dmc.Grid([
            dmc.GridCol([
                dmc.Paper([
                    dmc.Text('PM2.5 Trend over the Years'),
                    yr_trand(),  # Display the trend chart
                ], px="md", withBorder=True)
            ], span=12)  # Make it span the whole width
        ], gutter="xl"),
    ], fluid=True)
])


@callback(
    [
        Output('indicator', 'value'),
        Output('mapbox', 'figure'),
        Output('scatter', 'figure'),
    ],
    [
        input('year-dropdown', 'value'),
        input('mapbox', 'hoverData'),
    ]
)

def update_element(selected_year, hoverData):
    filtered_df = merged_df[merged_df['Year'] == selected_year]
    if selected_year:
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]