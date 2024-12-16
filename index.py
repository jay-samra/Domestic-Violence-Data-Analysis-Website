from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State

# Connecting to the app.py file
from app import app
from app import server

# Connecting to app pages from apps folder
# from apps import (page names)
# Landing Page
app.layout = html.Div([
    html.Div([
        dcc.Link('Link', href='/'),
    ], className='row'),
    # dash component to read url using pathname
    dcc.Location(id='url', refresh=False, pathname=''),
    #All app pages will go inside this div
    html.Div(id='page-content', children=[]),
])

if __name__ == '__main__':
    app.run_server(debug=False)