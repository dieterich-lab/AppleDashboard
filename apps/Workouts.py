from app import app
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table
import modules.load_dat_to_workout_tab as ld
import modules.load_data_to_tab_health_data as ldd
from db import connect_db

from Workout.selection_card import selection
from Workout.summary_workout import update_figure
from Workout.pie import update_pie
from Workout.workout_figure import workout_figure

day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
rdb = connect_db()
patients = ldd.patient(rdb)
selection = selection(patients)

layout = html.Div([
    dbc.Row([dbc.Col(selection)]),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Loading(
            dash_table.DataTable(
                id='table_workout',
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


# update table depending on the drop-downs
@app.callback(
    [Output('table_workout', 'data'),
     Output('table_workout', 'columns')],
    [Input("patient", "value")])
def update_table(patient):
    df = ld.workout_activity_data(rdb, patient)
    data = df.to_dict('records')
    columns = [{"name": str(i), "id": str(i)} for i in df.columns]
    return data, columns


# update summary figure depending on the drop-downs
@app.callback(
    [Output('summary_workout', 'figure'),
     Output("summary_workout", "clickData")],
    [Input("patient", "value"),
     Input('group by', "value"),
     Input("what", "value")])  # option for plot dropdown
def summary_workout(patient, group, what):
    df = ld.workout_activity_data(rdb, patient)
    click = None
    if df.empty:
        fig = {}
    else:
        fig = update_figure(df, group, what)
    return fig, click


# update pie figure depending on the drop-downs
@app.callback(
    Output('pie_graph', 'figure'),
    [Input("patient", "value"),
     Input('group by', "value"),
     Input("summary_workout", "clickData"),
     Input("what", "value")])  # option for plot dropdown
def pie_figure(patient, group, value, what):
    data, value = ld.workout_activity_pie_chart(rdb, patient, value, group, what)
    if data.empty:
        fig = {}
    else:
        fig = update_pie(data, group, what, patient)
    return fig


# update workout figure depending on the drop-downs
@app.callback(
    Output('graph', 'children'),
    [Input('group by', "value"),
     Input("summary_workout", "clickData"),
     Input("patient", "value")])
def hr_figure(group, click, patient):
    if group == 'date':
        df1, df2 = ld.heart_rate(rdb, click, patient)
        if df1.empty or df2.empty:
            graph = html.Div()
        else:
            fig = workout_figure(df1, df2)
            graph = html.Div([dcc.Graph(figure=fig)])
    else:
        graph = html.Div()
    return graph
