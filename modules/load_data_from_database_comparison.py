import pandas as pd
import time

def plots(rdb,gr, linear, bar):

    sql = """ select p."{2}",foo.name,foo.date,
                case 
                when name in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                'Walking Heart Rate Average') Then AVG("Value")
                ELSE sum("Value")
                end as "Value"
                from (SELECT "Name",date_trunc('day', "Date") as date,"name", "Value" FROM applewatch_numeric 
                where name in ('{0}','{1}')) as foo LEFT JOIN patient as p 
                on p."Name" = foo."Name" group by p."{2}",foo.date,foo.name""".format(linear, bar,gr)


    df = pd.read_sql(sql, rdb)

    return df

def linear_plot(rdb, line):

    sql = """select "Name",date_trunc('week', "Date") as week,AVG("Value") as "Value" FROM applewatch_numeric where 
    type='HKQuantityTypeIdentifierHeartRate' group by week,"Name" order by "Name",week """

    df = pd.read_sql(sql, rdb)

    return df

def Heart_Rate_workout_comparison(rdb,gr, type):

    sql = """select p."Name",w."HR_average" FROM workout as w 
    LEFT JOIN patient as p 
    where w."duration" > 10 and w."duration" < 300 and w.type = '{}' 
        order w."Start_Date"
          """.format(type,gr)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = []

    return df