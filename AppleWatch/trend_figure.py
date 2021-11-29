import pandas as pd
import plotly.express as px
from datetime import date
import datetime
from dateutil.relativedelta import relativedelta
import modules.load_data_from_database as ldd
from db import connect_db

# connection with database
rdb = connect_db()


def figure_trend(date_, value, group, patient):
    """ Update the "trend figure" in the Patient tab depending on drop downs """

    if group == 'M':
        color, trend = "month", "months"
        new_value = datetime.datetime.strptime(value + '-01', "%Y-%m-%d")
        start_date, end_date = new_value - relativedelta(months=3), new_value + relativedelta(months=1)
    elif group == 'W':
        color, trend = "week", "weeks"
        new_value = datetime.datetime.strptime(value + '/1', "%G/%V/%w")
        start_date, end_date = new_value - datetime.timedelta(weeks=3), new_value + datetime.timedelta(weeks=1)
    elif group == "DOW":
        color, trend = "DOW", "days"
        start_date, end_date = '1900-01-01', date.today()
    else:
        color, trend = 'date', 'days'
        start_date, end_date = (pd.to_datetime(date_) - pd.to_timedelta(3, unit='d')), \
                               (pd.to_datetime(date_) + pd.to_timedelta(1, unit='d'))

    df = ldd.trend_figure(rdb, patient, group, start_date, end_date)
    if df.empty:
        fig = {}
    else:
        fig = px.line(x=df['hour'], y=df['Value'], color=df[color])
        fig.update_layout(
            height=400,
            title='Trend from last 4 {}'.format(trend),
            template='plotly_white',
            xaxis_title="Hour",
            yaxis_title='Heart Rate',
            legend=dict(
                    yanchor="bottom",
                    y=0.9,
                    xanchor="right",
                    x=1))

    return fig
