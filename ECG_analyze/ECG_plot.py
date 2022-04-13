import modules.load_data_from_database as ldd
import plotly.express as px
import numpy as np
import pandas as pd
from db import connect_db
from itertools import product
from ecgdetectors import Detectors
from modules import export_data as ed



rdb = connect_db()


def add_minor_grid(fig, x_range, y_range, major_step_x=0.4, major_step_y=1, minorgridcount_x=9, minorgridcount_y=9):
    """ Create ECG grid """
    x_list = np.arange(x_range[0], x_range[1]+major_step_x, major_step_x)
    y_list = np.arange(y_range[0], y_range[1]+major_step_y, major_step_y)
    x, y = list(zip(*product(x_list, y_list)))

    fig.add_carpet(
        a=x,
        b=y,
        x=x,
        y=y,

        aaxis={
            'minorgridcount': minorgridcount_x,
            'showticklabels': 'none',
        },
        baxis={
            'minorgridcount': minorgridcount_y,
            'showticklabels': 'none',
        }
    )

    fig.layout.xaxis.range = x_range
    fig.layout.yaxis.range = y_range


def update_ecg_figure(day, time, patient, add):
    """ Update ECG graph in Patient and ECG tab depending on drop downs"""
    df = ldd.ecg_data(rdb, day, patient, time)

    if len(df) == 0:
        fig = {}
    else:
        data = np.array(df['Value'][0])/1000
        time = np.arange(0, len(data) / 511, 1 /511)
        time = time[0:len(data)]
        r_peaks = np.array(df['r_peaks'][0])
        df_data = pd.DataFrame()
        df_data['value'] = data
        df_data['time'] = time

        fig = px.line(x=time, y=data, template='plotly_white')

        # if minor grid or R peaks should be added to ECG plot
        if add == 'R_peaks':
            fig.add_scatter(x=r_peaks/ 511 , y=data[r_peaks], mode='markers', name="R_peaks" )
        else:
            add_minor_grid(fig, x_range=[0, 30], y_range=[-1.5, 1.5])
            fig.update_xaxes(showgrid=True, gridwidth=1.5, gridcolor='red', nticks=80, range=[0, 10],
                             rangeslider_visible=True, rangeslider_thickness=0.1)
            fig.update_yaxes(showgrid=True, gridwidth=1.5, gridcolor='red', zeroline=False, showticklabels=False)

        fig.update_layout(
            xaxis_title="Time(s)",
            yaxis_title="V",
            title={
                'text': '30 sec ECG {}'.format(df['Classification'].values[0]),
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})

    return fig, df_data

