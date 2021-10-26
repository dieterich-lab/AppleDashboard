from app import app
from dash.dependencies import Input, Output, ALL
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table
from datetime import date

import modules.load_data_from_database as ldd
import modules.load_data_from_database_Workout as lddw
from db import connect_db


from Workout.selection_card import selection
from Workout.barchart import update_figure
from Workout.pie import update_pie
from Workout.table import table
from Workout.workout_figure import workout_figure
from Workout.Recovery_heart_rate import graphs

day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


# Selection
selection = selection()

# connection with database
rdb = connect_db()

layout = html.Div([
    dbc.Row([dbc.Col(selection)]),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card(
            dash_table.DataTable(
                id='tableu',
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
            ), style={'height': '100%'}))]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='summary_workout'), style={'height': '100%'}), lg=7),
             dbc.Col(dbc.Card(dcc.Graph(id='pie_graph'), style={'height': '100%'}), lg=5)]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='workout_graph'), style={'height': '100%'}))]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='recovery_generally'), style={'height': '100%'}), lg=6),
             dbc.Col(dbc.Card(dcc.Graph(id='speed_generally'), style={'height': '100%'}), lg=6)]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='HR_max'), style={'height': '100%'}), lg=6),
             dbc.Col(dbc.Card(dcc.Graph(id='HR_min'), style={'height': '100%'}), lg=6)]),
    html.Br(),

])
# callback for change selector with month/week/day after choosing group by
@app.callback(
    Output('drop_down-container2', 'children'),
    [Input("summary_workout", "clickData"),
    Input('patient', "value"),
    Input('group by', "value")],
)
def update_selection(click,patient, value):
    if value == 'M':
        month = ldd.month(rdb, patient)
        if click:
            value_m = click["points"][0]["x"][:7]
        else:
            value_m = month[0]
        drop_down = html.Div([dcc.Dropdown(
            style={'height': '40px'},
            id={
                'type': 'filter-drop_down2',
                'index': 0
            },
            options=[{'label': name, 'value': name} for name in month],
            value=value_m,
            clearable=False
        )])
    elif value == 'W':
        week = ldd.week(rdb,patient)
        if click:
            value_w = click["points"][0]["x"]
        else:
            value_w = week[0]
        drop_down = html.Div([dcc.Dropdown(
            style={'height': '40px'},
            id={
                'type': 'filter-drop_down2',
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
                'type': 'filter-drop_down2',
                'index': 1
            },
            options=[{'label': name, 'value': name} for name in day_of_week],
            value=value_dow,
            clearable=False
        )])
    elif value == 'D':
        min_date, max_date = ldd.min_max_date_workout(rdb,patient)
        if click:
            value_day = str(click["points"][0]["x"])
        else:
            value_day = max_date
        drop_down = html.Div([dcc.DatePickerSingle(
            style={'height': '40px'},
            id={
                'type': 'filter-drop_down2',
                'index': 0
            },
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            display_format='D/M/Y',
            date=value_day
        )])

    return drop_down




# update table depends what values are chosen in selector
@app.callback(
    [Output('tableu', 'data'),
     Output('tableu', 'columns')],
    [Input('group by', "value"),
     Input("patient", "value")]
)
def update_table(group, patient):
    data = lddw.WorkoutActivity_data(rdb,patient)
    result = table(data, group, patient)
    data2 = result.to_dict('records')
    columns = [{"name": str(i), "id": str(i)} for i in result.columns]
    return data2, columns

# update summary figure depends what values are chosen in selector
@app.callback(
    Output('summary_workout', 'figure'),
    [Input("patient", "value"),
     Input('group by', "value"),
     Input("what", "value")]
)
def summary_workout(patient, group, what):
    data = lddw.WorkoutActivity_data(rdb,patient)
    fig = update_figure(data, group,what)
    return fig

# update table1 depends what values are chosen in selector
@app.callback(
    Output('pie_graph', 'figure'),
    [Input("patient", "value"),
     Input('group by', "value"),
     Input({"index": ALL, 'type': 'filter-drop_down2'}, 'date'),
     Input({"index": ALL, 'type': 'filter-drop_down2'}, 'value'),
     Input('drop_down-container2', 'children'),
    Input("what", "value")]
)
def pie_figure(patient, group, date,value,m,what):
    date = date[0]
    value = value[0]
    data = lddw.WorkoutActivity_pie_chart(rdb, patient,group,date, value)
    if data.empty:
        fig = {}
    else:
        fig = update_pie(data, group,what)
    return fig


# update table1 depends what values are chosen in selector
@app.callback(
    Output('workout_graph', 'figure'),
    [Input("patient", "value"),
     Input('group by', "value"),
     Input({"index": ALL, 'type': 'filter-drop_down2'}, 'date'),
     Input({"index": ALL, 'type': 'filter-drop_down2'}, 'value'),
     Input('drop_down-container2', 'children')]
)
def HR_figure(patient, group, date, value, m):
    date = date[0]
    value = value[0]
    df = lddw.Heart_Rate(rdb,date,patient)
    data = lddw.WorkoutActivity_pie_chart(rdb, patient,group,date, value)
    data = data[(data['duration'] > 10) & (data['duration'] < 300)]

    if group != 'D' or data.empty:
        fig = {}
    else:
        fig = workout_figure(df,data)
    return fig




# update selector depend from the summary graph
@app.callback(
    [Output('recovery_generally', 'figure'),
    Output('speed_generally', 'figure'),
     Output('HR_max', 'figure'),
     Output('HR_min', 'figure')],
    [Input("patient", "value"),
     Input('activity', 'value')]
)
def update_HRR_figure(patient, activity):

    df = lddw.HRR(rdb, patient, activity)
    fig1, fig2, fig3, fig4 = graphs(df)

    return fig1, fig2, fig3, fig4


