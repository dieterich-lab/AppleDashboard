import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from db import connect_db
import modules.load_data_from_database as ldd

# connection with database
rdb = connect_db()
patient,label_bar2 = ldd.patient(rdb),ldd.activity(rdb)
label_linear, label_bar = ldd.label(rdb)

# selection for first dropdowns
def selection():
    selection = [
        html.Br(),
        dbc.Row([
            dbc.Col(dbc.Card(
                dcc.Dropdown(
                    style={'height': '40px'},
                    id='group',
                    options=[{'label': 'Patient', 'value': 'Name'},
                             {'label': 'Age', 'value': 'Age'},
                             {'label': 'Sex', 'value': 'Sex'},
                             {'label': 'Illness', 'value': 'Illness'},
                             {'label': 'hours of Apple Watch use', 'value': 'Hours'}],
                    value='Name',
                    clearable=False
                )), style={'height': '100%'}),
            dbc.Col(dbc.Card(
                dcc.Dropdown(
                    style={'height': '40px'},
                    id='group by',
                    options=[{'label': 'by month', 'value': 'M'},
                             {'label': 'by week', 'value': 'W'},
                             {'label': 'by day of week', 'value': 'DOW'},
                             {'label': 'by day', 'value': 'D'}],
                    value='D',
                    clearable=False
                    )),style={'height': '100%'}),
            dbc.Col(dbc.Card(
                    dcc.Dropdown(
                        id='Bar chart',
                        style={'height': '100%'},
                        options=[{'label': name, 'value': name} for name in label_bar],
                        value=label_bar[0],
                        clearable=False,
                    ),)),
            dbc.Col(dbc.Card(dcc.Dropdown(
                    id='linear plot',
                    style={'height': '100%'},
                    options=[{'label': name, 'value': name} for name in label_linear],
                    value=label_linear[1],
                    clearable = False,
            ))),
            dbc.Col(
                dcc.Dropdown(
                    id='Bar chart2',
                    style={'height': '100%'},
                    options=[{'label': name, 'value': name} for name in label_bar2],
                    value=label_bar2[0],
                    clearable=False,
                )),
            dbc.Col(
                dcc.Dropdown(
                    id='what',
                    style={'height': '40px'},
                    options=[{'label': 'duration', 'value': 'duration'},
                             {'label': 'distance', 'value': 'distance'},
                             {'label': 'totalEnergy', 'value': 'totalEnergy'},
                             ],
                    value='duration'
                )),
        ]),
    ]
    return selection