import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

def figure_boxplot(df,group,linear,bar):

    dfa=df[df['name']==linear]
    dfu=df[df['name']==bar]

    fig_box_plot= px.box(dfa, y="Value",color=group)
    fig_box_plot.update_layout(showlegend=False)
    fig_box_plot.update_layout(
        margin=dict(l=30, r=30, t=30, b=50),
    )
    fig_box_plot2 = px.box(dfu, y="Value",color=group)
    fig_box_plot2.update_layout(
        margin=dict(l=30, r=30, t=30, b=50),
    )
    fig_box_plot2.update_yaxes(title=None)



    fig_histogram = px.histogram(dfa, x="Value",color=group)
    fig_histogram.update_layout(showlegend=False)
    fig_histogram.update_layout(
        margin=dict(l=30, r=30, t=30, b=50),
    )
    fig_histogram2 = px.histogram(dfu, x="Value",color=group)
    fig_histogram2.update_layout(
        margin=dict(l=30, r=30, t=30, b=50),
    )
    fig_histogram2.update_yaxes(title=None)

    df = df.pivot(index=[group,'date'], columns='name', values='Value').reset_index()

    fig = px.scatter(df, x=bar, y=linear, color=group)


    return fig_box_plot,fig_box_plot2,fig_histogram,fig_histogram2,fig



def figure_linear_plot(df,gr,linear):


    fig = px.scatter(df, x="week", y="Value", color="Name").update_traces(mode='lines+markers')

    return fig

def figure_workout_plot(df,gr,bar2):

    fig = px.box(df,x="Name", y="HR_average")
    fig.update_layout(
        title={
            'text': "Average Heart Rate during {}".format(bar2),
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return fig