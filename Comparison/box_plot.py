import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

def figure_boxplot(df,group,linear,bar):

    dfa=df[df['name']==linear]
    dfu=df[df['name']==bar]
    namee = df[group].unique()

    colors=px.colors.qualitative.Plotly


    start_time = time.time()
    fig_histogram = make_subplots(rows=1, cols=2,subplot_titles=(linear,bar))
    fig_box_plot = make_subplots(rows=1, cols=2,subplot_titles=(linear,bar))
    for a,i in enumerate(namee):
        dfs = dfa[dfa[group] == i]
        dfk = dfu[dfu[group] == i]
        i=str(i)
        fig_histogram.add_trace(go.Histogram(x=dfs['Value'],name=i,showlegend = False,legendgroup=i,marker_color=colors[a]), row=1, col=1)
        fig_histogram.add_trace(go.Histogram(x=dfk['Value'],name=i, legendgroup=i,marker_color=colors[a]), row=1, col=2)
        fig_box_plot.add_trace(go.Box(y=dfs['Value'],name=i,showlegend = False,legendgroup=i,marker_color=colors[a]), row=1, col=1)
        fig_box_plot.add_trace(go.Box(y=dfk['Value'],name=i, legendgroup=i,marker_color=colors[a]), row=1, col=2)

    # Overlay both histograms
    fig_histogram.update_layout(barmode='stack')
    fig_histogram.update_layout(  template='plotly_white')
    fig_box_plot.update_layout( template='plotly_white')

    #fig_box_plot = px.box(df, y="Value",color=group, facet_col="name")
    #fig_box_plot.layout.yaxis2.update(matches=None, showticklabels=True)

    end_time = time.time()
    times = end_time - start_time
    print('check first',times)



    df = df.pivot(index=[group,'date'], columns='name', values='Value').reset_index()

    fig = px.scatter(df, x=bar, y=linear, color=group, template='plotly_white')


    return fig_box_plot,fig_histogram,fig



def figure_linear_plot(df1,df2,gr,linear,bar):

    fig1 = px.scatter(df1, x="week", y="Value", color=gr, template='plotly_white').update_traces(mode='lines+markers')
    fig2 = px.scatter(df2, x="week", y="Value", color=gr, template='plotly_white').update_traces(
        mode='lines+markers')
    fig1.update_layout(
        title={
            'text': "{}".format(linear),
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig1.update_layout(
        title={
            'text': "{}".format(bar),
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return fig1,fig2

def figure_workout_plot(df,gr,bar2,df2):

    fig = px.box(df,x=gr, y="HR_average", template='plotly_white')
    fig.update_layout(
        title={
            'text': "Average Heart Rate during {}".format(bar2),
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig2 = px.scatter(df2, x="date", y="HR_average", color=gr, template='plotly_white').update_traces(mode='lines+markers')

    return fig,fig2