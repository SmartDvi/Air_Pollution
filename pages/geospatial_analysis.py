import dash_mantine_components as dmc
from dash import register_page, html, Input, Output, dcc, callback
import pandas as pd
import plotly.express as px
from utils import merged_df
from components import pm_indicator, yr_dropdown, country_dropdown, create_aqi_tab, create_pm25_fig, yr_trend, donut_charts_group, tabs


register_page(__name__, path='/geospatial_analysis', title='Geospatial Analysis')

style=['open-street-map',
'white-bg',
'carto-positron',
'carto-darkmatter',
'stamen-terrain',
'stamen-toner',
'stamen-watercolor',
'satellite',
'satellite-streets']

Average_trnd = merged_df['PM2.5'].mean()


# Mapbox scatter plot
def mapbox():
    fig = px.scatter_mapbox(
        merged_df, 
        lat='Latitude', 
        lon='Longitude',
        color='AQI_Level', 
        size='PM2.5',
        size_max=15, 
        #height=300,
        #width=500,
        hover_name='Country',
        zoom=1,
        hover_data={'Latitude': False, 'Longitude': False, 'PM2.5_Pct_Change': True, 'Yearly_Avg_PM2.5': True},
        mapbox_style=style[6],
    )
    
    # Update layout to place legend at the top
    fig.update_layout(
        legend=dict(
            orientation='h',  # Horizontal orientation
            yanchor='bottom',  # Anchor the legend to the bottom
            y=1.05,            # Position the legend above the plot
            xanchor='center',  # Center the legend horizontally
            x=0.5,
            font=dict(
                size=10
            ),
            itemwidth=30,  # Corrected value (min value is 30)
            title_font=dict(size=9)
        )
    )
    fig.update_layout(margin={'l': 0, 'b': 0, 'r': 0, 't':14})
    
    return fig

layout = dmc.MantineProvider(
    [
        dmc.Container(
            [
                dmc.Text('Geospatial_Analysis', tt="uppercase", size="xl", c="blue", ta="center", td="underline", fw=700),
                dmc.Grid([
                    dmc.GridCol([
                        dmc.Paper(
                            [
                                donut_charts_group()
                            ], 
                              p="xs", shadow='xs', radius='xs'
                        )
                    ])
                ]),
                dmc.Grid([
                    dmc.GridCol([
                        dmc.Paper(
                            [
                                dmc.Text('Mapbox Scatter Plot'),
                                dcc.Graph(id='mapbox',figure=mapbox(), style={'height': '250px'})
                   
                            ], p="xs", shadow='xs', radius='xs'
                        ),
                    ], span=7),
                    dmc.GridCol([
                        dmc.Paper(
                            [
                                dmc.Text('tab representation of PM2.5 levels on barchart'),
                                tabs()
                   
                            ], p="xs", shadow='xs', radius='xs'
                        ),
                    ], span=4.5),
                ], gutter='xl'),
                dmc.Grid([
                    dmc.GridCol([
                        dmc.Paper([
                            dmc.Text('PM2.5 Trend over the Years'),
                            yr_trend(),
                        ], px="md", withBorder=True)
            ], span=12)  
        ], gutter="xl"),
            ], fluid=True
        )
    ]
)



# Callback to update PM2.5 gauge
@callback(
    Output('indicator', 'value'),   # Update the value of the PM2.5 gauge
    Input('year-dropdown', 'value'),  # Get selected year
    Input("country-dropdown", 'value')  # Get selected country
)
def Gauge_indicator(selected_year, selected_country):
    filtered_df = merged_df[(merged_df['Year'] == selected_year) &
                            (merged_df['Country'] == selected_country)]

    # Get the average PM2.5 for the selected year and country
    pm25_value = filtered_df['PM2.5'].mean() if not filtered_df.empty else 0
    
    return pm25_value  # Return the PM2.5 value to update the gauge

@callback(
    Output('some-chart-id', 'figure'),  # Replace with your chart ID
    Input('tabs-id', 'value')  # The ID of your Tabs component
)
def update_chart(selected_tab):
    return create_aqi_tab(selected_tab)  # This assumes create_aqi_tab returns a Plotly figure
