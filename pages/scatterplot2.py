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

# scripts will run regardless of OS
# returns absolute path to datasets
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df1 = pd.read_csv(DATA_PATH.joinpath('laborforcestats.csv'))
df2 = pd.read_csv(DATA_PATH.joinpath('UHC_Data_Country_FP.csv'))
df3 = pd.read_csv(DATA_PATH.joinpath("violenceperception.csv"), encoding='ISO-8859-1')


df1.rename(columns={'Entity' : 'Country'}, inplace = True)
# Getting the latest data from each country
df1 = df1.sort_values(by=['Country', 'Year'], ascending=[True, False])
ndf1 = df1.groupby(by=['Country']).first().reset_index()
# newdf1 displays latest female to male labor force ratio

df2.rename(columns={'WB_cname' : 'Country', 'year' : 'Year', 'iso3c' : 'Code', 'SH.UHC.OOPC.10.ZS' : 'incomeSpent'}, inplace=True)

df2 = df2.sort_values(['Country', 'Year'], ascending=[True, False])
ndf2 = df2.groupby('Country').first().reset_index()

df3.rename(columns={"OBS_VALUE" : 'violenceNum', 'Reference area' : 'Country'}, inplace = True)

ndf1= pd.merge(ndf1, ndf2[['Country', 'incomeSpent']], on='Country', how='left')

ndf1.rename(columns={'Ratio of female to male labor force participation rate (%) (modeled ILO estimate)' : 'Ratio'}, inplace=True)
ndf1 = pd.merge(ndf1, df3[['Country', 'violenceNum']], on='Country', how='left')

ndf1['violenceNumCopy'] = ndf1['violenceNum']

ndf1['violenceNumCopy'].fillna(value=0, inplace=True)
ndf1['violenceNumCopy'] = ndf1['violenceNumCopy'].astype(int)

fig = px.scatter_3d(ndf1, x='Ratio', y='incomeSpent', z='violenceNum', color='Country', size='violenceNumCopy',  opacity=0.7, log_y=True,log_x=True, log_z=True)

layout = html.Div([
    html.H1('Displaying the Correlation Between Healthcare Costs, # of Women in Workforce, and % of Women Who Have Experience Violence', style={'textAlign': 'center'}),
    dcc.Graph(id='scatterplot2', figure=fig),
    html.P(
        'Measuring the correlation between total percentage of women who have experienced violence and median salary per month',
        style={'textAlign': 'center', 'color':'black', 'font-size': '16px'}),

        html.P("This 3D scatter plot, created using Plotly, provides a visualization of the relationship between three variables: workplace diversity, average household spending on healthcare, and total violence experienced. Through this plot, it is clear to see that total healthcare costs have a higher degree of correlation to the total percentage of women who have experienced violence in their respective countries. However, the scatterplot also displays that the countries that have low diversity workforces, such as Afghanistan and Iraq, "
               "report some of the higher violence rates in the world. Furthermore, this analysis solidifies the significance of economic factors, such as healthcare spending, in addressing and mitigating violence on a global scale, while highlighting the need to support economic justice worldwide.",
           style={'textAlign': 'center', 'color':'black', 'font-size': '18px', 'max-width': '900px', 'margin': '0 auto', 'padding': '20px'}),
])


