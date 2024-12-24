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

# Dataset Author: United States Department of Agriculture
df = pd.read_csv(DATA_PATH.joinpath("educationData.csv"), encoding='unicode_escape')
# Dataset Author: World Population Review
df2 = pd.read_csv(DATA_PATH.joinpath('americanRates.csv'))

# Cleaning data
df.drop(0, inplace=True)
df.reset_index(inplace=True)
df.drop('Unnamed: 1', axis=1, inplace=True)
df.rename(columns = {"Unnamed: 7" : "educationRate", 'Unnamed: 0' : 'state'}, inplace=True)

# merging dataset after cleaning
df = pd.merge(df, df2[['state', 'DomesticViolenceAgainstWomen']], on='state', how='left')

df.fillna(0)
df.drop(0, inplace=True)
df.drop(31, inplace=True)

# fixing read error
df['educationRate'] = df['educationRate'].str.replace(r'[^0-9.]', '', regex=True)
df['educationRate'] = df['educationRate'].str.strip()

df['educationRate'] = pd.to_numeric(df['educationRate'], errors='coerce')

# creatinf first scatterplot containing all states
fig1 = px.scatter(df, x='DomesticViolenceAgainstWomen', y='educationRate', size='educationRate', hover_data=['state'])
fig1.update_layout(
    xaxis_title='% of Women Who Have Experienced Violence',
    yaxis_title='% of Population With No College Education'
)
# creating seconf scatterplot containing only worst 10 states
df['Ranking'] = '>10'
# assigning states
dvRankings = {"Kentucky": '<=10', "Mississippi": '<=10', "Nevada": '<=10', "Alaska": '<=10',
             "Arizona": '<=10', "Indiana": '<=10', "South Carolina": '<=10', "Missouri": '<=10',
             "Oklahoma": '<=10', "Arkansas": '<=10', "Maine": '<=10',}
df['Ranking'] = df['state'].map(dvRankings)

values = {'Ranking' : '>10'}
df.fillna(value=values)

fig2 = px.scatter(df, x='DomesticViolenceAgainstWomen', y='educationRate', size='educationRate', hover_data=['state'],
                 color='Ranking')
fig2.update_layout(
    xaxis={
        'range': [28, 47]
    },
    xaxis_title='% of Women Who Have Experienced Violence',
    yaxis_title='% of Population With No College Education'

)

# page layout
layout = html.Div([
html.H1('Looking For Trends', style={'textAlign': 'center'}),
        dbc.Stack([
            html.Div(dcc.Graph(id='americanscatterplot1', figure=fig1),),
            html.Div(dcc.Graph(id='americanscatterplot2', figure=fig2),),
        ], gap=3)
])




# dbc.Button('Link to Next Page', href='/pages/scatterplot1'),

