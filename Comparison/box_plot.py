import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def figure_boxplot(df1,df2):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Box(x=df1["Name"], y=df1["Value"]), secondary_y=False)
    fig.add_trace(go.Box(x=df2["Name"], y=df2["Value"]), secondary_y=True)
    fig.update_layout(
        yaxis_title='normalized moisture',
        boxmode='group'  # group together boxes of the different traces for each value of x
    )
    #fig = px.box(df, x="Name", y="Value")
    return fig


def figure_histogram(df):
    fig = px.histogram(df, x="Value",color="Name")

    return fig

def figure_scatter_plot(df,group,linear,bar):

    if group == 'M': index = ['Name','month']
    elif group == 'W': index = ['Name','week']
    elif group == 'DOW': index = ['Name','DOW','DOW_number']
    else: index = ['Name','date']

    df = df.pivot(index=index, columns='name', values='Value') \
        .reset_index()

    fig = px.scatter(df, x=bar,y=linear,color="Name")

    return fig