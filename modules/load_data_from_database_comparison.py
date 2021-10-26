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

def day_night(rdb,gr, linear, bar):

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

def linear_plot(rdb,gr, linear, bar):

    sqla = """ select p."{2}",foo.name,foo.week,
                case 
                when name in ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                'Walking Heart Rate Average') Then AVG("Value")
                ELSE sum("Value")
                end as "Value"
                from (SELECT "Name",date_trunc('week', "Date") as week,"name", "Value" FROM applewatch_numeric 
                where name in ('{0}','{1}')) as foo LEFT JOIN patient as p 
                on p."Name" = foo."Name" group by p."{2}",foo.week,foo.name""".format(linear, bar,gr)


    start_time = time.time()
    df = pd.read_sql(sqla, rdb)
    if gr == 'Age':
        df[gr] = df[gr].astype(str)
    df1 = df[df['name'] == linear]
    df2 = df[df['name'] == bar]
    end_time = time.time()
    times = end_time - start_time
    print('second check',times)

    return df1,df2

def Heart_Rate_workout_comparison(rdb,gr, type):

    sql = """select p."{0}",w."HR_average" FROM workout as w 
    LEFT JOIN patient as p 
    on p."Name" = w."Name"
    where w."duration" > 10 and w."duration" < 300 and w.type = '{1}' 
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
    where w."duration" > 10 and w."duration" < 300 and w.type = '{1}' group by p."{0}",date
        order by p."{0}",date
          """.format(gr,type)

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = []

    return df