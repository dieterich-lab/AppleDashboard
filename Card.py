
import dash_bootstrap_components as dbc
import dash_html_components as html


def Cards_view():
    cards1 = [
    dbc.Row([dbc.Col(
    dbc.Card(
        [
            html.P("Resting Heart Rate Average", className="card-text"),
            html.H2(id='RestingHeartRate', className="card-title"),
        ],

        body=True,
        color="light",
        style={"width": "18rem"},

    ),),
    dbc.Col(
    dbc.Card(
        [
            html.P("Walking Heart Rate Average", className="card-text"),
            html.H2(id= 'WalkingHeartRate', className="card-title"),
        ],
        body=True,
        color="light",
        style={"width": "18rem"},
    ),),]),
    dbc.Row([dbc.Col(
        dbc.Card(
            [
                html.P("Average Heart Rate", className="card-text"),
                html.H2(id='HeartRate_mean', className="card-title"),
            ],
            body=True,
            color="light",
            style={"width": "18rem"},
        ), ),
        dbc.Col(
            dbc.Card(
                [
                    html.P("Steps", className="card-text"),
                    html.H2(id='step', className="card-title"),
                ],
                body=True,
                color="light",
                style={"width": "18rem"},
            ), ), ]),
    dbc.Row([dbc.Col(
        dbc.Card(
            [
                html.P("Active Calories", className="card-text"),
                html.H2(id ='ActivitySummary2', className="card-title"),
            ],
            body=True,
            color="light",
            style={"width": "18rem"},
        ), ),
        dbc.Col(
            dbc.Card(
                [
                    html.P("Exercise minutes", className="card-text"),
                    html.H2(id='Exercise_minute', className="card-title"),
                ],
                body=True,
                color="light",
                style={"width": "18rem"},
            ), ), ]),


]
    return cards1


def Card(date,date1,group,df):

    if group == 'M':
        df1 = df.groupby(['month', '@type'])['@Value'].mean().reset_index()
        df2 = df.groupby(['month', '@type'])['@Value'].sum().reset_index()
        if len(str(date1)) == 1:
            df1 = df1.loc[df1['month'] == '2020-0{}'.format(date1)]
            df2 = df2.loc[df2['month'] == '2020-0{}'.format(date1)]
        else:
            df1 = df1.loc[df1['month'] == '2020-{}'.format(date1)]
            df2 = df2.loc[df2['month'] == '2020-{}'.format(date1)]

    elif group == 'W':
        df1 = df.groupby(['week', '@type'])['@Value'].mean().reset_index()
        df2 = df.groupby(['week', '@type'])['@Value'].sum().reset_index()
        df1 = df1.loc[df1['week'] == date1]
        df2 = df2.loc[df2['week'] == date1]

    elif group == 'DOW':
        df1 = df.groupby(['DOW', '@type'])['@Value'].mean().reset_index()
        df2 = df.groupby(['DOW', '@type'])['@Value'].sum().reset_index()
        df1 = df1.loc[df1['DOW'] == date1]
        df2 = df2.loc[df2['DOW'] == date1]
    else:
        df1 = df.groupby(['date', '@type'])['@Value'].mean().reset_index()
        df2 = df.groupby(['date', '@type'])['@Value'].sum().reset_index()
        df1 = df1.loc[df1['date'] == date]
        df2 = df2.loc[df2['date'] == date]


    RestingHeartRate,WalkingHeartRate,HeartRate_mean,step,Exercise_minute,ActivitySummary2 ='Not measured','Not measured','Not measured','Not measured','Not measured','Not measured'

    try:
        RestingHeartRate = round(df1[df1['@type'] == 'HKQuantityTypeIdentifierRestingHeartRate'].iloc[0]['@Value'], 2)
    except:
        pass
    try:
        WalkingHeartRate = round(df1.loc[df1['@type'] == 'HKQuantityTypeIdentifierWalkingHeartRateAverage'].iloc[0]['@Value'], 2)
    except:
        pass
    try:
        HeartRate_mean = round(df1.loc[df1['@type'] == 'HKQuantityTypeIdentifierHeartRate'].iloc[0]['@Value'], 2)
    except:
        pass
    try:
        step = round(df2.loc[df2['@type'] == 'HKQuantityTypeIdentifierStepCount'].iloc[0]['@Value'], 2)
    except:
        pass
    try:
        Exercise_minute = round(df2.loc[df2['@type'] == 'HKQuantityTypeIdentifierAppleExerciseTime'].iloc[0]['@Value'], 2)
    except:
        pass
    try:
        ActivitySummary2 = round(df2.loc[df2['@type'] == 'HKQuantityTypeIdentifierActiveEnergyBurned'].iloc[0]['@Value'], 2)
    except:
        pass

    return RestingHeartRate, WalkingHeartRate, step, HeartRate_mean, Exercise_minute, ActivitySummary2