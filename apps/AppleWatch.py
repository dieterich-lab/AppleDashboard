from app import app
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ALL
from datetime import datetime as dt
import pandas as pd
import dash_table
import modules.load_data_from_database as ldd
from db import connect_db
from AppleWatch.Card import Card, Cards_view
from AppleWatch.trend_figure import figur_trend
from AppleWatch.summary_figure import figur2
from AppleWatch.day_figure import figur3
from AppleWatch.ECG import figur_ECG
from AppleWatch.selection_card import selection, selection2
from AppleWatch.table import table
from AppleWatch.patient_information import patient_information,info

month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
         'December']
day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


# Selection
selection = selection()
selection2 = selection2()

# connection with database
rdb = connect_db()
weight_and_height = ldd.weight_and_height(rdb)
ECG_irregular, ECG_inconclusive, ECG_over_120, ECG_under_50, dfr4 = ldd.irregular_ecg(rdb)
min_max_date = ldd.min_max_date(rdb)
min_date = min_max_date['min'].iloc[0]
min_date = min_date.date()
max_date = min_max_date['max'].iloc[0]
max_date = max_date.date()
df, df2 = ldd.Card(rdb)

# Cards
cards = Cards_view()
information = patient_information()

layout = html.Div([
    dbc.Row([dbc.Col(selection)]),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card(information), width=4),
        dbc.Col([dbc.Row([dbc.Col([card for card in cards])])])]),
    dbc.Row([dbc.Col(selection2)]),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card(
            dash_table.DataTable(
                id='table1',
                page_size=9,
                filter_action='native',
                sort_action="native",
                sort_mode="multi",
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )), width=4),
        dbc.Col(dcc.Graph(id='example-graph1'))]),
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Graph(id='example-graph4', hoverData={'points': [{'customdata': '1'}]})),
        dbc.Col([dbc.Col(dcc.Graph(id='example-graph2'))])
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card(dash_table.DataTable(
            id='table2',
            page_size=11,
            columns=[{"name": i, "id": i} for i in dfr4.columns],
            data=dfr4.to_dict('records'),
            filter_action='native',
            sort_action="native",
            sort_mode="multi",
            row_selectable='single',
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            }

        )), width=3),
        dbc.Col([dcc.Graph(id='example-graph3')])
    ]),
    html.Br(),

])


# callback fro change selector with month/week/day after chosing group by
@app.callback(
    Output('dropdown-container', 'children'),
    [Input('group by', "value")],
)
def update_selection(value):
    if value == 'M':
        new_drop_down = html.Div([dcc.Dropdown(
            style={'height': '40px'},
            id={
                'type': 'filter-dropdown',
                'index': 0
            },
            options=[{'label': name, 'value': i} for (i, name) in enumerate(month, 1)],
            value='1'
        )])
    elif value == 'W':
        week = []
        for i in range(1, 53):
            a = dt.strptime('2020 {} 1'.format(i), '%G %V %u').date()
            b = dt.strptime('2020 {} 7'.format(i), '%G %V %u').date()
            c = str(a)+'-' + str(b)
            week.append(c)

        new_drop_down = html.Div([dcc.Dropdown(
            style={'height': '40px'},
            id={
                'type': 'filter-dropdown',
                'index': 0
            },
            options=[{'label': name, 'value': i} for (i, name) in enumerate(week, 1)],
            value='1'
        )])
    elif value == 'DOW':
        new_drop_down = html.Div([dcc.Dropdown(
            style={'height': '40px'},
            id={
                'type': 'filter-dropdown',
                'index': 1
            },
            options=[{'label': name, 'value': i} for (i, name) in enumerate(day_of_week, 1)],
            value='1'
        )])
    elif value == 'D':
        new_drop_down = html.Div([dcc.DatePickerSingle(
            style={'height': '40px'},
            id={
                'type': 'filter-dropdown',
                'index': 0
            },
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            display_format='D/M/Y',
            date=min_date)])

    return new_drop_down


