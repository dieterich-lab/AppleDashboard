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
                                    "Date" text,
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

    create_table_patient = """CREATE TABLE patient AS select distinct "Name" from applewatch"""

    sql1 = """ALTER TABLE patient ADD "index" integer"""
    sql2 = """ALTER TABLE patient ADD "Age" integer"""
    sql3 = """ALTER TABLE patient ADD "Sex" text """
    sql4 = """ALTER TABLE patient ADD "min_date" timestamp"""
    sql5 = """ALTER TABLE patient ADD "max_date" timestamp"""

    sql6=""" UPDATE patient SET "Age" = '27', "Sex" = 'female',"index"='1',"min_date"='2020-02-20 14:35:28', "max_date"='2021-07-01 09:17:59' WHERE "Name" = 'Patient 1'  """
    sql7=""" UPDATE patient SET "Age" = '32', "Sex" = 'male',"index"='2',"min_date"='2019-05-18 18:13:39 ', "max_date"='2020-11-10 13:12:22'  WHERE "Name" = 'Patient 2' """
    sql8=""" UPDATE patient SET "Age" = '24', "Sex" = 'male',"index"='3',"min_date"='2019-09-20 16:30:00', "max_date"='2021-04-27 12:59:55 '  WHERE "Name" = 'Patient 3'  """
    sql9=""" UPDATE patient SET "Age" = '24', "Sex" = 'male',"index"='4',"min_date"='2016-12-25 07:35:50', "max_date"='2021-04-24 19:16:58 '  WHERE "Name" = 'Patient 4'  """
    sql10=""" UPDATE patient SET "Age" = '24', "Sex" = 'male',"index"='5',"min_date"='2018-12-28 12:37:51', "max_date"='2021-04-29 07:21:31'  WHERE "Name" = 'Patient 5' """
    sql11=""" UPDATE patient SET "Age" = '25', "Sex" = 'female',"index"='6',"min_date"='2021-04-02 18:15:52', "max_date"='2021-05-25 12:02:43'  WHERE "Name" = 'Patient 6' """
    sql12=""" UPDATE patient SET "Age" = '26', "Sex" = 'male',"index"='7',"min_date"='2021-06-10 15:38:33', "max_date"='2021-06-13 11:16:53'  WHERE "Name" = 'Patient 7'  """
    sql13=""" UPDATE patient SET "Age" = '26', "Sex" = 'male',"index"='8',"min_date"='2021-05-19 15:10:17', "max_date"='2021-06-17 16:25:21'  WHERE "Name" = 'Patient 8' """
    sql14=""" UPDATE patient SET "Age" = '23', "Sex" = 'female',"index"='9',"min_date"='2021-04-07 11:17:37', "max_date"='2021-05-19 10:08:23'  WHERE "Name" = 'Patient 9' """

    try:
        cur = rdb.cursor()
        cur.execute(add_column_name_to_table_apple_watch)
        cur.execute(update_column_name)
        cur.execute(create_table_apple_watch_numeric)
        cur.execute(create_table_apple_watch_categorical)

        cur.execute(create_table_patient)
        cur.execute(sql1)
        cur.execute(sql2)
        cur.execute(sql3)
        cur.execute(sql4)
        cur.execute(sql5)
        cur.execute(sql6)
        cur.execute(sql7)
        cur.execute(sql8)
        cur.execute(sql9)
        cur.execute(sql10)
        cur.execute(sql11)
        cur.execute(sql12)
        cur.execute(sql13)
        cur.execute(sql14)
        rdb.commit()
        return print('done alter_tables')
    except (ValueError, Exception):
        return print("Problem with connection with database")


