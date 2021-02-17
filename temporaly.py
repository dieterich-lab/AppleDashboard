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

dcc.Tab(
    label='About',
    value='what-is',
    children=html.Div(className='control-tab', children=[
        html.H4(className='what-is', children='Information about patient'),
        html.P('Age of Patient: 26 '),
        html.P('Weight: {0} last date: Height: {1}   last date:'.format(weight, height)),
        html.P("Patient's disease: None"),
        html.P('Number of inconclusive ECG:{}'.format(ECG_inconclusive.iloc[0]['count'])),
        html.P('Number of irregular ECG:{0} Over 150: {1} Under 50: {2}'
               .format(ECG_irregular.iloc[0]['count'], ECG_over_120.iloc[0]['count'], ECG_under_50
                       .iloc[0]['count'])),
        html.P('The number of days the Apple Watch has been worn for at least 6h:'),
    ]))