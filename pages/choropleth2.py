from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pathlib
import dash_bootstrap_components as dbc
from pathlib import Path
from app import app
import numpy as np
import country_converter as coco
import time

# scripts will run regardless of OS
# returns absolute path to datasets
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

# Dataset Author: World Population Review
df1 = pd.read_csv(DATA_PATH.joinpath('americanRates.csv'))

# choropleth figure
fig = go.Figure(data=go.Choropleth(
    locations = df1['code'],
    z = df1['DomesticViolenceAgainstWomen'].astype(float),
    locationmode = 'USA-states',
    colorscale = 'Reds',
    hovertext = df1['state'],
    showscale = True,
    marker_line_color = 'white',
    colorbar = dict(title=dict(
        text = '% of Women Who Have Experineced Violence'
    ))
))
# displaying american states on map
fig.update_layout(
    geo_scope = 'usa',
    title = 'The Prevalence of Domestic Violence in America',
)

# sorting by most violent states
df_sorted = df1[['state', 'DomesticViolenceAgainstWomen']].groupby('state').sum().sort_values(by='DomesticViolenceAgainstWomen', ascending=False).head(10)
df_sorted = df_sorted.reset_index()

# creating table to be displayed on page
table = go.Figure(data=[
    go.Table(
        header=dict(
            values=['State', 'Domestic Violence Against Women'],
            align='left',
            fill_color = '#E4D9C8'
        ),
        cells=dict(
            values=[df_sorted['state'], df_sorted['DomesticViolenceAgainstWomen']],
            align='left',
            fill_color = '#F5EEDF'
        )
    )
])

# page layout
layout = html.Div([
    html.H1('American Examination', style={'textAlign': 'center'}),
    dcc.Graph(id='americanMap', figure=fig),
    dcc.Graph(id='americanTable', figure=table),
    dbc.Button('Link to Next Page', href='/pages/scatterplot1'),
])