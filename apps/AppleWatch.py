from app import app, data_store
from dash.dependencies import Input, Output, ALL
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
import time
from datetime import date
import datetime
from flask import send_file
import pandas as pd
import io

import modules.load_data_from_database as ldd
from db import connect_db

from AppleWatch.Card import card_update, cards_view
from AppleWatch.trend_figure import figure_trend
from AppleWatch.summary_figure import update_figure
from AppleWatch.day_figure import day_figure_update
from ECG_analyze.ECG_plot import update_ecg_figure
from AppleWatch.selection_card import selection
from AppleWatch.patient_information import patient_information, info


# connection with database
rdb = connect_db()


day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


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
                id='table',
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

    dbc.Row([dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='figure_day', hoverData={'points': [{'customdata': '1'}]}),
                                          style={'height': '100%'})), lg=6),
             dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='figure_trend')), style={'height': '100%'}), lg=6)]),
    html.Br(),

    dbc.Row([
        dbc.Col(dbc.Card(dcc.Loading(dash_table.DataTable(
            id='table_ecg',
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

        )), style={'height': '100%'}), lg=3),
        dbc.Col(dbc.Card([html.A('Download ECG', id='my-link'), dcc.Graph(id='figure_ecg')], style={'height': '100%'}),
                lg=9)]),
    html.Br(),
])


# callback for change selector with month/week/day after choosing group by
@app.callback(
    Output('drop_down-container', 'children'),
    [Input("figure_summary", "clickData"),
     Input('patient', "value"),
     Input('group by', "value")],
)
def update_selection(click, patient, value):

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
            clearable=False
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
    return drop_down


# callback for information about patient update
@app.callback(
    Output("text", "children"),
    [Input("patient", "value")],
)
def update_information(patient):
    text = info(patient)
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
def update_card(patient, group, date, value, m):
    df = ldd.card(rdb, patient, group, date[0], value[0])
    if not date or df.empty:
        resting_hr, walking_hr, hr_mean, step, exercise_minute, activity_summary = 0, 0, 0, 0, 0, 0
    else:
        resting_hr, walking_hr, hr_mean, step, exercise_minute, activity_summary = card_update(df)
    return resting_hr, walking_hr, hr_mean, step, exercise_minute, activity_summary


# update table and summary_figure depending on the drop-downs
@app.callback(
    [Output('figure_summary', 'figure'),
     Output("figure_summary", "clickData"),
     Output('table', 'data'),
     Output('table', 'columns')],
    [Input('group by', "value"),
     Input("patient", "value"),
     Input('linear plot', 'value'),
     Input('Bar chart', 'value')])
def update_table(group, patient, linear, bar):
    df, group_by = ldd.table(rdb, patient, group, linear, bar)

    click = None
    data = df.to_dict('records')
    columns = [{"name": str(i), "id": str(i)} for i in df.columns]

    fig = update_figure(df, linear, bar, group_by)

    return fig,click, data, columns


# update day figure
@app.callback(
    Output('figure_day', 'figure'),
    [Input({"index": ALL, 'type': 'filter-drop_down'}, 'date'),
     Input({"index": ALL, 'type': 'filter-drop_down'}, 'value'),
     Input("group by", "value"),
     Input('Bar chart', 'value'),
     Input("patient", "value"),
     Input('drop_down-container', 'children')
     ]
)
def update_figure_day(date, value, group, bar, patient, m):
    if group == 'D': date = date[0]
    elif group == 'M': date = value[0] + '-01'
    elif group == 'W': date = datetime.datetime.strptime(value[0] + '/1', "%Y/%W/%w")
    elif group == 'DOW': date = value[0]
    df = ldd.day_figure(rdb, patient, bar, date)
    if not date or df.empty:
        fig3 = {}
    else:
        fig3 = day_figure_update(df, bar)

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
def update_figure_trend(value, date, group, patient, m):
    if date and value:
        date = pd.to_datetime(date[-1])
        value = value[-1]
        fig = figure_trend(date, value,  group, patient)
    else:
        fig = {}
    return fig


# update table_ecg
@app.callback(
    [Output('table_ecg', 'data'),
     Output('table_ecg', 'columns'),
     Output('table_ecg', 'row_selectable'),
     Output('table_ecg', 'selected_rows')],
    Input("patient", "value")
)
def update_table_ecg(patient):
    df = ldd.ecgs(rdb, patient)
    data = df.to_dict('records')
    columns = [{"name": i, "id": i} for i in df.columns]
    return data, columns, 'single', [0]


# update ECG figure
@app.callback(
    Output('figure_ecg', 'figure'),
    [Input('table_ecg', "selected_rows"),
     Input("patient", "value"),
     Input("table_ecg", 'data')]
)
def update_ecg(data, patient, data_tab):
    if not data_tab:
        fig = {}
    else:
        add = ''
        day = data_tab[data[0]]['Day']
        time = data_tab[data[0]]['time']

        fig, df_ecg = update_ecg_figure(day, time, patient, add)
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
    buf_str = io.StringIO(csv)  # Create a string buffer
    buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))  # Create a bytes buffer from the string buffer
    buf_str.close()
    return send_file(buf_byt,
                     mimetype='text/csv',
                     attachment_filename='data.csv',
                     as_attachment=True)


@app.server.route('/dash/Download2')
def download2_csv():
    csv = data_store.csv_apple
    buf_str = io.StringIO(csv)
    buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))
    buf_str.close()
    return send_file(buf_byt,
                     mimetype='text/csv',
                     attachment_filename='data_apple_watch.csv',
                     as_attachment=True)
                     


