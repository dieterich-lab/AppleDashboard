import modules.load_data_from_database as ldd
import plotly.express as px
import numpy as np


def figur_ECG(date,num,patient1):
    date=str(date)
    df = ldd.ECG_data(ldd.rdb, date,patient1,num)


    if len(df) == 0:
        fig={}
    else:
        data = df['Value'][0]
        l = len(data) / 511
        N = 511
        time = np.arange(0, l, 1 / N)


        fig = px.line(x=time, y=data, template='plotly_white')
        fig.update_layout(title={
        'text': '30 sec ECG {}'.format(df['Classification'].values[0]),
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='LightPink',showticklabels=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
        fig.update_yaxes(nticks=20)
        fig.update_xaxes(nticks=750)
        fig.update_layout(
            xaxis_title="",
            yaxis_title="",

        )

    return fig