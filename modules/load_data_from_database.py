import pandas as pd
from modules.models import Patient, KeyName, AppleWatchNumerical, ECG, AppleWatchCategorical
from sqlalchemy.sql import distinct, select, func, and_, case, extract
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
    labels = select(KeyName.key)
    df_labels = pd.read_sql(labels, rdb)
    labels_list = df_labels["key"].values.tolist()
    return labels_list


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
    sql = select(ECG).order_by(ECG.patient_id, ECG.day)
    return pd.read_sql(sql, rdb)


def scatter_plot_ecg(rdb, x_axis, y_axis):
    print(x_axis)

    return {}


def box_plot_ecg(rdb, x_axis):

    return {}

# Patient Workouts


def workout_activity_data(rdb, patient):
    """ Returns the DataFrame for table and summary figure on the Workouts Tab. The table is filtered by selected
        patient in drop down list """

    sql = """SELECT type,duration,distance,"EnergyBurned","Start_Date"::date AS date,"Start_Date"::time AS "Start",
                    "End_Date"::time AS "End",TO_CHAR("Start_Date",'YYYY-MM') AS month,
                    TO_CHAR("Start_Date", 'IYYY/IW') as week,TO_CHAR("Start_Date", 'Day') as "DOW"
             FROM workout  
             WHERE "Name"='{}' 
             ORDER BY type,"Start_Date"  """.format(patient)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()
    return df


def workout_activity_pie_chart(rdb, patient, value, group, what):
    """ Returns the DataFrame for pie plot on the Workouts Tab. The table is filtered and grouped by selected
        patient,day/week/month in drop down list  """

    if group == 'M':
        if value is not None: value = value["points"][0]["x"][:7]
        to_char = """ TO_CHAR("Start_Date",'YYYY-MM')"""
        group_by = "month"
    elif group == 'W':
        if value is not None: value = value["points"][0]["x"]
        to_char = """ TO_CHAR("Start_Date", 'IYYY/IW') """
        group_by = "week"
    elif group == 'DOW':
        if value is not None: value = value["points"][0]["x"].replace(" ", "")
        to_char = """TRIM(TO_CHAR("Start_Date", 'Day'))  """
        group_by = """ "DOW" """
    else:
        if value is not None: value = str(value["points"][0]["x"])
        to_char = """ "Start_Date"::date """
        group_by = "date"

    if value is None:
        value = """SELECT {}  AS {} 
                   FROM workout
                   WHERE "Name"='{}' 
                   LIMIT 1""".format(to_char, group, patient)
    else:
        value = "'"+value+"'"

    sql = """SELECT type,"{0}",{1} as {2}
                FROM workout  
                WHERE "Name"='{3}' 
                AND duration between 10 and 300 
                AND {1} in ({4}) """.format(what, to_char, group_by, patient, value)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()
    return df


def heart_rate(rdb, click, patient):
    """  Returns DataFrames to plot workout figure in Workout tab"""

    if click is None:
        click = """SELECT "Start_Date":: date  AS day 
                   FROM workout
                   WHERE "Name"='{}' 
                   LIMIT 1""".format(patient)
    else:
        click = "'" + str(click["points"][0]["x"]) + "'"

    sql1 = """SELECT type,"Start_Date","End_Date"
                FROM workout  
                WHERE "Name"='{}' 
                AND duration between 10 and 300 
                AND "Start_Date":: date in ({}) """.format(patient, click)

    sql2 = """SELECT "Name","Date","Value" 
                FROM applewatch_numeric 
                WHERE "Name"='{}' 
                AND "Date":: date in ({}) 
                AND type='Heart Rate' 
                order by "Date" """.format(patient, click)
    try:
        df1 = pd.read_sql(sql1, rdb)
        df2 = pd.read_sql(sql2, rdb)
    except:
        df1, df2 = pd.DataFrame(), pd.DataFrame()

    return df1, df2


# Comparison Tab
def activity_type(rdb):
    """  Select types of workouts for drop down in Comparison tab"""

    sql = """SELECT type FROM activity_type"""

    try:
        df = pd.read_sql(sql, rdb)
        df = df['type'].to_list()
    except:
        df = ['empty']

    return df


def plots_comparison(rdb, gr, linear, bar):
    """ Returns DataFrame to update box plots, histogram, scatter plot in comparison tab depending on the drop downs """

    sql = """SELECT p."{2}",an."Date"::date as date,an."type",
                CASE WHEN an.type in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2 Max',
                                'Walking Heart Rate Average') THEN AVG("Value") ELSE sum("Value")
                END as "Value" 
                FROM applewatch_numeric as an 
                LEFT JOIN patient as p 
                ON p."Name" = an."Name"
                WHERE an.type in ('{0}','{1}')
                GROUP BY p."{2}",(an."Date"::date),an.type""".format(linear, bar, gr)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()

    return df


def linear_plot(rdb, gr, linear, bar):
    """ Returns DataFrame to update linear plot in comparison tab depending on the drop downs """

    sql = """ SELECT p."{2}",date_trunc('week', an."Date") AS week,an."type",
                CASE WHEN type in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2 Max',
                                    'Walking Heart Rate Average') THEN AVG("Value") ELSE sum("Value")
                END AS "Value"
                FROM applewatch_numeric as an
                LEFT JOIN patient as p 
                ON p."Name" = an."Name"                  
                WHERE an.type in ('{0}','{1}')
                GROUP BY p."{2}",date_trunc('week', an."Date"),an.type
                ORDER BY week """.format(linear, bar, gr)

    try:
        df = pd.read_sql(sql, rdb)
        if gr == 'Age':
            df[gr] = df[gr].astype(str)
        df_linear = df[df['type'] == linear]
        df_bar = df[df['type'] == bar]
    except:
        df_linear, df_bar = pd.DataFrame(), pd.DataFrame()

    return df_linear, df_bar


def workout_hr_comparison(rdb, gr, type):
    """ Returns DataFrame to compare heart rate during workouts in comparison tab """

    sql = """SELECT p."{0}",w."HR_average" 
             FROM workout as w 
             LEFT JOIN patient as p 
             ON p."Name" = w."Name"
             WHERE w."duration" > 10 AND w."duration" < 300 
             AND "HR_average" !='0' 
             AND w.type = '{1}' 
             ORDER BY p."{0}",w."Start_Date" """.format(gr, type)

    sql2 = """SELECT p."{0}","Start_Date"::date as date,AVG(w."HR_average") as "HR_average" 
                FROM workout as w 
                LEFT JOIN patient as p 
                ON p."Name" = w."Name"
                WHERE w."duration" > 10 and w."duration" < 300 
                AND "HR_average" !='0' 
                AND w.type = '{1}' 
                GROUP BY p."{0}",date
                ORDER BY p."{0}",date""".format(gr, type)
    try:
        df_box = pd.read_sql(sql, rdb)
        df_scatter = pd.read_sql(sql2, rdb)
    except:
        df_box, df_scatter = pd.DataFrame(), pd.DataFrame()

    return df_box, df_scatter


def day_night(rdb, gr):
    """ Returns DataFrame with heart rate divided for night and day """

    sql = """SELECT p."{0}","Date":: date as date,AVG("Value") as "Heart rate", 
            CASE WHEN "Date"::time BETWEEN '06:00:00' AND '24:00:00' THEN 'day'
            ELSE 'night'
            END as day_night
            FROM applewatch_numeric as an
            LEFT JOIN patient as p 
            ON p."Name" = an."Name"     
            WHERE type='Heart Rate' 
            GROUP BY p."{0}",date,day_night""".format(gr)
    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()

    return df
