import dash
from dash import dcc
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
import time
import statsmodels.api as sm

import dash_bootstrap_components as dbc
from dash import html

# meta tags for mobile use
# MORPH, MINTY,
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY], suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
# Server for Gunicorn
server = app.server

# Layout definition (should work)
from pages import choropleth1, scatterplot1, scatterplot2, choropleth2, scatterplot3, kmeansNational, linearRegressionAK


cardMap = dbc.Card([])

navBar = dbc.NavbarSimple(
    dbc.NavItem(dbc.DropdownMenu(className="dropdown", label="Important Links", children=[
        dbc.DropdownMenuItem("Donate Today!", href='https://ncadv.org/donate'),
        dbc.DropdownMenuItem("LinkedIn", href='https://www.linkedin.com/in/jagroop-s-sam18731/', external_link=True),
    ],)),
    brand = 'Domestic Violence: A Global & National Case Study',
    class_name = "navbar-brand",
    # #A3E4D7
    # #003366 - Navy Blue
    # #2E856E - Clean
    #
    color='#2E856E',
    dark = True,
    className="navbar"
)

sidebar =  html.Div(
    [
        html.H2("Table of Contents", className="display-2"),
        html.H6("By: Jagroop Singh", className="display-6", style={"fontSize": "22px", "fontWeight": "lighter"}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.Stack([
                    dbc.NavLink("Introduction", href="/pages/choropleth1", active="exact"),
                    dbc.NavLink("Status of Laws", href="/pages/choropleth1", active="exact"),
                    dbc.NavLink("Possible Correlations", href="/pages/scatterplot1", active="exact"),
                    dbc.NavLink("3D-Analysis", href="/pages/scatterplot2", active="exact"),
                    dbc.NavLink("American Analysis", href="/pages/choropleth2", active="exact"),
                    dbc.NavLink("Trends in American Data", href="/pages/scatterplot3", active="exact"),
                    dbc.NavLink("Global Data Clustering & Segmentation", href="/", active="exact"),
                    dbc.NavLink("American Data Clustering & Segmentation", href="/pages/kmeansNational", active="exact"),
                    dbc.NavLink("Predictive Modeling", href="/pages/linearRegressionAK", active="exact"),
                    dbc.NavLink("Conclusion", href="/", active="exact"),
                ], gap = 3),

            ],
            vertical=True,
            pills=True,
        ),
    ],
    className = "sidebar",
)



# Landing Page
app.layout = html.Div([
    navBar,
    sidebar,

    # dash component to read url using pathname
    dcc.Location(id='url', refresh=False, pathname=''),
    html.Div([

    #All app pages will go inside this div
        html.Div(id='page-content', children=[]),
    ], className="content-wrapper")
], className="app-container")


# input: link
# output: switch to pages
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/choropleth1':
        return choropleth1.layout
    elif pathname == '/pages/scatterplot1':
        return scatterplot1.layout
    elif pathname == '/pages/scatterplot2':
        return scatterplot2.layout
    elif pathname == '/pages/choropleth2':
        return choropleth2.layout
    elif pathname == '/pages/scatterplot3':
        return scatterplot3.layout
    elif pathname == '/pages/kmeansNational':
        return kmeansNational.layout
    elif pathname == '/pages/linearRegressionAK':
        return linearRegressionAK.layout
    else:
        return
if __name__ == '__main__':
    app.run_server(debug=False)