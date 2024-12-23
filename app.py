import dash
import dash_bootstrap_components as dbc


# meta tags for mobile use
# MORPH, MINTY,
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY],suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

# if __name__ == '__main__':
#     app.run_server(debug=True)