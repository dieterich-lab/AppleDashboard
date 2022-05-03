import dash_bootstrap_components as dbc
from dash import html
import modules.load_data_from_database as ldd
from db import connect_db

# connection with database
rdb = connect_db()


def cards_view():
    """ card layout """
    cards = [
        dbc.Row([dbc.Col(dbc.Card(
            [
                html.P("Heart Rate", className="card-text"),
                html.H3(id='HeartRate', className="card-title"),
            ],
            body=True,
            color="light",
            style={'height': '100%'}
        ), sm=4), dbc.Col(dbc.Card(
            [
                html.P("Walking distance", className="card-text"),
                html.H3(id='Walking_distance', className="card-title"),
            ],
            body=True,
            color="light",
            style={'height': '100%'}
        ), sm=4), dbc.Col(dbc.Card(
            [
                html.P("Systolic blood pressure", className="card-text"),
                html.H3(id='Systolic_blood_pressure', className="card-title"),
            ],
            body=True,
            color="light",
            style={'height': '100%'}
        ), sm=4)]),
    ]
    return cards


def card_update(df):
    """ Changing values in cards depending on what is selected in the drop down."""

    if 'Heart rate 1 hour mean' not in df.type.values: heart_rate = 'Not measured'
    else: heart_rate = df[df['type'] == 'Heart rate 1 hour mean']["Value"]

    if 'Walking distance unspecified time Pedometer' not in df.type.values: walking_distance = 'Not measured'
    else: walking_distance = df[df['type'] == 'Walking distance unspecified time Pedometer']["Value"]

    if 'Systolic blood pressure' not in df.type.values: SBP = 'Not measured'
    else: SBP = df[df['type'] == 'Systolic blood pressure']["Value"]

    return  heart_rate, walking_distance, SBP
