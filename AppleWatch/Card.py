import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd


def cards_view():
    """

    :return: card layout
    """
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


days_of_week = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6,
                "Sunday": 7}


def card_update(df, group, date, value):
    """
    Change of values on cards depending on what is selected in the selector.

    :param df: DataFrame with all values
    :param patient:
    :param group:
    :param date:
    :param date:
    :return: updated values
    """
    if group == 'M':
        value = value[-1]
        df = df.loc[df['month'] == value]
        #df_sum_mean = df_sum_mean.loc[df_sum_mean['month'] == value]

    elif group == 'W':
        value = value[-1]
        df = df.loc[df['week'] == value]
        #df_sum_mean = df_sum_mean.loc[df_sum_mean['week'] == value]

    elif group == 'DOW':
        value = value[-1]
        df = df.loc[df['DOW_number'] == days_of_week[value]]
        #df_sum_mean = df_sum_mean.loc[df_sum_mean['DOW_number'] == days_of_week[value]]
    else:
        date = pd.to_datetime(date[-1])
        df = df.loc[df['date'] == date]

    if 'Resting Heart Rate' not in df.values: resting_heart_rate = 'Not measured'
    else: resting_heart_rate = str(round(df[df['name'] == 'Resting Heart Rate'].iloc[0]['mean'], 2))

    if 'Walking Heart Rate Average' not in df.values: walking_heart_rate = 'Not measured'
    else: walking_heart_rate = str(round(df.loc[df['name'] == 'Walking Heart Rate Average'].iloc[0]['mean'], 2))

    if 'Heart Rate' not in df.values: heart_rate_mean = 'Not measured'
    else: heart_rate_mean = str(round(df.loc[df['name'] == 'Heart Rate'].iloc[0]['mean'], 2))

    if 'Step Count' not in df.values: step = 'Not measured'
    else:
        if group == 'D':
            step = str(round(df.loc[df['name'] == 'Step Count'].iloc[0]['sum'], 2))
        else:
            step = str(round(df.loc[df['name'] == 'Step Count'].iloc[0]['sum'], 2))
    if 'Apple Exercise Time' not in df.values:
        exercise_minute = 'Not measured'
    else:
        if group == 'D':
            exercise_minute = str(round(df.loc[df['name'] == 'Apple Exercise Time'].iloc[0]['sum'], 2))
        else:
            exercise_minute = str(round(df.loc[df['name'] == 'Apple Exercise Time'].iloc[0]['sum'], 2))
    if 'Active Energy Burned' not in df.values: activity_summary = 'Not measured'
    else:
        if group == 'D':
            activity_summary = str(round(df.loc[df['name'] == 'Active Energy Burned'].iloc[0]['sum'], 2))
        else:
            activity_summary = str(round(df.loc[df['name'] == 'Active Energy Burned'].iloc[0]['sum'], 2))
    return resting_heart_rate, walking_heart_rate, heart_rate_mean, step, exercise_minute, activity_summary
