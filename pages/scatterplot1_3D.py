from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
import dash_bootstrap_components as dbc
from pathlib import Path
from app import app
import numpy as np
import country_converter as coco
import time

from pages import scatterplot2

# scripts will run regardless of OS
# returns absolute path to datasets
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

# Dataset Author:
# Datasets have been modified
df = pd.read_csv(DATA_PATH.joinpath("salary_data.csv"), encoding='ISO-8859-1')
df2 = pd.read_csv(DATA_PATH.joinpath("modifiedLawsProtectingWomen.csv"), encoding='ISO-8859-1')
df3 = pd.read_csv(DATA_PATH.joinpath("violenceperception.csv"), encoding='ISO-8859-1')


# prepping df2, merging relevant columns into df
df2.rename(columns={'Country':'country_name'}, inplace=True)
df = pd.merge(df, df2[['country_name', '2023', 'lawStatus']], on='country_name', how='left')
# prepping df3, merging relevant columns into df
df3.rename(columns={'Reference area':'country_name'}, inplace=True)
df = pd.merge(df, df3[['country_name', 'OBS_VALUE']], on='country_name', how='left')

df.rename(columns={'median_salary':'Median Salary', 'OBS_VALUE': 'Observed Violence'}, inplace=True)
# creating scatter plot from plotly
fig = px.scatter(df, x="Median Salary", y="Observed Violence", color='lawStatus', hover_name="country_name", hover_data={'lawStatus':True, 'Observed Violence':True})
# changing title of x axis
fig.update_layout(xaxis=dict(
    title = "Median Salary Per Month"
    )
)
# changing title of y axis
fig.update_layout(yaxis=dict(
    title = "% of Women Who Have Experienced Violence"
    )
)
# adjusting template
fig.update_layout(template="plotly_white")

fig.update_traces(marker=dict(symbol="circle", size=7, line=dict(width=0.5, color="black")))

layout = html.Div([
    html.H1('Correlation', style={'textAlign': 'center'}),
    dcc.Graph(id='scatterplot1', figure=fig),
    html.P('3d', style={'textAlign': 'center', 'font-family':'Helvetica', 'font-size': '16px'}),
    html.P("This scatterplot illustrates that nine out of the eleven countries represented, which lack penalties against domestic violence, have an average monthly income of less than two thousand dollars. "
           "This suggests a potential correlation between economic factors and the absence of legal protections. "
           "According to Action Aid, women living in low and lower-middle-income countries are 13% more likely to become victims of domestic violence. ",
           style={'textAlign': 'center', 'color' : 'black', 'font-size': '18px', 'max-width': '900px', 'margin': '0 auto', 'padding': '20px'}),
    dbc.Button("Next Page", href="/pages/scatterplot2"),
])

