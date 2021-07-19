import pandas as pd
import time



def patient(rdb):
    """
    :param rdb: connection with database
    :return: df: list patients
    """
    sql = """SELECT "Name" from patient order by index"""

    df = pd.read_sql(sql,rdb)
    df = df["Name"].values.tolist()

    return df


def age_sex(rdb,patient):
    """
    :param rdb: connection with database
    :return: df: list patients
    """
    sql = """SELECT "Age","Sex" from patient where "Name"='{}' """.format(patient)

    df = pd.read_sql(sql,rdb)

    return df


def month(rdb, patient):
    sql = """ select to_char(month,'YYYY-MM') as month from (SELECT distinct date_trunc('month', "Date")  as month 
    FROM applewatch_numeric where "Name"='{}' and name ='Resting Heart Rate' order by date_trunc('month', "Date")) 
    as foo""".format(patient)

    df = pd.read_sql(sql, rdb)
    df = df['month'].to_list()

    return df


def week(rdb, patient):
    sql = """ select distinct week from (SELECT to_char("Date", 'IYYY/IW') as week FROM applewatch_numeric 
    where "Name"='{}' and name ='Resting Heart Rate') as foo order by week """.format(patient)

    df = pd.read_sql(sql, rdb)
    df = df['week'].to_list()

    return df


def min_max_date(rdb, patient):

    sql = """SELECT min_date,max_date from patient where "Name"='{}'""".format(patient)

    df = pd.read_sql(sql, rdb)

    min_date, max_date = df['min_date'].iloc[0].date(), df['max_date'].iloc[0].date()

    return min_date, max_date

def min_max_date_workout(rdb, patient):

    sql = """SELECT MIN("Start_Date"),MAX("End_Date") from workout where "Name" ='{}'""".format(patient)

    df = pd.read_sql(sql, rdb)

    min_date, max_date = df['min'].iloc[0].date(), df['max'].iloc[0].date()

    return min_date, max_date



def label(rdb):
    sql = """SELECT distinct name from name where name in ('Heart Rate','Heart Rate Variability SDNN',
    'Resting Heart Rate','VO2Max','Walking Heart Rate Average')"""

    sql2 = """SELECT distinct name from name where name not in ('None','Heart Rate','Heart Rate Variability SDNN',
    'Resting Heart Rate','VO2Max','Walking Heart Rate Average')"""

    df, df2 = pd.read_sql(sql, rdb),pd.read_sql(sql2, rdb)
    df, df2 = df["name"].values.tolist(), df2["name"].values.tolist()

    return df, df2


def weight_and_height(rdb, patient):

    sql = """SELECT * from applewatch_numeric where "type" in ('HKQuantityTypeIdentifierHeight') and "Name" = '{}' """.format(patient)
    df = pd.read_sql(sql,rdb)
    if not df.empty:
        df = df.iloc[-1]['Value']
    else:
        df ='not information'

    return df


def irregular_ecg(rdb, patient):

    sql = """SELECT "Classification",count(*) from ecg where "Patient"='{}' group by "Classification" """.format(patient)
    sql2 = """ select "Day","number", "Classification" from ecg  where "Patient"='{}' order by "Day" """.format(patient)

    df = pd.read_sql(sql, rdb)
    df2 = pd.read_sql(sql2, rdb)

    return df, df2


def Card(rdb, patient, group, date, value):


    if group == 'M':
        sql = """ select name,month,sum("Value"),AVG("Value") from (SELECT to_char(date_trunc('month', "Date"),
        'YYYY-MM') as month,"name", "Value" FROM applewatch_numeric where "Name" = '{}' and "name" in 
        ('Active Energy Burned','Heart Rate','Walking Heart Rate Average','Resting Heart Rate','Step Count',
        'Apple Exercise Time') order by "name","Date") as foo where month='{}' group by month,name""".format(patient,value)
    elif group == 'W':
        sql = """ select name,week,sum("Value"),AVG("Value") from (SELECT to_char("Date", 'IYYY/IW') as week,"name",
        "Value" FROM applewatch_numeric where "Name" = '{}' and "name" in ('Active Energy Burned','Heart Rate',
        'Walking Heart Rate Average','Resting Heart Rate','Step Count','Apple Exercise Time') order by "name","Date")
         as foo where week='{}' group by week,name""".format(patient,value)
    elif group == 'DOW' :
        sql = """ select name,"DOW",sum("Value"),AVG("Value") from (SELECT trim(to_char("Date", 'Day')) as "DOW",
        "name","Value" FROM applewatch_numeric where "Name" = '{}' and "name" in ('Active Energy Burned',
        'Heart Rate','Walking Heart Rate Average','Resting Heart Rate','Step Count','Apple Exercise Time') 
        order by "name","Date") as foo where "DOW"='{}' group by "DOW",name""".format(patient,value)
    else:
        sql = """ select name,sum("Value"),AVG("Value") from (SELECT date_trunc('day', "Date") as date,"name",
                "Value" FROM applewatch_numeric where "Name" = '{}' and "name" in ('Active Energy Burned',
                'Heart Rate','Walking Heart Rate Average','Resting Heart Rate','Step Count','Apple Exercise Time')
                 order by "name","Date") as foo where date = '{}' group by date,name""".format(patient,date)

    df = pd.read_sql(sql, rdb)

    return df



