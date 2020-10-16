import pandas as pd
import xmltodict
import psycopg2
import io
import pytz
import os

user = 'test'
password = 'test'
host = 'localhost'
database = 'example'
port = 5425
DATABASE_URL= f'postgresql://{user}:{password}@{host}:{port}/{database}'


try:
    rdb = psycopg2.connect("dbname='example' user='test' host='localhost' port='5425' password='test'")
except:
    print ("I am unable to connect to the database 0")



"""Remove tables from database if exists and create new name_type and examination tables in the PostgreSQL database"""
sql1 = "DROP TABLE IF EXISTS AppleWatch"

statment_examination = """CREATE TABLE AppleWatch (
                                "@type" text,
                                "@sourceName" text,
                                "@sourceVersion" text,
                                "@unit" text,
                                "@creationDate" text,
                                "@startDate" text,
                                "@endDate" text,
                                "@Value" text)"""

try:
    cur = rdb.cursor()
    cur.execute(sql1)
    cur.execute(statment_examination)
    rdb.commit()
except Exception:
    print("Problem with connection with database 1")






input_path = '/home/magda/Apple_Watch/qs_ledger/qs_ledger/apple_health/data/export.xml'
with open(input_path, 'r') as xml_file:
    input_data = xmltodict.parse(xml_file.read())

records_list = input_data['HealthData']['Record']
df = pd.DataFrame(records_list)

convert_tz = lambda x: x.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT+1'))
format = '%Y-%m-%d %H:%M:%S %z'



df['@creationDate'] = pd.to_datetime(df['@creationDate']).map(convert_tz)
df['@startDate'] = pd.to_datetime(df['@startDate']).map(convert_tz)
df['@endDate'] = pd.to_datetime(df['@endDate']).map(convert_tz)

df = df.drop(['@device','MetadataEntry', 'HeartRateVariabilityMetadataList'], axis=1)

cur = rdb.cursor()
output = io.StringIO()
df.to_csv(output,index=False,header=False)
output.seek(0)
cur.copy_from(output, 'AppleWatch', null="", sep=',')  # null values become ''
rdb.commit()




