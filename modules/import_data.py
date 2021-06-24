from modules import export_data as ed
import io

def create_database_data(rdb):
    # Remove tables from database if exists and create new name_type and examination tables in the PostgreSQL database
    drop_all_tables = "DROP TABLE IF EXISTS AppleWatch,ECG,name,AppleWatch_numeric,AppleWatch_categorical,workout"

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
                                    "End_Date" timestamp)"""

    table_ecg = """CREATE TABLE ECG (
                                    "Patient" text,
                                    "Date" text,
                                    "Day" text,
                                    "number" text,
                                    "Classification" text,
                                    "Value" integer [])"""

    table_name = """CREATE TABLE name (
                                    "name" text,
                                    "type" text)"""

    try:
        cur = rdb.cursor()
        cur.execute(drop_all_tables)
        cur.execute(table_apple_watch)
        cur.execute(table_workout_apple_watch)
        cur.execute(table_ecg)
        cur.execute(table_name)
        rdb.commit()
        return print('done create_database_data')
    except (ValueError, Exception):
        return print("Problem with connection with database 1")


def load_health_data_to_database(rdb, files):
    df = ed.export_health_data_from_apple_watch(files)
    output = io.StringIO()
    df.to_csv(output, index=False, header=False)
    output.seek(0)
    cur = rdb.cursor()
    cur.copy_from(output, 'AppleWatch', null="", sep=',')  # null values become ''
    rdb.commit()
    df_workout = ed.export_workout_data_from_apple_watch(files)
    output_workout = io.StringIO()
    df_workout.to_csv(output_workout, index=False, header=False)
    output_workout.seek(0)
    cur.copy_from(output_workout, 'Workout', null="", sep=',')  # null values become ''
    rdb.commit()

    return print('done load health and workout data to database')


def load_ecg_data_to_database(rdb, directories):
    df = ed.export_ecg_data_from_apple_watch(directories)
    cur = rdb.cursor()
    for index, row in df.iterrows():
        cur.execute("INSERT INTO ECG VALUES (%s,%s,%s,%s,%s,%s)", row)
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
    add_column_name_to_table_apple_watch = """Alter table AppleWatch add column name text"""
    update_column_name = """UPDATE AppleWatch t2 SET name = t1.name FROM name t1 WHERE t2."type" = t1."type" """
    create_table_apple_watch_numeric = """CREATE TABLE AppleWatch_numeric AS SELECT "type","name","Name","unit",
    "Date",("Value"::double precision) as "Value" from AppleWatch where 
    "Value" ~ '-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?'"""
    create_table_apple_watch_categorical = """CREATE TABLE AppleWatch_categorical AS SELECT "type","name","Name",
    "unit","Date","Value" from AppleWatch where "Value" !~ '-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?'"""
    try:
        cur = rdb.cursor()
        cur.execute(add_column_name_to_table_apple_watch)
        cur.execute(update_column_name)
        cur.execute(create_table_apple_watch_numeric)
        cur.execute(create_table_apple_watch_categorical)
        rdb.commit()
        return print('done alter_tables')
    except (ValueError, Exception):
        return print("Problem with connection with database")


