import pandas as pd

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