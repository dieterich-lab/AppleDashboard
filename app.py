import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,ALL
from datetime import datetime as dt
import pandas as pd
from datetime import date

import modules.load_data_from_database as ldd
from db import connect_db
from Card import Card,Cards_view
from trend_figure import figur_trend
from summary_figure import figur2
from day_figure import figur3
from ECG import figur_ECG
from selection_card import selection

month =['January', 'February', 'March', 'April','May', 'June', 'July', 'August','September','October','November','December']
day_of_week=['Monday', 'Tuesday', 'Wednesday', 'Thursday','Friday', 'Saturday', 'Sunday']
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# change color of background
colors = {
    'background': '#e7e7e7',
    'text': '#7FDBFF'
}

# connection with database
rdb=connect_db()
df = ldd.Card(rdb)


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
app.layout = dbc.Container(style={'backgroundColor': colors['background']},
    children =[
    dbc.Row(dbc.Col(html.H1('HiGHmed patient dashboard',style={'textAlign': 'center',}),)),

    dbc.Card(Tab),
    html.Div(id='tabs-content')
], fluid=True)


#Selection
selection = selection()

#Cards
cards1=Cards_view()


@app.callback(Output('tabs-content', 'children'),[Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            dbc.Row([
                dbc.Col(dbc.Card(dbc.Col(selection)), width=3),
                dbc.Col([(card) for card in cards1], width=4),
                dbc.Col([dbc.Col(dcc.Graph(id='example-graph2', ))], )]),
            dbc.Row([dbc.Col(dcc.Graph(id='example-graph1', ))]),
            html.Div(id='tabs-content2'),
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])

@app.callback(Output('tabs-content2', 'children'),[Input('group by', 'value')])
def render_content2(tab):
    if tab == 'D':
        return html.Div([


            html.Br(),
            dbc.Col([dbc.Col(dcc.Graph(id='example-graph4', ))]),
            html.Br(),
            dbc.Row([dbc.Col(dcc.Graph(id='example-graph3', ))]),
        ])
    else:
        return html.Div([
            html.Br(),
        ])

@app.callback(
    Output('dropdown-container', 'children'),
    [Input('group by', "value")],
)
def Update_selection(value):
    if value == 'M':
        new_dropdown = dcc.Dropdown(
            id= {
            'type': 'filter-dropdown',
            'index': 0
        },
            options=[{'label': name, 'value': i} for (i,name) in enumerate(month,1)],
            value='1'
        )
    elif value == 'W':
        week = []
        for i in range(1, 53):
            a = dt.strptime('2020 {} 1'.format(i), '%G %V %u').date()
            b = dt.strptime('2020 {} 7'.format(i), '%G %V %u').date()
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
            options=[{'label': name, 'value': i} for (i,name) in enumerate(day_of_week,1)],
            value = '1'
        )
    elif value == 'D':
        new_dropdown = dcc.DatePickerSingle(
            id={
                'type': 'filter-dropdown',
                'index': 0
            },
            min_date_allowed=dt(2015, 8, 5),
            max_date_allowed=dt(2021, 9, 19),
            initial_visible_month=dt(2020, 3, 27),
            display_format='D/M/Y',
            date=date(2020,2,27))

    return new_dropdown


# callback for card
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
    if not date and not value:
        RestingHeartRate,WalkingHeartRate,step,HeartRate_mean,Exercise_minute,ActivitySummary2=0,0,0,0,0,0,
    else:
        date = pd.to_datetime(date[-1])
        value = value[-1]
        RestingHeartRate,WalkingHeartRate,step,HeartRate_mean,Exercise_minute,ActivitySummary2= Card(date,value,group,df)
    return RestingHeartRate,WalkingHeartRate,step,HeartRate_mean,Exercise_minute,ActivitySummary2

# callback for trend_figure
@app.callback(
    Output('example-graph2', 'figure'),
    [Input( {"index":ALL,'type':'filter-dropdown'}, 'value'),
     Input({'index':ALL,'type':'filter-dropdown'}, 'date'),
     Input('linear plot', 'value'),
     Input("group by", "value")],
)
def Update_figure_trend(value,date,input_value,group,):
    if date and value:
        date = pd.to_datetime(date[-1])
        value = value[-1]
        figa=figur_trend(date,value,input_value,group,df)
    else:
        figa = {}

    return figa



@app.callback(
    Output('example-graph1', 'figure'),
    [Input('linear plot', 'value'),
     Input('Bar chart', 'value'),
     Input("group by", "value")]
)
def Update_summary_figure(input_value1,input_value2,group):
    fig=figur2(input_value1,input_value2,group,df)
    return fig


@app.callback(
    Output('example-graph4', 'figure'),
    [Input( {"index":ALL,'type':'filter-dropdown'}, 'date'),]
)
def Update_figure_day(date):
    for date in date:
        date = pd.to_datetime(date)
    if date == None or not date :
        fig3={}
    else:
        fig3=figur3 (date,df)
    return fig3


@app.callback(
    Output('example-graph3', 'figure'),
    [Input( {"index":ALL,'type':'filter-dropdown'}, 'date'),]
)
def Update_ECG(date):
    fig={}
    for date in date:
        if date == None or not date :
            fig={}
        else:
            date = pd.to_datetime(date).date()
            fig=figur_ECG(date)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
