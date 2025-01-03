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

df4 = pd.read_csv(DATA_PATH.joinpath('ArkansasDataNEW.csv'), encoding='utf-8-sig')

# For limited data set
df4['Violent'] = df4['Violent'].str.replace(',', '').astype(float)
df4['Violent'] = df4['Violent'].replace({',': ''}, regex=True).astype(float)
# df4.rename(columns={"ï»¿Year" : "Year"}, inplace = True)
df4.columns = df4.columns.str.strip()

y = df4['Violent']
X = df4['Year']

X = X.str.replace(',', '').str.strip()
X = pd.to_numeric(X, errors='coerce')
X = X.astype(float)

plt.scatter(X, y)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state = 17)

X_train = np.array(X_train).reshape(-1,1)
X_test = np.array(X_test).reshape(-1,1)

lr = LinearRegression()
print(X.isnull().sum())  # Check how many NaN values exist in X
print(X[X.isnull()])
lr.fit(X_train, y_train)
# Y = mX + c
c = lr.intercept_
m = lr.coef_
#m = m[0]

X_train = np.array(X_train, dtype=float)

Y_pred_train = m*X_train + c
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
    name='First Training Data',
))

fig2.update_layout(
    title="Arkansas Crime Rate Training Model",
    template="ggplot2",
    xaxis_title="Year",
    yaxis_title="Violent Crime Rate",
)

title = "Arkansas Crime Rate Training Model",

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
    title="Arkansas Crime Rate Linear Regression Model",
    xaxis_title="Year",
    yaxis_title="Violent Crime Rate",
    template="plotly_white"
)


# page layout
layout = html.Div([
    html.H1('Filler', style={'textAlign': 'center', 'font-size': '33px'}),
    html.H1('Predictive Modeling (Arkansas)',
            style={'textAlign': 'center', 'color': 'black', 'font-size': '30px', 'textDecoration': 'underline'}),
    dbc.Stack([
        dcc.Graph(id='regression1', figure=fig2),
        html.P(
            'Arkansas Crime Rate Training Model',
            style={'textAlign': 'center', 'font-size': '16px'}),
        dcc.Graph(id='regression', figure=fig),

    ], gap=3),
    html.P(
        'Linear Regression Model Predicting a Growing Crime Rate',
        style={'textAlign': 'center', 'font-family': 'Trebuchet MS, Arial, sans-serif', 'font-size': '16px'}),

    html.P(
        "National domestic violence statistics show that the state of Arkansas has one of the worst offender rates in the country. This linear regression model which was implemented using Scikit Learn uses Arkansas’s history of domestic violence, beginning in 1960 to 2020. The regression line highlighted on the model predicts that Arkansas’s crime rate will continue to grow at a linear rate if it maintains the same variables that have caused this growth in crime. According to Arkansas State University Criminology Professor Angelo Brown Ph.D., Arkansas’ nation leading crime rate can be attributed to multiple factors shown in this case study including economic disparity and sub par education levels. Note: The data used in this training model was collected before the Covid-19 Pandemic",
        style={'textAlign': 'center', 'color' : 'black', 'font-size': '18px',
               'max-width': '900px', 'margin': '0 auto', 'padding': '20px'}),
])