import pandas as pd

def box_plot(rdb,line,bar):
    sql1 = """select * from (SELECT p."Age",p."Sex",an."Name",date_trunc('day', an."Date") as day,an."name",AVG(an."Value") as "Value"FROM applewatch_numeric as an LEFT JOIN patient as p 
    on p."Name" = an."Name" where an.name='{0}' group by p."Sex",p."Age",an."Name",an.name,day
    Union
    SELECT p."Age",p."Sex",an."Name",date_trunc('day', an."Date")as day,an.name,SUM(an."Value") as "Value" FROM applewatch_numeric as an LEFT JOIN patient as p 
    on p."Name" = an."Name" where 
    an.name='{1}' group by p."Sex",p."Age",an."Name",an.name,day) as results order by "Name" """.format(line,bar)

    df = pd.read_sql(sql1, rdb)

    return df

def scatter_plot(rdb, linear, bar):

    sql = """ select p."Age",p."Sex",foo."Name",foo.name,foo.date,
                case 
                when name in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                'Walking Heart Rate Average') Then AVG("Value")
                ELSE sum("Value")
                end as "Value"
                from (SELECT "Name",date_trunc('day', "Date") as date,"name", "Value" FROM applewatch_numeric 
                where name in ('{}','{}')) as foo LEFT JOIN patient as p 
                on p."Name" = foo."Name" group by p."Age",p."Sex",foo."Name",foo.date,foo.name""".format(linear, bar)

    df = pd.read_sql(sql, rdb)

    return df

def linear_plot(rdb, line):

    sql = """select "Name",date_trunc('week', "Date") as week,AVG("Value") as "Value" FROM applewatch_numeric where 
    type='HKQuantityTypeIdentifierHeartRate' group by week,"Name" order by "Name",week """

    df = pd.read_sql(sql, rdb)

    return df

def Heart_Rate_workout_comparison(rdb, type):

    sql = """select "Name","HR_average" FROM workout where "duration" > 10 and "duration" < 300 and type = '{}' 
        order by "Start_Date"  """.format(type)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = []

    return df