import plotly.express as px
import numpy as np


def workout_figure(df,data):

    fig = px.scatter(x=df['Date'], y=df['Value'])


    Start_Date = data['Start_Date'].values
    End_Date = data['End_Date'].values
    Recovery_heart_rate = data['End_Date'].values + np.timedelta64(1, 'm')


    for i in Start_Date:
        fig.add_vline(x=str(i), line_width=3, line_dash="dash", line_color="green")
    for i in End_Date:
        fig.add_vline(x=str(i), line_width=3, line_dash="dash", line_color="red")

    df_new = df[(df['Date'] > str(Start_Date[0])) & (df['Date'] < str(Recovery_heart_rate[0]))]
    fig2 = px.scatter(x=df_new['Date'],y=df_new['Value'])
    fig2.add_vline(x=str(End_Date[0]), line_width=3, line_dash="dash", line_color="green")

    return fig,fig2