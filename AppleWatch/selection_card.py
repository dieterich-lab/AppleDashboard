import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from db import connect_db
import modules.load_data_from_database as ldd

# connection with database
rdb = connect_db()
patient = ldd.patient(rdb)
label_linear, label_bar = ldd.label(rdb)

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
                )],style={'height': '100%'}),
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
                    multi=True
            ))),
            dbc.Col([
                html.Div(id='drop_down-container', children=[])
            ]),
        ]),
    ]
    return selection

