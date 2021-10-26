from app import app
from dash.dependencies import Input, Output, ALL
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table
import time
from datetime import date

from flask import send_file
import pandas as pd
import io

import modules.load_data_from_database as ldd
from db import connect_db

from AppleWatch.Card import card_update, cards_view
from AppleWatch.trend_figure import figure_trend
from AppleWatch.summary_figure import update_figure
from AppleWatch.day_figure import day_figure_update
from AppleWatch.ECG import update_ecg_figure
from AppleWatch.selection_card import selection
from AppleWatch.table import table
from AppleWatch.patient_information import patient_information, info


class DataStore():

    # for filter
    csv_ecg = None
    csv_ecgs = None
    csv_apple = None


data_store = DataStore()

# connection with database
rdb = connect_db()

# get data from database
day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


# get the card for Cards and card for information about patient
# Selection
selection = selection()
cards = cards_view()
information = patient_information()


layout = html.Div([
    dbc.Row(dbc.Col(selection)),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card(information, style={'height': '100%'}), lg=4),
        dbc.Col([dcc.Loading(dbc.Row([dbc.Col([card for card in cards])]))], lg=8)]),

    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card(
            dcc.Loading(dash_table.DataTable(
                id='table1',
                style_table={'overflowX': 'auto'},
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
                style_cell={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )), style={'height': '100%'}), lg=4),
        dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='figure_summary')), style={'height': '100%'}), lg=8)]),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id='figure_day', hoverData={'points': [{'customdata': '1'}]}),
                         style={'height': '100%'}), lg=6),
        dbc.Col(dbc.Card(dcc.Graph(id='figure_trend'), style={'height': '100%'}), lg=6)
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card(dash_table.DataTable(
            id='table2',
            style_table={'overflowX': 'auto'},
            page_size=11,
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

        ), style={'height': '100%'}), lg=3),
        dbc.Col(dbc.Card([html.A('Download ECG', id='my-link'),
        dcc.Graph(id='figure_ecg')], style={'height': '100%'}), lg=9)
    ]),
    html.Br(),

])


# callback for change selector with month/week/day after choosing group by
@app.callback(
    Output('drop_down-container', 'children'),
    [Input("figure_summary", "clickData"),
    Input('patient', "value"),
    Input('group by', "value")],
)
def update_selection(click,patient, value):
    start_time = time.time()
    if value == 'M':
        month = ldd.month(rdb, patient)
        if click:
            value_m = click["points"][0]["x"][:7]
        else:
            value_m = month[0]
        drop_down = html.Div([dcc.Dropdown(
            style={'height': '40px'},
            id={
                'type': 'filter-drop_down',
                'index': 0
            },
            options=[{'label': name, 'value': name} for name in month],
            value=value_m,
            clearable=False
        )])
    elif value == 'W':
        week = ldd.week(rdb, patient)
        if click:
            value_w = click["points"][0]["x"]
        else:
            value_w = week[0]
        drop_down = html.Div([dcc.Dropdown(
            style={'height': '40px'},
            id={
                'type': 'filter-drop_down',
                'index': 0
            },
            options=[{'label': name, 'value': name} for name in week],
            value=value_w,
            clearable = False
        )])
    elif value == 'DOW':
        if click:
            value_dow = click["points"][0]["x"].replace(" ", "")
        else:
            value_dow = day_of_week[0]
        drop_down = html.Div([dcc.Dropdown(
            style={'height': '40px'},
            id={
                'type': 'filter-drop_down',
                'index': 1
            },
            options=[{'label': name, 'value': name} for name in day_of_week],
            value=value_dow,
            clearable=False
        )])
    elif value == 'D':
        min_date, max_date = ldd.min_max_date(rdb,patient)
        if click:
            value_day = str(click["points"][0]["x"])
        else:
            value_day = max_date
        drop_down = html.Div([dcc.DatePickerSingle(
            style={'height': '40px'},
            id={
                'type': 'filter-drop_down',
                'index': 0
            },
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            display_format='D/M/Y',
            date=value_day)])
    end_time = time.time()
    times = end_time - start_time
    print('t2',times)
    return drop_down


# callback for information about patient update
@app.callback(
    Output("text", "children"),
    [Input("patient", "value")],
)
def update_information(patient):
    start_time = time.time()
    text = info(patient)
    end_time = time.time()
    times = end_time - start_time
    print('info',times)
    return text


