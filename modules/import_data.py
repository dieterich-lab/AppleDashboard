from modules import export_data as ed
import io

def create_database_data(rdb):
    # Remove tables from database if exists and create new name_type and examination tables in the PostgreSQL database
    drop_all_tables = "DROP TABLE IF EXISTS AppleWatch,ECG,name,AppleWatch_numeric,AppleWatch_categorical,workout,patient"

    table_apple_watch = """CREATE TABLE AppleWatch (
                                    "type" text,
                                    "Name" text,
                                    "unit" text,
                                    "Date" timestamp,
                                    "Value" text)"""

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

    table_name = """CREATE TABLE name (
                                    "name" text,
                                    "type" text)"""

    patient = """CREATE TABLE patient (
                                    "Name" text,
                                    "index" integer,
                                    "Age" text,
                                    "Sex" text,
                                    "min_date" timestamp,
                                    "max_date" timestamp
                                    
    
    )"""

    try:
        cur = rdb.cursor()
        cur.execute(drop_all_tables)
        cur.execute(table_apple_watch)
        cur.execute(table_workout_apple_watch)
        cur.execute(table_ecg)
        cur.execute(table_name)
        cur.execute(patient)
        rdb.commit()
        return print('done create_database_data')
    except (ValueError, Exception):
        return print("Problem with connection with database 1")


def load_basic_information(rdb, files):
    for file in files:
        cur = rdb.cursor()
        patient, n, age, sex, min_date, max_date = ed.basic_information(file)
        cur.execute("INSERT INTO patient VALUES (%s,%s,%s,%s,%s,%s)", [patient, n, age, sex, min_date, max_date])
        rdb.commit()

    return print('done load health and workout data to database')


def load_health_data_to_database(rdb, files):
    for file in files:
        df = ed.export_health_data_from_apple_watch(file)
        df_workout = ed.export_workout_data_from_apple_watch(file)
        df_workout_calculation = ed.calculate_HRR(df,df_workout)
        output = io.StringIO()
        output_workout = io.StringIO()
        df.to_csv(output, index=False, header=False)
        df_workout_calculation.to_csv(output_workout, index=False, header=False)
        output.seek(0)
        output_workout.seek(0)
        cur = rdb.cursor()
        cur.copy_from(output, 'applewatch', null="", sep=',')  # null values become ''
        rdb.commit()
        cur.copy_from(output_workout, 'workout', null="", sep=',')  # null values become ''
        rdb.commit()

    return print('done load health and workout data to database')


def load_ecg_data_to_database(rdb, directories):
    df = ed.export_ecg_data_from_apple_watch(directories)
    cur = rdb.cursor()
    for index, row in df.iterrows():
        try:
            cur.execute("INSERT INTO ecg VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", row)
        except:
            print(df['patient'])
    rdb.commit()

    return print('done load_ecg_data_to_database')


def load_data_to_name_table(rdb):
    cur = rdb.cursor()
    name = './import/name.csv'
    with open(name, 'r') as in_file:
        for row in in_file:
            row = row.replace("\n", "").split(",")
            cur.execute("INSERT INTO name VALUES (%s, %s)", row)
    rdb.commit()
    in_file.close()

    return print('done load_data_to_name_table')


def alter_tables(rdb):

    # Alters in database
    add_column_name_to_table_apple_watch = """Alter table applewatch add column name text"""

    update_column_name = """UPDATE applewatch t2 SET name = t1.name FROM name t1 WHERE t2."type" = t1."type" """

    create_table_apple_watch_numeric = """CREATE TABLE applewatch_numeric AS SELECT "type","name","Name","unit",
    "Date",("Value"::double precision) as "Value" from applewatch where 
    "Value" ~ '-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?'"""

    create_table_apple_watch_categorical = """CREATE TABLE applewatch_categorical AS SELECT "type","name","Name",
    "unit","Date","Value" from applewatch where "Value" !~ '-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?'"""

    sql = """CREATE INDEX IF NOT EXISTS "Key_index" ON applewatch_numeric (name)"""

    try:
        cur = rdb.cursor()
        cur.execute(add_column_name_to_table_apple_watch)
        cur.execute(update_column_name)
        cur.execute(create_table_apple_watch_numeric)
        cur.execute(create_table_apple_watch_categorical)
        cur.execute(sql)
        rdb.commit()
        return print('done alter_tables')
    except (ValueError, Exception):
        return print("Problem with connection with database")


