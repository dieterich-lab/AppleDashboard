import dash_bootstrap_components as dbc
import dash_html_components as html

# Card layout
def Cards_view():
    cards1 = [
        dbc.Row([dbc.Col(dbc.Card(
            [
                html.P("Resting Heart Rate Average", className="card-text"),
                html.H2(id='RestingHeartRate', className="card-title"),
            ],
            body=True,
            color="light",
            style={"width": "18rem"},
        )), dbc.Col(dbc.Card(
            [
                html.P("Walking Heart Rate Average", className="card-text"),
                html.H2(id= 'WalkingHeartRate', className="card-title"),
            ],
            body=True,
            color="light",
            style={"width": "18rem"},
        ))]),
        dbc.Row([dbc.Col(dbc.Card(
            [
                html.P("Average Heart Rate", className="card-text"),
                html.H2(id='HeartRate_mean', className="card-title"),
            ],
            body=True,
            color="light",
            style={"width": "18rem"},
        )), dbc.Col(dbc.Card(
                [
                    html.P("Steps", className="card-text"),
                    html.H2(id='step', className="card-title"),
                ],
                body=True,
                color="light",
                style={"width": "18rem"},
        ))]),
        dbc.Row([dbc.Col(dbc.Card(
                [
                    html.P("Active Calories", className="card-text"),
                    html.H2(id ='ActivitySummary2', className="card-title"),
                ],
                body=True,
                color="light",
                style={"width": "18rem"},
        )), dbc.Col(dbc.Card(
                [
                    html.P("Exercise minutes", className="card-text"),
                    html.H2(id='Exercise_minute', className="card-title"),
                ],
                body=True,
                color="light",
                style={"width": "18rem"},
            ))])
    ]
    return cards1


# change value in card depend rotm this what is choosen in selector
def Card(date,date1, group, patient1, check, df):
    df = df.loc[df["@sourceName"] == patient1]

    if group == 'M':
        df = df.groupby(["@sourceName",'month', 'date', '@type'])['@Value'].sum().reset_index()
        df3 = df.groupby(["@sourceName",'month', '@type'])['@Value'].mean().reset_index()
        df2 = df.groupby(["@sourceName", 'month', '@type'])['@Value'].sum().reset_index()

        if len(str(date1)) == 1:
            df2 = df2.loc[df2['month'] == '2020-0{}'.format(date1)]
            df3 = df3.loc[df3['month'] == '2020-0{}'.format(date1)]
        else:
            df2 = df2.loc[df2['month'] == '2020-{}'.format(date1)]
            df3 = df3.loc[df3['month'] == '2020-{}'.format(date1)]

    elif group == 'W':
        df2 = df.groupby(["@sourceName",'week', '@type'])['@Value'].sum().reset_index()
        df = df.groupby(["@sourceName",'week', 'date', '@type'])['@Value'].sum().reset_index()
        df3 = df.groupby(["@sourceName",'week', '@type'])['@Value'].mean().reset_index()
        df2 = df2.loc[df2['week'] == date1]
        df3 = df3.loc[df3['week'] == date1]

    elif group == 'DOW':
        df2 = df.groupby(["@sourceName",'DOW', '@type'])['@Value'].sum().reset_index()
        df = df.groupby(["@sourceName",'DOW', 'date', '@type'])['@Value'].sum().reset_index()
        df3 = df.groupby(["@sourceName",'DOW', '@type'])['@Value'].mean().reset_index()
        df2 = df2.loc[df2['DOW'] == date1]
        df3 = df2.loc[df3['DOW'] == date1]
    else:
        df3 = df.groupby(["@sourceName", 'date', '@type'])['@Value'].mean().reset_index()
        df2 = df.groupby(["@sourceName",'date', '@type'])['@Value'].sum().reset_index()
        df2 = df2.loc[df2['date'] == date]
        df3 = df3.loc[df3['date'] == date]

    RestingHeartRate,WalkingHeartRate,HeartRate_mean,step,Exercise_minute,ActivitySummary2 ='Not measured','Not measured','Not measured','Not measured','Not measured','Not measured'

    if check == 'sum':
        try:
            RestingHeartRate = str(round(df3[df3['@type'] == 'HKQuantityTypeIdentifierRestingHeartRate'].iloc[0]['@Value'],2))
        except:
            pass
        try:
            WalkingHeartRate = str(round(df3.loc[df3['@type'] == 'HKQuantityTypeIdentifierWalkingHeartRateAverage'].iloc[0]['@Value'], 2))
        except:
            pass
        try:
            HeartRate_mean = str(round(df3.loc[df3['@type'] == 'HKQuantityTypeIdentifierHeartRate'].iloc[0]['@Value'], 2))
        except:
            pass
        try:
            step = str(round(df2.loc[df2['@type'] == 'HKQuantityTypeIdentifierStepCount'].iloc[0]['@Value'], 2))
        except:
            pass
        try:
            Exercise_minute = str(round(df2.loc[df2['@type'] == 'HKQuantityTypeIdentifierAppleExerciseTime'].iloc[0]['@Value'], 2))
        except:
            pass
        try:
            ActivitySummary2 = str(round(df2.loc[df2['@type'] == 'HKQuantityTypeIdentifierActiveEnergyBurned'].iloc[0]['@Value'], 2))
        except:
            pass

        return RestingHeartRate, WalkingHeartRate, step, HeartRate_mean, Exercise_minute, ActivitySummary2
    elif check == 'mean':
        try:
            RestingHeartRate = str(
                round(df3[df3['@type'] == 'HKQuantityTypeIdentifierRestingHeartRate'].iloc[0]['@Value'], 2))
        except:
            pass
        try:
            WalkingHeartRate = str(
                round(df3.loc[df3['@type'] == 'HKQuantityTypeIdentifierWalkingHeartRateAverage'].iloc[0]['@Value'], 2))
        except:
            pass
        try:
            HeartRate_mean = str(
                round(df3.loc[df3['@type'] == 'HKQuantityTypeIdentifierHeartRate'].iloc[0]['@Value'], 2))
        except:
            pass
        try:
            step = str(round(df3.loc[df3['@type'] == 'HKQuantityTypeIdentifierStepCount'].iloc[0]['@Value'], 2))
        except:
            pass
        try:
            Exercise_minute = str(
                round(df3.loc[df3['@type'] == 'HKQuantityTypeIdentifierAppleExerciseTime'].iloc[0]['@Value'], 2))
        except:
            pass
        try:
            ActivitySummary2 = str(
                round(df3.loc[df3['@type'] == 'HKQuantityTypeIdentifierActiveEnergyBurned'].iloc[0]['@Value'], 2))
        except:
            pass

        return RestingHeartRate, WalkingHeartRate, step, HeartRate_mean, Exercise_minute, ActivitySummary2