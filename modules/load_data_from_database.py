import pandas as pd
import time

def patient(rdb):
    """
    :param rdb: connection with database
    :return: patients: list of patients
    """
    patients = """SELECT "Name" FROM patient order by index"""
    try:
        patients = pd.read_sql(patients, rdb)
        patients = patients["Name"].values.tolist()
    except:
        patients = ['Patient']
    return patients


def label(rdb):
    """
    Lists for drop downs related with bar plot and linear plot


    :param rdb: connection with database
    :return: label linear: list of names
    :return: label linear: list of names
    """

    sql = """SELECT type FROM name WHERE type IN ('Heart Rate','Heart Rate Variability SDNN', 'Resting Heart Rate',
                                                    'VO2Max','Walking Heart Rate Average')"""

    sql2 = """SELECT type FROM name WHERE type NOT IN ('Heart Rate','Heart Rate Variability SDNN',
                                                        'Resting Heart Rate','VO2 Max','Walking Heart Rate Average')"""

    try:
        df, df2 = pd.read_sql(sql, rdb), pd.read_sql(sql2, rdb)
        label_linear, label_bar = df["type"].values.tolist(), df2["type"].values.tolist()
    except:
        label_linear, label_bar = [], []
    return label_linear, label_bar


def month(rdb, patient):
    """
        Lists for month drop down


        :param rdb: connection with database
        :param patient: patient id/numer
        :return: list with months
    """
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
    """
        Lists for weeks drop down


        :param rdb: connection with database
        :param patient: patient id/numer
        :return: list with weeks
    """
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
    """
        min and max date for selected patient

        :param rdb: connection with database
        :param patient: patient id/numer
        :return min_date
        :return max_date
    """

    sql = """SELECT min_date,max_date FROM patient WHERE "Name"='{}'""".format(patient)

    try:
        df = pd.read_sql(sql, rdb)
        min_date, max_date = df['min_date'].iloc[0].date(), df['max_date'].iloc[0].date()
    except:
        min_date, max_date = '', ''

    return min_date, max_date


def min_max_date_workout(rdb, patient):
    """
        min and max date for selected patient

        :param rdb: connection with database
        :param patient: patient id/numer
        :return min_date
        :return max_date
    """

    sql = """SELECT min_date_workout,max_date_workout FROM workout WHERE "Name" ='{}'""".format(patient)

    try:
        df = pd.read_sql(sql, rdb)
        min_date, max_date = df['min_date_workout'].iloc[0].date(), df['max_date_workout'].iloc[0].date()
    except:
        min_date, max_date = '', ''

    return min_date, max_date


def age_sex(rdb, patient):
    """
    :param rdb: connection with database
    :return: df: list patients
    """

    sql = """SELECT "Age","Sex" from patient where "Name"='{}' """.format(patient)

    try:
        df = pd.read_sql(sql, rdb)
        age, sex = df['Age'][0], df['Sex'][0]
    except:
        age, sex = '', ''
    return age, sex


def irregular_ecg(rdb, patient):
    """
    :param rdb: connection with database
    :return: df: list patients
    """

    sql = """SELECT "Classification",count(*) FROM ecg WHERE "Patient"='{}' GROUP BY "Classification" """.format(patient)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()
    return df


def number_of_days_more_6(rdb, patient):
    """
    :param rdb: connection with database
    :return: df: list patients
    """
    sql = """SELECT count (*) 
             FROM (SELECT dat
                   FROM applewatch_categorical 
                   WHERE "Name" = '{}'
                   AND "type" = 'Apple Stand Hour' 
                   GROUP BY dat
                   HAVING count(dat) > 6) days  """.format(patient)
    try:
        df = pd.read_sql(sql, rdb)
        df = df.iloc[0]['count']
    except:
        df = '0'

    return df


def card(rdb, patient, group, date, value):
    """
    :param rdb: connection with database
    :param patient: connection with database
    :param group: connection with database
    :param date: connection with database
    :param value: connection with database

    :return: : list patients
    """
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
    """
    :param rdb: connection with database
    :param patient: connection with database
    :param group: connection with database
    :param date: connection with database
    :param value: connection with database

    :return: : list patients
    """
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

    return df,group_by


def day_figure(rdb, patient, bar, date):
    """
    :param rdb: connection with database
    :param patient: connection with database
    :param bar: connection with database
    :param date: connection with database

    :return: : list patients
    """

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
    """
    :param rdb: connection with database
    :param patient: connection with database
    :param bar: connection with database
    :param date: connection with database

    :return: : list patients
    """
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


###### ECG_anlayse


def ecgs(rdb, patient):
    """
    :param rdb: connection with database
    :param patient: connection with database
    :param bar: connection with database
    :param date: connection with database

    :return: : list patients
    """
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
    """
    Retreive DataFrame with ECG data

    Parameters:
    ------------
    rdb: connection to database
    day: the day the ECG was taken
    patient: Patient ID
    time: the time the ECG was taken


    Returns:
    ---------
    df : DataFrame with ECG values

    """

    sql = """SELECT * FROM ECG where "Day"='{0}' and "Patient"='{1}' and "Date"::time='{2}' """.format(day, patient, time)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()
    return df


