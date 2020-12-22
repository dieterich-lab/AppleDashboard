import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html



def selection():
    selection = [
        html.Br(),
        dbc.Row([dbc.Col(
            [
            "Select Patient:",
            dcc.Dropdown(
                id ='patients1',
                options=[{'label': 'Patient 1', 'value': 'Patient1'},
                         {'label': 'Patient 2', 'value': 'Patient2'},
                         {'label': 'Patient 3', 'value': 'Patient3'}],
                value='Patient1',
            ),], ), ]),
        html.Br(),
        dbc.Row([dbc.Col(
            ["Plot:",
             dcc.Dropdown(
                 id='Bar chart',
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
             ), ], ), ]),
        dbc.Row(dbc.Col([
            "and:",
            dcc.Dropdown(
                id='linear plot',
                options=[{'label': 'Heart Rate', 'value': 'Heart Rate'},
                         {'label': 'Heart Rate Variability SDNN', 'value': 'Heart Rate Variability SDNN'},
                         {'label': "Resting Heart Rate'", 'value': "Resting Heart Rate'"},
                         {'label': 'VO2Max', 'value': 'VO2Max'},
                         {'label': 'Walking Heart Rate Average', 'value': 'Walking Heart Rate Average'},
                         ],
                value='Heart Rate'
            ), ]), ),
        html.Br(),
        dbc.Row(
            [dbc.Col(
                [
                    "Group by:",
                    dcc.Dropdown(
                        id='group by',
                        options=[{'label': 'by month', 'value': 'M'},
                                 {'label': 'by week', 'value': 'W'},
                                 {'label': 'by day of week', 'value': 'DOW'},
                                 {'label': 'by day', 'value': 'D'}],
                        value='D'
                    ), ],
            ), ], ),
        html.Br(),
        dbc.Row(
            [dbc.Col(
                [
                    "Select:",
                    html.Div(id='dropdown-container', children=[]), ],
            ), ], ),
        html.Br(),
        dbc.Col(dcc.RadioItems(
            id='choice',
            options=[
                {'label': 'Sum', 'value': 'sum'},
                {'label': 'Mean', 'value': 'mean'},
            ],
            value='sum',

        ))

    ]
    return selection



