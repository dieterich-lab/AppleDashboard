import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime as dt
from dash.dependencies import Input, Output
import flask
import modules.load_data_from_database as ldd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go




server = flask.Flask(__name__)
app = dash.Dash(__name__,
                server=server,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config['suppress_callback_exceptions'] = True


colors = {
    'background': '#e7e7e7',
    'text': '#7FDBFF'
}

def all_data():
    df1,df2,df3 = ldd.Card(ldd.rdb)

def Card(date):
    RestingHeartRate, WalkingHeartRate, step, HeartRate_mean, Exercise_minute, ActivitySummary2 = ldd.Card(ldd.rdb)
    get_date = lambda x: x.date()

    RestingHeartRate['@creationDate'] = pd.to_datetime(RestingHeartRate['@creationDate'])
    WalkingHeartRate['@creationDate'] = pd.to_datetime(WalkingHeartRate['@creationDate'])
    step['@creationDate'] = pd.to_datetime(step['@creationDate'])
    HeartRate_mean['@creationDate'] = pd.to_datetime(HeartRate_mean['@creationDate'])
    Exercise_minute['@creationDate'] = pd.to_datetime(Exercise_minute['@creationDate'])
    ActivitySummary2['@creationDate'] = pd.to_datetime(ActivitySummary2['@creationDate'])

    RestingHeartRate['date'] = RestingHeartRate['@creationDate'].map(get_date)
    WalkingHeartRate['date'] = WalkingHeartRate['@creationDate'].map(get_date)
    step['date'] = step['@creationDate'].map(get_date)
    HeartRate_mean['date'] = HeartRate_mean['@creationDate'].map(get_date)
    Exercise_minute['date'] = Exercise_minute['@creationDate'].map(get_date)
    ActivitySummary2['date'] = ActivitySummary2['@creationDate'].map(get_date)

    RestingHeartRate = RestingHeartRate.loc[RestingHeartRate['date'] == date]

    WalkingHeartRate = WalkingHeartRate.loc[WalkingHeartRate['date'] == date]
    step = step.loc[step['date'] == date]
    HeartRate_mean = HeartRate_mean.loc[HeartRate_mean['date'] == date]
    Exercise_minute = Exercise_minute.loc[Exercise_minute['date'] == date]
    ActivitySummary2 = ActivitySummary2.loc[ActivitySummary2['date'] == date]

    RestingHeartRate = RestingHeartRate.iloc[0]['@Value']
    WalkingHeartRate = str(WalkingHeartRate.iloc[0]['@Value'])
    step['@Value'] = pd.to_numeric(step['@Value'])
    step = step['@Value'].sum()


    HeartRate_mean['@Value'] = pd.to_numeric(HeartRate_mean['@Value'])
    HeartRate_mean=HeartRate_mean['@Value'].mean()
    HeartRate_mean = round(HeartRate_mean, 2)


    Exercise_minute['@Value'] = pd.to_numeric(Exercise_minute['@Value'])
    Exercise_minute = Exercise_minute['@Value'].sum()


    ActivitySummary2['@Value'] = pd.to_numeric(ActivitySummary2['@Value'])
    ActivitySummary2 = ActivitySummary2['@Value'].sum()
    ActivitySummary2 = round(ActivitySummary2, 2)
    return RestingHeartRate, WalkingHeartRate,step, HeartRate_mean, Exercise_minute, ActivitySummary2

def figur_trend(date,input_value):

    get_hour = lambda x: x.hour
    get_date = lambda x: x.date()

    HeartRate,ActCal = ldd.graphs(ldd.rdb)

    HeartRate['@creationDate'] = pd.to_datetime(HeartRate['@creationDate'])
    HeartRate['date'], HeartRate['hour'] = HeartRate['@creationDate'].map(get_date), HeartRate['@creationDate'].map(
        get_hour)
    start_date, end_date = (pd.to_datetime(date)-pd.to_timedelta(4, unit='d')), (pd.to_datetime(date)+pd.to_timedelta(1, unit='d'))
    HeartRate = HeartRate.loc[(HeartRate['date'] > start_date) & (HeartRate['date'] < end_date)]
    HeartRate['@Value'] = pd.to_numeric(HeartRate['@Value'])
    HeartRate = HeartRate.groupby(['date', 'hour'])['@Value'].mean().reset_index()
    HeartRate['date'] = HeartRate['date'].astype(str)

    figa = px.line(x=HeartRate['hour'], y=HeartRate['@Value'], color=HeartRate['date'])

    figa.update_layout(
        height=400,
        title='Trend from last 4 days',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
    figa.update_xaxes(title_text="hour")
    figa.update_yaxes(title_text='{}'.format(input_value))
    return figa


def figur2(date,input_value1,input_value2):
    HeartRate, ActCal = ldd.graphs(ldd.rdb)

    get_date = lambda x: x.date()

    HeartRate['@creationDate'] = pd.to_datetime(HeartRate['@creationDate'])
    HeartRate['date'] = HeartRate['@creationDate'].map(get_date)
    HeartRate = HeartRate.loc[HeartRate['date'] == date]
    HeartRate['@Value'] = pd.to_numeric(HeartRate['@Value'])

    ActCal['@creationDate'] = pd.to_datetime(ActCal['@creationDate'])
    ActCal['@Value'] = pd.to_numeric(ActCal['@Value'])
    ActCal['date'] = ActCal['@creationDate'].map(get_date)
    ActCal = ActCal.loc[ActCal['date'] == date]
    ActCal = ActCal.resample('5Min', on='@creationDate').sum().reset_index()

    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=HeartRate['@creationDate'], y=HeartRate['@Value'], name="Heart Rate"), secondary_y=False)
    fig.add_trace(go.Bar(x=ActCal['@creationDate'], y=ActCal['@Value'], name="Active Calories"), secondary_y=True)

    fig.update_layout(
        height=400,
        template='plotly_white',
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text='{}'.format(input_value1), secondary_y=True)
    fig.update_yaxes(title_text='{}'.format(input_value2), secondary_y=False)

    return fig


