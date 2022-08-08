import pandas as pd
from modules.models import Patient
from sqlalchemy import select
import time


def patient(rdb):
    select(Patient.patient_id).order(Patient.index)
    patients = """SELECT "Name" FROM patient ORDER BY index"""

    patients_df = pd.read_sql(patients, rdb)
    patients_list = patients_df["Name"].values.tolist()
    return patients_list


def label(rdb):
    sql = """SELECT type FROM name """

    sql2 = """SELECT type FROM name """

    df, df2 = pd.read_sql(sql, rdb), pd.read_sql(sql2, rdb)
    label_linear, label_bar = df["type"].values.tolist(), df2["type"].values.tolist()

    return label_linear, label_bar


def month(rdb, patient):
    """ Returns list of months in database for selected patient """

    sql = """SELECT DISTINCT TO_CHAR("Date",'YYYY-MM')  AS month 
             FROM applewatch_numeric 
             WHERE "Name"='{}' 
             AND type ='Resting Heart Rate' 
             ORDER BY month""".format(patient)

    try:
        df = pd.read_sql(sql, rdb)
        months = df['month'].to_list()
    except:
        months = []
    return months


def week(rdb, patient):
    """  Returns list of weeks in database for selected patient  """

    sql = """SELECT DISTINCT TO_CHAR("Date", 'IYYY/IW') AS week 
             FROM applewatch_numeric 
             WHERE "Name"='{}' 
             AND type ='Resting Heart Rate'
             ORDER BY week """.format(patient)

    try:
        df = pd.read_sql(sql, rdb)
        weeks = df['week'].to_list()
    except:
        weeks = []
    return weeks


def min_max_date(rdb, patient):
    """ Returns min and max date for selected patient """

    sql = """SELECT min_date,max_date FROM patient WHERE "Name"='{}'""".format(patient)

    try:
        df = pd.read_sql(sql, rdb)
        min_date, max_date = df['min_date'].iloc[0].date(), df['max_date'].iloc[0].date()
    except:
        min_date, max_date = '', ''

    return min_date, max_date


def age_sex(rdb, patient):
    """ Returns age and gender for selected patient"""

    sql = """SELECT "Age","Sex" from patient where "Name"='{}' """.format(patient)

    try:
        df = pd.read_sql(sql, rdb)
        age, sex = df['Age'][0], df['Sex'][0]
    except:
        age, sex = '', ''
    return age, sex


def classification_ecg(rdb, patient):
    """ Returns ecg classification for patient information card """

    sql = """SELECT "Classification",count(*) FROM ecg WHERE "Patient"='{}' GROUP BY "Classification" """.format(patient)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()
    return df


def number_of_days_more_6(rdb, patient):
    """ Returns number of days the patient had the Apple Watch on their hand for more than 6 hours"""

    sql = """SELECT count (*) 
             FROM (SELECT "Date"::date
                   FROM applewatch_categorical 
                   WHERE "Name" = '{}'
                   AND "type" = 'Apple Stand Hour' 
                   GROUP BY "Date"::date
                   HAVING count("Date"::date) > 6) days  """.format(patient)
    try:
        df = pd.read_sql(sql, rdb)
        df = df.iloc[0]['count']
    except:
        df = '0'

    return df


def card(rdb, patient, group, date, value):
    """ Returns DataFrame with resting, working, mean hear rate, step count, exercise time, activity for the cards """
    if group == 'M':
        to_char = """ TO_CHAR("Date",'YYYY-MM') """
        group_by = "month"
    elif group == 'W':
        to_char = """ TO_CHAR("Date", 'IYYY/IW') """
        group_by = "week"
    elif group == 'DOW':
        to_char = """ TRIM(TO_CHAR("Date", 'Day')) """
        group_by = "DOW"
    else:
        to_char = """ "Date"::date """
        group_by = "date"
        value = date

    sql = """SELECT {0} AS {3},type,
             CASE 
                WHEN type in ('Active Energy Burned','Step Count','Apple Exercise Time') THEN SUM("Value")
                WHEN type in ('Heart Rate','Walking Heart Rate Average','Resting Heart Rate') THEN AVG("Value")
             END AS "Value"
             FROM applewatch_numeric 
             WHERE "Name" = '{1}'
             AND type in ('Active Energy Burned','Step Count','Apple Exercise Time','Heart Rate',
                            'Walking Heart Rate Average','Resting Heart Rate')               
             AND {0}='{2}' 
             GROUP BY {3},type""".format(to_char, patient, value, group_by)

    try:
        df = pd.read_sql(sql, rdb)
        df["Value"] = df["Value"].round(2)

    except:
        df = pd.DataFrame()

    return df


