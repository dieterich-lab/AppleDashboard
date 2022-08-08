from sqlalchemy import Column, Integer, String, Numeric, text, DateTime, ARRAY
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class KeyName(Base):
    __tablename__ = "key_name"
    key = Column(String, primary_key=True)


class ActivityName(Base):
    __tablename__ = "activity_name"
    key = Column(String, primary_key=True)


class Patient(Base):
    __tablename__ = "patient"
    patient_id = Column(String, primary_key=True)
    index = Column(Integer)
    age = Column(Integer)
    sex = Column(String)
    blood_group = Column(String)
    skin_type = Column(String)
    min_date = Column(DateTime)
    max_date = Column(DateTime)


class AppleWatchNumerical(Base):
    __tablename__ = "apple_watch_numerical"
    id = Column(Integer, primary_key=True)
    key = Column(String)
    patient_id = Column(String)
    unit = Column(String)
    date = Column(DateTime)
    value = Column(Numeric)


class AppleWatchCategorical(Base):
    __tablename__ = "apple_watch_categorical"
    id = Column(Integer, primary_key=True)
    key = Column(String)
    patient_id = Column(String)
    unit = Column(String)
    date = Column(DateTime)
    value = Column(String)


class OtherSources(Base):
    __tablename__ = "other_source"
    id = Column(Integer, primary_key=True)
    key = Column(String)
    source_name = Column(String)
    unit = Column(String)
    date = Column(DateTime)
    value = Column(String)
    patient_id = Column(String)


class Workout(Base):
    __tablename__ = "workout"
    id = Column(Integer, primary_key=True)
    key = Column(String)
    duration = Column(Numeric)
    duration_unit = Column(String)
    distance = Column(Numeric)
    distance_unit = Column(String)
    energyburned = Column(Numeric)
    energyburnedunit = Column(String)
    patient_id = Column(String)
    start_date = Column(Numeric)
    end_date = Column(Numeric)
    hrr_1_min = Column(Numeric)
    hrr_2_min = Column(Numeric)
    hr_max = Column(Numeric)
    hr_min = Column(Numeric)
    hr_average = Column(Numeric)
    speed = Column(Numeric)
    hr_rs_index = Column(Numeric)


class ECG(Base):
    __tablename__ = "ecg"
    patient_id = Column(String)
    date = Column(DateTime)
    day = Column(String)
    number = Column(String)
    classification = Column(String)
    value = Column(ARRAY(Numeric))
    hrvOwn = Column(Numeric)
    sdnn = Column(Numeric)
    senn = Column(Numeric)
    sdsd = Column(Numeric)
    pnn20 = Column(Numeric)
    pnn50 = Column(Numeric)
    lf = Column(Numeric)
    hf = Column(Numeric)
    lf_hf_ratio = Column(Numeric)
    total_power = Column(Numeric)
    vlf = Column(Numeric)


def drop_tables(rdb):
    Base.metadata.drop_all(rdb)


def create_tables(rdb):
    Base.metadata.create_all(rdb)


def check_if_tables_exists(rdb):
    table = ''
    connection = rdb.connect()
    result = connection.execute(text("SELECT to_regclass('public.examination_numerical')"))
    for row in result:
        table = row[0]
    if table != 'examination_numerical':
        create_tables(rdb)