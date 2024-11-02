import dash_mantine_components as dmc
from dash import register_page, html, Input, Output, dcc, callback
import pandas as pd
import dash_daq as daq
import dash




register_page(__name__, path='/geospatial_analysis', title='Geospatial Analysis')


import plotly.express as px
from utils import merged_df, group_aqi_level


Average_trnd = merged_df['PM2.5'].mean()
default_year = merged_df['Year'].max()
# Mapbox scatter plot


color_map = {
    'Good': 'green',
    'Moderate': 'yellow',
    'Unhealthy for Sensitive Groups': 'orange',
    'Unhealthy': 'red',
    'Very Unhealthy': 'purple', 
    'Hazardous': 'maroon'
}




print(color_map.keys())
# Dropdown for year selection
yr_dropdown = dmc.Select(
    id="year-dropdown",
    label='Select Year',
    data=[{'label': year, 'value': year} for year in merged_df['Year'].unique()],
    value='2021'
)

# Dropdown for country selection
def create_country_dropdown(merged_df):
    return dmc.Select(
        id="country-dropdown",
        label='Select Country',
        data=[{'label': country, 'value': country} for country in sorted(merged_df['Country'].unique())],
        value=sorted(merged_df['Country'].unique())[0]
    )

country_dropdown = create_country_dropdown(merged_df)


# Define gauge indicator with adjusted color range
pm_indicator = daq.Gauge(
    id='indicator',
    color={
        'gradient': True,
        'ranges': {
            "green": [0, 12],
            "yellow": [12.1, 35.4],
            "orange": [35.5, 55],
            "purple": [55.1, 75.4],
            "red": [75.1, 90],
            "black": [90.1, 100],
              
        }
    },
    min=0,
    max=100,
    showCurrentValue=True,
    units="µg/m³",
    value=Average_trnd,  # set to average PM2.5 or other current value
    size=150,
    label="PM2.5 Indicator",
    scale={'start': 0, 'interval': 10}
)


def create_donut_chart_with_label(aqi_level, year, country):
    # Filter the data based on selected year and country
    data = merged_df[(merged_df['Year'] == year) & (merged_df['Country'] == country)]

    # Calculate total PM2.5 and AQI levels based on filtered data
    total_pm25 = data['PM2.5'].sum()
    aqi_value = data[data['AQI_Level'] == aqi_level]['PM2.5'].sum()

    percentage_value = (aqi_value / total_pm25) * 100 if total_pm25 != 0 else 0

    chart_data = [
        {'name': aqi_level, 'value': aqi_value, 'color': color_map[aqi_level]},
        {'name': 'Others', 'value': total_pm25 - aqi_value, 'color': 'gray'}
    ]

    return html.Div(
        [
            html.Div(aqi_level, style={"textAlign": "center", "fontWeight": "bold"}),
            dmc.DonutChart(
                id='pm_gauge',
                data=chart_data,
                size=82,
                thickness=18,
                withTooltip=True,
                mx='auto',
                chartLabel=f"{percentage_value:.1f}%",
                startAngle=180,
                endAngle=0
            ),
        ]
    )
style={
        "width": "100%",        
        "maxWidth": "1200px",   
        "margin": "0 auto",   
        "padding": "0",         
        "display": "flex",      
        "justifyContent": "right", 
        "alignItems": "right",  
        "height": "auto"         
    },

# AQI Level-Based Bar Chart Function
def create_aqi_tab(aqi_level, year):
    data = merged_df[(merged_df['AQI_Level'] == aqi_level) & (merged_df['Year'] == year)]
    data_for_chart = data.groupby('City')['PM2.5'].sum().reset_index()
    top_10 = data_for_chart.nlargest(10, 'PM2.5')
    least_10 = data_for_chart.nsmallest(10, 'PM2.5')
    comb = pd.concat([top_10, least_10])

    return dmc.BarChart(
        id=f'aqi_tab_{aqi_level}',
        h=180,
        dataKey="City",
        data=comb.to_dict('records'),
        orientation="vertical",
        yAxisProps={"width": 80},
        series=[{
            "name": "PM2.5",
            "data": comb['PM2.5'].tolist(),
            "color": color_map[aqi_level],
        }]
    )

