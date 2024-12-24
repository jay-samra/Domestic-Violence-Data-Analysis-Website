import dash
import dash_bootstrap_components as dbc
from dash import html

# meta tags for mobile use
# MORPH, MINTY,
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY], suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
# Server for Gunicorn
server = app.server

# Layout definition (should work)
app.layout = html.Div([
    dbc.NavbarSimple(
        brand="Domestic Violence: A Global & National Case Study",
        color="#2E856E", dark=True,
    ),

])