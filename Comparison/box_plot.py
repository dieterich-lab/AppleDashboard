import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def figure_boxplot(df1,df2,group,linear,bar):

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Box(x=df1[group], y=df1[linear],name="{}".format(linear)), secondary_y=False)
    fig.add_trace(go.Box(x=df2[group], y=df2["Value"],name="{}".format(bar)), secondary_y=True)
    fig.update_layout(
        yaxis_title='normalized moisture',
        boxmode='group'  # group together boxes of the different traces for each value of x
    )
    fig.update_yaxes(title_text='{}'.format("Value"), secondary_y=False)
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))
    #fig = px.box(df, x="Name", y="Value")
    return fig


def figure_histogram(df,group,linear):
    fig = px.histogram(df, x=linear,color=group)

    return fig


def figure_scatter_plot(df,gr,group,linear,bar):

    if group == 'M': index = ['Name', 'Age', 'Sex', 'month']
    elif group == 'W': index = ['Name', 'Age', 'Sex', 'week']
    elif group == 'DOW': index = ['Name', 'Age', 'Sex', 'DOW', 'DOW_number']
    else: index = ['Name', 'Age', 'Sex', 'date']

    df = df.pivot(index=index, columns='name', values='Value') \
        .reset_index()

    fig = px.scatter(df, x=bar, y=linear, color=gr)

    return fig


def figure_linear_plot(df,gr, group,linear):
    #if group == 'M': index = ['Name','month']
    #elif group == 'W': index = ['Name','week']
    #elif group == 'DOW': index = ['Name','DOW','DOW_number']
    #else: index = ['Name','date']

    #df = df.pivot(index=index, columns='name', values='Value') \
    #    .reset_index()

    fig = px.line(df, x="date", y="Value", color='Name')

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