# Dynamic Tabs Component
def tabs(year):
    return dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.TabsTab('Good', value='Good'),
                    dmc.TabsTab('Moderate', value='Moderate'),
                    dmc.TabsTab('Unhealthy', value='Unhealthy'),
                    dmc.TabsTab('Unhealthy for Sensitive Groups', value='Unhealthy for Sensitive Groups'),
                    dmc.TabsTab('Very Unhealthy', value='Very Unhealthy'),
                    dmc.TabsTab('Hazardous', value='Hazardous')
                ], grow=True
            ),
            dmc.TabsPanel(create_aqi_tab('Good', year), value='Good'),
            dmc.TabsPanel(create_aqi_tab('Moderate', year), value='Moderate'),
            dmc.TabsPanel(create_aqi_tab('Unhealthy', year), value='Unhealthy'),
            dmc.TabsPanel(create_aqi_tab('Unhealthy for Sensitive Groups', year), value='Unhealthy for Sensitive Groups'),
            dmc.TabsPanel(create_aqi_tab('Very Unhealthy', year), value='Very Unhealthy'),
            dmc.TabsPanel(create_aqi_tab('Hazardous', year), value='Hazardous'),
        ],
        value='Good',
        id='return_tabs'
    )




layout = dmc.MantineProvider(
    [
        dmc.Container(
            [
                dmc.Text('Geospatial_Analysis', tt="uppercase", size="xl", c="blue", ta="center", td="underline", fw=700, py=27),
                dmc.Grid([
                    dmc.GridCol([
                        dmc.Paper(
                            [
                                html.Div(
                                    [
                                        dmc.Container(id='donut_chart_container',px=0,
                                                        )
                                    ]
                                )
                            ], 
                              p="xs", shadow='xs', radius='xs'
                        )
                    ])
                ]),
                dmc.Grid([
                    dmc.GridCol([
                        dmc.Paper(
                            [
                                dmc.Text('Distributions of PM2.5 levels across different Cities'),
                                dcc.Graph(id='mapbox', style={'height': '235px'})

                   
                            ], p=0, shadow='xs', radius='xs'
                        ),
                    ], span=7.4),
                    dmc.GridCol([
                        dmc.Paper(
                            [
                                dmc.Text('Cities with the 10 top and Least PM2.5'),
                                tabs(year=merged_df.Year)
                   
                            ], p=0, shadow='xs', radius='xs'
                        ),
                    ], span=4.5),
                ], gutter='xl'),
                dmc.Grid([
                    dmc.GridCol([
                        dmc.Paper([
                            dmc.Container(
                                [
                                    html.Div(
                                    [
                                        dmc.Text('PM2.5 Year Trend by Country'),
                                        dmc.Container( id='yr_trend', m=0,
                                                       px=0, p=0, mx=0,
                                                        style=style
                                                      )
                                    ]
                                )
                                ]
                            )
                        ], px="xs", withBorder=True)
            ], span=12)  
        ], gutter="xl"),
            ], fluid=True
        )
    ]
)



# Callback to update PM2.5 gauge
@callback(
    Output('indicator', 'value'),   
    Input('year-dropdown', 'value'),
    Input("country-dropdown", 'value')  
)
def Gauge_indicator(selected_year, selected_country):
    filtered_df = merged_df[(merged_df['Year'] == selected_year) &
                            (merged_df['Country'] == selected_country)]

    # Get the average PM2.5 for the selected year and country
    pm25_value = filtered_df['PM2.5'].mean() if not filtered_df.empty else 0
    
    return pm25_value  
