import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import modules.load_data_from_database as ldd
from db import connect_db

# connection with database
rdb = connect_db()


def day_figure_update(date, value, group, patient, linear,bar):
    date = date[0]
    value = value[0]
    df = ldd.day_figure(rdb, patient, group, linear, bar, date, value)

    if not df.empty:
        df_bar = df[df['name'] == bar]
        df = df[df['name'] == 'Heart Rate']
        df_bar = df_bar.resample('5Min', on='Date').sum().reset_index()
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=df['Date'], y=df["Value"], name="Heart Rate"), secondary_y=False)
        fig.add_trace(go.Bar(x=df_bar['Date'], y=df_bar["Value"], name='{}'.format(bar)), secondary_y=True)
        fig.update_layout(
            height=400,
            template='plotly_white',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ))
        fig.update_xaxes(title_text="Time")
        fig.update_yaxes(title_text='{}'.format(bar), secondary_y=False)
    else:
        fig = {}

    return fig
