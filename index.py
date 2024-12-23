from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import time
import statsmodels.api as sm

# Connecting to the app.py file
from app import app
from app import server
from pages import choropleth1

# Connecting to app pages from pages folder
from pages import choropleth1, scatterplot1, scatterplot2, choropleth2


cardMap = dbc.Card([])

navBar = dbc.NavbarSimple(
    dbc.NavItem(dbc.DropdownMenu(label="Important Links", children=[
        dbc.DropdownMenuItem("Donate Today!", href='https://ncadv.org/donate'),
        dbc.DropdownMenuItem("LinkedIn", href='www.linkedin.com/in/jagroop-s-sam18731', external_link=True),
    ],)),
    brand = 'Measuring the Socioeconomic Factors on Domestic Violence: A Global & National Case Study',
    # #A3E4D7
    # #003366 - Navy Blue
    # #2E856E - Clean
    #
    color='#2E856E',
    dark = True,
)
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "22rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar =  html.Div(
    [
        html.H2("Table of Contents", className="display-2"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Status of Laws", href="/pages/choropleth1", active="exact"),
                dbc.NavLink("Possible Correlations", href="/pages/scatterplot1", active="exact"),
                dbc.NavLink("3D-Analysis", href="/pages/scatterplot2", active="exact"),
                dbc.NavLink("American Analysis", href="/pages/choropleth2", active="exact"),
                dbc.NavLink("Correlations in American Data", href="/", active="exact"),
                dbc.NavLink("Global Data Clustering & Segmentation", href="/", active="exact"),
                dbc.NavLink("American Data Clustering & Segmentation", href="/2", active="exact"),
                dbc.NavLink("Predictive Modeling", href="/", active="exact"),
                dbc.NavLink("Conclusion", href="/", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style= SIDEBAR_STYLE,
)



# Landing Page
app.layout = html.Div([
    navBar,
    sidebar,

    # dash component to read url using pathname
    dcc.Location(id='url', refresh=False, pathname=''),
    html.Div([
        dcc.Link("Link to Map", href="/pages/choropleth1"),
        dcc.Link('Link to scatterplot', href='/pages/scatterplot1'),
        dcc.Link('Link to ameircan', href='/pages/choropleth2'),
    ], className='row'),

    #All app pages will go inside this div
    html.Div(id='page-content', children=[]),
])
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
    else:
        return

if __name__ == '__main__':
    app.run_server(debug=False)