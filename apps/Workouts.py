from app import app
from dash.dependencies import Input, Output, ALL
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table
from datetime import date

import modules.load_data_from_database as ldd
from db import connect_db

from Workout.selection_card import selection
from Workout.summary_workout import update_figure
from Workout.pie import update_pie
from Workout.workout_figure import workout_figure

day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Selection
selection = selection()

# connection with database
rdb = connect_db()

layout = html.Div([
    dbc.Row([dbc.Col(selection)]),
    html.Br(),

    dbc.Row([
        dbc.Col(dbc.Card(dcc.Loading(
            dash_table.DataTable(
                id='table',
                style_table={'overflowX': 'auto'},
                page_size=5,
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
            ), style={'height': '100%'})))]),
    html.Br(),

    dbc.Row([dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='summary_workout')), style={'height': '100%'}), lg=7),
             dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='pie_graph')), style={'height': '100%'}), lg=5)]),
    html.Br(),

    dbc.Row([dbc.Col(dbc.Card(dcc.Loading(html.Div(id='graph', children=[])), style={'height': '100%'}))]),
    html.Br(),
])


# update table depends what values are chosen in selector
@app.callback(
    [Output('table', 'data'),
     Output('table', 'columns')],
    [Input('group by', "value"),
     Input("patient", "value")]
)
def update_table(group, patient):
    df = ldd.workout_activity_data(rdb, patient)
    df = df[['type', 'date', 'Start', 'End', 'duration', 'distance', 'EnergyBurned']].round(2)
    data = df.to_dict('records')
    columns = [{"name": str(i), "id": str(i)} for i in df.columns]
    return data, columns


# update summary figure depends what values are chosen in selector
@app.callback(
    Output('summary_workout', 'figure'),
    [Input("patient", "value"),
     Input('group by', "value"),
     Input("what", "value")]
)
def summary_workout(patient, group, what):
    data = ldd.workout_activity_data(rdb, patient)
    if data.empty:
        fig = {}
    else:
        fig = update_figure(data, group, what)
    return fig


# update table1 depends what values are chosen in selector
@app.callback(
    Output('pie_graph', 'figure'),
    [Input("patient", "value"),
     Input('group by', "value"),
     Input("summary_workout", "clickData"),
     Input("what", "value")]
)
def pie_figure(patient, group, value, what):
    if value:
        value = value["points"][0]["x"].replace(" ", "")
    else:
        value = ldd.workout_maxdate(rdb)
    data = ldd.workout_activity_pie_chart(rdb, patient, value, group, what)
    if data.empty:
        fig = {}
    else:
        fig = update_pie(data, group, what)
    return fig

"""
# update table depends what values are chosen in selector
@app.callback(
    Output('workout_graph', 'figure'),
    [Input("patient", "value"),
     Input('group by', "value"),
     Input({"index": ALL, 'type': 'filter-drop_down'}, 'date'),
     Input({"index": ALL, 'type': 'filter-drop_down'}, 'value'),
     Input('drop_down-container', 'children')]
)
def HR_figure(patient, group, date, value, m):
    date = date[0]
    value = value[0]
    df = ldd.Heart_Rate(rdb,date,patient)
    data = ldd.WorkoutActivity_pie_chart(rdb, patient,group,date, value)
    data = data[(data['duration'] > 10) & (data['duration'] < 300)]

    if group != 'D' or data.empty:
        fig = {}
    else:
        fig = workout_figure(df,data)
    return fig

"""





