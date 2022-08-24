import dash_bootstrap_components as dbc
from dash import dcc
from dash import html


# selection for first drop downs
def selection(hrv_features):
    """ Drop downs for ECG tab """
    selection_layout = [
        html.Br(),
        dbc.Row([dbc.Col([
            html.Div([
                'X axis:',
                dcc.Dropdown(
                    id='x axis',
                    style={'height': '100%'},
                    options=[{'label': name, 'value': name} for name in hrv_features],
                    value=hrv_features[0],
                    clearable=False,
                )]),
            html.Div([
                'Y axis:',
                dcc.Dropdown(
                    id='y axis',
                    style={'height': '100%'},
                    options=[{'label': name, 'value': name} for name in hrv_features],
                    value=hrv_features[1],
                    clearable=False,
                )])])
        ]),
    ]
    return selection_layout
