import modules.load_data_from_database as ldd
import plotly.express as px
import numpy as np
import pandas as pd
from db import connect_db
from itertools import product
from ecgdetectors import Detectors

rdb = connect_db()

def update_ecg_figure(day, time, patient):
    df = ldd.ECG_data(rdb, day, patient, time)

    if len(df) == 0:
        fig = {}
    else:
        data = np.array(df['Value'][0])/1000
        time = np.arange(0, len(data) / 511, 1 /511)
        time = time[0:len(data)]
        df_data = pd.DataFrame()
        df_data['value'] = data
        df_data['time'] = time
        r_peaks = detect_r_peaks(511,data)

        fig = px.line(x=time, y=data, template='plotly_white')
        fig.add_scatter(x=r_peaks / 511, y=data[r_peaks], mode='markers',name="R_peaks" )

        fig.update_layout(
            xaxis_title="Time(s)",
            yaxis_title="V",
            title={
            'text': '30 sec ECG {}'.format(df['Classification'].values[0]),
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return fig

def detect_r_peaks(SampleRate,data):
    # use library and implementation of peak detection to get array of r peak positions
    detectors = Detectors(SampleRate)
    # engzee worked best because it detects the position of max of the r peaks
    r_peaks = detectors.engzee_detector(data)
    # convert list to array
    r_peaks = np.array(r_peaks)
    return r_peaks