from app import app
from dash.dependencies import Input, Output, ALL
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import modules.load_data_from_database as ldd
from db import connect_db


from Workout.selection_card import selection
from Workout.barchart import update_figure
from Workout.Recovery_heart_rate import calculate_HRR

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
data = ldd.WorkoutActivity_data(rdb)


weight_and_height = ldd.weight_and_height(rdb)
min_date, max_date = ldd.min_max_date(rdb)


dfr4, df_ECG = ldd.irregular_ecg(rdb)
df= ldd.Heart_Rate(rdb)
df_time = ldd.number_of_days_more_6(rdb)
df_summary = df[["Name", "Date", "name", "Value"]]
data_store.csv_apple = df_summary.to_csv(index=False)
month = df['month'].unique()
month.sort()

week = df['week'].unique()
week.sort()

#dum = calculate_HRR(data,df)

layout = html.Div([
    dbc.Row([dbc.Col(selection)]),
    html.Br(),

    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='summary_workout'), style={'height': '100%'}), lg=7),
             dbc.Col(dbc.Card(dcc.Graph(id='pie_graph'), style={'height': '100%'}), lg=5)]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='workout_graph'), style={'height': '100%'}), lg=7),
             dbc.Col(dbc.Card(dcc.Graph(id='recovery_graph'), style={'height': '100%'}), lg=5)]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='recovery_generally'), style={'height': '100%'}), lg=6),
             dbc.Col(dbc.Card(dcc.Graph(id='speed_generally'), style={'height': '100%'}), lg=6)]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='HR_max'), style={'height': '100%'}), lg=6),
             dbc.Col(dbc.Card(dcc.Graph(id='HR_min'), style={'height': '100%'}), lg=6)]),
    html.Br(),

])


# update table1 depends what values are chosen in selector
@app.callback(
    [Output('summary_workout', 'figure'),
     Output('pie_graph', 'figure'),
     Output('workout_graph', 'figure'),
     Output('recovery_graph', 'figure'),
     Output('recovery_generally', 'figure'),
     Output('HR_max', 'figure'),
     Output('HR_min', 'figure'),
     Output('speed_generally', 'figure')],
    [Input("patient", "value"),
     Input('group by', "value"),
     Input('Bar chart', 'value'),
     Input('filter-drop_down', 'date')]
)
def summary_workout(patient, group, bar,date):

    fig, fig2, fig3, fig4, fig5, fig6, fig7, fig8 = update_figure(data,patient, group, bar, date, df)
    return fig, fig2, fig3, fig4, fig5, fig6, fig7, fig8

"""
# update table1 depends what values are chosen in selector
@app.callback(
    [Output('table1', 'data'),
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
    return data, columns
"""
"""
# update table1 depends what values are chosen in selector
@app.callback(
    Output('recovery_generally', 'figure'),
    Input('Bar chart', 'value')
)
def calculate_HRR(group):
    fig, fig2, fig3, fig4 = update_figure(data, group, df)
    figr = {}
    return figr
"""

"""
dbc.Row([dbc.Col(dbc.Card(
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
        ), style={'height': '100%'}))]),
html.Br(),
"""