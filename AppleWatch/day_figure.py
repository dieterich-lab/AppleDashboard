from plotly.subplots import make_subplots
import plotly.graph_objects as go
from db import connect_db

# connection with database
rdb = connect_db()


def day_figure_update(df, bar):
    """ Update day figure depends on drop downs """

    df_bar = df[df['key'] == bar]
    df = df[df['key'] == 'Heart Rate']
    if not df_bar.empty:
        df_bar = df_bar.resample('5Min', on='date').sum().reset_index()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df['date'], y=df["value"], name="Heart Rate"), secondary_y=False)
    fig.add_trace(go.Bar(x=df_bar['date'], y=df_bar["value"], name='{}'.format(bar)), secondary_y=True)
    fig.update_layout(
        height=400,
        template='plotly_white',
        xaxis_title="Time",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
    fig.update_yaxes(title_text='{}'.format(bar), secondary_y=False)

    return fig