# callback for card
@app.callback(
    Output("text", "children"),
    [Input("patient", "value")],
)
def update_information(patient):
    text = info(weight_and_height, ECG_irregular, ECG_inconclusive, ECG_over_120, ECG_under_50, patient)

    return text


# callback for card
@app.callback(
    [Output("RestingHeartRate", "children"),
     Output("WalkingHeartRate", "children"),
     Output("HeartRate_mean", "children"),
     Output("step", "children"),
     Output("Exercise_minute", "children"),
     Output("ActivitySummary2", "children")],
    [Input("patient", "value"),
     Input("group by", "value"),
     Input({"index": ALL, 'type': 'filter-dropdown'}, 'date'),
     Input({"index": ALL, 'type': 'filter-dropdown'}, 'value')],
)
def update_card(patient, group, date, value):
    if not date and not value:
        RestingHeartRate, WalkingHeartRate, HeartRate_mean, step, Exercise_minute, ActivitySummary2 = 0, 0, 0, 0, 0, 0
    else:
        date = pd.to_datetime(date[-1])
        value = value[-1]
        RestingHeartRate, WalkingHeartRate, HeartRate_mean, step, Exercise_minute, ActivitySummary2 = Card(df, df2, patient,
                                                                                                           group, date,
                                                                                                           value)
    return RestingHeartRate, WalkingHeartRate, HeartRate_mean, step, Exercise_minute, ActivitySummary2


@app.callback(
    [Output('table1', 'data'),
     Output('table1', 'columns')],
    [Input('group by', "value"),
     Input("patient", "value"),
     Input('linear plot', 'value'),
     Input('Bar chart', 'value')]
)
def update_table(value, patient, linear, bar):
    result = table(df, patient, value, linear, bar)
    data = result.to_dict('records')
    columns = [{"name": i, "id": i} for i in result.columns]

    return data, columns


@app.callback(
    Output('example-graph1', 'figure'),
    [Input('linear plot', 'value'),
     Input('Bar chart', 'value'),
     Input("group by", "value"),
     Input("patient", "value")]
)
def update_summary_figure(input_value1, input_value2, group, patient1):
    fig = figur2(input_value1, input_value2, group, patient1, df)
    return fig


@app.callback(
    Output('example-graph2', 'figure'),
    [Input({"index": ALL, 'type': 'filter-dropdown'}, 'value'),
     Input({'index': ALL, 'type': 'filter-dropdown'}, 'date'),
     Input('linear plot', 'value'),
     Input("group by", "value"),
     Input("patient", "value")],
)
def update_figure_trend(value, date, input_value, group, patient1):
    if date and value:
        date = pd.to_datetime(date[-1])
        value = value[-1]
        fig = figur_trend(date, value, input_value, group, patient1, df)
    else:
        fig = {}

    return fig


@app.callback(
    Output({'index': ALL, 'type': 'filter-dropdown'}, 'date'),
    [Input("example-graph1", "selectedData"), Input("example-graph1", "clickData")],
)
def update_bar_selector(value, click_data):
    holder = ['2020-02-27']
    if click_data:
        holder = []
        holder.append(str(click_data["points"][0]["x"]))
    if value:
        holder = []
        for x in value["points"]:
            holder.append(str(int(x["x"])))
    return list(set(holder))


@app.callback(
    Output('example-graph4', 'figure'),
    [Input({"index": ALL, 'type': 'filter-dropdown'}, 'date'),
     Input("patient", "value")]
)
def update_figure_day(date, patient1):
    for date in date:
        date = pd.to_datetime(date)
    if date is None or not date:
        fig3 = {}
    else:
        fig3 = figur3(date, patient1, df)
    #fig3.show(renderer="browser")
    return fig3


@app.callback(
    Output('example-graph3', 'figure'),
    [Input({"index": ALL, 'type': 'filter-dropdown'}, 'date'),
     Input("patient", "value")]
)
def update_ecg(date, patient1):
    fig = {}
    for date in date:
        if date is None or not date:
            fig = {}
        else:
            date = pd.to_datetime(date).date()
            fig = figur_ECG(date, patient1)
    return fig
