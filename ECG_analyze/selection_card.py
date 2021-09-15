import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from db import connect_db
import modules.load_data_from_database as ldd

# connection with database
rdb = connect_db()
patient = ldd.patient(rdb)

features_list = ['hrvOwn', 'SDNN', 'SENN', 'SDSD', 'pNN20', 'pNN50', 'lf', 'hf', 'lf_hf_ratio', 'total_power', 'vlf']

# selection for first dropdowns
def selection():
    selection = [
        html.Br(),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    style={'height': '40px'},
                    id='patient',
                    options=[{'label': name, 'value': name} for name in patient],
                    value=patient[0],
                    clearable=False
                )], style={'height': '100%'}),
            dbc.Col(dbc.Card(
                dcc.Dropdown(
                    style={'height': '40px'},
                    id='group by',
                    options=[{'label': 'Patient', 'value': 'P'},
                             {'label': 'Classification', 'value': 'C'}],
                    value='P',
                    clearable=False
                )), style={'height': '100%'}),
            dbc.Col(dbc.Card(
                dcc.Dropdown(
                    id='x axis',
                    style={'height': '100%'},
                    options=[{'label': name, 'value': name} for name in features_list],
                    value=features_list[0],
                    clearable=False,
                ), )),
            dbc.Col(dbc.Card(dcc.Dropdown(
                id='y axis',
                style={'height': '100%'},
                options=[{'label': name, 'value': name} for name in features_list],
                value=features_list[1],
                clearable=False,
            ))),

        ]),
    ]
    return selection