from sqlalchemy import Column, Integer, String, Numeric, text, DateTime, ARRAY, Index
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
    index = Column(Integer, primary_key=True)
    key = Column(String)
    patient_id = Column(String)
    unit = Column(String)
    date = Column(DateTime)
    value = Column(Numeric)
    __table_args__ = (Index('idx_key_num', 'key'), Index('idx_patient_id_num', 'patient_id'))


class AppleWatchCategorical(Base):
    __tablename__ = "apple_watch_categorical"
    index = Column(Integer, primary_key=True)
    key = Column(String)
    patient_id = Column(String)
    unit = Column(String)
    date = Column(DateTime)
    value = Column(String)
    __table_args__ = (Index('idx_key_cat', 'key'), Index('idx_patient_id_cat', 'patient_id'))


class OtherSources(Base):
    __tablename__ = "other_source"
    index = Column(Integer, primary_key=True)
    key = Column(String)
    source_name = Column(String)
    unit = Column(String)
    date = Column(DateTime)
    value = Column(String)
    patient_id = Column(String)


class Workout(Base):
    __tablename__ = "workout"
    index = Column(Integer, primary_key=True)
    key = Column(String)
    duration = Column(Numeric)
    duration_unit = Column(String)
    distance = Column(Numeric)
    distance_unit = Column(String)
    energyburned = Column(Numeric)
    energyburnedunit = Column(String)
    patient_id = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    hrr_1_min = Column(Numeric)
    hrr_2_min = Column(Numeric)
    hr_max = Column(Numeric)
    hr_min = Column(Numeric)
    hr_average = Column(Numeric)
    speed = Column(Numeric)
    hr_rs_index = Column(Numeric)


class ECG(Base):
    __tablename__ = "ecg"
    index = Column(Integer, primary_key=True)
    patient_id = Column(String)
    date = Column(DateTime)
    day = Column(String)
    number = Column(String)
    classification = Column(String)
    data = Column(ARRAY(Numeric))
    hrv = Column(Numeric)
    sdnn = Column(Numeric)
    senn = Column(Numeric)
    sdsd = Column(Numeric)
    pnn20 = Column(Numeric)
    pnn50 = Column(Numeric)


def drop_tables(rdb):
    Base.metadata.drop_all(rdb)


def create_tables(rdb):
    Base.metadata.create_all(rdb)


def check_if_tables_exists(rdb):
    table = ''
    connection = rdb.connect()
    result = connection.execute(text("SELECT to_regclass('public.apple_watch_numerical')"))
    for row in result:
        table = row[0]
    if table != 'apple_watch_numerical':
        create_tables(rdb)
