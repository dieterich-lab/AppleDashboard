import dash_bootstrap_components as dbc
from dash import dcc
from dash import html


# selection for first drop-downs
def selection(patient):
    """ Drop-downs for Workout tab """
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
                         options=[{'label': 'by month', 'value': 'month'},
                                  {'label': 'by week', 'value': 'week'},
                                  {'label': 'by day of week', 'value': 'DOW'},
                                  {'label': 'by date', 'value': 'date'}],
                         value='date',
                         clearable=False)]),
            dbc.Col(['Plot:',
                     dcc.Dropdown(
                        id='what',
                        style={'height': '40px'},
                        options=[{'label': 'duration', 'value': 'duration'},
                                 {'label': 'distance', 'value': 'distance'},
                                 {'label': 'totalEnergy', 'value': 'energyburned'}],
                        value='duration',
                        clearable=False)]),
        ]),
    ]
    return selection_layout
