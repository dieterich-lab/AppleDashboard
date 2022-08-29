import dash_bootstrap_components as dbc
from dash import html


def cards_view():
    cards = [
        dbc.Row([dbc.Col(dbc.Card(
            [
                html.P("Resting Heart Rate Average", className="card-text"),
                html.H3(id='RestingHeartRate', className="card-title"),
            ],
            body=True,
            color="light",
            style={'height': '100%'}
        ), sm=4), dbc.Col(dbc.Card(
            [
                html.P("Walking Heart Rate Average", className="card-text"),
                html.H3(id='WalkingHeartRate', className="card-title"),
            ],
            body=True,
            color="light",
            style={'height': '100%'}
        ), sm=4), dbc.Col(dbc.Card(
            [
                html.P("Average Heart Rate", className="card-text"),
                html.H3(id='HeartRate_mean', className="card-title"),
            ],
            body=True,
            color="light",
            style={'height': '100%'}
        ), sm=4)]),
        html.Br(),
        dbc.Row([dbc.Col(dbc.Card(
            [
                html.P("Steps", className="card-text"),
                html.H3(id='step', className="card-title"),
            ],
            body=True,
            color="light",
            style={'height': '100%'}
        ), sm=4), dbc.Col(dbc.Card(
            [
                html.P("Active Calories", className="card-text"),
                html.H3(id='ActivitySummary', className="card-title"),
            ],
            body=True,
            color="light",
            style={'height': '100%'}
        ), sm=4), dbc.Col(dbc.Card(
            [
                html.P("Exercise minutes ", className="card-text"),
                html.H3(id='Exercise_minute', className="card-title"),
            ],
            body=True,
            color="light",
            style={'height': '100%'}
        ), sm=4)])
    ]
    return cards


def card_update(df):
    """ Changing values in cards depending on what is selected in the drop down."""
    if 'Resting Heart Rate' not in df.key.values: resting_hr = 'Not measured'
    else: resting_hr = df[df['key'] == 'Resting Heart Rate']["Value"]

    if 'Walking Heart Rate Average' not in df.key.values: walking_hr = 'Not measured'
    else: walking_hr = df[df['key'] == 'Walking Heart Rate Average']["Value"]

    if 'Heart Rate' not in df.key.values: hr_mean = 'Not measured'
    else: hr_mean = df[df['key'] == 'Heart Rate']["Value"]

    if 'Step Count' not in df.key.values: step = 'Not measured'
    else: step = df[df['key'] == 'Step Count']["Value"]

    if 'Apple Exercise Time' not in df.key.values: exercise_minute = 'Not measured'
    else: exercise_minute = df[df['key'] == 'Step Count']["Value"]

    if 'Active Energy Burned' not in df.key.values: activity_summary = 'Not measured'
    else: activity_summary = df[df['key'] == 'Active Energy Burned']["Value"]

    return resting_hr, walking_hr, hr_mean, step, exercise_minute, activity_summary