def table(rdb, patient, group, linear, bar):
    if group == 'M':
        sql = """ select name,month,
                case 
                when name in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                'Walking Heart Rate Average') Then AVG("Value")
                ELSE sum("Value")
                end as "Value"
                from (SELECT to_char(date_trunc('month', "Date"),
                'YYYY-MM') as month,"name", "Value" FROM applewatch_numeric where "Name" = '{}' and "name" in 
                ('{}','{}') order by "name","Date") as foo group by month,name""".format(patient,linear,bar)
    elif group == 'W':
        sql = """ select name,week,
                case 
                when name in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                'Walking Heart Rate Average') Then AVG("Value")
                ELSE sum("Value")
                end as "Value"
                from (SELECT to_char("Date", 'IYYY/IW') as week,"name",
                "Value" FROM applewatch_numeric where "Name" = '{}' and "name" in ('{}','{}') order by "name","Date")
                as foo group by week,name""".format(patient,linear,bar)
    elif group == 'DOW' :
        sql = """ select name,"DOW_number","DOW",
                case 
                when name in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                'Walking Heart Rate Average') Then AVG("Value")
                ELSE sum("Value")
                end as "Value"
                from (SELECT trim(to_char("Date", 'Day')) as "DOW",extract('ISODOW' from "Date") as "DOW_number",
                "name","Value" FROM applewatch_numeric where "Name" = '{}' and "name" in ('{}','{}') 
                order by "name","Date") as foo group by "DOW","DOW_number",name order by "DOW_number" """.format(patient,linear,bar)
    else:
        sql = """ select name,date,
                case 
                when name in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                'Walking Heart Rate Average') Then AVG("Value")
                ELSE sum("Value")
                end as "Value"
                from (SELECT date_trunc('day', "Date") as date,"name",
                "Value" FROM applewatch_numeric where "Name" = '{0}' and "name" in ('{1}','{2}')
                 order by "name","Date") as foo group by date,name""".format(patient,linear,bar)

    df = pd.read_sql(sql, rdb)

    return df


def day_figure(rdb, patient, group, linear, bar, date, value):
    if group == 'M':
        sql = """ select "Date",name,month,"Value"from (SELECT "Date",to_char(date_trunc('month', "Date"),
            'YYYY-MM') as month,"name", "Value" FROM applewatch_numeric where "Name" = '{}' and "name" in 
            ('{}','{}') order by "name","Date") as foo where month='{}' """.format(
            patient,linear,bar, value)
    elif group == 'W':
        sql = """ select "Date",name,week,"Value" from (SELECT "Date",to_char("Date", 'IYYY/IW') as week,"name",
            "Value" FROM applewatch_numeric where "Name" = '{}' and "name" in ('{}','{}') order by "name","Date")
             as foo where week='{}' """.format(patient,linear,bar, value)
    elif group == 'DOW':
        sql = """ select "Date",date,name,"DOW","Value" from (SELECT "Date",trim(to_char("Date", 'Day')) as "DOW",
        date_trunc('day', "Date") as date,name,"Value" FROM applewatch_numeric where "Name" = '{}' and "name" in ('{}','{}') 
            order by "name","Date") as foo where "DOW"='{}' and date = (SELECT Max(date_trunc('day', "Date")) FROM applewatch_numeric) """.format(patient,linear,bar, value)
    else:
        sql = """ select "Date",name,"Value" from (SELECT "Date",date_trunc('day', "Date") as date,"name",
                    "Value" FROM applewatch_numeric where "Name" = '{}' and "name" in ('{}','{}')
                     order by "name","Date") as foo where date = '{}' """.format(patient,linear,bar, date)
    s = """ SELECT distinct date_trunc('day', "Date")) FROM applewatch_numeric"""

    df = pd.read_sql(sql, rdb)

    return df


