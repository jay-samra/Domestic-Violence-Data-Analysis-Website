import pandas as pd
import numpy as np
import pathlib
import country_converter as coco
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df4 = pd.read_csv(DATA_PATH.joinpath('NewYorkData.csv'), encoding='latin1')

# For limited data set
df4['Violent'] = df4['Violent'].str.replace(',', '').astype(float)
df4['Violent'] = df4['Violent'].replace({',': ''}, regex=True).astype(float)

df4.columns = df4.columns.str.strip()

y = df4['Violent']
X = df4['Year']

# print(type(X))
# print(type(y))
# print(X.isnull().sum())
# print(y.isnull().sum())
# print(X.dtype)
# print(y.dtype)

X = X.str.replace(',', '').str.strip()
X = pd.to_numeric(X, errors='coerce')
X = X.astype(float)

plt.scatter(X, y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=17)

X_train = np.array(X_train).reshape(-1, 1)
X_test = np.array(X_test).reshape(-1, 1)

lr = LinearRegression()

lr.fit(X_train, y_train)
# Y = mX + c
c = lr.intercept_
m = lr.coef_
# m = m[0]

X_train = np.array(X_train, dtype=float)

Y_pred_train = m * X_train + c
Y_pred_train.flatten()

# predict calculates the same
y_pred_train1 = lr.predict(X_train)

plt.scatter(X_train, y_train)
plt.plot(X_train, y_pred_train1, color="red")

fig = go.Figure()
fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=X,
    y=y,
    mode='markers',
    name='First Training Data'
))

fig2.update_layout(
    title="New York Crime Rate Training Model",
    template="ggplot2",
    xaxis_title="Year",
    yaxis_title="Violent Crime Rate",
)

fig.add_trace(go.Scatter(
    x=X_train.flatten(),
    y=y_train,
    mode='markers',
    name='Training Data'
))

fig.add_trace(go.Scatter(
    x=X_train.flatten(),
    y=y_pred_train1,
    mode='lines',
    name='Regression Line',
    line=dict(color='red')
))

fig.update_layout(
    title="New York Crime Rate Linear Regression Model",
    xaxis_title="Year",
    yaxis_title="Violent Crime Rate",
    template="plotly_white"
)

# page layout
layout = html.Div([
    html.H1('Filler', style={'textAlign': 'center', 'font-size': '33px'}),
    html.H1('Predictive Modeling (New York)',
            style={'textAlign': 'center', 'color': 'black', 'font-size': '30px', 'textDecoration': 'underline'}),
    dbc.Stack([
        dcc.Graph(id='regression1', figure=fig2),
        html.P(
        'New York Crime Rate Training Model',
        style={'textAlign': 'center', 'font-size': '16px'}),
        dcc.Graph(id='regression', figure=fig),

    ], gap=3),
    html.P(
        'Linear Regression Model Predicting a Falling Crime Rate',
        style={'textAlign': 'center', 'font-size': '16px'}),

    html.P(
        "Linear regression testing conducted using Scikit-learn revealed that New York has experienced a significant decline in crime rates since its peak in 1990. Consequently, the state now reports one of the lowest domestic violence crime rates in the nation. According to economists and university professors Hope Corman and Naci Mocan, the decrease in unemployment rates and the rise in wage equality in New York are likely key factors contributing to this notable reduction in crime. Note: The data used in this training model was collected before the Covid-19 Pandemic",
        style={'textAlign': 'center',  'color' : 'black', 'font-size': '18px',
               'max-width': '900px', 'margin': '0 auto', 'padding': '20px'}),
])