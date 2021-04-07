import modules.load_data_from_database as ldd
import plotly.express as px
import numpy as np
import pandas as pd
from db import connect_db
from itertools import product
rdb = connect_db()


def add_minor_grid(fig, x_range, y_range, major_step_x=1, major_step_y=500, minorgridcount_x=9, minorgridcount_y=9):

    x_list = range(x_range[0], x_range[1]+major_step_x, major_step_x)
    y_list = range(y_range[0], y_range[1]+major_step_y, major_step_y)
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


def update_ecg_figure(day, number, patient):
    df = ldd.ECG_data(rdb, day, patient, number)

    if len(df) == 0:
        fig = {}
    else:
        data = df['Value'][0]
        time = np.arange(0, len(data) / 511, 1 /511)
        time = time[0:len(data)]
        df_data = pd.DataFrame()
        df_data['value'] = data
        df_data['time'] = time

        fig = px.line(x=time, y=data, template='plotly_white')
        fig.update_layout(title={
            'text': '30 sec ECG {}'.format(df['Classification'].values[0]),
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

        add_minor_grid(fig, x_range=[0, 30], y_range=[-500, 1200])
        fig.update_xaxes(showgrid=True, gridwidth=1.5, gridcolor='red')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
        fig.update_yaxes(nticks=20)
        fig.update_layout(
            xaxis_title="Time(s)",
            yaxis_title="",

        )
    return fig, df_data
