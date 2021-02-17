import modules.load_data_from_database as ldd
import psycopg2.extras
import os
import time



# Connection with database
def connect_db():
    """ connects to database """
    try:
        db = psycopg2.connect(  host="localhost",
                                database="example",
                                user="test",
                                password="test",
                                port=5424)
        return db
    except Exception:
        time.sleep(0.1)

rdb = connect_db()

df, df2 = ldd.Card(rdb)



df = df.loc[df["@sourceName"] == 'Patient1']
df2 = df2.loc[df2["@sourceName"] == 'Patient1']
print(df)
print(df2)

"""
    if group == 'M':
        df = df.groupby(["@sourceName", 'month', 'date', '@type'])['@Value'].sum().reset_index()
        df3 = df.groupby(["@sourceName", 'month', '@type'])['@Value'].mean().reset_index()
        df2 = df.groupby(["@sourceName", 'month', '@type'])['@Value'].sum().reset_index()

        if len(str(date)) == 1:
            df2 = df2.loc[df2['month'] == '2020-0{}'.format(date)]
            df3 = df3.loc[df3['month'] == '2020-0{}'.format(date)]
        else:
            df2 = df2.loc[df2['month'] == '2020-{}'.format(date)]
            df3 = df3.loc[df3['month'] == '2020-{}'.format(date)]

    elif group == 'W':
        df2 = df.groupby(["@sourceName",'week', '@type'])['@Value'].sum().reset_index()
        df = df.groupby(["@sourceName",'week', 'date', '@type'])['@Value'].sum().reset_index()
        df3 = df.groupby(["@sourceName",'week', '@type'])['@Value'].mean().reset_index()
        df2 = df2.loc[df2['week'] == date]
        df3 = df3.loc[df3['week'] == date]

    elif group == 'DOW':
        df2 = df.groupby(["@sourceName",'DOW', '@type'])['@Value'].sum().reset_index()
        df = df.groupby(["@sourceName",'DOW', 'date', '@type'])['@Value'].sum().reset_index()
        df3 = df.groupby(["@sourceName",'DOW', '@type'])['@Value'].mean().reset_index()
        df2 = df2.loc[df2['DOW'] == date]
        df3 = df2.loc[df3['DOW'] == date]
    else:
        df3 = df.groupby(["@sourceName", 'date', '@type'])['@Value'].mean().reset_index()
        df2 = df.groupby(["@sourceName",'date', '@type'])['@Value'].sum().reset_index()
        df2 = df2.loc[df2['date'] == date]
        df3 = df3.loc[df3['date'] == date]

    """
RestingHeartRate,WalkingHeartRate,HeartRate_mean,step,Exercise_minute,ActivitySummary2 = 'Not measured', \
                                                                                             'Not measured',\
                                                                                             'Not measured',\
                                                                                             'Not measured',\
                                                                                             'Not measured',\
                                                                                             'Not measured'
"""
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
        step = str(round(df2.loc[df2['@type'] == 'HKQuantityTypeIdentifierStepCount'].iloc[0]['@Value'], 2)) #+ '|' + str(round(df3.loc[df3['@type'] == 'HKQuantityTypeIdentifierStepCount'].iloc[0]['@Value'], 2))
    except:
        pass
    try:
        Exercise_minute = str(round(df2.loc[df2['@type'] == 'HKQuantityTypeIdentifierAppleExerciseTime'].iloc[0]['@Value'], 2)) #+ '|' + str(
                #round(df3.loc[df3['@type'] == 'HKQuantityTypeIdentifierAppleExerciseTime'].iloc[0]['@Value'], 2))
    except:
        pass
    try:
        ActivitySummary2 = str(round(df2.loc[df2['@type'] == 'HKQuantityTypeIdentifierActiveEnergyBurned'].iloc[0]['@Value'], 2)) #+ '|' + str(
                #round(df3.loc[df3['@type'] == 'HKQuantityTypeIdentifierActiveEnergyBurned'].iloc[0]['@Value'], 2))
    except:
        pass
        
"""
