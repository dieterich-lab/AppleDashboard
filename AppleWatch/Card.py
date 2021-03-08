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


def card_update(df, patient, group, date, value):
    """
    Change of values on cards depending on what is selected in the selector.

    :param df: DataFrame with all values
    :param patient:
    :param group:
    :param date:
    :param date:
    :return: updated values
    """

    df = df.loc[df["@sourceName"] == patient]
    
    if group == 'M':
        value = value[-1]
        df2 = df.groupby(["@sourceName", 'month', '@type'])['@Value'].sum().reset_index()
        df4 = df.groupby(["@sourceName", 'month', '@type'])['@Value'].mean().reset_index()
        df = df.groupby(["@sourceName", 'month', 'date', '@type'])['@Value'].sum().reset_index()
        df3 = df.groupby(["@sourceName", 'month', '@type'])['@Value'].mean().reset_index()

        df2 = df2.loc[df2['month'] == value]
        df3 = df3.loc[df3['month'] == value]
        df4 = df4.loc[df4['month'] == value]

    elif group == 'W':
        value = value[-1]
        df2 = df.groupby(["@sourceName", 'week', '@type'])['@Value'].sum().reset_index()
        df4 = df.groupby(["@sourceName", 'week', '@type'])['@Value'].mean().reset_index()
        df = df.groupby(["@sourceName", 'week', 'date', '@type'])['@Value'].sum().reset_index()
        df3 = df.groupby(["@sourceName", 'week', '@type'])['@Value'].mean().reset_index()
        df2 = df2.loc[df2['week'] == value]
        df3 = df3.loc[df3['week'] == value]
        df4 = df4.loc[df4['week'] == value]

    elif group == 'DOW':
        value = value[-1]
        df2 = df.groupby(["@sourceName", 'DOW','DOW_number', '@type'])['@Value'].sum().reset_index()
        df4 = df.groupby(["@sourceName", 'DOW','DOW_number', '@type'])['@Value'].mean().reset_index()
        df = df.groupby(["@sourceName", 'DOW','DOW_number', 'date', '@type'])['@Value'].sum().reset_index()
        df3 = df.groupby(["@sourceName", 'DOW','DOW_number', '@type'])['@Value'].mean().reset_index()
        days_of_week = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6,
                        "Sunday": 7}
        df2 = df2.loc[df2['DOW_number'] == days_of_week[value]]
        df3 = df3.loc[df3['DOW_number'] == days_of_week[value]]
        df4 = df4.loc[df4['DOW_number'] == days_of_week[value]]
    else:
        date = pd.to_datetime(date[-1])
        df4 = df.groupby(["@sourceName", 'date', '@type'])['@Value'].mean().reset_index()
        df3 = df.groupby(["@sourceName", 'date', '@type'])['@Value'].mean().reset_index()
        df2 = df.groupby(["@sourceName", 'date', '@type'])['@Value'].sum().reset_index()
        df2 = df2.loc[df2['date'] == date]
        df4 = df4.loc[df4['date'] == date]
        df3 = df3.loc[df3['date'] == date]

    if 'HKQuantityTypeIdentifierRestingHeartRate' not in df4.values:
        resting_heart_rate = 'Not measured'
    else:
        resting_heart_rate = \
            str(round(df4[df4['@type'] == 'HKQuantityTypeIdentifierRestingHeartRate'].iloc[0]['@Value'], 2))
    if 'HKQuantityTypeIdentifierWalkingHeartRateAverage' not in df4.values:
        walking_heart_rate = 'Not measured'
    else:
        walking_heart_rate = \
            str(round(df4.loc[df4['@type'] == 'HKQuantityTypeIdentifierWalkingHeartRateAverage'].iloc[0]['@Value'], 2))
    if 'HKQuantityTypeIdentifierHeartRate' not in df4.values:
        heart_rate_mean = 'Not measured'
    else:
        heart_rate_mean = str(round(df4.loc[df4['@type'] == 'HKQuantityTypeIdentifierHeartRate'].iloc[0]['@Value'], 2))
    if 'HKQuantityTypeIdentifierStepCount' not in df4.values:
        step = 'Not measured'
    else:
        if group == 'D':
            step = str(round(df2.loc[df2['@type'] == 'HKQuantityTypeIdentifierStepCount'].iloc[0]['@Value'], 2))
        else:
            step = str(round(df3.loc[df3['@type'] == 'HKQuantityTypeIdentifierStepCount'].iloc[0]['@Value'], 2))
    if 'HKQuantityTypeIdentifierAppleExerciseTime' not in df4.values:
        exercise_minute = 'Not measured'
    else:
        if group == 'D':
            exercise_minute = \
                str(round(df2.loc[df2['@type'] == 'HKQuantityTypeIdentifierAppleExerciseTime'].iloc[0]['@Value'], 2))
        else:
            exercise_minute = \
                str(round(df3.loc[df3['@type'] == 'HKQuantityTypeIdentifierAppleExerciseTime'].iloc[0]['@Value'], 2))
    if 'HKQuantityTypeIdentifierActiveEnergyBurned' not in df4.values:
        activity_summary = 'Not measured'
    else:
        if group == 'D':
            activity_summary = \
                str(round(df2.loc[df2['@type'] == 'HKQuantityTypeIdentifierActiveEnergyBurned'].iloc[0]['@Value'], 2))
        else:
            activity_summary =\
                str(round(df3.loc[df3['@type'] == 'HKQuantityTypeIdentifierActiveEnergyBurned'].iloc[0]['@Value'], 2))

    return resting_heart_rate, walking_heart_rate, heart_rate_mean, step, exercise_minute, activity_summary
