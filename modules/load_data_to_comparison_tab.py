import pandas as pd
from modules.models import Patient, AppleWatchNumerical, Workout, ActivityName
from sqlalchemy.sql import select, func, and_, case, text
from sqlalchemy import Time, Date


def activity_type(rdb):
    sql = select(ActivityName.key)
    df = pd.read_sql(sql, rdb)
    df = df['key'].to_list()
    return df


def plots_comparison(rdb, group, linear, bar):
    sql = select(text('patient.'+f'{group}'), AppleWatchNumerical.date.cast(Date), AppleWatchNumerical.key,
                 case((AppleWatchNumerical.key.in_(('Heart Rate', 'Heart Rate Variability SDNN', 'Resting Heart Rate',
                                                    'VO2 Max', 'Walking Heart Rate Average')),
                       func.avg(AppleWatchNumerical.value)),
                      else_=func.sum(AppleWatchNumerical.value)).label("Value")).\
        where(and_(Patient.patient_id == AppleWatchNumerical.patient_id, AppleWatchNumerical.key.in_([linear, bar]))).\
        group_by(text('patient.'+f'{group}'), AppleWatchNumerical.date.cast(Date), AppleWatchNumerical.key)
    return pd.read_sql(sql, rdb)


def plots_linear(rdb, group, linear, bar):
    sql = select(text('patient.'+f'{group}'), func.to_char(AppleWatchNumerical.date, 'IYYY/IW').label('week'),
                 AppleWatchNumerical.key,
                 case((AppleWatchNumerical.key.in_(('Heart Rate', 'Heart Rate Variability SDNN', 'Resting Heart Rate',
                                                    'VO2 Max', 'Walking Heart Rate Average')),
                       func.avg(AppleWatchNumerical.value)),
                      else_=func.sum(AppleWatchNumerical.value)).label("Value")).\
        where(and_(Patient.patient_id == AppleWatchNumerical.patient_id, AppleWatchNumerical.key.in_([linear, bar]))).\
        group_by(text('patient.'+f'{group}'), 'week', AppleWatchNumerical.key).\
        order_by('week')

    df = pd.read_sql(sql, rdb)
    df[group] = df[group].astype(str)
    return df


def workout_hr_comparison(rdb, group, key):
    sql = select(text('patient.'+f'{group}'), Workout.hr_average).\
        where(and_(Patient.patient_id == Workout.patient_id, Workout.duration.between(10, 300), Workout.hr_average != 0,
                   Workout.key == key)).order_by(text('patient.'+f'{group}'), Workout.start_date)
    sql2 = select(text('patient.'+f'{group}'), Workout.start_date.cast(Date).label('date'),
                  func.avg(Workout.hr_average).label("hr_average")).\
        where(and_(Patient.patient_id == Workout.patient_id, Workout.duration.between(10, 300), Workout.hr_average != 0,
                   Workout.key == key)).group_by(text('patient.'+f'{group}'), 'date').\
        order_by(text('patient.'+f'{group}'), 'date')
    df_box = pd.read_sql(sql, rdb)
    df_scatter = pd.read_sql(sql2, rdb)
    return df_box, df_scatter


def day_night(rdb, group):
    sql = select(text('patient.'+f'{group}'), AppleWatchNumerical.date.cast(Date).label('date'),
                 func.avg(AppleWatchNumerical.value).label('Heart Rate'),
                 case((AppleWatchNumerical.date.cast(Time).between('06:00:00', '24:00:00'), 'day'),
                      else_='night').label("day_night")).\
        where(and_(Patient.patient_id == AppleWatchNumerical.patient_id, AppleWatchNumerical.key == 'Heart Rate')).\
        group_by(text('patient.'+f'{group}'), 'date', 'day_night')
    df = pd.read_sql(sql, rdb)
    return df
