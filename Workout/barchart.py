from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

def update_figure(df,group,what):
    df = df[(df['duration'] > 10) & (df['duration'] < 300)]
    if group == 'M':
        df = df.groupby(['month',"type"]).sum().reset_index()
        fig = px.bar(x=df['month'], y=df[what], color=df["type"])
    elif group == 'W':
        df = df.groupby(['week',"type"]).sum().reset_index()
        fig= px.bar(x=df['week'], y=df[what], color=df["type"])
    elif group == 'DOW':
        df = df.groupby(['DOW','DOW_number',"type"]).sum().reset_index()
        fig= px.bar(x=df['DOW'], y=df[what], color=df["type"])
    else:
        df = df.groupby(['date',"type"]).sum().reset_index()
        fig = px.bar(x=df['date'],  y=df[what], color=df["type"])
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
    fig.update_yaxes(title_text=what)

    return fig