import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from db import connect_db
import modules.load_data_from_database as ldd

# connection with database
rdb = connect_db()
patient, label_bar = ldd.patient(rdb), ldd.activity_type(rdb)
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
                        options=[{'label': 'Patient', 'value': 'patient_id'},
                                 {'label': 'Age', 'value': 'age'},
                                 {'label': 'Sex', 'value': 'sex'}],
                        value='patient_id',
                        clearable=False
                    ))], style={'height': '100%'}),
            dbc.Col([
                'X axis',
                dbc.Card(
                    dcc.Dropdown(
                        id='Bar chart',
                        style={'height': '100%'},
                        options=[{'label': name, 'value': name} for name in list(labels.keys())],
                        value=list(labels.keys())[0],
                        clearable=False,
                    ))]),
            dbc.Col([
                'Y axis',
                dbc.Card(dcc.Dropdown(
                    id='linear plot',
                    style={'height': '100%'},
                    options=[{'label': name, 'value': name} for name in labels],
                    value=list(labels.keys())[0],
                    clearable=False,
                ))]),
        ]),
    ]
    selection_workout = [html.Br(),
                         dbc.Row([dbc.Col(['Show heart rate during',
                                           dcc.Dropdown(
                                                id='Bar chart2',
                                                style={'height': '100%'},
                                                options=[{'label': name, 'value': name} for name in label_bar],
                                                value='Walking',
                                                clearable=False,
                                            )])])]
    return selection_health, selection_workout
