
import dash_mantine_components as dmc
import dash_ag_grid as dag
import pandas as pd
import dash
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dash import Dash, _dash_renderer, dcc, page_container, callback, Input, Output, State, html, get_relative_path


from utils import merged_df

_dash_renderer._set_react_version("18.2.0")


stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
]

app = Dash(
    external_stylesheets=stylesheets, 
    use_pages=True,
    
)

links = dmc.Stack(
    [
        dmc.Anchor(f"{page['name']}", href=page["relative_path"])
        for page in dash.page_registry.values()
        if page["module"] != "pages.not_found_404"
    ]
)

theme_toggle = dmc.ActionIcon(
    [
        dmc.Paper(DashIconify(icon="radix-icons:sun", width=25), darkHidden=True),
        dmc.Paper(DashIconify(icon="radix-icons:moon", width=25), lightHidden=True),
    ],
    variant="transparent",
    color="yellow",
    id="color-scheme-toggle",
    size="lg",
    ms="auto",
)

header = dmc.Group(
    [
        dmc.Burger(id="burger-button", opened=True, hiddenFrom="md"),
        dmc.Text("Global Air Quality Analys with Plotly (1850 - 2021)", size="lg",ta='center',c='blue', fw=700),
        theme_toggle
    ],
    justify="flex-start",
    h=70
)


# Dropdown for year selection
yr_dropdown = dmc.Select(
    id="year-dropdown",
    label='Select Year',
    data=[{'label': year, 'value': year} for year in merged_df['Year'].unique()],
    value='2021'
)

# Dropdown for year selection
country_dropdown = dmc.Select(
    id="country-dropdown",
    label='Select Country',
    data=[{'label': country, 'value': country} for country in merged_df['Country'].unique()],
    value=merged_df['Country'][0]
)


# Create the Gauge indicator
pm_indicator = daq.Gauge(
    id='indicator',
    color={
        'gradient': True,
        'ranges': {
            "green": [0, 12.1],
            "yellow": [12.1, 35.5],
            "orange": [35.5, 55.5],
            "red": [55.5, 150.4],
            "purple": [150.5, 250.4],
            "brown": [250.5, 500]
        }
    },
    min=0,  
    max=125,  
    showCurrentValue=True,
    units="PM2.5",
    value=merged_df['PM2.5'].mean(),  
    size=150,  
    label="PM2.5 Indicator for the Year",  
    scale={
        'start': 0,
        'interval': 25  
    }
)



# developing the side setup inside a variable 
navbar = dcc.Loading(
    dmc.ScrollArea(
            dmc.Stack(
                [
                    
                    links,
                  
                    yr_dropdown,
                  
                    pm_indicator,
                   
                    country_dropdown

                ]
            )
    )
)


app_shell = dmc.AppShell(
    [
        dmc.AppShellHeader(header, px=15),
        dmc.AppShellNavbar(navbar, p=19),
        dmc.AppShellMain(dash.page_container, pt=30),
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
                                dmc.NavLink(label="PY.CAFE", href='https://py.cafe/SmartDvi/plotly-global-air-quality')
                            ]

                        )
                    ], justify='lg'
                )
            ]
        )
    ],
    header={"height": 70},
    padding="xl",
    navbar={
        "width": 250,
        "breakpoint": "md",
        "collapsed": {"mobile": True},
    },
)

app.layout = dmc.MantineProvider(
    [
        dcc.Store(id="theme-store", storage_type="local", data="light"),
        app_shell,
       # dash.page_container
    ],
    id="mantine-provider",
    forceColorScheme="light",
)


@callback(
    Output("app-shell", "navbar"),
    Input("burger-button", "opened"),
    State("app-shell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": opened}
    return navbar


@callback(
    Output("mantine-provider", "forceColorScheme"),
    Input("color-scheme-toggle", "n_clicks"),
    State("mantine-provider", "forceColorScheme"),
    prevent_initial_call=True,
)
def switch_theme(_, theme):
    return "dark" if theme == "light" else "light"



if __name__ == "__main__":
    app.run_server(debug=True, port=6070)