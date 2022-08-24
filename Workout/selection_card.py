import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from db import connect_db
import modules.load_data_from_database as ldd

# connection with database
rdb = connect_db()
patient = ldd.patient(rdb)


# selection for first drop downs
def selection():
    """ Drop downs for Workout tab """
    selection_layout = [
        html.Br(),
        dbc.Row([
            dbc.Col(['Patient selection:',
                dcc.Dropdown(
                    style={'height': '40px'},
                    id='patient',
                    options=[{'label': name, 'value': name} for name in patient],
                    value=patient[0],
                    clearable=False
                )]),
            dbc.Col(['Group by:',
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
            dbc.Col(['Plot:',
                dcc.Dropdown(
                    id='what',
                    style={'height': '40px'},
                    options=[{'label': 'duration', 'value': 'duration'},
                             {'label': 'distance', 'value': 'distance'},
                             {'label': 'totalEnergy', 'value': 'energyburned'},
                             ],
                    value='duration',
                    clearable=False
                )]),
        ]),

    ]
    return selection_layout