#Header
Header = [
    dbc.Col(html.H1('HiGHmed patient dashboard',
        style={
            'textAlign': 'center',
        }),)
]

#Tabs
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
             options=[{'label': 'Active Energy Burned', 'value': 'AEB'},
                      {'label': 'Apple Exercise Time', 'value': 'AET'},
                      {'label': 'Apple Stand Time', 'value': 'AST'},
                      {'label': 'Basal Energy Burned', 'value': 'BEB'},
                      {'label': 'Distance Cycling', 'value': 'DC'},
                      {'label': 'Distance Walking Running', 'value': 'DWR'},
                      {'label': 'Sleep Analysis', 'value': 'SA'},
                      {'label': 'Step Count', 'value': 'SC'}
                      ],
             value='AEB'
         ), ], ), ]),
    dbc.Row(dbc.Col([
        "and:",
        dcc.Dropdown(
            id='linear plot',
            options=[{'label': 'Heart Rate', 'value': 'HR'},
                     {'label': 'Heart Rate Variability SDNN', 'value': 'HRV'},
                     {'label': 'Resting Heart Rate', 'value': 'RHR'},
                     {'label': 'VO2Max', 'value': 'VO2'},
                     {'label': 'Walking Heart Rate Average', 'value': 'WRA'},
                     ],
            value='HR'
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
                             {'label': 'by day', 'value': 'D'}],
                    value='D'
                ), ],
        ), ], ),
    html.Br(),
    dbc.Row([dbc.Col(
        [
        "Select day:\t",
        dcc.DatePickerSingle(
            id='date-picker',
            min_date_allowed=dt(2015, 8, 5),
            max_date_allowed=dt(2021, 9, 19),
            initial_visible_month=dt(2020, 3, 27),
            display_format='D/M/Y',
            date=str(dt(2020, 2, 27, 23, 59, 59))),
    ],),],),
    html.Br(),

]

#Cards

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





#graph
graphs1 = [
    dcc.Graph(
        id='example-graph1',
    )
]

graphs3 = [
    [
        dcc.Graph(
            id='example-graph2',
        )
    ],

]


#table

df = pd.DataFrame(
    {
        "First Name": ["Arthur", "Ford", "Zaphod", "Trillian"],
        "Last Name": ["Dent", "Prefect", "Beeblebrox", "Astra"],
        "First Name2": ["Arthur", "Ford", "Zaphod", "Trillian"],
    }
)

table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

#ECG



app.layout = dbc.Container(style={'backgroundColor': colors['background']},
    children =[
    dbc.Row(Header),

    dbc.Card(Tab),
    html.Div(id='tabs-content')
],
fluid=True)




@app.callback(Output('tabs-content', 'children'),[Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            dbc.Row([
            dbc.Col(dbc.Card(dbc.Col(selection)),width=3),
            dbc.Col([(card) for card in cards1], width=4),
            dbc.Col([dbc.Col(graph) for graph in graphs3],)]),
            dbc.Row([dbc.Col(graph) for graph in graphs1]),


        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])


@app.callback(Output('date_picker', 'children'),
              [Input('group by', 'value')])
def Update_date_picker(group):
    if group == 'D':
        return "bbb"
    else:
        return 'ooo'


@app.callback(
    [Output("RestingHeartRate", "children"),
     Output("WalkingHeartRate", "children"),
     Output("step", "children"),
     Output("HeartRate_mean", "children"),
     Output("Exercise_minute", "children"),
     Output("ActivitySummary2", "children")],
    [Input("date-picker", "date")],
)
def Update_Card(date2):
    date2=pd.to_datetime(date2)
    RestingHeartRate,WalkingHeartRate,step,HeartRate_mean,Exercise_minute,ActivitySummary2= Card(date2)
    return RestingHeartRate,WalkingHeartRate,step,HeartRate_mean,Exercise_minute,ActivitySummary2



@app.callback(
    Output('example-graph1', 'figure'),
    [Input("date-picker", "date"),
     Input('Bar chart', 'value'),
     Input('linear plot', 'value')]
)
def update_figure2(date,input_value1,input_value2):
    date = pd.to_datetime(date)
    fig=figur2(date,input_value1,input_value2)
    return fig


@app.callback(
    Output('example-graph2', 'figure'),
    [Input("date-picker", "date"),
    Input('linear plot', 'value')]
)
def update_figure_trend(date,input_value):
    date = pd.to_datetime(date)
    figa=figur_trend(date,input_value)
    return figa


if __name__ == "__main__":
    app.run_server(debug=True)