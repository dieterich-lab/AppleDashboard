import pandas as pd
import xmltodict
import psycopg2
import io
import pytz
from os import listdir
from os.path import isfile, join


def import_data(rdb, files, directories):
    # Remove tables from database if exists and create new name_type and examination tables in the PostgreSQL database
    sql1 = "DROP TABLE IF EXISTS AppleWatch,ECG,name,AppleWatch_numeric,AppleWatch_categorical"

    statment_examination = """CREATE TABLE AppleWatch (
                                    "@type" text,
                                    "@sourceName" text,
                                    "@sourceVersion" text,
                                    "@unit" text,
                                    "@creationDate" timestamp,
                                    "@startDate" timestamp,
                                    "@endDate" timestamp,
                                    "@Value" text)"""

    statment_examination2 = """CREATE TABLE ECG (
                                    "Patient" text,
                                    "Name" text,
                                    "Day" text,
                                    "number" text,
                                    "Classification" text,
                                    "Value" integer [])"""

    statment_examination3 = """CREATE TABLE name (
                                    "name" text,
                                    "@type" text)"""

    try:
        cur = rdb.cursor()
        cur.execute(sql1)
        cur.execute(statment_examination)
        cur.execute(statment_examination2)
        cur.execute(statment_examination3)
        rdb.commit()
        print('done')
    except Exception:
        print("Problem with connection with database 1")


    appended_data = []
    for i in files:
        # export data from xml file
        input_path = './import/{}'.format(i)
        with open(input_path, 'r') as xml_file:
            input_data = xmltodict.parse(xml_file.read())

        records_list = input_data['HealthData']['Record']
        df = pd.DataFrame(records_list)
        n = int(''.join(filter(str.isdigit, i)))
        df['@sourceName'] = df['@sourceName'].apply(lambda x: 'Patient {}'.format(n))
        xml_file.close()

        appended_data.append(df)

    df = pd.concat(appended_data)

    # convert time to you time zone
    convert_tz = lambda x: x.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT+1'))
    format = '%Y-%m-%d %H:%M:%S %z'

    df['@creationDate'] = pd.to_datetime(df['@creationDate']).map(convert_tz)
    df['@startDate'] = pd.to_datetime(df['@startDate']).map(convert_tz)
    df['@endDate'] = pd.to_datetime(df['@endDate']).map(convert_tz)

    # Remove not necessary data
    df = df.drop(['@device','MetadataEntry', 'HeartRateVariabilityMetadataList'], axis=1)


    # load data to SQL database by copy csv file
    output = io.StringIO()
    df.to_csv(output,index=False,header=False)
    output.seek(0)

    cur = rdb.cursor()
    cur.copy_from(output, 'AppleWatch', null="", sep=',')  # null values become ''
    rdb.commit()
    print('done')
    # Loading ECG data to database
    for i in directories:
        onlyfiles = [f for f in listdir('./import/{}/'.format(i))
                    if isfile(join('./import/{}/'.format(i), f))]
        n = int(''.join(filter(str.isdigit, i)))
        patient = 'Patient{}'.format(n)
        for ecg_file in onlyfiles:
            path = './import/{0}/{1}'.format(i,ecg_file)
            ECG = pd.read_csv(path, error_bad_lines=False,warn_bad_lines=False)
            ECG.reset_index(level=0, inplace=True)
            data = pd.to_numeric(ECG['index'][8:]).to_list()
            ecg_file = ecg_file.replace('ecg_','').replace('.csv', '')

            if '_' not in ecg_file:
                ecg_file = ecg_file+'_0'

            day, number = ecg_file[:10], ecg_file[-1]
            line =[]
            line.append(patient)
            line.append(ecg_file)
            line.append(day)
            line.append(number)
            line.append(ECG['Name'][2])
            #line.append([patient, name, day, number, ECG['Name'][2],data])
            line.append(data)


            cur.execute("INSERT INTO ECG VALUES (%s,%s,%s,%s,%s,%s)", line)
        rdb.commit()
        print('done')

    # create table with name for Apple Watch entities
    name = './import/name.csv'
    with open(name, 'r') as in_file:
        for row in in_file:
            row = row.replace("\n", "").split(",")
            cur.execute("INSERT INTO name VALUES (%s, %s)", row)
    rdb.commit()
    in_file.close()

    # Alters in database
    sql1 = """Alter table AppleWatch add column name text"""
    sql2 = """UPDATE AppleWatch t2 SET name = t1.name FROM name t1 WHERE t2."@type" = t1."@type" """
    sql3 = """CREATE TABLE AppleWatch_numeric AS SELECT "@type","name","@sourceName","@sourceVersion","@unit",
                "@creationDate","@startDate","@endDate",("@Value"::double precision) as "@Value" from AppleWatch 
                where "@Value" ~ '-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?'"""
    sql4 = """CREATE TABLE AppleWatch_categorical AS SELECT "@type","name","@sourceName","@sourceVersion","@unit",
            "@creationDate","@startDate","@endDate","@Value" from AppleWatch 
            where "@Value" !~ '-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?'"""
    try:
        cur = rdb.cursor()
        cur.execute(sql1)
        cur.execute(sql2)
        cur.execute(sql3)
        cur.execute(sql4)
        rdb.commit()
        print('done')
    except Exception:
        print("Problem with connection with database")


