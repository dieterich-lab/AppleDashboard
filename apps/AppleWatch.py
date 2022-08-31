from app import app
from dash.dependencies import Input, Output, ALL
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
import datetime
import pandas as pd
import modules.load_data_to_tab_health_data as ld
from db import connect_db

from AppleWatch.Card import card_update, cards_view
from AppleWatch.trend_figure import figure_trend
from AppleWatch.summary_figure import update_figure
from AppleWatch.day_figure import day_figure_update
from AppleWatch.selection_card import selection
from AppleWatch.patient_information import patient_information, info


# connection with database
rdb = connect_db()
labels = ld.label(rdb)
patients = ld.patient(rdb)

day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


# Selection
selection = selection(labels, patients)
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
                style_data_conditional=[{
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'}],
                style_cell={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                })), style={'height': '100%'}), lg=4),
        dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='figure_summary')), style={'height': '100%'}), lg=8)]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='figure_day', hoverData={'points': [{'customdata': '1'}]}),
                                          style={'height': '100%'})), lg=6),
             dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='figure_trend')), style={'height': '100%'}), lg=6)]),
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
        month = ld.month(rdb, patient)
        if click:
            value_m = click["points"][0]["x"][:7]
        else:
            value_m = month[0]
        drop_down = create_drop_down_for_selection(month, value_m)
    elif value == 'W':
        week = ld.week(rdb, patient)
        value_w = check_if_click_is_none(click, week)
        drop_down = create_drop_down_for_selection(week, value_w)
    elif value == 'DOW':
        value_dow = check_if_click_is_none(click, day_of_week)
        drop_down = create_drop_down_for_selection(day_of_week, value_dow)
    else:
        min_date, max_date = ld.min_max_date(rdb, patient)
        if click:
            value_day = str(click["points"][0]["x"])
        else:
            value_day = max_date
        drop_down = create_datepicksingle_for_selection(max_date, min_date, value_day)
    return drop_down


def create_datepicksingle_for_selection(max_date, min_date, value_day):
    drop_down = html.Div([dcc.DatePickerSingle(
        style={'height': '40px'},
        id={'type': 'filter-drop_down',
            'index': 0},
        min_date_allowed=min_date,
        max_date_allowed=max_date,
        display_format='D/M/Y',
        date=value_day)])
    return drop_down


def check_if_click_is_none(click, week):
    if click:
        value_w = click["points"][0]["x"]
    else:
        value_w = week[0]
    return value_w


def create_drop_down_for_selection(group, value):
    drop_down = html.Div([dcc.Dropdown(
        style={'height': '40px'},
        id={'type': 'filter-drop_down',
            'index': 0},
        options=[{'label': name, 'value': name} for name in group],
        value=value,
        clearable=False
    )])
    return drop_down


# callback for information about patient update
@app.callback(
    Output("text", "children"),
    [Input("patient", "value")],
)
def update_information(patient):
    age, sex = ld.age_sex(rdb, patient)
    ecg_classification = ld.classification_ecg(rdb, patient)
    days = ld.number_of_days_more_6(rdb, patient)
    text = info(age, sex, ecg_classification, days)
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
    df = ld.card(rdb, patient, group, date[0], value[0])
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
    df, group_by = ld.table(rdb, patient, group, linear, bar)
    if df.empty:
        fig, click, columns, data = {}, None, [], [{}]
    else:
        click = None
        data = df.to_dict('records')
        columns = [{"name": str(i), "id": str(i)} for i in df.columns]
        fig = update_figure(df, linear, bar, group_by, labels)
    return fig, click, data, columns


# update day figure
@app.callback(
    Output('figure_day', 'figure'),
    [Input({"index": ALL, 'type': 'filter-drop_down'}, 'date'),
     Input({"index": ALL, 'type': 'filter-drop_down'}, 'value'),
     Input("group by", "value"),
     Input('Bar chart', 'value'),
     Input("patient", "value"),
     Input('drop_down-container', 'children')])
def update_figure_day(date, value, group, bar, patient, m):
    if group == 'D': date = date[0]
    elif group == 'M': date = value[0] + '-01'
    elif group == 'W': date = datetime.datetime.strptime(value[0] + '/1', "%Y/%W/%w")
    elif group == 'DOW': date = date[0]
    df = pd.DataFrame()
    if date:
        df = ld.day_figure(rdb, patient, bar, date)
    if df.empty:
        fig = {}
    else:
        fig = day_figure_update(df, bar, date, labels)
    return fig


# update trend figure
@app.callback(
    Output('figure_trend', 'figure'),
    [Input({"index": ALL, 'type': 'filter-drop_down'}, 'value'),
     Input({'index': ALL, 'type': 'filter-drop_down'}, 'date'),
     Input("group by", "value"),
     Input("patient", "value"),
     Input('drop_down-container', 'children')])
def update_figure_trend(value, date, group, patient, m):
    if date[0]:
        date = date[0]
    if value[0]:
        value = value[0]
    df = ld.trend_figure(rdb, value, date, group, patient)
    if df.empty:
        fig = {}
    else:
        fig = figure_trend(df, group)
    return fig
