import pandas as pd
import psycopg2

try:
    rdb = psycopg2.connect("dbname='example' user='test' host='localhost' port='5425' password='test'")
except:
    rdb ="I am unable to connect to the database 0"
    print (rdb)

def basic_values(rdb):
    sql1 = """SELECT min("@creationDate") FROM AppleWatch """
    sql2 = """SELECT max("@creationDate") FROM AppleWatch"""
    sql3 = """SELECT Distinct("@type") FROM AppleWatch"""
    #sql4 = """SELECT Distinct("Patient") FROM AppleWatch"""

    df1 = pd.read_sql(sql1, rdb)
    df2 = pd.read_sql(sql2, rdb)
    df3 = pd.read_sql(sql3, rdb)
    #df4 = pd.read_sql(sql4, rdb)
    return df1, df2, df3


def Card(rdb):

    sql1 = """SELECT "@creationDate","@Value" FROM AppleWatch WHERE "@type"='HKQuantityTypeIdentifierRestingHeartRate'"""
    sql2 = """SELECT "@creationDate","@Value" FROM AppleWatch WHERE "@type"='HKQuantityTypeIdentifierWalkingHeartRateAverage'"""
    sql3 = """SELECT "@creationDate","@Value" FROM AppleWatch WHERE "@type"='HKQuantityTypeIdentifierStepCount'"""
    sql4 = """SELECT "@creationDate","@Value" FROM AppleWatch WHERE "@type"='HKQuantityTypeIdentifierHeartRate'"""
    sql5 = """SELECT "@creationDate","@Value" FROM AppleWatch WHERE "@type"='HKQuantityTypeIdentifierAppleExerciseTime'"""
    sql6 = """SELECT "@creationDate","@Value" FROM AppleWatch WHERE "@type"='HKQuantityTypeIdentifierActiveEnergyBurned'"""

    df1 = pd.read_sql(sql1, rdb)
    df2 = pd.read_sql(sql2, rdb)
    df3 = pd.read_sql(sql3, rdb)
    df4 = pd.read_sql(sql4, rdb)
    df5 = pd.read_sql(sql5, rdb)
    df6 = pd.read_sql(sql6, rdb)
    return df1, df2, df3, df4, df5, df6


def graphs(rdb):

    sql1 = """SELECT "@creationDate","@Value" FROM AppleWatch WHERE "@type"='HKQuantityTypeIdentifierHeartRate'"""
    sql2 = """SELECT "@creationDate","@Value" FROM AppleWatch WHERE "@type"='HKQuantityTypeIdentifierActiveEnergyBurned'"""
    try:
        df1 = pd.read_sql(sql1, rdb)
        df2 = pd.read_sql(sql2, rdb)

    except Exception:
        return None, "Problem with load data from database"
    return df1,df2

def graphs2(rdb):

    sql1 = """SELECT "@creationDate","@Value" FROM AppleWatch """
    try:
        df = pd.read_sql(sql1, rdb)
    except Exception:
        return None, "Problem with load data from database"
    return df
