from modules import export_data as ed
import xmltodict
import io
from os import listdir
from os.path import isfile, join
import pandas as pd


def insert_data(rdb, files):
    """
    Inserting basic information, health and workout data into tables
    """
    rdb_connection = rdb.raw_connection()
    cur = rdb_connection.cursor()
    last_value = 0
    last_value_workout_df = 0
    for file in files:
        input_path = './import/{}'.format(file)

        with open(input_path, 'r', errors='ignore') as xml_file:
            input_data = xmltodict.parse(xml_file.read())
            n = int(''.join(filter(str.isdigit, file)))

        xml_file.close()

        df, df2, min_date, max_date = ed.export_health_data_from_apple_watch(input_data, n)
        df['index'] = df.index + last_value
        last_value = df['index'].iat[-1] + 1
        df_numerical = df[pd.to_numeric(df['@value'], errors='coerce').notnull()]
        df_categorical = df[~pd.to_numeric(df['@value'], errors='coerce').notnull()]
        copy_data_frame_to_database(cur, df_numerical, 'apple_watch_numerical')
        copy_data_frame_to_database(cur, df_categorical, 'apple_watch_categorical')

        data = ed.basic_information(input_data, n)
        data['min_date'], data['max_date'] = min_date, max_date
        copy_data_frame_to_database(cur, data, 'patient')

        df_workout = ed.export_workout_data_from_apple_watch(input_data, n)
        df_workout_calculation = ed.calculate_hrr(df, df_workout)
        df_workout_calculation['index'] = df_workout_calculation.index + last_value_workout_df
        last_value_workout_df = df_workout_calculation['index'].iat[-1] + 1
        copy_data_frame_to_database(cur, df_workout_calculation, 'workout')

        rdb_connection.commit()
    return print('done load health and workout data to database')


def copy_data_frame_to_database(cur, df, table):
    output = io.StringIO()
    df.to_csv(output, index=False, header=False)
    output.seek(0),
    cur.copy_from(output, f'{table}', null="", sep=',')


def load_ecg_data_to_database(rdb, directories):
    """
    Inserting ECG data into tables
    """
    rdb_connection = rdb.raw_connection()
    cur = rdb_connection.cursor()
    last_value_ecg_df = 0
    # Loading ECG data to database
    for directory in directories:
        files = [f for f in listdir('./import/{}/'.format(directory)) if isfile(join('./import/{}/'.format(directory), f))]

        n = int(''.join(filter(str.isdigit, directory)))
        patient = 'Patient {}'.format(n)
        df = ed.export_ecg_data_from_apple_watch(files, directory, patient)
        df['index'] = df.index + last_value_ecg_df
        last_value_ecg_df = df['index'].iat[-1] + 1
        for index, row in df.iterrows():
            cur.execute("INSERT INTO ecg VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", row)

        rdb_connection.commit()
    return print('done load_ecg_data_to_database')


def create_tables_type(rdb):
    rdb_connection = rdb.raw_connection()
    cur = rdb_connection.cursor()

    name_table = """INSERT INTO key_name (SELECT DISTINCT key,unit FROM apple_watch_numerical)"""
    activity_type = """INSERT INTO activity_name (SELECT DISTINCT key FROM workout WHERE key is not NULL )"""
    cur.execute(name_table)
    cur.execute(activity_type)
    rdb_connection.commit()



