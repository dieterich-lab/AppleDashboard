import pandas as pd


def patient(rdb):
    """
    :param rdb: connection with database
    :return: df: list patients
    """
    sql = """SELECT "Name" from patient order by index"""
    try:
        df = pd.read_sql(sql,rdb)
        df = df["Name"].values.tolist()
    except:
        df = []
    return df




def age_sex(rdb,patient):
    """
    :param rdb: connection with database
    :return: df: list patients
    """
    sql = """SELECT "Age","Sex" from patient where "Name"='{}' """.format(patient)
    try:
        df = pd.read_sql(sql,rdb)
    except:
        df = []
    return df


def month(rdb, patient):
    sql = """ select to_char(month,'YYYY-MM') as month from (SELECT distinct date_trunc('month', "Date")  as month 
    FROM applewatch_numeric where "Name"='{}' and name ='Resting Heart Rate' order by date_trunc('month', "Date")) 
    as foo""".format(patient)

    try:
        df = pd.read_sql(sql, rdb)
        df = df['month'].to_list()
    except:
        df = []
    return df


def week(rdb, patient):
    sql = """ select distinct week from (SELECT to_char("Date", 'IYYY/IW') as week FROM applewatch_numeric 
    where "Name"='{}' and name ='Resting Heart Rate') as foo order by week """.format(patient)

    try:
        df = pd.read_sql(sql, rdb)
        df = df['week'].to_list()
    except:
        df = []

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



def label(rdb):
    sql = """SELECT distinct name from name where name in ('Heart Rate','Heart Rate Variability SDNN',
    'Resting Heart Rate','VO2Max','Walking Heart Rate Average')"""

    sql2 = """SELECT distinct name from name where name not in ('None','Heart Rate','Heart Rate Variability SDNN',
    'Resting Heart Rate','VO2Max','Walking Heart Rate Average')"""

    try:
        df, df2 = pd.read_sql(sql, rdb),pd.read_sql(sql2, rdb)
        df, df2 = df["name"].values.tolist(), df2["name"].values.tolist()
    except:
        df,df2 = [],[]
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
    sql2 = """ select "Day","Date"::time as Time, "Classification" from ecg  where "Patient"='{}' order by "Day" """.format(patient)
    sql3 = """ select "Patient","Day","Date"::time as Time, "hrvOwn", "SDNN", "SENN", "SDSD", "pNN20", "pNN50", "lf", "hf", "lf_hf_ratio",
            "total_power", "vlf", "Classification" from ecg  order by "Patient","Day" """

    try:
        df, df2, df3 = pd.read_sql(sql, rdb), pd.read_sql(sql2, rdb), pd.read_sql(sql3, rdb)
    except:
        df, df2, df3 = [], [],[]
    return df, df2, df3


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

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df=[]

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
        sql = """ select name,month,
                case 
                when name in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                'Walking Heart Rate Average') Then AVG("Value")
                ELSE sum("Value")
                end as "Value"
                from (SELECT to_char(date_trunc('month', "Date"),
                'YYYY-MM') as month,"name", "Value" FROM applewatch_numeric where "Name" = '{}' and "name" in 
                ({},{}) order by "name","Date") as foo group by month,name""".format(patient, linear, bar)
    elif group == 'W':
        sql = """ select name,week,
                case 
                when name in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                'Walking Heart Rate Average') Then AVG("Value")
                ELSE sum("Value")
                end as "Value"
                from (SELECT to_char("Date", 'IYYY/IW') as week,"name",
                "Value" FROM applewatch_numeric where "Name" = '{}' and "name" in ({},{}) order by "name","Date")
                as foo group by week,name""".format(patient,linear,bar)
    elif group == 'DOW' :
        sql = """ select name,"DOW_number","DOW",
                case 
                when name in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                'Walking Heart Rate Average') Then AVG("Value")
                ELSE sum("Value")
                end as "Value"
                from (SELECT trim(to_char("Date", 'Day')) as "DOW",extract('ISODOW' from "Date") as "DOW_number",
                "name","Value" FROM applewatch_numeric where "Name" = '{}' and "name" in ({},{}) 
                order by "name","Date") as foo group by "DOW","DOW_number",name order by "DOW_number" """.format(patient,linear,bar)
    else:
        sql = """ select name,date,
                case 
                when name in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                'Walking Heart Rate Average') Then AVG("Value")
                ELSE sum("Value")
                end as "Value"
                from (SELECT "name",date_trunc('day', "Date")::date as date,
                "Value" FROM applewatch_numeric where "Name" = '{0}' and "name" in ({1},{2})
                 order by "name","Date") as foo group by date,name""".format(patient,linear,bar)
    try:
        df = pd.read_sql(sql, rdb)
    except:
        df=[]

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
        sql = """ select "Date",name,month,"Value"from (SELECT "Date",to_char(date_trunc('month', "Date"),
            'YYYY-MM') as month,"name", "Value" FROM applewatch_numeric where "Name" = '{}' and "name" in 
            ('Heart Rate',{}) order by "name","Date") as foo where month='{}' """.format(
            patient,bar, value)
    elif group == 'W':
        sql = """ select "Date",name,week,"Value" from (SELECT "Date",to_char("Date", 'IYYY/IW') as week,"name",
            "Value" FROM applewatch_numeric where "Name" = '{}' and "name" in ({},{}) order by "name","Date")
             as foo where week='{}' """.format(patient,linear,bar, value)
    elif group == 'DOW':
        sql = """ select "Date",date,name,"DOW","Value" from (SELECT "Date",trim(to_char("Date", 'Day')) as "DOW",
        date_trunc('day', "Date") as date,name,"Value" FROM applewatch_numeric where "Name" = '{}' and "name" in ({},{}) 
            order by "name","Date") as foo where "DOW"='{}' and date = (SELECT Max(date_trunc('day', "Date")) FROM applewatch_numeric) """.format(patient,linear,bar, value)
    else:
        sql = """ select "Date",name,"Value" from (SELECT "Date",date_trunc('day', "Date") as date,"name",
                    "Value" FROM applewatch_numeric where "Name" = '{}' and "name" in ('Heart Rate',{})
                     order by "name","Date") as foo where date = '{}' """.format(patient,bar, date)
    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = []

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
    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = []
    return df


