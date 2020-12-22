import pandas as pd
import psycopg2
import time
import os


user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
database = os.environ['POSTGRES_DB']
port = os.environ['POSTGRES_PORT']
DATABASE_URL= f'postgresql://{user}:{password}@{host}:{port}/{database}'

# Connection with database
def connect_db():
    """ connects to database """
    try:
        db = psycopg2.connect(DATABASE_URL)
        return db
    except Exception:
        time.sleep(0.1)


rdb = connect_db()


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
    sql1 = """SELECT min("@creationDate") FROM AppleWatch """
    sql2 = """SELECT max("@creationDate") FROM AppleWatch"""
    sql3 = """SELECT Distinct("@type") FROM AppleWatch"""
    #sql4 = """SELECT Distinct("Patient") FROM AppleWatch"""

    df1 = pd.read_sql(sql1, rdb)
    df1['@Value'] = pd.to_numeric(df1['@Value'])
    df2 = pd.read_sql(sql2, rdb)
    df2['@Value'] = pd.to_numeric(df2['@Value'])
    df3 = pd.read_sql(sql3, rdb)
    df3['@Value'] = pd.to_numeric(df3['@Value'])
    #df4 = pd.read_sql(sql4, rdb)
    return df1, df2, df3


def Card (rdb):
    """

    :param rdb: connection with database
    :return: df: DataFrame with all values
    """

    sql = """SELECT "@sourceName","@creationDate",to_char(date_trunc('month', "@creationDate"),'YYYY-MM') as month,
                                    extract('week' from "@creationDate") as week,
                                    extract('ISODOW' from "@creationDate") as "DOW",
                                    date_trunc('day', "@creationDate") as date,
                                    extract('hour' from "@creationDate") as hour,"@type","name", "@Value" FROM applewatch_numeric order by "@type","@creationDate" """

    df = pd.read_sql(sql, rdb)

    return df


