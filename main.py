import dash
import pandas as pd
import dash_mantine_components as dmc
from dash import Dash, _dash_renderer, dcc, callback, Input, Output, State, html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from utils import melted_df

_dash_renderer._set_react_version("18.2.0")

app = Dash(__name__, use_pages=True, external_stylesheets=dmc.styles.ALL)

# developing the icon and theme for changing theme color
themes_toggle = dmc.ActionIcon(
    [
        dmc.Paper(DashIconify(icon='radix-icons:sun', width=25), darkHidden=True),
         dmc.Paper(DashIconify(icon='radix-icons:sun', width=25), darkHidden=True)
    ],
    variant="transparent",
    color="blue",
    id="toggle-color",
    ms="auto"
)

# developing setup
header = dmc.Group(
    [
        
    dmc.Burger(id="burger-icon", opened=False, hiddenFrom="md"),
    dmc.Text(['Analysis on Pm2.5 Air Pollution from 1850 - 2021'],
    size="lg",
    fw='700',
    tt='center',
    
   # leftSection=DashIconify(icon=''
    )
    ], justify = "flex-start",
    h=70,
    

)
# developing the side setup inside a variable 
navbar = dcc.dcc.Loading(
    dmc.ScrollArea(
        [
            dmc.NavLink(label='Introduction and Project Detail',),
            dmc.Space(h='md'),
            dmc.NavLink(label='Geospatial and Analysis',),
            dmc.Space(h='md'),
            dmc.NavLink(label='Project Report and Recommendation',),
            dmc.Space(h='md'),
            dmc.Select(
                id="year-dropdown",
                label='Select Year',
                data=[{'label': Year, 'value': Year} for Year in melted_df['Year']]
            )
        ]
    )
)


# developing app layout
app.layout = dbc.Container(
    dbc.Col(
        [
            dash.page_container
        ]
    )
)





if __name__ =="__main__":
    app.run(debug=True, port=8060)