def ECG_number(rdb, date):

    sql = """SELECT distinct number from ECG where "Day"='{}' order by number""".format(str(date))
    try :
        df = pd.read_sql(sql,rdb)
        df = df['number'].to_list()
    except:
        df = []
    return df


def ECG_data(rdb,date,patient,num):

    sql="""SELECT * from ECG where "Day"='{0}' and "Patient"='{1}' and "Date"::time='{2}' """.format(date,patient,num)

    try:
        df = pd.read_sql(sql,rdb)
    except:
        df = []
    return df


def number_of_days_more_6(rdb,patient):
    sql = """select "Name",count(*) from(SELECT "Name",date_trunc('day', "Date") as date,"type","name",count(*) 
    as number FROM applewatch_categorical where "type" = 'HKCategoryTypeIdentifierAppleStandHour' group by "Name",
    date,"type","name" having count(*) > 6 order by "Name",date) as foo where "Name" = '{}' group by "Name" """.format(patient)
    try:
        df = pd.read_sql(sql, rdb)
        df = df.iloc[0]['count']
    except:
        df =''

    return df


def activity(rdb):

    sql = """SELECT distinct type from workout"""

    try:
        df = pd.read_sql(sql, rdb)
        df = df['type'].to_list()
    except:
        df = []

    return df



def box_plot(rdb, group, line,bar):

    if group == 'M':
        sql1 = """ select "Name",AVG("Value") from (SELECT "Name",to_char(date_trunc('month', "Date"),
            'YYYY-MM') as month,"name", "Value" FROM applewatch_numeric where "name" in 
            ('{}')) as foo group by "Name",month """.format(bar)
        sql2 = """ select "Name",name,"Value" from (SELECT "Name",to_char(date_trunc('month', "Date"),
            'YYYY-MM') as month,"name", "Value" FROM applewatch_numeric where "name" in 
            ('{}')) as foo "Name",month """.format(line)
    elif group == 'W':
        sql1 = """ select "Name",AVG("Value") from (SELECT "Name",to_char("Date", 'IYYY/IW') as week,"name", 
            "Value" FROM applewatch_numeric where "name" in ('{}')) as foo group by "Name",week """.format(bar)
        sql2 = """ select "Name",name,"Value" from (SELECT "Name",to_char("Date", 'IYYY/IW') as week,"name",
            "Value" FROM applewatch_numeric where "name" in ('{}')) as foo "Name",week """.format(line)

    elif group == 'DOW':
        sql1 = """ select "Name",AVG("Value") from (SELECT "Name",trim(to_char("Date", 'Day')) as "DOW","name",
            "Value" FROM applewatch_numeric where "name" in ('{}')) as foo group by "Name","DOW" """.format(bar)
        sql2 = """ select "Name",name,"Value" from (SELECT "Name",trim(to_char("Date", 'Day')) as "DOW","name",
                "Value" FROM applewatch_numeric where "name" in ('{}')) as foo "Name","DOW" """.format(line)
    else:
        sql1 = """ select "Name",AVG("Value") from (SELECT "Name",date_trunc('day', "Date") as date,"name",
            "Value" FROM applewatch_numeric where "name" in ('{}')) as foo group by "Name",date """.format(bar)
        sql2 = """ select "Name",name,"Value" from (SELECT "Name",date_trunc('day', "Date") as date,"name",
                "Value" FROM applewatch_numeric where "name" in ('{}')) as foo "Name",date """.format(line)


    df1 = pd.read_sql(sql1, rdb)
    df2 = pd.read_sql(sql2, rdb)

    return df1,df2


def histogram_plot(rdb, group, line):

    sql = """SELECT "Name","Value" FROM applewatch_numeric where 
    type='HKQuantityTypeIdentifierHeartRate' """

    df = pd.read_sql(sql, rdb)

    return df



def during_workout(rdb, group, line):

    sql = """SELECT "Name",date_trunc('day', "Date") as date,AVG("Value") as "Value" FROM applewatch_numeric where 
    type='HKQuantityTypeIdentifierHeartRate' group by "Name",date_trunc('day', "Date") order by  "Name",date_trunc('day', "Date") """

    df = pd.read_sql(sql, rdb)

    return df


def scatter_plot_ecg(rdb,x_axis, y_axis):

    sql = """ select "Patient","{0}","{1}" from ecg """.format(x_axis, y_axis)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = []
    return df


def box_plot_ecg(rdb,x_axis):

    sql = """ select "Patient","{}" from ecg """.format(x_axis)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = []
    return df

"""
select *,"@startDate"::timestamp - lag("@startDate"::timestamp) over(partition by "@sourceName" order by "@sourceName",
"@startDate") as difference from applewatch_numeric where "@type" ='HKQuantityTypeIdentifierHeartRate';
"""


