import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def figure_boxplot(df,group):

    fig_box_plot= px.box(df, y="Value",color=group, facet_col="name")
    fig_box_plot.layout.yaxis2.update(matches=None)
    fig_histogram = px.histogram(df, x="Value",color=group, facet_col="name")
    fig_histogram.layout.yaxis2.update(matches=None)

    return fig_box_plot,fig_histogram

def figure_scatter_plot(df,gr,linear,bar):

    index = ['Name', 'Age', 'Sex', 'date']

    df = df.pivot(index=index, columns='name', values='Value') \
        .reset_index()

    fig = px.scatter(df, x=bar, y=linear, color=gr)

    return fig


def figure_linear_plot(df,gr,linear):


    fig = px.scatter(df, x="week", y="Value", color="Name").update_traces(mode='lines+markers')

    return fig

def figure_workout_plot(df,gr):
    #if group == 'M': index = ['Name','month']
    #elif group == 'W': index = ['Name','week']
    #elif group == 'DOW': index = ['Name','DOW','DOW_number']
    #else: index = ['Name','date']

    #df = df.pivot(index=index, columns='name', values='Value') \
    #    .reset_index()

    fig = px.box(df,x="Name", y="HR_average")

    return fig