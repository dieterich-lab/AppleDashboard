import pandas as pd


def patient(rdb):
    """

    :param rdb: connection with database
    :return: df: list patients
    """
    sql = """SELECT distinct "Name" from applewatch """
    df = pd.read_sql(sql,rdb)
    df = df["Name"].values.tolist()
    return df


def min_max_date(rdb):
    """

    :param rdb: connection with database
    :return: df: DataFrame with min and maximal data
    """
    sql = """SELECT MIN("Date"),MAX("Date") from applewatch_numeric """
    df = pd.read_sql(sql, rdb)
    min_date = df['min'].iloc[0]
    min_date = min_date.date()
    max_date = df['max'].iloc[0]
    max_date = max_date.date()
    return min_date, max_date


def weight_and_height(rdb):
    """

    :param rdb: connection with database
    :param date:
    :return: df: list of ECG records from date
    """
    sql = """SELECT * from applewatch_numeric where "type" in ('HKQuantityTypeIdentifierHeight')"""
    df = pd.read_sql(sql,rdb)

    return df


def irregular_ecg(rdb):
    """

    :param rdb: connection with database
    :return: df: list of ECG records from date
    """

    sql = """SELECT "Patient","Classification",count(*) from ecg group by "Patient","Classification" """
    sql4 = """ select "Patient","Day", "number", "Classification" from ecg order by "Day" """

    df4 = pd.read_sql(sql4, rdb)
    df = pd.read_sql(sql, rdb)

    return df4, df

def Card (rdb):
    """

    :param rdb: connection with database
    :return: df: DataFrame with all values
    """

    sql = """SELECT "Name","Date",to_char(date_trunc('month', "Date"),'YYYY-MM') as month,
                                    to_char("Date", 'IYYY/IW') as week,
                                    extract('week' from "Date") as week_num,
                                    extract('ISODOW' from "Date") as "DOW_number",
                                    to_char("Date", 'Day') as "DOW",
                                    date_trunc('day', "Date") as date,
                                    extract('hour' from "Date") as hour,"type","name", "Value" 
                                    FROM applewatch_numeric order by "type","Date" """

    sql2 = """SELECT "Name","Date",extract('month' from  "Date") as month,
                                    extract('week' from "Date") as week,
                                    extract('ISODOW' from "Date") as "DOW",
                                    date_trunc('day', "Date") as date,
                                    extract('hour' from "Date") as hour,"type","name", "Value" 
                                    FROM applewatch_numeric where "name" in 
                                    ('Heart Rate','Heart Rate Variability SDNN','Resting Heart Rate','VO2Max',
                                    'Walking Heart Rate Average') order by "type","Date" """

    """
    where "name" in ('Active Energy Burned', 'Apple Exercise Time', 'Apple Stand Time',
        'Basal Energy Burned', 'Distance Cycling', 'Distance Walking Running',
        'Sleep Analysis', 'Step Count')
    """

    df = pd.read_sql(sql, rdb)
    df2 = pd.read_sql(sql2, rdb)

    return df,df2



def ECG_number(rdb,date):
    """

    :param rdb: connection with database
    :param date:
    :return: df: list of ECG records from date
    """
    sql = """SELECT distinct number from ECG where "Day"='{}' order by number""".format(str(date))
    df = pd.read_sql(sql,rdb)
    df = df['number'].to_list()
    return df


def ECG_data(rdb,date,patient1,num):
    """
    :param rdb:
    :param date:
    :param patient1:
    :param num:
    :return:
    """

    sql="""SELECT * from ECG where "Day"='{0}' and "Patient"='{1}' and number='{2}' """.format(date,patient1,num)
    df = pd.read_sql(sql,rdb)
    return df


def basic_values(rdb):
    """

    :param rdb:
    :return:
    """
    sql1 = """SELECT min("Date") FROM AppleWatch """
    sql2 = """SELECT max("Date") FROM AppleWatch"""
    sql3 = """SELECT Distinct("type") FROM AppleWatch"""
    #sql4 = """SELECT Distinct("Patient") FROM AppleWatch"""

    df1 = pd.read_sql(sql1, rdb)
    df1['Value'] = pd.to_numeric(df1['Value'])
    df2 = pd.read_sql(sql2, rdb)
    df2['Value'] = pd.to_numeric(df2['Value'])
    df3 = pd.read_sql(sql3, rdb)
    df3['Value'] = pd.to_numeric(df3['Value'])
    #df4 = pd.read_sql(sql4, rdb)
    return df1, df2, df3


def number_of_days_more_6(rdb):
    sql = """select "Name",count(*) from(SELECT "Name",date_trunc('day', "Date") as date,"type","name",count(*) 
    as number FROM applewatch_categorical where "type" = 'HKCategoryTypeIdentifierAppleStandHour' group by "Name",
    date,"type","name" having count(*) > 6 order by "Name",date) as foo group by "Name" """
    df = pd.read_sql(sql, rdb)
    return df

"""
select *,"@startDate"::timestamp - lag("@startDate"::timestamp) over(partition by "@sourceName" order by "@sourceName",
"@startDate") as difference from applewatch_numeric where "@type" ='HKQuantityTypeIdentifierHeartRate';
"""


