import pandas as pd


def patient(rdb):
    """ Returns list of patients """

    patients = """SELECT "Name" FROM patient ORDER BY index"""
    try:
        patients = pd.read_sql(patients, rdb)
        patients = patients["Name"].values.tolist()
    except:
        patients = ['Patient']
    return patients


def label(rdb):
    """ Returns list of parameter for linear and bar drop down """

    sql = """SELECT type FROM name """

    try:
        df = pd.read_sql(sql, rdb)
        label_linear = df["type"].values.tolist()
    except:
        label_linear = []
    return label_linear


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
                WHEN type in ('Walking distance unspecified time Pedometer') THEN SUM("Value")
                WHEN type in ('Heart rate 1 hour mean','Systolic blood pressure') THEN AVG("Value")
             END AS "Value"
             FROM applewatch_numeric 
             WHERE "Name" = '{1}'
             AND type in ('Walking distance unspecified time Pedometer','Heart rate 1 hour mean','Systolic blood pressure')               
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

# Comparison Tab

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
