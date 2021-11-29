import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time


def figure_box_hist(df, group, linear, bar):
    """ Update box plot and histogram in comparison tab depending on drop downs """
    df_linear = df[df['type'] == linear]
    df_bar = df[df['type'] == bar]
    name = df[group].unique()

    colors = px.colors.qualitative.Plotly

    fig_histogram = make_subplots(rows=1, cols=2, subplot_titles=(linear, bar))
    fig_box_plot = make_subplots(rows=1, cols=2, subplot_titles=(linear, bar))
    for name, i in enumerate(name):
        df_l = df_linear[df_linear[group] == i]
        df_b = df_bar[df_bar[group] == i]
        i = str(i)
        fig_histogram.add_trace(go.Histogram(x=df_l['Value'], name=i, showlegend=False, legendgroup=i,
                                             marker_color=colors[name]), row=1, col=1)
        fig_histogram.add_trace(go.Histogram(x=df_b['Value'], name=i, legendgroup=i, marker_color=colors[name]),
                                row=1, col=2)
        fig_box_plot.add_trace(go.Box(y=df_l['Value'],name=i, showlegend=False, legendgroup=i,
                                      marker_color=colors[name]), row=1, col=1)
        fig_box_plot.add_trace(go.Box(y=df_b['Value'], name=i, legendgroup=i, marker_color=colors[name]), row=1, col=2)

    # Overlay both histograms
    fig_histogram.update_layout(barmode='stack')
    fig_histogram.update_layout(template='plotly_white')
    fig_box_plot.update_layout(template='plotly_white')

    return fig_box_plot, fig_histogram


def figure_linear_plot(df1, df2, gr, linear, bar):
    """ Update linear plot in comparison tab depending on drop downs """

    fig1 = px.scatter(df1, x="week", y="Value", color=gr, template='plotly_white').update_traces(mode='lines+markers')
    fig2 = px.scatter(df2, x="week", y="Value", color=gr, template='plotly_white').update_traces(mode='lines+markers')
    fig1.update_layout(
        title={
            'text': "{}".format(linear),
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig2.update_layout(
        title={
            'text': "{}".format(bar),
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return fig1, fig2


def figure_workout_plot(df_box, df_scatter, gr, bar):
    """ Update workouts plot and histogram in comparison tab depending on drop downs """

    fig_box_plot = px.box(df_box, x=gr, y="HR_average", template='plotly_white')
    fig_box_plot.update_layout(
        title={
            'text': "Average Heart Rate during {}".format(bar),
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig_scatter_plot = px.scatter(df_scatter, x="date", y="HR_average", color=gr,
                                  template='plotly_white').update_traces(mode='lines+markers')
    fig_scatter_plot.update_layout(
        title={
            'text': "Average Heart Rate during {}".format(bar),
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return fig_box_plot, fig_scatter_plot