"""
@callback(
    Output('aqi_tab', 'figure'),  
    Input('year-dropdown', 'value')  
)
def update_chart(selected_tab):
    return create_aqi_tab(selected_tab)  

"""
# Callback to update Mapbox based on selected year
@callback(
    Output('mapbox', 'figure'),
    Input('year-dropdown', 'value'),
    
)
def update_mapbox(selected_year):
    print(f"Selected Year: {selected_year}")  
    filtered_df = merged_df[merged_df['Year'] == selected_year]
    print(f"Filtered Data: {filtered_df.shape[0]} rows")  
    
    
    fig = px.scatter_mapbox(
        filtered_df, 
        lat='Latitude', 
        lon='Longitude',
        color='AQI_Level',
        color_discrete_map={
           'Good': 'green',
            'Hazardous': 'red',
            'Moderate': 'yellow',
            'Unhealthy': 'orange',
            'Unhealthy for Sensitive Groups': 'purple',
            'Others': 'gray' 
        },
        size='PM2.5', 
        size_max=23,
        hover_name='Country',
        text=filtered_df['City'],
        zoom=0.5, 
        center={"lat": 20, "lon": 0},
        hover_data={'Latitude': False, 'Longitude': False, 'PM2.5_Pct_Change': True, 'Yearly_Avg_PM2.5': True},
        mapbox_style='open-street-map',
    )
    
    # Update layout to place legend at the top
    fig.update_layout(
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.05,
            xanchor='center',
            x=0.5,
            font=dict(size=10),
            itemwidth=30,
            title_font=dict(size=9)
        )
    )
    fig.update_layout(margin={'l': 0, 'b': 0, 'r': 0, 't': 8})

    fig.update_traces(
        textposition='top center',
        textfont=dict(size=16))
    
    return fig

@callback(
    Output('return_tabs', 'children'),
    Input('year-dropdown', 'value')
)
def update_tabs_based_on_year(selected_year):
    return tabs(selected_year)

@callback(
    Output('yr_trend', 'children'),
    Input('country-dropdown', 'value')
)
def update_year_trend(selected_country):
    yearly_data = merged_df[merged_df['Country'] == selected_country]
    
    if yearly_data.empty:
        return dmc.Text("No data available for the selected country", color="red", align="center")

    yearly_data = yearly_data.groupby('Year').agg(
        {
            'PM2.5': 'mean',
            'PM2.5_Anomaly': 'mean',
            'PM2.5_Pct_Change': 'mean'
        }).reset_index()

    # Dynamic color based on PM2.5 levels
    series_data = [
        {
            "name": "PM2.5",
            "data": yearly_data.to_dict("records"),
            "color": 'green',
        },
        {
            "name": "PM2.5_Pct_Change",
            "data": yearly_data.to_dict("records"),
            "color": 'blue',
        }
    ]

    return dmc.LineChart(
        id='yr_trend_chart',
        h=230,
        data=yearly_data.to_dict('records'),
        dataKey='Year',
        tooltipAnimationDuration=10,
        referenceLines=[{'y': Average_trnd, 'label': 'Average PM2.5', 'color': 'blue'}],
        series=series_data,
        withLegend=True,
        style={
            "w": "100%",      
            "maw": "1200px", 
            "m": "0 auto",    
            "p": "0",
            "px": "0",
            "h": "100%" 
         },
        legendProps={"verticalAlign": "top"},
        xAxisLabel="Year",
        yAxisLabel="Yearly_Avg_PM2.5",
        withDots=True,
        withTooltip=True,
        withXAxis={'type': 'category', 'label': {'display': True, 'text': "Year"}, 'tickInterval': 1}
    )


@callback(
    Output('donut_chart_container', 'children'),  # Update the output container for donut charts
    [Input('year-dropdown', 'value'),
     Input('country-dropdown', 'value')]
)
def update_donut_charts(selected_year, selected_country):
    return dmc.Group(
        [
            create_donut_chart_with_label('Good', selected_year, selected_country),
            create_donut_chart_with_label('Hazardous', selected_year, selected_country),
            create_donut_chart_with_label('Moderate', selected_year, selected_country),
            create_donut_chart_with_label('Unhealthy', selected_year, selected_country),
            create_donut_chart_with_label('Very Unhealthy', selected_year, selected_country),
            create_donut_chart_with_label('Unhealthy for Sensitive Groups', selected_year, selected_country)
        ],
        justify="center",
        gap=10,
        grow=True
    )