def trend_figure(rdb, patient, group, start_date,end_date):

    if group == 'M':
        sql = """ select month,hour,avg("Value") as "Value" from (SELECT to_char(date_trunc('month', "Date"),
            'YYYY-MM') as month,extract('hour' from "Date") as hour,"Value" 
        FROM applewatch_numeric where "Name" = '{}' and "name"= 'Heart Rate' and "Date" > '{}' and "Date" < '{}' 
        order by "Date") as foo group by month,hour order by month,hour""".format(patient,start_date,end_date)
    elif group == 'W':
        sql = """ select week,hour,avg("Value") as "Value" from (SELECT to_char("Date", 'IYYY/IW') as week,extract('hour' from "Date") as hour,
            "Value" FROM applewatch_numeric where "Name" = '{}' and name='Heart Rate' and "Date" > '{}' and "Date" < '{}' order by "Date")
             as foo group by week,hour order by week,hour""".format(patient,start_date,end_date)
    elif group == 'DOW':
        sql = """ select "DOW","DOW_number",hour,avg("Value") as "Value" from (SELECT trim(to_char("Date", 'Day')) as "DOW",
        extract('ISODOW' from "Date") as "DOW_number",extract('hour' from "Date") as hour,"Value" FROM applewatch_numeric 
        where "Name" = '{}' and name='Heart Rate' order by "Date") as foo where "DOW_number" > '{}' and "DOW_number" < '{}' 
        group by "DOW","DOW_number",hour  """.format(patient, start_date,end_date)
    else:
        sql = """ select date,hour,avg("Value") as "Value" from (SELECT "Date",extract('hour' from "Date") as hour,date_trunc('day', "Date") as date,"name",
                    "Value" FROM applewatch_numeric where "Name" = '{}' and name='Heart Rate' and "Date" > '{}' and "Date" < '{}'
                     order by "Date") as foo group by date,hour """.format(patient,start_date,end_date)
    df = pd.read_sql(sql, rdb)
    return df


def ECG_number(rdb, date):

    sql = """SELECT distinct number from ECG where "Day"='{}' order by number""".format(str(date))
    df = pd.read_sql(sql,rdb)
    df = df['number'].to_list()
    return df


def ECG_data(rdb,date,patient,num):

    sql="""SELECT * from ECG where "Day"='{0}' and "Patient"='{1}' and number='{2}' """.format(date,patient,num)
    df = pd.read_sql(sql,rdb)
    return df


def number_of_days_more_6(rdb,patient):
    sql = """select "Name",count(*) from(SELECT "Name",date_trunc('day', "Date") as date,"type","name",count(*) 
    as number FROM applewatch_categorical where "type" = 'HKCategoryTypeIdentifierAppleStandHour' group by "Name",
    date,"type","name" having count(*) > 6 order by "Name",date) as foo where "Name" = '{}' group by "Name" """.format(patient)
    df = pd.read_sql(sql, rdb)
    df = df.iloc[0]['count']

    return df

def HKWorkoutActivity(rdb):
    sql = """select distinct @workoutActivityType FROM workout  """
    df = pd.read_sql(sql, rdb)
    return df

def WorkoutActivity_data(rdb,patient):
    sql = """select *,
                to_char(date_trunc('month', "Start_Date"),'YYYY-MM') as month,
                to_char("Start_Date", 'IYYY/IW') as week,
                extract('week' from "Start_Date") as week_num,
                extract('ISODOW' from "Start_Date") as "DOW_number",
                to_char("Start_Date", 'Day') as "DOW",
                date_trunc('day', "Start_Date") as date
                FROM workout  where "Name"='{}' order by "type","Start_Date"  """.format(patient)

    df = pd.read_sql(sql, rdb)
    return df


def WorkoutActivity_pie_chart(rdb,patient,group,date,value):
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
                    FROM workout  where "Name"='{}' and trim(to_char("Start_Date", 'Day'))='{}' order by "type","Start_Date"  """.format(patient,value)
    else:
        sql = """select *,
                    date_trunc('day', "Start_Date") as date
                    FROM workout  where "Name"='{}' and date_trunc('day', "Start_Date") ='{}'
                     order by "type","Start_Date"  """.format(patient,date)

    df = pd.read_sql(sql, rdb)

    return df

def Heart_Rate(rdb,date,patient):

    sql = """SELECT "Name","Date",name,"Value" FROM applewatch_numeric where "Name"='{}' and 
    date_trunc('day', "Date")='{}' and type='HKQuantityTypeIdentifierHeartRate' order by "Date" """.format(patient,date)

    df = pd.read_sql(sql, rdb)

    return df


"""
select *,"@startDate"::timestamp - lag("@startDate"::timestamp) over(partition by "@sourceName" order by "@sourceName",
"@startDate") as difference from applewatch_numeric where "@type" ='HKQuantityTypeIdentifierHeartRate';
"""


