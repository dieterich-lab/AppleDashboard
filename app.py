import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime as dt
from dash.dependencies import Input, Output, State, MATCH, ALL,ALLSMALLER
import flask
import modules.load_data_from_database as ldd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
from datetime import datetime


server = flask.Flask(__name__)
app = dash.Dash(__name__,
                server=server,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config['suppress_callback_exceptions'] = True


colors = {
    'background': '#e7e7e7',
    'text': '#7FDBFF'
}

get_hour = lambda x: x.hour
get_date = lambda x: x.date()
get_month = lambda x: '{}-{:02}'.format(x.year, x.month)
get_day = lambda x: '{}-{:02}-{:02}'.format(x.year, x.month, x.day) #inefficient
get_week = lambda x: x.isocalendar()[1]
get_day_of_week = lambda x: x.isoweekday()

def Card(date,date1,group):
    df = ldd.Card(ldd.rdb)


    if group == 'M':
        df['month'] = df['@creationDate'].map(get_month)

        df1 = df.groupby(['month', '@type'])['@Value'].mean().reset_index()
        df2 = df.groupby(['month', '@type'])['@Value'].sum().reset_index()
        if len(str(date1)) == 1:
            df1 = df1.loc[df1['month'] == '2020-0{}'.format(date1)]
            df2 = df2.loc[df2['month'] == '2020-0{}'.format(date1)]
        else:
            df1 = df1.loc[df1['month'] == '2020-{}'.format(date1)]
            df2 = df2.loc[df2['month'] == '2020-{}'.format(date1)]

    elif group == 'W':
        df['week'] = df['@creationDate'].map(get_week)
        df1 = df.groupby(['week', '@type'])['@Value'].mean().reset_index()
        df2 = df.groupby(['week', '@type'])['@Value'].sum().reset_index()
        df1 = df1.loc[df1['week'] == date1]
        df2 = df2.loc[df2['week'] == date1]

    elif group == 'DOW':
        df['DOW'] = df['@creationDate'].map(get_day_of_week)
        df1 = df.groupby(['DOW', '@type'])['@Value'].mean().reset_index()
        df2 = df.groupby(['DOW', '@type'])['@Value'].sum().reset_index()
        df1 = df1.loc[df1['DOW'] == date1]
        df2 = df2.loc[df2['DOW'] == date1]
    else:
        df['date'] = df['@creationDate'].map(get_date)
        df1 = df.groupby(['date', '@type'])['@Value'].mean().reset_index()
        df2 = df.groupby(['date', '@type'])['@Value'].sum().reset_index()
        df1 = df1.loc[df1['date'] == date]
        df2 = df2.loc[df2['date'] == date]

    RestingHeartRate,WalkingHeartRate,HeartRate_mean,step,Exercise_minute,ActivitySummary2 ='Not measured','Not measured','Not measured','Not measured','Not measured','Not measured'
    try:
        RestingHeartRate = round(df1[df1['@type'] == 'HKQuantityTypeIdentifierRestingHeartRate'].iloc[0]['@Value'], 2)
    except:
        pass
    try:
        WalkingHeartRate = round(df1.loc[df1['@type'] == 'HKQuantityTypeIdentifierWalkingHeartRateAverage'].iloc[0]['@Value'], 2)
    except:
        pass
    try:
        HeartRate_mean = round(df1.loc[df1['@type'] == 'HKQuantityTypeIdentifierHeartRate'].iloc[0]['@Value'], 2)
    except:
        pass
    try:
        step = round(df2.loc[df2['@type'] == 'HKQuantityTypeIdentifierStepCount'].iloc[0]['@Value'], 2)
    except:
        pass
    try:
        Exercise_minute = round(df2.loc[df2['@type'] == 'HKQuantityTypeIdentifierAppleExerciseTime'].iloc[0]['@Value'], 2)
    except:
        pass
    try:
        ActivitySummary2 = round(df2.loc[df2['@type'] == 'HKQuantityTypeIdentifierActiveEnergyBurned'].iloc[0]['@Value'], 2)
    except:
        pass


    return RestingHeartRate, WalkingHeartRate, step, HeartRate_mean, Exercise_minute, ActivitySummary2

def figur_trend(date,date1,input_value,group):


    df = ldd.Card(ldd.rdb)
    df = df.loc[df['@type'] == 'HKQuantityTypeIdentifierHeartRate']

    if group == 'M':
        df['month'],df['hour'] = df['@creationDate'].map(get_month), df['@creationDate'].map(get_hour)
        if int(date1) < 10:
            dateu='2020-0{}'.format(date1)
        else:
            dateu='2020-0{}'.format(date1)
        if dateu in df['month'].values:
            if int(date1) > 3:
                if date1 <10:
                    start_date,end_date ='2020-0{}'.format(int(date1) - 4), '2020-0{}'.format(int(date1) + 1)
                else:
                    start_date, end_date = '2020-{}'.format(int(date1) - 4), '2020-{}'.format(int(date1) + 1)
                df = df.loc[(df['month'] > start_date) & (df['month'] < end_date)]
            else:
                start_date, end_date = '2020-0{}'.format(int(date1) + 12 - 4), '2020-0{}'.format(int(date1) + 1)
                df = df.loc[(df['month'] > start_date) | (df['month'] < end_date)]
            df = df.groupby(['month', 'hour'])['@Value'].mean().reset_index()
            df['month'] = df['month'].astype(str)
            figa = px.line(x=df['hour'], y=df['@Value'], color=df['month'])
        else :
            figa={}

    elif group == 'W':
        df['week'],df['hour'] = df['@creationDate'].map(get_week), df['@creationDate'].map(get_hour)
        if int(date1) in df['week'].values:
            if int(date1) > 3:
                start_date, end_date = int(date1) - 4, int(date1) + 1
                df = df.loc[(df['week'] > start_date) & (df['week'] < end_date)]
            else:
                start_date, end_date = int(date1) + 53 - 4, int(date1) + 1
                df = df.loc[(df['week'] > start_date) | (df['week'] < end_date)]
            df = df.groupby(['week', 'hour'])['@Value'].mean().reset_index()
            df['week'] = df['week'].astype(str)
            figa = px.line(x=df['hour'], y=df['@Value'], color=df['week'])
        else:
            figa={}

    elif group == 'DOW':
        df['DOW'],df['hour'] = df['@creationDate'].map(get_day_of_week), df['@creationDate'].map(get_hour)
        if int(date1) in df['DOW'].values:
            if int(date1) > 3:
                start_date, end_date = int(date1) - 4, int(date1) + 1
                df = df.loc[(df['DOW'] > start_date) & (df['DOW'] < end_date)]
            else:
                start_date, end_date = int(date1) + 7 - 4, int(date1) + 1
                df = df.loc[(df['DOW'] > start_date) | (df['DOW'] < end_date)]

            df = df.groupby(['DOW', 'hour'])['@Value'].mean().reset_index()
            df['DOW'] = df['DOW'].astype(str)
            figa = px.line(x=df['hour'], y=df['@Value'], color=df['DOW'])
        else:
            figa={}

    else:

        df['date'], df['hour'] = df['@creationDate'].map(get_date), df['@creationDate'].map(get_hour)
        if pd.to_datetime(date) in df['date'].values:
            start_date, end_date = (pd.to_datetime(date) - pd.to_timedelta(4, unit='d')), (pd.to_datetime(date) + pd.to_timedelta(1, unit='d'))
            df = df.loc[(df['date'] > start_date) & (df['date'] < end_date)]
            df = df.groupby(['date', 'hour'])['@Value'].mean().reset_index()
            df['date'] = df['date'].astype(str)
            figa = px.line(x=df['hour'], y=df['@Value'], color=df['date'])
        else:
            figa={}

    if figa:
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
    else:
        figa = {
            "layout": {
            "xaxis": {"visible": 'false'},
            "yaxis": {"visible": 'false'},
            "annotations": [
            {
                "text": "No matching data found",
                "xref": "paper",
                "yref": "paper",
                "showarrow": 'false',
                "font": {"size": 28}
            }
                            ]
                    }
            }




    return figa

def figur2(input_value1,input_value2,group):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    df = ldd.Card(ldd.rdb)

    if group == 'M':
        df['month'] = df['@creationDate'].map(get_month)
        df1 = df.groupby(['month','name'])['@Value'].mean().reset_index()
        df2 = df.groupby(['month','name'])['@Value'].sum().reset_index()
        df1 = df1.loc[df1['name'] == input_value1]
        df2 = df2.loc[df2['name'] == input_value2]

        fig.add_trace(go.Bar(x=df2['month'], y=df2['@Value'], name="Active Calories"), secondary_y=False)
        fig.add_trace(go.Scatter(x=df1['month'], y=df1['@Value'], name="Heart Rate"), secondary_y=True)


    elif group == 'W':
        df['week'] = df['@creationDate'].map(get_week)
        df1 = df.groupby(['week','name'])['@Value'].mean().reset_index()
        df2 = df.groupby(['week','name'])['@Value'].sum().reset_index()
        df1 = df1.loc[df1['name'] == input_value1]
        df2 = df2.loc[df2['name'] == input_value2]

        fig.add_trace(go.Bar(x=df2['week'], y=df2['@Value'], name="Active Calories"), secondary_y=False)
        fig.add_trace(go.Scatter(x=df1['week'], y=df1['@Value'], name="Heart Rate"), secondary_y=True)

    elif group == 'DOW':
        df['DOW'] = df['@creationDate'].map(get_day_of_week)
        df1 = df.groupby(['DOW','name'])['@Value'].mean().reset_index()
        df2 = df.groupby(['DOW','name'])['@Value'].sum().reset_index()
        df1 = df1.loc[df1['name'] == input_value1]
        df2 = df2.loc[df2['name'] == input_value2]

        fig.add_trace(go.Bar(x=df2['DOW'], y=df2['@Value'], name="Active Calories"), secondary_y=False)
        fig.add_trace(go.Scatter(x=df1['DOW'], y=df1['@Value'], name="Heart Rate"), secondary_y=True)
    else:
        df['day'] = df['@creationDate'].map(get_day)
        df1 = df.groupby(['day','name'])['@Value'].mean().reset_index()
        df2 = df.groupby(['day','name'])['@Value'].sum().reset_index()
        df1 = df1.loc[df1['name'] == input_value1]
        df2 = df2.loc[df2['name'] == input_value2]

        fig.add_trace(go.Bar(x=df2['day'], y=df2['@Value'], name="Active Calories"), secondary_y=False)
        fig.add_trace(go.Scatter(x=df1['day'], y=df1['@Value'], name="Heart Rate"), secondary_y=True)

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


def figur3(date):
    df = ldd.Card(ldd.rdb)
    df['date'] = df['@creationDate'].map(get_date)
    if pd.to_datetime(date) in df['date'].values:
        HeartRate=df.loc[df['@type'] == 'HKQuantityTypeIdentifierHeartRate']
        ActCal=df.loc[df['@type'] == 'HKQuantityTypeIdentifierActiveEnergyBurned']

        HeartRate = HeartRate.loc[HeartRate['date'] == date]

        ActCal = ActCal.loc[ActCal['date'] == date]
        ActCal = ActCal.resample('5Min', on='@creationDate').sum().reset_index()


        fig3 = make_subplots(specs=[[{"secondary_y": True}]])

        fig3.add_trace(go.Scatter(x=HeartRate['@creationDate'], y=HeartRate['@Value'], name="Heart Rate"), secondary_y=False)
        fig3.add_trace(go.Bar(x=ActCal['@creationDate'], y=ActCal['@Value'], name="Active Calories"), secondary_y=True)

        fig3.update_layout(
            height=400,
            template='plotly_white',
            legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
        fig3.update_xaxes(title_text="Time")
    else:
        fig3={}
    return fig3

def figur_ECG(date):
    date=str(date)+'_1'

    df = ldd.ECG_data(ldd.rdb,date)
    if len(df) == 0:
        fig={}
    else:
        data = df['Value'][0]
        l = len(data) / 511
        N = 511
        time = np.arange(0, l, 1 / N)


        fig = px.line(x=time, y=data, template='plotly_white')
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='LightPink',showticklabels=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
        fig.update_yaxes(nticks=20)
        fig.update_xaxes(nticks=750)
        fig.update_layout(
            xaxis_title="",
            yaxis_title="",

        )

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


#table

df = pd.DataFrame(
    {
        "First Name": ["Arthur", "Ford", "Zaphod", "Trillian"],
        "Last Name": ["Dent", "Prefect", "Beeblebrox", "Astra"],
        "First Name2": ["Arthur", "Ford", "Zaphod", "Trillian"],
    }
)

table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)





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
            html.Br(),
            dbc.Col([dbc.Col(graph) for graph in graphs5]),
            html.Br(),
            dbc.Row([dbc.Col(graph) for graph in graphs4]),



        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])

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



if __name__ == "__main__":
    app.run_server(debug=True)