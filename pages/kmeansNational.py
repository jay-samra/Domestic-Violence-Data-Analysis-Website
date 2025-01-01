import plotly.express as px
import pandas as pd
import pathlib
from dash import dcc, html
import dash_bootstrap_components as dbc
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
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

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("educationData.csv"), encoding='unicode_escape')
df2 = pd.read_csv(DATA_PATH.joinpath('americanRates.csv'))

df.drop(0, inplace=True)
df.reset_index(inplace=True)
df.drop('Unnamed: 1', axis=1, inplace=True)
df.rename(columns={"Unnamed: 7": "educationRate", 'Unnamed: 0': 'state'}, inplace=True)

df = pd.merge(df, df2[['state', 'DomesticViolenceAgainstWomen']], on='state', how='left')
df.fillna(0, inplace=True)
df.drop(0, inplace=True)
df.drop(31, inplace=True)

df['educationRate'] = df['educationRate'].str.replace(r'[^0-9.]', '', regex=True)
df['educationRate'] = df['educationRate'].str.strip()
df['educationRate'] = pd.to_numeric(df['educationRate'], errors='coerce')

# KMeans clustering
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[['DomesticViolenceAgainstWomen', 'educationRate']])

kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit(scaled_data)

labels = kmeans.labels_
df['Cluster'] = labels

plot_data = pd.DataFrame(scaled_data, columns=['Violence', 'Education'])
plot_data['Cluster'] = labels

# creating scatter plot
fig = px.scatter(plot_data, x='Violence', y='Education', color='Cluster',
                 title='KMeans Clustering', labels={'Violence': '% of Women Who Have Experienced Violence', 'Education': '% of Population With No College Education'},
                 color_continuous_scale='viridis')

fig.update_layout(
    template="ggplot2",
)
# Add centroids to the Plotly plot
for i, centroid in enumerate(kmeans.cluster_centers_):
    fig.add_trace(go.Scatter(x=[centroid[0]], y=[centroid[1]], mode='markers', marker=dict(color='red', size=12, symbol='x'),
                             name=f'Centroid {i}'))

# page layout
layout = html.Div([
    html.H1('Filler', style={'textAlign': 'center', 'font-size': '33px'}),
    html.H1('American Data Clustering & Segmentation',
            style={'textAlign': 'center', 'color': 'black', 'font-size': '30px', 'textDecoration': 'underline'}),
    dbc.Stack([
        dcc.Graph(id='kmeans', figure=fig),
    ], gap=3),
    html.P(
        'Measuring the correlation between total percentage of women who have experienced violence and median salary per month',
        style={'textAlign': 'center', 'color': 'black', 'font-size': '16px'}),

    html.P(
        "The unsupervised learning algorithm K-Means was applied with three centroids to segment the data into three distinct clusters. Cluster 1 encompasses states characterized by low domestic violence rates and high levels of college-educated individuals. Cluster 2 identifies states with a high proportion of residents lacking a college education, accompanied by elevated domestic violence rates. Cluster 0 represents states where educational attainment is comparable to Cluster 1, but domestic violence rates are moderately higher. Clustering and segmentation are essential techniques in data science, as they facilitate the identification of underlying patterns and relationships within complex datasets, enabling data-driven strategies for targeted solutions and informed decision-making.",
        style={'textAlign': 'center', 'color': 'black', 'font-size': '18px',
               'max-width': '900px', 'margin': '0 auto', 'padding': '20px'}),
])
