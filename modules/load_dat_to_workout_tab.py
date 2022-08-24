import pandas as pd
from modules.models import AppleWatchNumerical, Workout
from sqlalchemy.sql import select, func, and_,  text
from sqlalchemy import Time, Date


def workout_activity_data(rdb, patients):
    sql = select(Workout.key, Workout.distance, Workout.duration, Workout.energyburned,
                 Workout.start_date.cast(Date).label('date'),
                 Workout.start_date.cast(Time).label("Start"), Workout.end_date.cast(Time).label("End"),
                 func.to_char(Workout.start_date, 'YYYY-MM').label('month'),
                 func.to_char(Workout.start_date, 'IYYY/IW').label('week'),
                 func.trim(func.to_char(Workout.start_date, 'Day')).label("DOW")).\
        where(Workout.patient_id == patients).order_by(Workout.key, Workout.start_date,
                                                       Workout.duration.between(10, 300))
    df = pd.read_sql(sql, rdb)
    df = df[['key', 'date', 'Start', 'End', 'duration', 'distance', 'energyburned']].round(2)
    return df


def workout_check_by_what_group_by(group):
    if group == 'month':
        to_char = func.to_char(Workout.start_date, 'YYYY-MM')
    elif group == 'week':
        to_char = func.to_char(Workout.start_date, 'IYYY/IW')
    elif group == 'DOW':
        to_char = func.trim(func.to_char(Workout.start_date, 'Day'))
    else:
        to_char = Workout.start_date.cast(Date)
    return to_char


def workout_activity_pie_chart(rdb, patients, value, group, what):
    to_char = workout_check_by_what_group_by(group)
    if value:
        if group == 'month': value = value["points"][0]["x"][:7]
        elif group == 'week': value = value["points"][0]["x"]
        elif group == 'DOW': value = value["points"][0]["x"]
        else: value = str(value["points"][0]["x"])
        sql = select(Workout.key, text("Workout."+f'{what}'), to_char.label(group)).\
            where(and_(Workout.patient_id == patients, Workout.duration.between(10, 300), to_char == value))
    else:
        sql = select(Workout.key, to_char.label(group), text("Workout."+f'{what}'), Workout.start_date.cast(Date)).\
            where(Workout.patient_id == patients).limit(1)
    df = pd.read_sql(sql, rdb)
    if not value and not df.empty:
        value = df['start_date'].values[0]
    return df, value


def heart_rate(rdb, click, patients):
    """  Returns DataFrames to plot workout figure in Workout tab"""
    if click is None:
        click = select(Workout.start_date.cast(Date)).where(Workout.patient_id == patients).limit(1).scalar_subquery()
    else:
        click = "'" + str(click["points"][0]["x"]) + "'"

    sql_workout = select(Workout.key, Workout.start_date, Workout.end_date).\
        where(and_(Workout.patient_id == patients, Workout.duration.between(10, 300),
                   Workout.start_date.cast(Date) == click))

    sql_heart_rate = select(AppleWatchNumerical.patient_id, AppleWatchNumerical.date, AppleWatchNumerical.value).\
        where(and_(AppleWatchNumerical.patient_id == patients, AppleWatchNumerical.key == 'Heart Rate',
                   AppleWatchNumerical.date.cast(Date) == click)).\
        order_by(AppleWatchNumerical.date)

    df_workout = pd.read_sql(sql_workout, rdb)
    df_heart_rate = pd.read_sql(sql_heart_rate, rdb)
    return df_workout, df_heart_rate
