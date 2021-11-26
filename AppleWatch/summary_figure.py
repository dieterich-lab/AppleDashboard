from plotly.subplots import make_subplots
import plotly.graph_objects as go
import modules.load_data_from_database as ldd
from db import connect_db
import numpy as np

# connection with database
rdb = connect_db()


def update_figure(df, linear, bar, index):

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(x=df[index], y=df[bar], name='{}'.format(bar)), secondary_y=False)

    if isinstance(linear, list):
        for i in linear:
            df_linear = df[[index, i]]
            df_linear = df_linear.replace('', np.nan).dropna(subset=[i])
            fig.add_trace(go.Scatter(x=df_linear[index], y=df_linear[i], name='{}'.format(i), mode='lines+markers'),
                          secondary_y=True)
    else:
        df_linear = df[[index, linear]]
        df_linear = df_linear.replace('', np.nan).dropna(subset=[linear])
        fig.add_trace(
            go.Scatter(x=df_linear[index], y=df_linear[linear], name='{}'.format(linear), mode='lines+markers'),
            secondary_y=True)

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
    if not isinstance(linear, list):
        fig.update_yaxes(title_text='{}'.format(linear), secondary_y=True)
    fig.update_yaxes(title_text='{}'.format(bar), secondary_y=False)
    return fig
