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
