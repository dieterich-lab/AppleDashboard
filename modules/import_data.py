from modules import export_data as ed
import xmltodict
import io


def create_database_data(rdb):
    """
    CREATE the necessary tables in  a PostgreSQL database
    """
    # Remove tables from database if exists and create new name_type and examination tables in the PostgreSQL database
    drop_all_tables = """ DROP TABLE IF EXISTS AppleWatch,AppleWatch_numeric,AppleWatch_categorical,
                            other_sources,workout,ECG,name,patient,activity_type """

    table_apple_watch = """CREATE TABLE AppleWatch (
                                    "type" text,
                                    "Name" text,
                                    "unit" text,
                                    "Date" timestamp,
                                    "Value" text)"""

    table_other_sources = """CREATE TABLE other_sources (
                                    "type" text,
                                    "Name" text,
                                    "unit" text,
                                    "Date" timestamp,
                                    "Value" text,
                                    "Patient" text)"""

    table_workout_apple_watch = """CREATE TABLE Workout (
                                    "type" text,
                                    "duration" float,
                                    "duration_unit" text,
                                    "distance" float,
                                    "distance_unit" text,
                                    "EnergyBurned" float,
                                    "EnergyBurnedUnit" text,
                                    "Name" text,
                                    "Start_Date" timestamp,
                                    "End_Date" timestamp,
                                    "HRR_1_min" float,
                                    "HRR_2_min" float,
                                    "HR_max" float,
                                    "HR_min" float,
                                    "HR_average" float,
                                    "speed" float,
                                    "HR-RS_index" float)"""

    table_ecg = """CREATE TABLE ECG (
                                    "Patient" text,
                                    "Date" timestamp,
                                    "Day" text,
                                    "number" text,
                                    "Classification" text,
                                    "Value" integer [],
                                    "hrvOwn" integer,
                                    "SDNN" integer,
                                    "SENN" integer,
                                    "SDSD" integer,
                                    "pNN20" integer,
                                    "pNN50" integer,
                                    "lf" integer,
                                    "hf" integer,
                                    "lf_hf_ratio" integer,
                                    "total_power" integer,
                                    "vlf" integer)"""

    patient = """CREATE TABLE patient (
                                    "Name" text,
                                    "index" integer,
                                    "Age" text,
                                    "Sex" text,
                                    "blood_group" text,
                                    "skin_type" text,
                                    "min_date" timestamp,
                                    "max_date" timestamp)"""

    try:
        cur = rdb.cursor()
        cur.execute(drop_all_tables)
        cur.execute(table_apple_watch)
        cur.execute(table_other_sources)
        cur.execute(table_workout_apple_watch)
        cur.execute(table_ecg)
        cur.execute(patient)
        rdb.commit()
        return print('done create_database_data')
    except (ValueError, Exception):
        return print("Problem with connection with database 1")


def insert_data(rdb, files):
    """
    Inserting basic information, health and workout data into tables
    """
    cur = rdb.cursor()
    for file in files:
        # export data from xml file
        input_path = './import/{}'.format(file)

        with open(input_path, 'r', errors='ignore') as xml_file:
            input_data = xmltodict.parse(xml_file.read())
            n = int(''.join(filter(str.isdigit, file)))

        xml_file.close()

        data = ed.basic_information(input_data, n)
        df, df2, min_date, max_date = ed.export_health_data_from_apple_watch(input_data, n)
        data.extend([min_date, max_date])
        cur.execute("INSERT INTO patient VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", data)
        df_workout = ed.export_workout_data_from_apple_watch(input_data, n)
        df_workout_calculation = ed.calculate_HRR(df, df_workout)

        output, output_workout = io.StringIO(), io.StringIO()
        df.to_csv(output, index=False, header=False)
        df_workout_calculation.to_csv(output_workout, index=False, header=False)
        output.seek(0), output_workout.seek(0)

        cur.copy_from(output, 'applewatch', null="", sep=',')  # null values become ''
        cur.copy_from(output_workout, 'workout', null="", sep=',')  # null values become ''
        rdb.commit()

    return print('done load health and workout data to database')


def load_ecg_data_to_database(rdb, directories):
    """
    Inserting ECG data into tables
    """
    df = ed.export_ecg_data_from_apple_watch(directories)
    cur = rdb.cursor()
    for index, row in df.iterrows():
        try:
            cur.execute("INSERT INTO ecg VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", row)
        except:
            print(df['patient'])
    rdb.commit()

    return print('done load_ecg_data_to_database')


def alter_tables(rdb):
    """
    CREATE tables for numeric and categorical data and necessary indexes.
    """
    # Alters in database
    create_table_apple_watch_numeric = """CREATE TABLE applewatch_numeric AS 
                                            SELECT "type","Name","unit","Date",("Value"::double precision) AS "Value" 
                                            FROM applewatch 
                                            WHERE "Value" ~ '-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?'"""

    create_table_apple_watch_categorical = """CREATE TABLE applewatch_categorical AS 
                                                SELECT "type","Name","unit","Date","Value" 
                                                FROM applewatch 
                                                WHERE "Value" !~ '-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?'"""

    sql = """CREATE INDEX IF NOT EXISTS "Key_index" ON applewatch_numeric (type)"""

    name_table = """CREATE TABLE name AS SELECT DISTINCT type FROM applewatch_numeric"""

    activity_type = """CREATE TABLE activity_type AS SELECT DISTINCT type FROM Workout"""

    try:
        cur = rdb.cursor()
        cur.execute(create_table_apple_watch_numeric)
        cur.execute(create_table_apple_watch_categorical)
        cur.execute(sql)
        cur.execute(name_table)
        cur.execute(activity_type)
        rdb.commit()
        return print('done alter_tables')
    except (ValueError, Exception):
        return print("Problem with connection with database")


