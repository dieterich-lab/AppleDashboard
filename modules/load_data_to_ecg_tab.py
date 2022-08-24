import pandas as pd
from modules.models import ECG
from sqlalchemy.sql import select, and_, text
from sqlalchemy import Time


def ecg_data(rdb, day, patients, time):
    sql = select(ECG).where(and_(ECG.day == day, ECG.patient_id == patients,
                                 ECG.date.cast(Time) == time))
    return pd.read_sql(sql, rdb)


def table_hrv(rdb):
    sql = select(ECG.patient_id, ECG.date.cast(Time).label("time"), ECG.day, ECG.number, ECG.classification).\
        order_by(ECG.patient_id, ECG.day)
    return pd.read_sql(sql, rdb)


def scatter_plot_ecg(rdb, x_axis, y_axis):
    sql = select(ECG.patient_id, text('ECG.' + f'{x_axis}'), text('ECG.' + f'{y_axis}'))

    return pd.read_sql(sql, rdb)


def box_plot_ecg(rdb, x_axis):
    sql = select(ECG.patient_id, text('ECG.' + f'{x_axis}'))
    return pd.read_sql(sql, rdb)
