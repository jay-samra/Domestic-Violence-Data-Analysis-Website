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
    dbc.NavItem(dbc.NavLink("Table of Contents", href="/pages/scatterplot1")),
    brand = 'Measuring the Socioeconomic Factors on Domestic Violence: A Global & National Case Study',
    color='green',
    dark = True,
)


# Landing Page
app.layout = html.Div([
    navBar,
    # dash component to read url using pathname
    dcc.Location(id='url', refresh=False, pathname=''),
    html.Div([
        dbc.Button("Next Page", href="/pages/choropleth1"),
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