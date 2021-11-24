import pandas as pd


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
                                                        'Resting Heart Rate','VO2Max','Walking Heart Rate Average')"""

    try:
        df, df2 = pd.read_sql(sql, rdb), pd.read_sql(sql2, rdb)
        label_linear, label_bar = df["type"].values.tolist(), df2["type"].values.tolist()
    except:
        label_linear, label_bar = [], []
    return label_linear, label_bar


def age_sex(rdb, patient):
    """
    :param rdb: connection with database
    :return: df: list patients
    """
    sql = """SELECT "Age","Sex" from patient where "Name"='{}' """.format(patient)
    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()
    return df


def min_max_date(rdb, patient):

    sql = """SELECT min_date,max_date from patient where "Name"='{}'""".format(patient)

    try:
        df = pd.read_sql(sql, rdb)
        min_date, max_date = df['min_date'].iloc[0].date(), df['max_date'].iloc[0].date()
    except:
        min_date,max_date='',''

    return min_date, max_date


def min_max_date_workout(rdb, patient):

    sql = """SELECT MIN("Start_Date"),MAX("End_Date") from workout where "Name" ='{}'""".format(patient)

    df = pd.read_sql(sql, rdb)
    min_date, max_date = df['min'].iloc[0].date(), df['max'].iloc[0].date()

    return min_date, max_date


def irregular_ecg(rdb, patient):

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
    sql = """SELECT "Name",count(*) 
            FROM (SELECT "Name",DATE_TRUNC('day', "Date") AS date,"type","type",
                                                  count(*) AS number 
                  FROM applewatch_categorical 
                  WHERE "type" = 'HKCategoryTypeIdentifierAppleStandHour' 
                  GROUP BY "Name",date,"type","type" 
                  HAVING count(*) > 6 
                  ORDER BY "Name",date) AS foo 
            WHERE "Name" = '{}' 
            GROUP BY "Name" """.format(patient)
    try:
        df = pd.read_sql(sql, rdb)
        df = df.iloc[0]['count']
    except:
        df = ''

    return df


def month(rdb, patient):
    sql = """ SELECT to_char(month,'YYYY-MM') AS month 
              FROM (SELECT distinct date_trunc('month', "Date")  AS month 
                    FROM applewatch_numeric 
                    where "Name"='{}' 
                    and type ='Resting Heart Rate' 
                    order by date_trunc('month', "Date")) as foo""".format(patient)

    try:
        df = pd.read_sql(sql, rdb)
        df = df['month'].to_list()
    except:
        df = pd.DataFrame()
    return df


def week(rdb, patient):
    sql = """ select distinct week 
              from (SELECT to_char("Date", 'IYYY/IW') as week 
                    FROM applewatch_numeric 
                    where "Name"='{}' 
                    and type ='Resting Heart Rate') as foo 
              order by week """.format(patient)

    try:
        df = pd.read_sql(sql, rdb)
        df = df['week'].to_list()
    except:
        df = pd.DataFrame()

    return df













def Card(rdb, patient, group, date, value):

    if group == 'M':
        sql = """ SELECT type,month,sum("Value"),AVG("Value") 
                   FROM (SELECT to_char(date_trunc('month', "Date"),'YYYY-MM') AS month,type,"Value" 
                         FROM applewatch_numeric 
                         WHERE "Name" = '{}' 
                         AND type in ('Active Energy Burned','Heart Rate','Walking Heart Rate Average',
                                        'Resting Heart Rate','Step Count','Apple Exercise Time') 
                          ORDER BY type,"Date") as foo 
                    WHERE month='{}' 
                    GROUP BY month,type""".format(patient, value)
    elif group == 'W':
        sql = """ select type,week,sum("Value"),AVG("Value") 
                  from (SELECT to_char("Date", 'IYYY/IW') as week,type,"Value" 
                        FROM applewatch_numeric 
                        where "Name" = '{}' 
                        and type in ('Active Energy Burned','Heart Rate','Walking Heart Rate Average',
                                    'Resting Heart Rate','Step Count','Apple Exercise Time') 
                        order by type,"Date") as foo 
                  where week='{}' 
                  group by week,type""".format(patient,value)
    elif group == 'DOW' :
        sql = """ select type,"DOW",sum("Value"),AVG("Value") 
                  from (SELECT trim(to_char("Date", 'Day')) as "DOW",type,"Value" 
                        FROM applewatch_numeric 
                        where "Name" = '{}' 
                        and type in ('Active Energy Burned','Heart Rate','Walking Heart Rate Average',
                                    'Resting Heart Rate','Step Count','Apple Exercise Time') 
                        order by type,"Date") as foo 
                  where "DOW"='{}' 
                  group by "DOW",type""".format(patient,value)
    else:
        sql = """ select type,sum("Value"),AVG("Value") 
                  from (SELECT date_trunc('day', "Date") as date,type,"Value" 
                        FROM applewatch_numeric 
                        where "Name" = '{}' 
                        and type in ('Active Energy Burned','Heart Rate','Walking Heart Rate Average',
                                        'Resting Heart Rate','Step Count','Apple Exercise Time')
                        order by type,"Date") as foo 
                  where date = '{}' 
                  group by date,type""".format(patient,date)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()

    return df


def table(rdb, patient, group, linear, bar):

    if isinstance(bar, list):
        bar = "'" + "','".join(bar) + "'"
    else:
        bar = "'"+bar+"'"
    if isinstance(linear, list):
        linear = "'" + "','".join(linear) + "'"
    else:
        linear = "'" + linear + "'"

    if group == 'M':
        sql = """ select type,month,
                    case when type in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                                'Walking Heart Rate Average') 
                    Then AVG("Value")
                    ELSE sum("Value")
                    end as "Value"
                    from (SELECT to_char(date_trunc('month', "Date"),'YYYY-MM') as month,"type", "Value" 
                          FROM applewatch_numeric 
                          where "Name" = '{}' 
                          and "type" in ({},{}) 
                          order by "type","Date") as foo 
                    group by month,type""".format(patient, linear, bar)
    elif group == 'W':
        sql = """ select type,week,
                    case when type in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                                        'Walking Heart Rate Average') Then AVG("Value")
                    ELSE sum("Value")
                    end as "Value"
                    from (SELECT to_char("Date", 'IYYY/IW') as week,"type","Value" 
                          FROM applewatch_numeric 
                          where "Name" = '{}' 
                          and "type" in ({},{}) 
                          order by "type","Date") as foo 
                    group by week,type""".format(patient,linear,bar)
    elif group == 'DOW' :
        sql = """ select type,"DOW_number","DOW",
                    case when type in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                                    'Walking Heart Rate Average') 
                    Then AVG("Value")
                    ELSE sum("Value")
                    end as "Value"
                    from (SELECT trim(to_char("Date", 'Day')) as "DOW",extract('ISODOW' from "Date") as "DOW_number",
                                    "type","Value" 
                          FROM applewatch_numeric 
                          where "Name" = '{}' 
                          and "type" in ({},{}) 
                          order by "type","Date") as foo 
                    group by "DOW","DOW_number",type 
                    order by "DOW_number" """.format(patient,linear,bar)
    else:
        sql = """ select type,date,
                    case when type in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                                        'Walking Heart Rate Average') 
                    Then AVG("Value")
                    ELSE sum("Value")
                    end as "Value"
                    from (SELECT "type",date_trunc('day', "Date")::date as date,"Value" 
                          FROM applewatch_numeric 
                          where "Name" = '{0}' 
                          and "type" in ({1},{2})
                          order by "type","Date") as foo 
                    group by date,type""".format(patient,linear,bar)
    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()

    return df


def day_figure(rdb, patient, group, linear, bar, date, value):
    if isinstance(bar, list):
        bar = "'" + "','".join(bar) + "'"
    else:
        bar = "'"+bar+"'"
    if isinstance(linear, list):
        linear = "'" + "','".join(linear) + "'"
    else:
        linear = "'" + linear + "'"

    if group == 'M':
        sql = """ select "Date",type,month,"Value"
                  from (SELECT "Date",to_char(date_trunc('month', "Date"),'YYYY-MM') as month,"type", "Value" 
                        FROM applewatch_numeric 
                        where "Name" = '{}' 
                        and "type" in ('Heart Rate',{}) 
                        order by "type","Date") as foo 
                  where month='{}' """.format(patient, bar, value)
    elif group == 'W':
        sql = """ select "Date",type,week,"Value" 
                  from (SELECT "Date",to_char("Date", 'IYYY/IW') as week,"type","Value" 
                        FROM applewatch_numeric 
                        where "Name" = '{}' 
                        and "type" in ({},{}) 
                        order by "type","Date") as foo 
                  where week='{}' """.format(patient,linear,bar, value)
    elif group == 'DOW':
        sql = """ select "Date",date,type,"DOW","Value" 
                  from (SELECT "Date",trim(to_char("Date", 'Day')) as "DOW",date_trunc('day', "Date") as date,
                                type,"Value" 
                        FROM applewatch_numeric 
                        where "Name" = '{}' 
                        and "type" in ({},{}) 
                        order by "type","Date") as foo 
                  where "DOW"='{}' 
                  and date = (SELECT Max(date_trunc('day', "Date")) FROM applewatch_numeric) """.format(patient,linear,bar, value)
    else:
        sql = """ select "Date",type,"Value" 
                  from (SELECT "Date",date_trunc('day', "Date") as date,"type","Value" 
                        FROM applewatch_numeric 
                        where "Name" = '{}' 
                        and "type" in ('Heart Rate',{})
                        order by "type","Date") as foo 
                  where date = '{}' """.format(patient,bar, date)
    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()

    return df


def trend_figure(rdb, patient, group, start_date,end_date):

    if group == 'M':
        sql = """ select month,hour,avg("Value") as "Value" 
                  from (SELECT to_char(date_trunc('month', "Date"),'YYYY-MM') as month,extract('hour' from "Date") as hour,"Value" 
                        FROM applewatch_numeric 
                        where "Name" = '{}' 
                        and "type"= 'Heart Rate' 
                        and "Date" > '{}' 
                        and "Date" < '{}' 
                        order by "Date") as foo 
                  group by month,hour order by month,hour""".format(patient,start_date,end_date)
    elif group == 'W':
        sql = """ select week,hour,avg("Value") as "Value" 
                  from (SELECT to_char("Date", 'IYYY/IW') as week,extract('hour' from "Date") as hour,"Value" 
                        FROM applewatch_numeric 
                        where "Name" = '{}' 
                        and type='Heart Rate' 
                        and "Date" > '{}' 
                        and "Date" < '{}' 
                        order by "Date")
                  as foo group by week,hour 
                  order by week,hour""".format(patient,start_date,end_date)
    elif group == 'DOW':
        sql = """ select "DOW","DOW_number",hour,avg("Value") as "Value" 
                  from (SELECT trim(to_char("Date", 'Day')) as "DOW",extract('ISODOW' from "Date") as "DOW_number",
                                extract('hour' from "Date") as hour,"Value" 
                        FROM applewatch_numeric 
                        where "Name" = '{}' 
                        and type='Heart Rate' 
                        order by "Date") as foo 
                  where "DOW_number" > '{}' 
                  and "DOW_number" < '{}' 
                  group by "DOW","DOW_number",hour  """.format(patient, start_date,end_date)
    else:
        sql = """ select date,hour,avg("Value") as "Value" 
                  from (SELECT "Date",extract('hour' from "Date") as hour,date_trunc('day', "Date") as date,"type","Value" 
                        FROM applewatch_numeric 
                        where "Name" = '{}' 
                        and type='Heart Rate' 
                        and "Date" > '{}' 
                        and "Date" < '{}'
                  order by "Date") as foo 
                  group by date,hour """.format(patient,start_date,end_date)
    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()
    return df


def box_plot(rdb, group, line,bar):

    if group == 'M':
        sql1 = """select "Name",AVG("Value") 
                  from (SELECT "Name",to_char(date_trunc('month', "Date"),'YYYY-MM') as month,"type", "Value" 
                        FROM applewatch_numeric 
                        where "type" in ('{}')) as foo 
                  group by "Name",month """.format(bar)

        sql2 = """select "Name",type,"Value" 
                  from (SELECT "Name",to_char(date_trunc('month', "Date"),'YYYY-MM') as month,"type", "Value" 
                        FROM applewatch_numeric 
                        where "type" in ('{}')) as foo 
                  group by "Name",month""".format(line)
    elif group == 'W':
        sql1 = """select "Name",AVG("Value") 
                  from (SELECT "Name",to_char("Date", 'IYYY/IW') as week,"type", "Value" 
                        FROM applewatch_numeric 
                        where "type" in ('{}')) as foo 
                  group by "Name",week """.format(bar)

        sql2 = """select "Name",type,"Value" 
                  from (SELECT "Name",to_char("Date", 'IYYY/IW') as week,"type","Value" 
                        FROM applewatch_numeric 
                        where "type" in ('{}')) as foo 
                   group by "Name",week """.format(line)

    elif group == 'DOW':
        sql1 = """select "Name",AVG("Value") 
                  from (SELECT "Name",trim(to_char("Date", 'Day')) as "DOW","type","Value" 
                        FROM applewatch_numeric 
                        where "type" in ('{}')) as foo 
                  group by "Name","DOW" """.format(bar)

        sql2 = """select "Name",type,"Value" 
                  from (SELECT "Name",trim(to_char("Date", 'Day')) as "DOW","type","Value" 
                        FROM applewatch_numeric 
                        where "type" in ('{}')) as foo 
                  group by "Name","DOW" """.format(line)
    else:
        sql1 = """select "Name",AVG("Value") from (SELECT "Name",date_trunc('day', "Date") as date,"type",
            "Value" FROM applewatch_numeric where "type" in ('{}')) as foo group by "Name",date """.format(bar)

        sql2 = """select "Name",type,"Value" from (SELECT "type",date_trunc('day', "Date") as date,"type",
                "Value" FROM applewatch_numeric where "name" in ('{}')) as foo "Name",date """.format(line)


    df1 = pd.read_sql(sql1, rdb)
    df2 = pd.read_sql(sql2, rdb)

    return df1,df2


def histogram_plot(rdb, group, line):

    sql = """SELECT "Name","Value" FROM applewatch_numeric where type='HKQuantityTypeIdentifierHeartRate' """

    df = pd.read_sql(sql, rdb)

    return df



def during_workout(rdb, group, line):

    sql = """SELECT "Name",date_trunc('day', "Date") as date,AVG("Value") as "Value" 
             FROM applewatch_numeric 
             where type='HKQuantityTypeIdentifierHeartRate' 
             group by "Name",date_trunc('day', "Date") 
             order by "Name",date_trunc('day', "Date") """

    df = pd.read_sql(sql, rdb)

    return df




"""
select *,"@startDate"::timestamp - lag("@startDate"::timestamp) over(partition by "@sourceName" order by "@sourceName",
"@startDate") as difference from applewatch_numeric where "@type" ='HKQuantityTypeIdentifierHeartRate';
"""
##### Patient workouts

def HKWorkoutActivity(rdb):
    sql = """select distinct @workoutActivityType FROM workout  """
    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = []
    return df

def WorkoutActivity_data(rdb,patient):
    sql = """select type,duration,distance,"EnergyBurned",
                "Start_Date"::time as "Start",
                "End_Date"::time as "End",
                to_char(date_trunc('month', "Start_Date"),'YYYY-MM') as month,
                to_char("Start_Date", 'IYYY/IW') as week,
                extract('week' from "Start_Date") as week_num,
                extract('ISODOW' from "Start_Date") as "DOW_number",
                to_char("Start_Date", 'Day') as "DOW",
                date_trunc('day', "Start_Date")::date  as date
                FROM workout  where "Name"='{}' order by "type","Start_Date"  """.format(patient)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df=[]
    return df


def WorkoutActivity_pie_chart(rdb, patient, group, date, value):

    if group == 'M':
        sql = """select *,
                    to_char(date_trunc('month', "Start_Date"),'YYYY-MM') as month
                    FROM workout  where "Name"='{}' and to_char(date_trunc('month', "Start_Date"),'YYYY-MM') ='{}'
                     order by "type","Start_Date"  """.format(patient,value)
    elif group == 'W':
        sql = """select *,
                    to_char("Start_Date", 'IYYY/IW') as week
                    FROM workout  where "Name"='{}' and to_char("Start_Date", 'IYYY/IW')='{}'
                     order by "type","Start_Date"  """.format(patient,value)
    elif group == 'DOW':
        sql = """select *,
                    trim(to_char("Start_Date", 'Day')) as "DOW",
                    extract('ISODOW' from "Start_Date") as "DOW_number"
                    FROM workout  where "Name"='{}' and trim(to_char("Start_Date", 'Day'))='{}'
                     order by "type","Start_Date"  """.format(patient,value)
    else:
        sql = """select *,
                    date_trunc('day', "Start_Date") as date
                    FROM workout  where "Name"='{}' and date_trunc('day', "Start_Date") ='{}'
                     order by "type","Start_Date"  """.format(patient,date)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.Dataframe()

    return df

def Heart_Rate(rdb, date, patient):

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

##### Patient comparison


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


def plots(rdb, gr, linear, bar):
    """
    :param rdb: connection with database
    :return: df: list of workouts type

    """
    sql = """ SELECT p."{2}",foo.type,foo.date,
                CASE 
                WHEN type in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                            'Walking Heart Rate Average') THEN AVG("Value")
                ELSE sum("Value")
                END as "Value"
                FROM (SELECT "Name",date_trunc('day', "Date") as date,"type", "Value" FROM applewatch_numeric 
                WHERE type in ('{0}','{1}')) as foo 
                LEFT JOIN patient as p 
                ON p."Name" = foo."Name"
                GROUP BY p."{2}",foo.date,foo.type""".format(linear, bar,gr)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = pd.DataFrame()

    return df

def day_night(rdb,):

    sql = """ SELECT "Name",date_trunc('day', "Date") as date,AVG("Value") as "Heart rate", 
            CASE when "Date"::time between '06:00:00' and '24:00:00' THEN 'day'
            ELSE 'night'
            END as day_night
            FROM applewatch_numeric 
                where type='Heart Rate' group by "Name",date,day_night"""

    df_day_time = pd.read_sql(sql, rdb)

    return df_day_time



def linear_plot(rdb,gr, linear, bar):

    sql = """ select p."{2}",foo.type,foo.week,
                case 
                when type in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                'Walking Heart Rate Average') Then AVG("Value")
                ELSE sum("Value")
                end as "Value"
                from (SELECT "Name",date_trunc('week', "Date") as week,"type", "Value" FROM applewatch_numeric 
                where type in ('{0}','{1}')) as foo LEFT JOIN patient as p 
                on p."Name" = foo."Name" group by p."{2}",foo.week,foo.type""".format(linear, bar,gr)



    df = pd.read_sql(sql, rdb)
    if gr == 'Age':
        df[gr] = df[gr].astype(str)
    df1 = df[df['type'] == linear]
    df2 = df[df['type'] == bar]


    return df1,df2

def Heart_Rate_workout_comparison(rdb,gr, type):

    sql = """select p."{0}",w."HR_average" FROM workout as w 
    LEFT JOIN patient as p 
    on p."Name" = w."Name"
    where w."duration" > 10 and w."duration" < 300 and "HR_average" !='0' and w.type = '{1}' 
        order by p."{0}",w."Start_Date"
          """.format(gr,type)


    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = []

    return df

def Heart_Rate_workout_changes(rdb,gr, type):

    sql = """select p."{0}",date_trunc('day', w."Start_Date") as date,AVG(w."HR_average") as "HR_average" FROM workout as w 
    LEFT JOIN patient as p 
    on p."Name" = w."Name"
    where w."duration" > 10 and w."duration" < 300 and "HR_average" !='0' and w.type = '{1}' group by p."{0}",date
        order by p."{0}",date
          """.format(gr,type)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = []

    return df


###### ECG_anlayse


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
                "hf", "lf_hf_ratio","total_power", "vlf", "Classification" from ecg  order by "Patient","Day" """

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


def irregular_ecg2(rdb, patient):


    sql2 = """ select "Day","Date"::time as Time, "Classification" from ecg  where "Patient"='{}' order by "Day" """.format(patient)

    try:
        df = pd.read_sql(sql2, rdb)
    except:
        df = pd.DataFrame()
    return df