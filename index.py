from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State

# Connecting to the app.py file
from app import app
from app import server
from pages import choropleth1

# Connecting to app pages from pages folder
from pages import choropleth1, scatterplot1
# Landing Page
app.layout = html.Div([

    # dash component to read url using pathname
    dcc.Location(id='url', refresh=False, pathname=''),
    html.Div([
        dcc.Link('Link to map', href='/pages/choropleth1'),
        dcc.Link('Link to scatterplot', href='/pages/scatterplot1'),
    ], className='row'),

    #All app pages will go inside this div
    html.Div(id='page-content', children=[]),
])
# input: link
# output: switch to page with map
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/choropleth1':
        return choropleth1.layout
    elif pathname == '/pages/scatterplot1':
        return scatterplot1.layout
    else:
        return

if __name__ == '__main__':
    app.run_server(debug=False)