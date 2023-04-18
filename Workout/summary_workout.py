import plotly.express as px
import pandas as pd


def update_figure(df, group, what):
    """ Update summary workout figure in Workout tab depending on drop downs"""
    df = df.groupby([group, "key"]).sum().reset_index()
    if group == 'DOW':
        cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df['DOW'] = pd.Categorical(df['DOW'], categories=cats, ordered=True)
        df = df.sort_values('DOW')

    if what == 'duration':
        title = F'Workout duration grouped by {group}'
        unit = ' [min]'
    elif what == 'distance':
        title = F'Distance covered during workout grouped by {group}'
        unit = ' [km]'
    else:
        title = F'Calories burned during workout grouped by {group}'
        unit = ' [kcal]'
    fig = px.bar(x=df[group],  y=df[what], color=df["key"])
    fig.update_layout(
        height=400,
        title=title,
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.02,
            xanchor="right",
            x=1
        ))
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text=what + unit)

    return fig
