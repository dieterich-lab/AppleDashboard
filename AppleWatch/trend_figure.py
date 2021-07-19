import pandas as pd
import plotly.express as px
import dateutil.relativedelta
import datetime
from dateutil.relativedelta import relativedelta
import modules.load_data_from_database as ldd
from db import connect_db

# connection with database
rdb = connect_db()

days_of_week = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}


def figure_trend(date, value, input_value,group, patient):

    if group == 'M':
        color, trend = "month", "months"
        new_value = datetime.datetime.strptime(value + '-01', "%Y-%m-%d")
        start_date,end_date = new_value - relativedelta(months=3),new_value + relativedelta(months=1)
    elif group == 'W':
        color, trend = "week", "weeks"
        new_value = datetime.datetime.strptime(value + '/1', "%G/%V/%w")
        start_date, end_date = new_value - datetime.timedelta(weeks=3),new_value + datetime.timedelta(weeks=1)
    elif group == "DOW":
        color, trend = "DOW","days"
        new_value = days_of_week[value]
        start_date, end_date = new_value - 4,new_value+1
    else:
        color,trend = 'date','days'
        start_date, end_date = (pd.to_datetime(date) - pd.to_timedelta(3, unit='d')), \
                               (pd.to_datetime(date) + pd.to_timedelta(1, unit='d'))
    df = ldd.trend_figure(rdb, patient, group, start_date,end_date)
    if df.empty:
        fig = {}
    else:
        fig = px.line(x=df['hour'], y=df['Value'], color=df[color])


    if fig:
        fig.update_layout(
            height=400,
            title='Trend from last 4 {}'.format(trend),
            template='plotly_white',
            legend=dict(
                yanchor="bottom",
                y=0.9,
                xanchor="right",
                x=1
            ))
        fig.update_xaxes(title_text="Hour")
        fig.update_yaxes(title_text='Heart Rate')
    else:
        fig = {
            "layout": {
            "xaxis": {"visible": 'false'},
            "yaxis": {"visible": 'false'},
            "annotations": [
            {
                "text": "No matching data found",
                "xref": "paper",
                "yref": "paper",
                "showarrow": 'false',
                "font": {"size": 28}
            }
                            ]
                    }
            }
    return fig
