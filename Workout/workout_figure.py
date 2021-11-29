import plotly.express as px
import numpy as np


def workout_figure(data, df):
    """ Update workout figure in Workout tab depending on drop downs"""
    fig = px.scatter(x=df['Date'], y=df['Value'], template="plotly_white")

    Start_Date = data['Start_Date'].values
    End_Date = data['End_Date'].values
    type = data['type'].values

    for i, j, k in zip(Start_Date, End_Date, type):
        fig.add_vline(x=str(i), line_width=3, line_dash="dash", line_color="green")
        fig.add_vline(x=str(j), line_width=3, line_dash="dash", line_color="red")
        fig.add_vrect(x0=str(i), x1=str(j), annotation_text=k, annotation_textangle=-90,
                      annotation_position="bottom left", annotation=dict(font_size=15, font_family="Times New Roman"),
                      fillcolor="green", opacity=0.25, line_width=0)
    fig.update_yaxes(title_text='Heart Rate')
    fig.update_xaxes(title_text='Time')

    return fig
