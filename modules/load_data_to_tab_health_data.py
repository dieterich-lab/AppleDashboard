import pandas as pd
from modules.models import Patient, AppleWatchNumerical, ECG, AppleWatchCategorical, KeyName
from sqlalchemy.sql import select, func, and_, case, extract, distinct
from sqlalchemy import Time, Date
from datetime import date
import datetime
from dateutil.relativedelta import relativedelta


def patient(rdb):
    select_patient_id = select(Patient.patient_id).order_by(Patient.index)
    patients_id_df = pd.read_sql(select_patient_id, rdb)
    patients_id_list = patients_id_df["patient_id"].values.tolist()
    if not patients_id_list:
        patients_id_list = ['']
    return patients_id_list


def label(rdb):
    labels = select(KeyName.key, KeyName.unit)
    df_labels = pd.read_sql(labels, rdb)
    dict_labels = dict(zip(df_labels.key, df_labels.unit))
    if not dict_labels:
        dict_labels = {'empty': 'empty'}
    return dict_labels


def month(rdb, patients):
    months = select(distinct(func.to_char(AppleWatchNumerical.date, 'YYYY-MM')).label('month')).\
        where(AppleWatchNumerical.patient_id == patients).\
        order_by('month')
    df_months = pd.read_sql(months, rdb)
    months_list = df_months['month'].to_list()
    if not months_list:
        months_list = ['2022-01']
    return months_list


def week(rdb, patients):
    weeks = select(distinct(func.to_char(AppleWatchNumerical.date, 'IYYY/IW')).label('week')).\
        where(AppleWatchNumerical.patient_id == patients).\
        order_by('week')
    df_weeks = pd.read_sql(weeks, rdb)
    weeks_list = df_weeks['week'].to_list()
    if not weeks_list:
        weeks_list = ['2022/04']
    return weeks_list


def min_max_date(rdb, patients):
    sql = select(Patient.min_date, Patient.max_date).where(Patient.patient_id == patients)
    df = pd.read_sql(sql, rdb)
    if df.empty:
        min_date, max_date = datetime.datetime.now(), datetime.datetime.now()
    else:
        min_date, max_date = df['min_date'].iloc[0].date(), df['max_date'].iloc[0].date()
    return min_date, max_date


def age_sex(rdb, patients):
    sql = select(Patient.age, Patient.sex).where(Patient.patient_id == patients)
    df = pd.read_sql(sql, rdb)
    if df.empty:
        age, sex = '', ''
    else:
        age, sex = df['age'][0], df['sex'][0]

    return age, sex


def classification_ecg(rdb, patients):
    sql = select(ECG.classification, func.count(ECG.index)).where(ECG.patient_id == patients).\
        group_by(ECG.classification)
    return pd.read_sql(sql, rdb)


def number_of_days_more_6(rdb, patients):
    sql = select(AppleWatchCategorical.date.cast(Date).label("date")).\
        where(and_(AppleWatchCategorical.patient_id == patients, AppleWatchCategorical.key == 'Apple Stand Hour')).\
        group_by(AppleWatchCategorical.date.cast(Date)).having(func.count("date") > 6)
    sql_number_of_days_standing_more_6_h = select(func.count(sql.c.date).label("count"))
    df = pd.read_sql(sql_number_of_days_standing_more_6_h, rdb)
    return df.iloc[0]['count']


def card(rdb, patients, group, date_value, value):
    group_by_value, to_char, value = check_by_what_group_by(group, date_value, value)

    sql = select(to_char.label(group_by_value), AppleWatchNumerical.key,
                 case((AppleWatchNumerical.key.in_(('Active Energy Burned', 'Step Count', 'Apple Exercise Time')),
                       func.sum(AppleWatchNumerical.value)),
                      (AppleWatchNumerical.key.in_(('Heart Rate', 'Walking Heart Rate Average', 'Resting Heart Rate')),
                       func.avg(AppleWatchNumerical.value))).label("Value")). \
        where(and_(AppleWatchNumerical.patient_id == patients,
                   AppleWatchNumerical.key.in_(('Active Energy Burned', 'Step Count', 'Apple Exercise Time',
                                               'Heart Rate', 'Walking Heart Rate Average', 'Resting Heart Rate')),
                   to_char == value)). \
        group_by(to_char, AppleWatchNumerical.key).order_by(AppleWatchNumerical.key, group_by_value)
    df = pd.read_sql(sql, rdb)
    df["Value"] = df["Value"].round(2)
    return df


