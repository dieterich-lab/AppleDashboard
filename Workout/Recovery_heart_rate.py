from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px


def graphs(df):

    df = df[(df['duration'] > 10) & (df['duration'] < 300)]
    fig1 = px.scatter(df, x="speed", y="HRR_1_min", template="plotly_white")
    fig2 = px.scatter(df, x="speed", y="HR_min", template="plotly_white")
    fig3 = px.scatter(df, x="Start_Date", y="HR_max", template="plotly_white",color="speed")
    fig4 = px.scatter(df, x="speed", y="HR_average", template="plotly_white")

    return fig1, fig2, fig3, fig4