from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State

# Connecting to the app.py file
from app import app
from app import server
from apps import secondPage

# Connecting to app pages from apps folder
# from apps import (page names)
# Landing Page
app.layout = html.Div([
    # dash component to read url using pathname
    dcc.Location(id='url', refresh=False, pathname=''),
    html.Div([
        dcc.Link('Link', href='/apps/secondPage'),
    ], className='row'),

    #All app pages will go inside this div
    html.Div(id='page-content', children=[]),
])
# input: link
# output: switch to page with map
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/secondPage':
        return secondPage.layout
    else:
        return app.layout

if __name__ == '__main__':
    app.run_server(debug=False)