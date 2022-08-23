import pandas as pd
from modules.models import Patient, KeyName, AppleWatchNumerical, ECG, AppleWatchCategorical, Workout, ActivityName
from sqlalchemy.sql import distinct, select, func, and_, case, extract, text
from sqlalchemy import Time, Date
from datetime import date
import datetime
from dateutil.relativedelta import relativedelta


def patient(rdb):
    select_patient_id = select(Patient.patient_id).order_by(Patient.index)
    patients_id_df = pd.read_sql(select_patient_id, rdb)
    patients_id_list = patients_id_df["patient_id"].values.tolist()
    return patients_id_list


def label(rdb):
    labels = select(KeyName.key, KeyName.unit)
    df_labels = pd.read_sql(labels, rdb)
    return dict(zip(df_labels.key, df_labels.unit))


def month(rdb, patients):
    months = select(distinct(func.to_char(AppleWatchNumerical.date, 'YYYY-MM')).label('month')).\
        where(AppleWatchNumerical.patient_id == patients).\
        order_by('month')
    df_months = pd.read_sql(months, rdb)
    months_list = df_months['month'].to_list()
    return months_list


def week(rdb, patients):
    weeks = select(distinct(func.to_char(AppleWatchNumerical.date, 'IYYY/IW')).label('week')).\
        where(AppleWatchNumerical.patient_id == patients).\
        order_by('week')
    df_weeks = pd.read_sql(weeks, rdb)
    weeks_list = df_weeks['week'].to_list()
    return weeks_list


def min_max_date(rdb, patients):
    sql = select(Patient.min_date, Patient.max_date).where(Patient.patient_id == patients)
    df = pd.read_sql(sql, rdb)
    min_date, max_date = df['min_date'].iloc[0].date(), df['max_date'].iloc[0].date()

    return min_date, max_date


def age_sex(rdb, patients):
    sql = select(Patient.age, Patient.sex).where(Patient.patient_id == patients)
    df = pd.read_sql(sql, rdb)
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
    df = df.pivot(index=group_by_value, columns='key', values='Value').reset_index()
    df = df.round(2)
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


# Patient Workouts
def workout_activity_data(rdb, patients):
    sql = select(Workout.key, Workout.distance, Workout.duration, Workout.energyburned,
                 Workout.start_date.cast(Date).label('date'),
                 Workout.start_date.cast(Time).label("Start"), Workout.end_date.cast(Time).label("End"),
                 func.to_char(Workout.start_date, 'YYYY-MM').label('month'),
                 func.to_char(Workout.start_date, 'IYYY/IW').label('week'),
                 func.trim(func.to_char(Workout.start_date, 'Day')).label("DOW")).\
        where(Workout.patient_id == patients).order_by(Workout.key, Workout.start_date)
    df = pd.read_sql(sql, rdb)
    return df


def workout_check_by_what_group_by(group):
    if group == 'M':
        to_char = func.to_char(Workout.start_date, 'YYYY-MM')
        group_by = "month"
    elif group == 'W':
        to_char = func.to_char(Workout.start_date, 'IYYY/IW')
        group_by = "week"
    elif group == 'DOW':
        to_char = func.trim(func.to_char(Workout.start_date, 'Day'))
        group_by = "DOW"
    else:
        to_char = Workout.start_date.cast(Date)
        group_by = "date"

    return group_by, to_char


def workout_activity_pie_chart(rdb, patients, value, group, what):
    group_by_value, to_char = workout_check_by_what_group_by(group)
    if value:
        if group == 'M': value = value["points"][0]["x"][:7]
        elif group == 'W': value = value["points"][0]["x"]
        elif group == 'DOW': value = value["points"][0]["x"]
        else: value = str(value["points"][0]["x"])
        sql = select(Workout.key, text("Workout."+f'{what}'), to_char.label(group_by_value)).\
            where(and_(Workout.patient_id == patients, Workout.duration.between(10, 300), to_char == value))
    else:
        sql = select(Workout.key, to_char.label(group_by_value), text("Workout."+f'{what}'), Workout.start_date.cast(Date)).\
            where(Workout.patient_id == patients).limit(1)
    df = pd.read_sql(sql, rdb)
    if not value:
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


# Comparison Tab
def activity_type(rdb):
    sql = select(ActivityName.key)

    df = pd.read_sql(sql, rdb)
    df = df['key'].to_list()
    return df


def plots_comparison(rdb, group, linear, bar):
    sql1 = select(text('patient.'+f'{group}'), AppleWatchNumerical.date.cast(Date), AppleWatchNumerical.key,
                 case((AppleWatchNumerical.key.in_(('Heart Rate', 'Heart Rate Variability SDNN', 'Resting Heart Rate',
                                                    'VO2 Max', 'Walking Heart Rate Average')),
                       func.avg(AppleWatchNumerical.value)),
                      else_=func.sum(AppleWatchNumerical.value)).label("Value")).\
        where(and_(Patient.patient_id == AppleWatchNumerical.patient_id, AppleWatchNumerical.key.in_([linear, bar]))).\
        group_by(text('patient.'+f'{group}'), AppleWatchNumerical.date.cast(Date), AppleWatchNumerical.key)

    sql2 = select(text('patient.'+f'{group}'), func.to_char(AppleWatchNumerical.date, 'IYYY/IW').label('week'),
                  AppleWatchNumerical.key,
                  case((AppleWatchNumerical.key.in_(('Heart Rate', 'Heart Rate Variability SDNN', 'Resting Heart Rate',
                                                    'VO2 Max', 'Walking Heart Rate Average')),
                       func.avg(AppleWatchNumerical.value)),
                       else_=func.sum(AppleWatchNumerical.value)).label("Value")).\
        where(and_(Patient.patient_id == AppleWatchNumerical.patient_id, AppleWatchNumerical.key.in_([linear, bar]))).\
        group_by(text('patient.'+f'{group}'), 'week', AppleWatchNumerical.key).\
        order_by('week')

    df = pd.read_sql(sql1, rdb)
    df2 = pd.read_sql(sql2, rdb)
    if group == 'Age':
        df2[group] = df2[group].astype(str)
    df_linear = df2[df2['key'] == linear]
    df_bar = df2[df2['key'] == bar]
    return df, df_linear, df_bar


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


# Query data for ECG_analyse

def ecgs(rdb, patients):
    sql = select(ECG.day, ECG.date.cast(Time).label("time"), ECG.classification).\
        where(ECG.patient_id == patients).order_by(ECG.day)
    return pd.read_sql(sql, rdb)


def ecg_data(rdb, day, patients, time):
    sql = select(ECG).where(and_(ECG.day == day, ECG.patient_id == patients,
                                 ECG.date.cast(Time) == time))
    return pd.read_sql(sql, rdb)


def table_hrv(rdb):
    sql = select(ECG.patient_id, ECG.date.cast(Time).label("time"), ECG.day, ECG.number, ECG.classification).\
        order_by(ECG.patient_id, ECG.day)
    return pd.read_sql(sql, rdb)


def scatter_plot_ecg(rdb, x_axis, y_axis):
    sql = select(ECG.patient_id, text('ECG.' + f'{x_axis}'), text('ECG.' + f'{y_axis}'))

    return pd.read_sql(sql, rdb)


def box_plot_ecg(rdb, x_axis):
    sql = select(ECG.patient_id, text('ECG.' + f'{x_axis}'))
    return pd.read_sql(sql, rdb)
