import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def figure_box_hist(df, group, linear, bar, labels):
    """ Update box plot and histogram in comparison tab depending on drop downs """
    df_linear = df[df['key'] == linear]
    df_bar = df[df['key'] == bar]
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
        fig_box_plot.add_trace(go.Box(y=df_l['Value'], name=i, showlegend=False, legendgroup=i,
                                      marker_color=colors[name]), row=1, col=1)
        fig_box_plot.add_trace(go.Box(y=df_b['Value'], name=i, legendgroup=i, marker_color=colors[name]), row=1, col=2)

    fig_histogram.update_layout(barmode='stack', template='plotly_white')
    fig_histogram['layout']['yaxis1'].update(title='count')
    fig_histogram['layout']['xaxis1'].update(title=linear + ' [' + labels[linear] + ']')
    fig_histogram['layout']['xaxis2'].update(title=bar + ' [' + labels[bar] + ']')
    fig_box_plot.update_layout(template='plotly_white')
    fig_box_plot['layout']['yaxis1'].update(title=linear + ' [' + labels[linear] + ']')
    fig_box_plot['layout']['yaxis2'].update(title=bar + ' [' + labels[bar] + ']')

    return fig_box_plot, fig_histogram


def figure_linear_plot(df1, df2, gr, linear, bar, labels):
    """ Update linear plot in comparison tab depending on drop downs """

    fig1 = px.scatter(df1, x="week", y="Value", labels={"Value": linear + ' [' + labels[linear] + ']'},
                      color=gr, template='plotly_white').update_traces(mode='lines+markers')
    fig2 = px.scatter(df2, x="week", y="Value", labels={"Value": bar + ' [' + labels[bar] + ']'}, color=gr,
                      template='plotly_white').update_traces(mode='lines+markers')
    fig1.update_layout(
        title={
            'text': F"{linear}",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig2.update_layout(
        title={
            'text': F"{bar}",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return fig1, fig2


def figure_workout_plot(df_box, df_scatter, gr, bar):
    """ Update workouts plot and histogram in comparison tab depending on drop downs """

    fig_box_plot = px.box(df_box, x=gr, y="hr_average", labels={"hr_average": "Average Heart Rate [bpm]"},
                          template='plotly_white')
    fig_box_plot.update_layout(title=F"Average Heart Rate during {bar}", title_x=0.5)

    fig_scatter_plot = px.scatter(df_scatter, x="date", y="hr_average",
                                  labels={"hr_average": "Average Heart Rate [bpm]"}, color=gr,
                                  template='plotly_white').update_traces(mode='lines+markers')
    fig_scatter_plot.update_layout(title=F"Average Heart Rate during {bar}", title_x=0.5)

    return fig_box_plot, fig_scatter_plot