def table_hrv(rdb):
    """
    Retrieve DataFrame with HRV features calculation

    Parameters:
    ------------
    rdb: connection to database


    Returns:
    ---------
    df : DataFrame with HRV features

    """
    sql = """ SELECT "Patient","Day","Date"::time as Time, "hrvOwn", "SDNN", "SENN", "SDSD", "pNN20", "pNN50", "lf", 
                "hf", "lf_hf_ratio","total_power", "vlf", "Classification" FROM ecg ORDER BY "Patient","Day" """

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()
    return df


def scatter_plot_ecg(rdb, x_axis, y_axis):
    """
    Retrieve DataFrame with filtered HRV features

    Parameters:
    ------------
    rdb: connection to database
    x_axis: name of column to select from ECG table
    y_axis: name of column to select from ECG table


    Returns:
    ---------
    df : DataFrame with selected HRV features

    """

    sql = """ SELECT "Patient","{0}","{1}" FROM ecg """.format(x_axis, y_axis)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()
    return df


def box_plot_ecg(rdb, x_axis):
    """
    Retrieve DataFrame with filtered HRV features

    Parameters:
    ------------
    rdb: connection to database
    x_axis: name of column to select from ECG table



    Returns:
    ---------
    df : DataFrame with HRV feature

    """

    sql = """ SELECT "Patient","{}" FROM ecg """.format(x_axis)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()
    return df


##### Patient workouts

def workout_activity_data(rdb, patient):
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

    if group == 'M':
        to_char = """ TO_CHAR("Start_Date",'YYYY-MM')"""
        group_by = "month"
    elif group == 'W':
        to_char = """ TO_CHAR("Start_Date", 'IYYY/IW') """
        group_by = "week"
    elif group == 'DOW':
        to_char = """TRIM(TO_CHAR("Start_Date", 'Day'))  """
        group_by = """ "DOW" """
    else:
        to_char = """ "Start_Date"::date """
        group_by = "date"

    sql = """SELECT type,"{0}",{1} as {2}
                FROM workout  
                WHERE "Name"='{3}' 
                AND {1} ='{4}' """.format(what, to_char, group_by, patient, value)
    print(sql)
    try:
        df = pd.read_sql(sql, rdb)
        print(df)
    except:
        df = pd.DataFrame()

    return df


def heart_rate(rdb, date, patient):

    if date == None:
        sql = """SELECT "Name","Date",name,"Value" FROM applewatch_numeric where "Name"='{}' and 
        date_trunc('day', "Date")='2020-08-01' and type='HKQuantityTypeIdentifierHeartRate' order by "Date" """.format(patient,
                                                                                                               date)
    else:
        sql = """SELECT "Name","Date",name,"Value" FROM applewatch_numeric where "Name"='{}' and 
        date_trunc('day', "Date")='{}' and type='HKQuantityTypeIdentifierHeartRate' order by "Date" """.format(patient,date)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = []

    return df

def HRR(rdb, patient,activity):
    sql = """SELECT "Start_Date",type,duration,"HRR_1_min","HRR_2_min","HR_max","HR_min","HR_average","speed","HR-RS_index" 
    FROM Workout where "Name"='{}' and type = '{}' order by "Start_Date" """.format(patient,activity)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df=[]

    return df


##### Comparison Tab


def activity_type(rdb):
    """
    :param rdb: connection with database
    :return: df: list of workouts type

    """

    sql = """SELECT type FROM activity_type"""

    try:
        df = pd.read_sql(sql, rdb)
        df = df['type'].to_list()
    except:
        df = ['empty']

    return df


def plots_comparison(rdb, gr, linear, bar):
    """
    :param rdb: connection with database
    :return: df: list of workouts type

    """

    sql = """SELECT p."{2}",an."Date"::date as date,an."type",
                CASE WHEN an.type in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
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
    """
    :param rdb: connection with database
    :return: df: list of workouts type

    """
    sql = """ SELECT p."{2}",date_trunc('week', an."Date") AS week,an."type",
                CASE WHEN type in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                                    'Walking Heart Rate Average') THEN AVG("Value") ELSE sum("Value")
                END AS "Value"
                FROM applewatch_numeric as an
                LEFT JOIN patient as p 
                ON p."Name" = an."Name"                  
                WHERE an.type in ('{0}','{1}')
                GROUP BY p."{2}",date_trunc('week', an."Date"),an.type""".format(linear, bar, gr)

    try:
        df = pd.read_sql(sql, rdb)
        if gr == 'Age':
            df[gr] = df[gr].astype(str)
        df_linear = df[df['type'] == linear]
        df_bar = df[df['type'] == bar]
    except:
        df_linear, df_bar = pd.DataFrame(), pd.DataFrame()

    return df_linear, df_bar


def workout_hr_comparison(rdb,gr, type):
    """
    :param rdb: connection with database
    :return: df: list of workouts type

    """
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
    """
    :param rdb: connection with database
    :return: df: list of workouts type

    """
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
