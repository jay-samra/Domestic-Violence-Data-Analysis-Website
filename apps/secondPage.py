from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from pathlib import Path
from app import app

# scripts will run regardless of OS
# returns absolute path to datasets
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

# Dataset Author: World Bank Group
# Dataset has been modified
df = pd.read_csv(DATA_PATH.joinpath("LawsProtectingWomen.csv"), encoding='ISO-8859-1')

# modifying dataset: renaming relevant columns & adding status of law existence
df = df.rename(columns={'Country Code': 'code', '2023 [YR2023]' : '2023', 'Country Name':'Country'})
df['lawStatus'] = df['2023'].map({'1':'Protections Exist', '0':'No Protections Exist', '..':'No Data'})

# creating choropleth map
mapFig = px.choropleth(df, title="Examining Global Protection Standards", locations="code", color='2023', hover_name="Country", hover_data={'lawStatus': True, '2023': False, 'code':False})

mapFig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.1
))
# page layout
layout = html.Div([
    html.H1('Global Stats', style={'textAlign': 'center'}),
    dcc.Graph(id='globalMap', figure=mapFig),
])