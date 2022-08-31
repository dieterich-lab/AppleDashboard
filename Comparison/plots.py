import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def figure_box_hist(df, group, linear, bar, labels):
    """ Update box plot and histogram in comparison tab depending on drop downs """
    df_linear, df_bar, name = df[df['key'] == linear], df[df['key'] == bar], df[group].unique()
    colors = px.colors.qualitative.Plotly
    fig_histogram = make_subplots(rows=1, cols=2, subplot_titles=(linear, bar))
    fig_box_plot = make_subplots(rows=1, cols=2, subplot_titles=(linear, bar))
    fig_add_traces(colors, df_bar, df_linear, fig_box_plot, fig_histogram, group, name)
    fig_update_layout(bar, fig_box_plot, fig_histogram, labels, linear)
    return fig_box_plot, fig_histogram


def fig_add_traces(colors, df_bar, df_linear, fig_box_plot, fig_histogram, group, i):
    for i, name in enumerate(i):
        if i > 10:
            i -= 10
        df_l = df_linear[df_linear[group] == name]
        df_b = df_bar[df_bar[group] == name]
        name = str(name)
        fig_histogram.add_trace(go.Histogram(x=df_l['Value'], name=name, showlegend=False, legendgroup=name,
                                             marker_color=colors[i]), row=1, col=1)
        fig_histogram.add_trace(go.Histogram(x=df_b['Value'], name=name, legendgroup=name, marker_color=colors[i]),
                                row=1, col=2)
        fig_box_plot.add_trace(go.Box(y=df_l['Value'], name=name, showlegend=False, legendgroup=name,
                                      marker_color=colors[i]), row=1, col=1)
        fig_box_plot.add_trace(go.Box(y=df_b['Value'], name=name, legendgroup=name, marker_color=colors[i]), row=1, col=2)


def fig_update_layout(bar, fig_box_plot, fig_histogram, labels, linear):
    fig_histogram.update_layout(barmode='stack', template='plotly_white')
    fig_histogram['layout']['yaxis1'].update(title='count')
    fig_histogram['layout']['xaxis1'].update(title=linear + ' [' + labels[linear] + ']')
    fig_histogram['layout']['xaxis2'].update(title=bar + ' [' + labels[bar] + ']')
    fig_box_plot.update_layout(template='plotly_white')
    fig_box_plot['layout']['yaxis1'].update(title=linear + ' [' + labels[linear] + ']')
    fig_box_plot['layout']['yaxis2'].update(title=bar + ' [' + labels[bar] + ']')


def figure_linear_plot(df, gr, linear, bar, labels):
    """ Update linear plot in comparison tab depending on drop downs """
    df_linear, df_bar = df[df['key'] == linear], df[df['key'] == bar]
    fig_linear = px.scatter(df_linear, x="week", y="Value", labels={"Value": linear + ' [' + labels[linear] + ']'},
                            color=gr, template='plotly_white').update_traces(mode='lines+markers')
    fig_bar = px.scatter(df_bar, x="week", y="Value", labels={"Value": bar + ' [' + labels[bar] + ']'}, color=gr,
                         template='plotly_white').update_traces(mode='lines+markers')

    fig_linear.update_layout(title=F"{linear}", title_x=0.5)
    fig_bar.update_layout(title=F"{bar}", title_x=0.5)

    return fig_linear, fig_bar


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

