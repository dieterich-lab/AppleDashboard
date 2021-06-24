import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from db import connect_db
import modules.load_data_from_database as ldd
from datetime import date

# connection with database
rdb = connect_db()
patient = ldd.patient(rdb)
min_date, max_date = ldd.min_max_date(rdb)

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
                    value='Patient 1',
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
                        options=[{'label': 'HKWorkoutActivityTypeWalking', 'value': 'HKWorkoutActivityTypeWalking'},
                                 {'label': 'HKWorkoutActivityTypeCycling', 'value': 'HKWorkoutActivityTypeCycling'},
                                 {'label': 'HKWorkoutActivityTypeRunning', 'value': 'HKWorkoutActivityTypeRunning'},
                                 {'label': 'HKWorkoutActivityTypeHiking', 'value': 'HKWorkoutActivityTypeHiking'},
                                 ],
                        value='HKWorkoutActivityTypeWalking'
                    )),
            dbc.Col(
                dcc.Dropdown(
                    id='what',
                    style={'height': '40px'},
                    options=[{'label': 'duration', 'value': 'duration'},
                             {'label': 'distance', 'value': 'distance'},
                             {'label': 'totalEnergy', 'value': 'totalEnergy'},
                             ],
                    value='HKWorkoutActivityTypeWalking'
                )),
                dbc.Col(dcc.Dropdown(
                    id='linear plot',
                    style={'height': '40px'},
                    options=[{'label': 'Heart Rate', 'value': 'Heart Rate'},
                             {'label': 'Heart Rate Variability SDNN', 'value': 'Heart Rate Variability SDNN'},
                             {'label': 'Resting Heart Rate', 'value': "Resting Heart Rate"},
                             {'label': 'VO2Max', 'value': 'VO2Max'},
                             {'label': 'Walking Heart Rate Average', 'value': 'Walking Heart Rate Average'},
                             {'label': 'Body Mass', 'value': 'Body Mass'},
                             ],
                    value='Heart Rate'
                )),
            dbc.Col(dcc.DatePickerSingle(
            style={'height': '40px'},
            id='filter-drop_down',
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            display_format='D/M/Y',
            date=date(2020, 5, 20))),

        ]),
    ]
    return selection