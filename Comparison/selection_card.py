import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from db import connect_db
import modules.load_data_from_database as ldd

# connection with database
rdb = connect_db()
patient = ldd.patient(rdb),
labels = ldd.label(rdb)


# selection for first drop downs
def selection():
    """ Drop downs for Comparison tab """
    selection_health = [
        html.Br(),
        dbc.Row([
            dbc.Col([
                'Group by:',
                dbc.Card(
                    dcc.Dropdown(
                        style={'height': '40px'},
                        id='group',
                        options=[{'label': 'Patient', 'value': 'Name'},
                                 {'label': 'Age', 'value': 'Age'},
                                 {'label': 'Sex', 'value': 'Sex'}],
                        value='Name',
                        clearable=False
                    ))], style={'height': '100%'}),
            dbc.Col([
                'First plot(x axis)',
                dbc.Card(
                    dcc.Dropdown(
                        id='Bar chart',
                        style={'height': '100%'},
                        options=[{'label': name, 'value': name} for name in labels],
                        value=labels,
                        clearable=False,
                    ))]),
            dbc.Col([
                'Second plot(y axis)',
                dbc.Card(dcc.Dropdown(
                    id='linear plot',
                    style={'height': '100%'},
                    options=[{'label': name, 'value': name} for name in labels],
                    value=labels,
                    clearable=False,
                ))]),
        ]),
    ]

    return selection_health