def table(rdb, patients, group, linear, bar):
    if isinstance(linear, list):
        key_list = linear + [bar]
    else:
        key_list = [linear, bar]
    group_by_value, to_char, value = check_by_what_group_by(group, '', '')
    sql = select(to_char.label(group_by_value), AppleWatchNumerical.key,
                 case((AppleWatchNumerical.key.in_(('Heart Rate', 'Heart Rate Variability SDNN', 'Resting Heart Rate',
                                                   'VO2 Max', 'Walking Heart Rate Average')),
                       func.avg(AppleWatchNumerical.value)),
                      else_=func.sum(AppleWatchNumerical.value)).label("Value")).\
        where(and_(AppleWatchNumerical.patient_id == patients, AppleWatchNumerical.key.in_(key_list))).\
        group_by(to_char, AppleWatchNumerical.key).order_by(AppleWatchNumerical.key, group_by_value)
    df = pd.read_sql(sql, rdb)
    if group == 'DOW':
        cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df['DOW'] = pd.Categorical(df['DOW'], categories=cats, ordered=True)
        df = df.sort_values('DOW')
        group_by_value = "DOW"
    df = df.pivot(index=group_by_value, columns='key', values='Value').reset_index().round(2)
    return df, group_by_value


def check_by_what_group_by(group, date_value, value):
    if group == 'M':
        to_char = func.to_char(AppleWatchNumerical.date, 'YYYY-MM')
        group_by = "month"
    elif group == 'W':
        to_char = func.to_char(AppleWatchNumerical.date, 'IYYY/IW')
        group_by = "week"
    elif group == 'DOW':
        to_char = func.trim(func.to_char(AppleWatchNumerical.date, 'Day'))
        group_by = "DOW"
    else:
        to_char = AppleWatchNumerical.date.cast(Date)
        group_by = "date"
        value = date_value
    return group_by, to_char, value


def day_figure(rdb, patients, bar, date_value):
    sql = select(AppleWatchNumerical.date, AppleWatchNumerical.key, AppleWatchNumerical.value).\
        where(and_(AppleWatchNumerical.patient_id == patients, AppleWatchNumerical.date.cast(Date) == date_value,
                   AppleWatchNumerical.key.in_(('Heart Rate', bar)))).\
        order_by(AppleWatchNumerical.key, AppleWatchNumerical.date)
    df = pd.read_sql(sql, rdb)
    return df


def trend_figure(rdb, value, date_, group, patients):
    end_date, start_date = calculate_start_and_end_date_for_trend_figure(date_, group, value)

    group_by_value, to_char, value = check_by_what_group_by(group, '', '')
    subquery = select(to_char.label('group'), extract('hour', AppleWatchNumerical.date).label('hour'),
                      AppleWatchNumerical.value).\
        where(and_(AppleWatchNumerical.patient_id == patients, AppleWatchNumerical.key == 'Heart Rate',
                   AppleWatchNumerical.date.between(start_date, end_date)))
    sql = select(subquery.c.group.label(group_by_value), subquery.c.hour, func.avg(subquery.c.value).label("Value")).\
        group_by(group_by_value, "hour").order_by(group_by_value, "hour")
    df = pd.read_sql(sql, rdb)
    if group == 'DOW':
        cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df['DOW'] = pd.Categorical(df['DOW'], categories=cats, ordered=True)
        df = df.sort_values(['DOW', "hour"])
    return df


def calculate_start_and_end_date_for_trend_figure(date_, group, value):
    if group == 'M':
        new_value = datetime.datetime.strptime(value + '-01', "%Y-%m-%d")
        start_date, end_date = new_value - relativedelta(months=3), new_value + relativedelta(months=1)
    elif group == 'W':
        new_value = datetime.datetime.strptime(value + '/1', "%G/%V/%w")
        start_date, end_date = new_value - datetime.timedelta(weeks=3), new_value + datetime.timedelta(weeks=1)
    elif group == "DOW":
        start_date, end_date = '1900-01-01', date.today()
    else:
        start_date, end_date = (pd.to_datetime(date_) - pd.to_timedelta(3, unit='d')), \
                               (pd.to_datetime(date_) + pd.to_timedelta(1, unit='d'))
    return end_date, start_date


def ecgs(rdb, patients):
    sql = select(ECG.day, ECG.date.cast(Time).label("time"), ECG.classification).\
        where(ECG.patient_id == patients).order_by(ECG.day)
    return pd.read_sql(sql, rdb)