# callback for update values in card
@app.callback(
    [Output("RestingHeartRate", "children"),
     Output("WalkingHeartRate", "children"),
     Output("HeartRate_mean", "children"),
     Output("step", "children"),
     Output("Exercise_minute", "children"),
     Output("ActivitySummary", "children")],
    [Input("patient", "value"),
     Input("group by", "value"),
     Input({"index": ALL, 'type': 'filter-drop_down'}, 'date'),
     Input({"index": ALL, 'type': 'filter-drop_down'}, 'value'),
     Input('drop_down-container', 'children')],
)
def update_card(patient, group, date, value,m):
    start_time = time.time()
    if not date:
        resting_heart_rate, walking_heart_rate, heart_rate_mean, step, exercise_minute, activity_summary =\
            0, 0, 0, 0, 0, 0
    else:
        resting_heart_rate, walking_heart_rate, heart_rate_mean, step, exercise_minute, activity_summary =\
            card_update(patient,group, date,value)
    end_time = time.time()
    times = end_time - start_time
    print('cards',times)
    return resting_heart_rate, walking_heart_rate, heart_rate_mean, step, exercise_minute, activity_summary


# update table1 depends what values are chosen in selector
@app.callback(
    [Output('figure_summary', 'figure'),
    Output('table1', 'data'),
     Output('table1', 'columns')],
    [Input('group by', "value"),
     Input("patient", "value"),
     Input('linear plot', 'value'),
     Input('Bar chart', 'value'),
     ]
)
def update_table(group, patient, linear, bar):
    start_time = time.time()
    df = ldd.table(rdb, patient, group, linear, bar)
    result = table(df, group)
    data = result.to_dict('records')
    columns = [{"name": str(i), "id": str(i)} for i in result.columns]
    fig = update_figure(df, linear, bar, group)
    end_time = time.time()
    times = end_time - start_time
    print('summary',times)
    return fig, data, columns



# update day figure
@app.callback(
    Output('figure_day', 'figure'),
    [Input({"index": ALL, 'type': 'filter-drop_down'}, 'date'),
     Input({"index": ALL, 'type': 'filter-drop_down'}, 'value'),
     Input("group by", "value"),
     Input('linear plot', 'value'),
     Input('Bar chart', 'value'),
     Input("patient", "value")
     ]
)
def update_figure_day(date, value, group,linear, bar, patient):
    if not date and not value:
        fig3 = {}
    else:
        fig3 = day_figure_update(date, value, group, patient, linear, bar)
    return fig3


# update trend figure
@app.callback(
    Output('figure_trend', 'figure'),
    [Input({"index": ALL, 'type': 'filter-drop_down'}, 'value'),
     Input({'index': ALL, 'type': 'filter-drop_down'}, 'date'),
     Input("group by", "value"),
     Input("patient", "value"),
     Input('drop_down-container', 'children')],
)
def update_figure_trend(value, date, group, patient,m):
    if date and value:
        date = pd.to_datetime(date[-1])
        value = value[-1]
        fig = figure_trend(date, value,  group, patient)
    else:
        fig = {}
    return fig


# update table2
@app.callback(
    [Output('table2', 'data'),
     Output('table2', 'columns'),
     Output('table2', 'row_selectable'),
     Output('table2', 'selected_rows')],
    Input("patient", "value")
)
def update_table2(patient):
    df2 = ldd.irregular_ecg2(rdb, patient)
    data = df2.to_dict('records')
    columns = [{"name": i, "id": i} for i in df2.columns]
    return data, columns, 'single', [0]


# update ECG figure
@app.callback(
    Output('figure_ecg', 'figure'),
    [Input('table2', "selected_rows"),
    Input("patient", "value"),
    Input("table2", 'data')]
)
def update_ecg2(data, patient, data_tab):
    if not data_tab:
        fig = {}
    else:
        day = data_tab[data[0]]['Day']
        number = data_tab[data[0]]['time']
        fig, df_ecg = update_ecg_figure(day, number, patient)
        data_store.csv_ecg = df_ecg.to_csv(index=False)
    return fig


@app.callback(Output('my-link', 'href'), [Input('table2', 'selected_rows')])
def update_link(value):
    return '/dash/urlToDownload'


@app.callback(Output('my-link2', 'href'), [Input('table2', 'selected_rows')])
def update_link(value):
    return '/dash/Download2'


@app.server.route('/dash/urlToDownload')
def download_csv():
    csv = data_store.csv_ecg
    # Create a string buffer
    buf_str = io.StringIO(csv)
    # Create a bytes buffer from the string buffer
    buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))
    buf_str.close()
    return send_file(buf_byt,
                     mimetype='text/csv',
                     attachment_filename='data.csv',
                     as_attachment=True)


@app.server.route('/dash/Download2')
def download2_csv():
    csv = data_store.csv_apple
    # Create a string buffer
    buf_str = io.StringIO(csv)
    # Create a bytes buffer from the string buffer
    buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))
    buf_str.close()
    return send_file(buf_byt,
                     mimetype='text/csv',
                     attachment_filename='data_apple_watch.csv',
                     as_attachment=True)

