from plotly.subplots import make_subplots
import plotly.express as px


def update_figure(df, group, what):

    if group == 'M': index = 'month'
    elif group == 'W': index = 'week'
    elif group == 'DOW': index = 'DOW'
    else: index = 'date'

    df = df[(df['duration'] > 10) & (df['duration'] < 300)]
    df = df.groupby([index, "type"]).sum().reset_index()
    fig = px.bar(x=df[index],  y=df[what], color=df["type"])
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
