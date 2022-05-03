from modules import ZIV_export as ziv
import io


def create_database_data(rdb):
    """
    CREATE the necessary tables in  a PostgreSQL database
    """
    # Remove tables from database if exists and create new name_type and examination tables in the PostgreSQL database
    drop_all_tables = """ DROP TABLE IF EXISTS AppleWatch,AppleWatch_numeric,AppleWatch_categorical,
                            other_sources,name,patient,activity_type """

    table_apple_watch = """CREATE TABLE AppleWatch (
                                    "type" text,
                                    "Name" text,
                                    "unit" text,
                                    "Date" timestamp,
                                    "Value" text)"""

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
        cur.execute(patient)
        rdb.commit()
        return print('done create_database_data')
    except (ValueError, Exception):
        return print("Problem with connection with database 1")


def load_json_data_to_database(rdb, path_list):
    """
    Inserting basic information, health and workout data into tables
    """
    cur = rdb.cursor()
    for path in path_list:
        path = './import/{}'.format(path)

        data = ziv.export_json_data(path)

        output = io.StringIO()
        data.to_csv(output, index=False, header=False)
        output.seek(0)

        cur.copy_from(output, 'applewatch', null="", sep=',')  # null values become ''
        rdb.commit()

    return print('done load json date')


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

    remove_date = """ TRUNCATE TABLE patient """
    insert_in_patient_table = """ INSERT INTO patient("Name", min_date, max_date) select "Name", min("Date"), max("Date") from applewatch group by "Name" """

    name_table = """CREATE TABLE name AS SELECT DISTINCT type FROM applewatch_numeric"""


    try:
        cur = rdb.cursor()
        cur.execute(create_table_apple_watch_numeric)
        cur.execute(create_table_apple_watch_categorical)
        cur.execute(sql)
        cur.execute(remove_date)
        cur.execute(insert_in_patient_table)
        cur.execute(name_table)
        rdb.commit()
        return print('done alter_tables')
    except (ValueError, Exception):
        return print("Problem with connection with database")


