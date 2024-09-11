import dash
import pandas as pd
import dash_mantine_components as dmc
from dash import Dash, _dash_renderer, dcc, callback, Input, Output, State, html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from utils import melted_df

_dash_renderer._set_react_version("18.2.0")

stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
]

app = Dash(__name__, 
           use_pages=True, 
           external_stylesheets=stylesheets,
           suppress_callback_exceptions=True,
           prevent_initial_callbacks=False,
           )

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
navbar = dcc.Loading(
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

page_content = [
    dash.page_container
]

app_shell = dmc.AppShell(
    [
        dmc.AppShellHeader(header, px=25),
        dmc.AppShellNavbar(navbar, p=24),
        dmc.AppShellMain(page_content),
        dmc.AppShellFooter(
            [
                dmc.Group(
                    [
                        dmc.NavLink(
                            label= 'Sources Code',
                            description='double Sources',
                            leftSection=dmc.Badge(
                                "2", size="xs", variant='filled', color='orange', w=16, h=16,p=0
                            ),
                            childrenOffset=28,
                            children=[
                                dmc.NavLink(label="GitHub", href='https://github.com/SmartDvi/Air_Pollution.git'),
                                dmc.NavLink(label="GitHub", href='https://py.cafe/SmartDvi/plotly-global-air-quality')
                            ]

                        )
                    ], justify='lg'
                )
            ]
        )
    ]
),
id='app_shell'

# developing app layout
app.layout = dmc.MantineProvider(
    [
        dcc.Store(id='theme_store', storage_type='local', data='light'),
        app_shell
    ],
    id='mantine_provider',
    forceColorScheme='light',
)

@callback(
    Output('app_shell', 'navbar'),
    Input('burger-icon', 'opened'),
    State('app_shell', 'navbar')
)

def navbar_is_open(opened, navbar):
    navbar['collapsed'] = {'mobile': not opened}
    return navbar

@callback(
    Output('mantine_provider', 'forceColorScheme'),
    Input('toggle-color', 'n_click'),
    State('mantine_provider', 'forceColorScheme'),
    prevent_initial_call = True,
)

def switch_theme(_, theme):
    return 'dark' if theme == 'light' else 'light'



if __name__ =="__main__":
    app.run(debug=True, port=8060)