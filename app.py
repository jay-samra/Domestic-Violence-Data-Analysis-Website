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
from pages import choropleth1, scatterplot1_3D, scatterplot2, choropleth2, scatterplot3, kmeansNational, linearRegressionAK, linearRegressionNY


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
                    # dbc.NavLink("Introduction", href="/pages/choropleth1", active="exact"),
                    dbc.NavLink("A Look Around the World", href="/pages/choropleth1", active="exact"),
                    dbc.NavLink("Impact of Class Disparities", href="/pages/scatterplot1_3D", active="exact"),
                    dbc.NavLink("A Zoom In on the Workforce", href="/pages/scatterplot2", active="exact"),
                    dbc.NavLink("A Glance at America", href="/pages/choropleth2", active="exact"),
                    dbc.NavLink("Trends in American Data", href="/pages/scatterplot3", active="exact"),
                    dbc.NavLink("American Data Clustering & Segmentation", href="/pages/kmeansNational", active="exact"),
                    dbc.NavLink("Predictive Modeling (Arkansas)", href="/pages/linearRegressionAK", active="exact"),
                    dbc.NavLink("Predictive Modeling (New York)", href="/pages/linearRegressionNY", active="exact"),
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
    elif pathname == '/pages/scatterplot1_3D':
        return scatterplot1_3D.layout
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
    elif pathname == '/pages/linearRegressionNY':
        return linearRegressionNY.layout
    else:
        return
if __name__ == '__main__':
    app.run_server(debug=False)