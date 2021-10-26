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
            dbc.Col([
                'Group by:',
                dbc.Card(
                dcc.Dropdown(
                    style={'height': '40px'},
                    id='group',
                    options=[{'label': 'Patient', 'value': 'Name'},
                             {'label': 'Age', 'value': 'Age'},
                             {'label': 'Sex', 'value': 'Sex'},
                             #{'label': 'Illness', 'value': 'Illness'},
                             #{'label': 'hours of Apple Watch use', 'value': 'Hours'}
                             ],
                    value='Name',
                    clearable=False
                ))], style={'height': '100%'}),
            dbc.Col([
                'First plot(x axis)',
                dbc.Card(
                    dcc.Dropdown(
                        id='Bar chart',
                        style={'height': '100%'},
                        options=[{'label': name, 'value': name} for name in label_bar],
                        value=label_bar[0],
                        clearable=False,
                    ))]),
            dbc.Col([
                'Second plot(y axis)',
                dbc.Card(dcc.Dropdown(
                    id='linear plot',
                    style={'height': '100%'},
                    options=[{'label': name, 'value': name} for name in label_linear],
                    value=label_linear[1],
                    clearable = False,
            ))]),
            dbc.Col([
                'Show heart rate during',
                dcc.Dropdown(
                    id='Bar chart2',
                    style={'height': '100%'},
                    options=[{'label': name, 'value': name} for name in label_bar2],
                    value='Walking',
                    clearable=False,
                )]),
        ]),
    ]
    return selection