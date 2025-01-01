from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
import dash_bootstrap_components as dbc
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
    x=0.1,
))

mapFig.update_layout(margin=dict(l=150, r=150))
mapFig.update_layout(paper_bgcolor="#e0e0e0")

# page layout
layout = html.Div([
    html.H1('A Look Across the Globe', style={'textAlign': 'center', 'font-family':'Trebuchet MS, Arial, sans-serif', 'font-size': '8px'}),
    dcc.Graph(id='globalMap', figure=mapFig),
    html.P('This interactive map displays the existence of laws protecting against domestic violence in every country across the world.', style={'textAlign': 'center', 'font-family':'Trebuchet MS, Arial, sans-serif', 'font-size': '16px'}),
    html.P("This interactive choropleth map highlights the current status of countries worldwide in providing legal protections against domestic violence, "
           "distinguishing between those that have implemented safeguards for their citizens and those that have yet to enact such measures. "
           "According to Our World In Data, twenty years ago, 80% of the world population lived in a country that had no penalties for domestic violence."
           " Today, 90% of the world population live in countries with legal policies to penalize domestic violence. "
           "This trend reflects significant progress in the global effort to combat violence, "
           "underscoring society's commitment to addressing this issue and we will continue to learn more about the factors that cause domestic violence.",
           style={'textAlign': 'center',  'color' : 'black', 'font-size': '18px', 'max-width': '900px', 'margin': '0 auto', 'padding': '20px'}),
])