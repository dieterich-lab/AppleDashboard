import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from db import connect_db
import modules.load_data_from_database as ldd

# connection with database
rdb = connect_db()

patient = ldd.patient(rdb)
labels = ldd.label(rdb)


# selection for first drop downs
def selection():
    """ Drop downs for AppleWatch tab """
    selection = [
        html.Br(),
        dbc.Row([
            dbc.Col([
                'Patient selection:',
                dcc.Dropdown(
                    style={'height': '40px'},
                    id='patient',
                    options=[{'label': name, 'value': name} for name in patient],
                    value=patient[0],
                    clearable=False
                )],
                style={'height': '100%'}),
            dbc.Col(['Group by:',
                    dbc.Card(
                        dcc.Dropdown(
                            style={'height': '40px'},
                            id='group by',
                            options=[{'label': 'by month', 'value': 'M'},
                                     {'label': 'by week', 'value': 'W'},
                                     {'label': 'by day of week', 'value': 'DOW'},
                                     {'label': 'by day', 'value': 'D'}],
                            value='D',
                            clearable=False
                        ))], style={'height': '100%'}),
            dbc.Col(['Barchart:',
                     dbc.Card(
                        dcc.Dropdown(
                            id='Bar chart',
                            style={'height': '100%'},
                            options=[{'label': name, 'value': name} for name in labels],
                            value=labels[0],
                            clearable=False,
                        ))]),
            dbc.Col(['Linear plot:',
                    dbc.Card(dcc.Dropdown(
                        id='linear plot',
                        style={'height': '100%'},
                        options=[{'label': name, 'value': name} for name in labels],
                        value=labels[0],
                        clearable=False,
                        multi=True
                    ))]),
            dbc.Col(['Update cards:',
                    html.Div(id='drop_down-container', children=[])]),
        ]),
    ]
    return selection

