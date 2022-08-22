import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from db import connect_db
import modules.load_data_from_database as ldd

# connection with database
rdb = connect_db()
patient = ldd.patient(rdb)

hrv_features = ['hrv', 'sdnn', 'senn', 'sdsd', 'pnn20', 'pnn50']


# selection for first drop downs
def selection():
    """ Drop downs for ECG tab """
    selection = [
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
    return selection