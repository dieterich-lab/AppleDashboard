import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from db import connect_db
import modules.load_data_from_database as ldd
from datetime import date

# connection with database
rdb = connect_db()
patient,label_bar = ldd.patient(rdb),ldd.activity(rdb)


# selection for first drop downs
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
                )]),
            dbc.Col([
                dcc.Dropdown(
                    style={'height': '40px'},
                    id='group by',
                    options=[{'label': 'by month', 'value': 'M'},
                             {'label': 'by week', 'value': 'W'},
                             {'label': 'by day of week', 'value': 'DOW'},
                             {'label': 'by day', 'value': 'D'}],
                    value='D',
                    clearable=False
                    )]),
            dbc.Col(dbc.Card(
                dcc.Dropdown(
                    id='activity',
                    style={'height': '100%'},
                    options=[{'label': name, 'value': name} for name in label_bar],
                    value=label_bar[0],
                    clearable=False,
                ), )),
            dbc.Col(
                dcc.Dropdown(
                    id='what',
                    style={'height': '40px'},
                    options=[{'label': 'duration', 'value': 'duration'},
                             {'label': 'distance', 'value': 'distance'},
                             {'label': 'totalEnergy', 'value': 'EnergyBurned'},
                             ],
                    value='duration',
                    clearable=False
                )),
            dbc.Col([
                html.Div(id='drop_down-container2', children=[])
            ]),

        ]),

    ]
    return selection