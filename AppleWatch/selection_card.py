import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from db import connect_db
import modules.load_data_from_database as ldd

# connection with database
rdb = connect_db()
patient = ldd.patient(rdb)
min_max_date = ldd.min_max_date(rdb)
min_date = min_max_date['min'].iloc[0]
min_date = min_date.date()
max_date = min_max_date['max'].iloc[0]
max_date = max_date.date()


# selction for first dropdowns
def selection():
    selection = [
        html.Br(),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    style={'height': '40px'},
                    id='patient',
                    options=[{'label': name, 'value': name} for name in patient],
                    value='Patient1',
                )]),
            dbc.Col([
                dcc.Dropdown(
                    style={'height': '40px'},
                    id='group by',
                    options=[{'label': 'by month', 'value': 'M'},
                             {'label': 'by week', 'value': 'W'},
                             {'label': 'by day of week', 'value': 'DOW'},
                             {'label': 'by day', 'value': 'D'}],
                    value='D'
                    )]),
            dbc.Col(
                    dcc.Dropdown(
                        id='Bar chart',
                        style={'height': '40px'},
                        options=[{'label': 'Active Energy Burned', 'value': 'Active Energy Burned'},
                                 {'label': 'Apple Exercise Time', 'value': 'Apple Exercise Time'},
                                 {'label': 'Apple Stand Time', 'value': 'Apple Stand Time'},
                                 {'label': 'Basal Energy Burned', 'value': 'Basal Energy Burned'},
                                 {'label': 'Distance Cycling', 'value': 'Distance Cycling'},
                                 {'label': 'Distance Walking Running', 'value': 'Distance Walking Running'},
                                 {'label': 'Sleep Analysis', 'value': 'Sleep Analysis'},
                                 {'label': 'Step Count', 'value': 'Step Count'}
                                 ],
                        value='Active Energy Burned'
                    )),
                dbc.Col(dcc.Dropdown(
                    id='linear plot',
                    style={'height': '40px'},
                    options=[{'label': 'Heart Rate', 'value': 'Heart Rate'},
                             {'label': 'Heart Rate Variability SDNN', 'value': 'Heart Rate Variability SDNN'},
                             {'label': 'Resting Heart Rate', 'value': "Resting Heart Rate'"},
                             {'label': 'VO2Max', 'value': 'VO2Max'},
                             {'label': 'Walking Heart Rate Average', 'value': 'Walking Heart Rate Average'},
                             {'label': 'Body Mass', 'value': 'Body Mass'},
                             ],
                    value='Heart Rate'
                )),
            dbc.Col([
                html.Div(id='drop_down-container', children=[])
            ]),
        ]),
    ]
    return selection

