from app import app
from datetime import datetime
from Card import Card
from trend_figure import figur_trend
from summary_figure import figur2
from day_figure import figur3
from ECG import figur_ECG
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime as dt
from dash.dependencies import Input, Output, ALL


#Header
Header = [
    dbc.Col(html.H1('HiGHmed patient dashboard',
        style={
            'textAlign': 'center',
        }),)
]
Tab =[
    dcc.Tabs([
        dcc.Tab(label='Apple Watch', value='tab-1',),
        dcc.Tab(label='Medical data', value='tab-2'),
        dcc.Tab(label='Questionnaire', value='tab-3'),
    ],
    id="tabs",
    ),

]

#Selection
selection = [
    html.Br(),
    dbc.Row([dbc.Col(
        [
        "Select Patient:",
        dcc.Dropdown(
            id ='patients',
            options=[{'label': 'Patient 1', 'value': '1'},
                     {'label': 'Patient 2', 'value': '2'},
                     {'label': 'Patient 3', 'value': '3'}],
            value='1'
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
                     {'label': 'Resting Heart Rate', 'value': 'Resting Heart Rate'},
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

]

# Card components
cards1 = [
    dbc.Row([dbc.Col(
    dbc.Card(
        [
            html.P("Resting Heart Rate Average", className="card-text"),
            html.H2(id='RestingHeartRate', className="card-title"),
        ],

        body=True,
        color="light",
        style={"width": "18rem"},

    ),),
    dbc.Col(
    dbc.Card(
        [
            html.P("Walking Heart Rate Average", className="card-text"),
            html.H2(id= 'WalkingHeartRate', className="card-title"),
        ],
        body=True,
        color="light",
        style={"width": "18rem"},
    ),),]),
    dbc.Row([dbc.Col(
        dbc.Card(
            [
                html.P("Average Heart Rate", className="card-text"),
                html.H2(id='HeartRate_mean', className="card-title"),
            ],
            body=True,
            color="light",
            style={"width": "18rem"},
        ), ),
        dbc.Col(
            dbc.Card(
                [
                    html.P("Steps", className="card-text"),
                    html.H2(id='step', className="card-title"),
                ],
                body=True,
                color="light",
                style={"width": "18rem"},
            ), ), ]),
    dbc.Row([dbc.Col(
        dbc.Card(
            [
                html.P("Active Calories", className="card-text"),
                html.H2(id ='ActivitySummary2', className="card-title"),
            ],
            body=True,
            color="light",
            style={"width": "18rem"},
        ), ),
        dbc.Col(
            dbc.Card(
                [
                    html.P("Exercise minutes", className="card-text"),
                    html.H2(id='Exercise_minute', className="card-title"),
                ],
                body=True,
                color="light",
                style={"width": "18rem"},
            ), ), ]),


]

#Graph

graphs3 = [
    [
        dcc.Graph(
            id='example-graph2',
        )
    ],

]

graphs1 = [
    dcc.Graph(
        id='example-graph1',
    )
]

graphs4 = [
    [
        dcc.Graph(
            id='example-graph3',

        )
    ],


]

graphs5 = [
    [
        dcc.Graph(
            id='example-graph4',

        )
    ],

]


layout = html.Div([
    dbc.Row(Header),
    dbc.Card(Tab),
    dbc.Row([
        dbc.Col(dbc.Card(dbc.Col(selection)), width=3),
        dbc.Col([(card) for card in cards1], width=4),
        dbc.Col([dbc.Col(graph) for graph in graphs3], )]),
    dbc.Row([dbc.Col(graph) for graph in graphs1]),
    html.Br(),
    dbc.Col([dbc.Col(graph) for graph in graphs5]),
    html.Br(),
    dbc.Row([dbc.Col(graph) for graph in graphs4]),
    html.Div(id='app-1-display-value'),
    dcc.Link('Go to App 2', href='/apps/AppleWatch')
])
@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    Output('dropdown-container', 'children'),
    [Input('group by', "value")],
)
def update_figureg(value):
    if value == 'M':
        new_dropdown = dcc.Dropdown(
            id= {
            'type': 'filter-dropdown',
            'index': 0
        },
            options=[{'label': name, 'value': i} for (i,name) in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August','September','October','November','December'],1)],
            value='1'
        )
    elif value == 'W':
        week = []
        for i in range(1, 53):
            a = datetime.strptime('2020 {} 1'.format(i), '%G %V %u').date()
            b = datetime.strptime('2020 {} 7'.format(i), '%G %V %u').date()
            c = str(a)+'-'+ str(b)
            week.append(c)

        new_dropdown = dcc.Dropdown(
            id={
            'type': 'filter-dropdown',
            'index': 0
        },
            options=[{'label': name, 'value': i} for (i,name) in enumerate(week,1)],
            value='1'
        )
    elif value == 'DOW':
        new_dropdown = dcc.Dropdown(
            id={
            'type': 'filter-dropdown',
            'index': 0
        },
            options=[{'label': name, 'value': i} for (i,name) in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                                                                            'Friday', 'Saturday', 'Sunday'],1)],
            value = '1'
        )
    else:
        new_dropdown = dcc.DatePickerSingle(
            id={
                'type': 'filter-dropdown',
                'index': 0
            },
            min_date_allowed=dt(2015, 8, 5),
            max_date_allowed=dt(2021, 9, 19),
            initial_visible_month=dt(2020, 3, 27),
            display_format='D/M/Y',
            date=str(dt(2020, 2, 27, 23, 59, 59)))

    return new_dropdown

@app.callback(
    [Output("RestingHeartRate", "children"),
     Output("WalkingHeartRate", "children"),
     Output("step", "children"),
     Output("HeartRate_mean", "children"),
     Output("Exercise_minute", "children"),
     Output("ActivitySummary2", "children")],
    [Input( {"index":ALL,'type':'filter-dropdown'}, 'date'),
     Input( {"index":ALL,'type':'filter-dropdown'}, 'value'),
     Input("group by", "value")],
)
def Update_Card(date,value,group):
    for date in date:
        date=pd.to_datetime(date)
        if date == None or not date:
            date=0
        else:
            date=date
    for value in value:
        value=value
    RestingHeartRate,WalkingHeartRate,step,HeartRate_mean,Exercise_minute,ActivitySummary2= Card(date,value,group)
    return RestingHeartRate,WalkingHeartRate,step,HeartRate_mean,Exercise_minute,ActivitySummary2

@app.callback(
    Output('example-graph2', 'figure'),
    [Input({'index':ALL,'type':'filter-dropdown'}, 'date'),
     Input( {"index":ALL,'type':'filter-dropdown'}, 'value'),
     Input('linear plot', 'value'),
     Input("group by", "value")],
)
def update_figure_trend(date,value,input_value,group):
    for date in date:
        date = pd.to_datetime(date)
    for value in value:
        value=value
    figa=figur_trend(date,value,input_value,group)


    return figa



@app.callback(
    Output('example-graph1', 'figure'),
    [Input('linear plot', 'value'),
     Input('Bar chart', 'value'),
     Input("group by", "value")]
)
def update_figure2(input_value1,input_value2,group):
    fig=figur2(input_value1,input_value2,group)
    return fig


@app.callback(
    Output('example-graph4', 'figure'),
    [Input( {"index":ALL,'type':'filter-dropdown'}, 'date'),]
)
def update_figure3(date):
    for date in date:
        date = pd.to_datetime(date)
    if date == None or not date :
        fig3={}
    else:
        fig3=figur3 (date)
    return fig3


@app.callback(
    Output('example-graph3', 'figure'),
    [Input( {"index":ALL,'type':'filter-dropdown'}, 'date'),]
)
def update_figure3(date):
    for date in date:
        if date == None or not date :
            fig={}
        else:
            date = pd.to_datetime(date).date()
            fig=figur_ECG(date)
    return fig
