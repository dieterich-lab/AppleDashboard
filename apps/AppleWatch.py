from app import app
from dash.dependencies import Input, Output, ALL
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from flask import send_file
import pandas as pd
import io

import modules.load_data_from_database as ldd
from db import connect_db

from AppleWatch.Card import card_update, cards_view
from AppleWatch.trend_figure import figure_trend
from AppleWatch.summary_figure import update_figure
from AppleWatch.day_figure import day_figure_update,day_date_update
from AppleWatch.ECG import update_ecg_figure
from AppleWatch.selection_card import selection
from AppleWatch.table import table, table2
from AppleWatch.patient_information import patient_information, info
from AppleWatch.grouping import grouping1,grouping2

class DataStore():

    # for filter
    csv_ecg = None
    csv_apple = None


data_store = DataStore()


month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
         'December']
day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


# Selection
selection = selection()

# connection with database
rdb = connect_db()

# get data from database
weight_and_height = ldd.weight_and_height(rdb)
min_date, max_date = ldd.min_max_date(rdb)


dfr4, df_ECG = ldd.irregular_ecg(rdb)
df, df2 = ldd.Card(rdb)
df_time = ldd.number_of_days_more_6(rdb)
df_summary = df[["Name", "Date", "name", "Value"]]
data_store.csv_apple = df_summary.to_csv(index=False)
month = df['month'].unique()
month.sort()

week = df['week'].unique()
week.sort()

# get the card for Cards and card for information about patient
cards = cards_view()
information = patient_information()

layout = html.Div([
    dbc.Row([dbc.Col(selection)]),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card(information, style={'height': '100%'}), lg=4),
        dbc.Col([dbc.Row([dbc.Col([card for card in cards])])], lg=8)]),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card(
            dash_table.DataTable(
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
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            ), style={'height': '100%'}), lg=4),
        dbc.Col(dbc.Card(dcc.Graph(id='figure_summary'), style={'height': '100%'}), lg=8)]),
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
    [Input('group by', "value")],
)
def update_selection(value):
    if value == 'M':
        drop_down = html.Div([dcc.Dropdown(
            style={'height': '40px'},
            id={
                'type': 'filter-drop_down',
                'index': 0
            },
            options=[{'label': name, 'value': name} for name in month],
            value='1'
        )])
    elif value == 'W':
        drop_down = html.Div([dcc.Dropdown(
            style={'height': '40px'},
            id={
                'type': 'filter-drop_down',
                'index': 0
            },
            options=[{'label': name, 'value': name} for name in week],
            value='1'
        )])
    elif value == 'DOW':
        drop_down = html.Div([dcc.Dropdown(
            style={'height': '40px'},
            id={
                'type': 'filter-drop_down',
                'index': 1
            },
            options=[{'label': name, 'value': name} for name in day_of_week],
            value='1'
        )])
    elif value == 'D':
        drop_down = html.Div([dcc.DatePickerSingle(
            style={'height': '40px'},
            id={
                'type': 'filter-drop_down',
                'index': 0
            },
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            display_format='D/M/Y',
            date=min_date)])

    return drop_down


# callback for information about patient update
@app.callback(
    Output("text", "children"),
    [Input("patient", "value")],
)
def update_information(patient):
    text = info(weight_and_height, df_ECG, df_time, patient)
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
     Input({"index": ALL, 'type': 'filter-drop_down'}, 'value')],
)
def update_card(patient, group, date, value):
    if not date:
        resting_heart_rate, walking_heart_rate, heart_rate_mean, step, exercise_minute, activity_summary =\
            0, 0, 0, 0, 0, 0
    else:
        df_u = grouping1(df, patient, group)
        #df_sum_mean = grouping2(df, patient, group)
        resting_heart_rate, walking_heart_rate, heart_rate_mean, step, exercise_minute, activity_summary =\
            card_update(df_u,group, date,value)
    return resting_heart_rate, walking_heart_rate, heart_rate_mean, step, exercise_minute, activity_summary


# update table1 depends what values are chosen in selector
@app.callback(
    [Output('figure_summary', 'figure'),
    Output('table1', 'data'),
     Output('table1', 'columns')],
    [Input('group by', "value"),
     Input("patient", "value"),
     Input('linear plot', 'value'),
     Input('Bar chart', 'value')]
)
def update_table(group, patient, linear, bar):
    df_a = df[df.name.isin([linear,bar])]
    df_u = grouping1(df_a, patient, group)
    result = table(df_u, group, linear, bar)
    data = result.to_dict('records')
    columns = [{"name": str(i), "id": str(i)} for i in result.columns]
    fig = update_figure(df_u,linear, bar, group)
    return fig, data, columns



# update selector depend from the summary graph
@app.callback(
    [Output({'index': ALL, 'type': 'filter-drop_down'}, 'date'),
     Output({"index": ALL, 'type': 'filter-drop_down'}, 'value')],
    [Input("figure_summary", "selectedData"),
     Input("figure_summary", "clickData"),
     Input("group by", "value")],
)
def update_bar_selector(value, click_data, group):
    if group == 'D':
        holder = ['2020-02-27']
        if click_data:
            holder[0] = str(click_data["points"][0]["x"])
        holder2 = [None]
    else:
        if group == 'M':
            holder2 = ['2020-02']
            if click_data:
                holder2[0] = click_data["points"][0]["x"][:7]
        elif group == 'DOW':
            holder2 = ['Monday']
            if click_data:
                holder2[0] = click_data["points"][0]["x"].replace(" ","")
        else:
            holder2 = ['2020/08']
            if click_data:
                holder2[0] = click_data["points"][0]["x"]
        holder = ['2020-02-27']
    return list(set(holder)), list(set(holder2))


# update day figure
@app.callback(
    Output('figure_day', 'figure'),
    [Input({"index": ALL, 'type': 'filter-drop_down'}, 'date'),
     Input({"index": ALL, 'type': 'filter-drop_down'}, 'value'),
     Input("group by", "value"),
     Input('Bar chart', 'value'),
     Input("patient", "value")]
)
def update_figure_day(date, value, group, bar_value, patient):
    if not date and not value:
        fig3 = {}
    else:
        df_linear, df_bar=day_date_update(date, value, group, patient, bar_value, df)
        fig3 = day_figure_update(df_linear, df_bar, bar_value)
    return fig3


# update trend figure
@app.callback(
    Output('figure_trend', 'figure'),
    [Input({"index": ALL, 'type': 'filter-drop_down'}, 'value'),
     Input({'index': ALL, 'type': 'filter-drop_down'}, 'date'),
     Input('linear plot', 'value'),
     Input("group by", "value"),
     Input("patient", "value")],
)
def update_figure_trend(value, date, input_value, group, patient1):
    if date and value:
        date = pd.to_datetime(date[-1])
        value = value[-1]
        fig = figure_trend(date, value, input_value, group, patient1, df)
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
    result = table2(dfr4, patient)
    data = result.to_dict('records')
    columns = [{"name": i, "id": i} for i in result.columns]
    return data, columns, 'single', [0]


# update ECG figure
@app.callback(
    Output('figure_ecg', 'figure'),
    [Input('table2', "selected_rows"),
    Input("patient", "value"),
    Input("table2",'data')]
)
def update_ecg2(data, patient,data_tab):
    day = data_tab[data[0]]['Day']
    number = data_tab[data[0]]['number']
    fig,df_ecg = update_ecg_figure(day, number, patient)
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