def table(rdb, patient, group, linear, bar):
    """ Returns a table with the patient and parameters that were selected from drop downs """

    if isinstance(linear, list):
        linear = "'" + "','".join(linear) + "'"
    else:
        linear = "'" + linear + "'"

    if group == 'M':
        to_char = """ TO_CHAR("Date",'YYYY-MM')"""
        group_by = "month"
    elif group == 'W':
        to_char = """ TO_CHAR("Date", 'IYYY/IW') """
        group_by = "week"
    elif group == 'DOW':
        to_char = """ TRIM(TO_CHAR("Date",'Day'))  """
        group_by = ' "DOW" '
    else:
        to_char = """ "Date"::date """
        group_by = "date"

    sql = """SELECT {0} as {4},"type",
                CASE WHEN type IN ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2 Max',
                                    'Walking Heart Rate Average') THEN AVG("Value") ELSE SUM("Value")
                END AS "Value"
                FROM applewatch_numeric 
                WHERE "Name" = '{1}' 
                AND "type" in ({2},'{3}') 
                GROUP BY {0},type
                ORDER BY "type",{4} """.format(to_char, patient, linear, bar, group_by)

    try:
        df = pd.read_sql(sql, rdb)
        if group == 'DOW':
            cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            df['DOW'] = pd.Categorical(df['DOW'], categories=cats, ordered=True)
            df = df.sort_values('DOW')
            group_by = "DOW"
        df = df.pivot(index=group_by, columns='type', values='Value').reset_index()
    except:
        df = pd.DataFrame()

    return df, group_by


def day_figure(rdb, patient, bar, date):
    """ Returns DataFrame for day figure with heart rate and selected parameter and patient """

    sql = """ SELECT "Date","type","Value" 
              FROM applewatch_numeric 
              WHERE "Name" = '{}'
              AND "Date"::date='{}' 
              AND "type" in ('Heart Rate','{}') 
              ORDER BY "type","Date" """.format(patient, date, bar)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()

    return df


def trend_figure(rdb, patient, group, start_date, end_date):
    """ Returns DataFrame for trend figure """

    if group == 'M':
        to_char = """ TO_CHAR("Date",'YYYY-MM')"""
        group_by = "month"
    elif group == 'W':
        to_char = """ TO_CHAR("Date", 'IYYY/IW') """
        group_by = "week"
    elif group == 'DOW':
        to_char = """TRIM(TO_CHAR("Date", 'Day'))  """
        group_by = """ "DOW" """
    else:
        to_char = """ "Date"::date """
        group_by = "date"

        """ TRIM(TO_CHAR("Date", 'Day')) in ()"""

    sql = """SELECT {0} as {1},extract('hour' from "Date") as hour,AVG("Value") AS "Value"
             FROM applewatch_numeric 
             WHERE "Name" = '{2}' 
             AND type='Heart Rate' 
             AND "Date" BETWEEN '{3}' AND '{4}' 
             GROUP BY {0},extract('hour' from "Date") 
             ORDER BY {1},hour """.format(to_char, group_by, patient, start_date, end_date)
    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()
    return df

# Query data for ECG_analyse


def ecgs(rdb, patient):
    """  Returns DataFrame for table_ecg"""
    
    sql2 = """SELECT "Day","Date"::time AS Time, "Classification" 
                FROM ecg  
                WHERE "Patient"='{}' 
                ORDER BY "Day" """.format(patient)

    try:
        df = pd.read_sql(sql2, rdb)
    except:
        df = pd.DataFrame()
    return df


def ecg_data(rdb, day, patient, time):
    """ Returns DatFrame to plot  ecg signal   """

    sql = """SELECT * FROM ECG where "Day"='{0}' and "Patient"='{1}' and "Date"::time='{2}' """.format(day, patient, time)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()
    return df


def table_hrv(rdb):
    """ Returns DataFrame with all information about ecg ann calculate HRV feature for time and frequency domain   """

    sql = """ SELECT "Patient","Day","Date"::time as Time, "hrvOwn", "SDNN", "SENN", "SDSD", "pNN20", "pNN50", "lf", 
                "hf", "lf_hf_ratio","total_power", "vlf", "Classification" FROM ecg ORDER BY "Patient","Day" """

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()
    return df


def scatter_plot_ecg(rdb, x_axis, y_axis):
    """ Returns DataFrame for scatter plot with patients ids/numbers and selected features """

    sql = """ SELECT "Patient","{0}","{1}" FROM ecg """.format(x_axis, y_axis)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()
    return df


def box_plot_ecg(rdb, x_axis):
    """ Returns DataFrame for box plot with patients ids/numbers and selected feature    """

    sql = """ SELECT "Patient","{}" FROM ecg """.format(x_axis)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()
    return df

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
