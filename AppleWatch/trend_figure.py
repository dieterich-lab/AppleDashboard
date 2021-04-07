import pandas as pd
import plotly.express as px
import dateutil.relativedelta
import datetime

days_of_week = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}
def figure_trend(date, date1, input_value, group, patient, df):
    if len(patient) == 0:
        fig = {}
    else:
        df = df.loc[df["Name"] == patient]
        df = df.loc[df['type'] == 'HKQuantityTypeIdentifierHeartRate']
        if group == 'M':
            trend = 'months'
            if date1 in df['month'].values:
                start_date,end_date = pd.to_datetime(date1) - dateutil.relativedelta.relativedelta(months=4),pd.to_datetime(date1)+ dateutil.relativedelta.relativedelta(months=1)
                if len(str(end_date.month)) == 1:
                    start_date = str(start_date.year)+'-0'+str(start_date.month)
                    end_date = str(end_date.year)+'-0'+ str(end_date.month)
                else:
                    start_date = str(start_date.year)+'-'+str(start_date.month)
                    end_date = str(end_date.year)+'-'+ str(end_date.month)
                df = df.loc[(df['month'] > start_date) & (df['month'] < end_date)]
                df = df.groupby(['month', 'hour'])['Value'].mean().reset_index()
                fig = px.line(x=df['hour'], y=df['Value'], color=df['month'])
            else :
                fig={}

        elif group == 'W':
            trend = 'weeks'

            if date1 in df['week'].values:
                date1 = date1[-2:]
                if int(date1) > 3:
                    start_date, end_date = int(date1) - 4, int(date1) + 1
                    df = df.loc[(df['week_num'] > start_date) & (df['week_num'] < end_date)]
                else:
                    start_date, end_date = int(date1) + 53 - 4, int(date1) + 1
                    df = df.loc[(df['week_num'] > start_date) | (df['week_num'] < end_date)]
                df = df.groupby(['week_num','week', 'hour'])['Value'].mean().reset_index()
                fig = px.line(x=df['hour'], y=df['Value'], color=df['week'])
            else:
                fig={}

        elif group == 'DOW':
            trend ='days'
            df = df.groupby(['DOW','DOW_number', 'hour'])['Value'].mean().reset_index()

            if days_of_week[date1] in df['DOW_number'].values:
                if int(days_of_week[date1]) > 3:
                    start_date, end_date = int(days_of_week[date1]) - 4, int(days_of_week[date1]) + 1
                    df = df.loc[(df['DOW_number'] > start_date) & (df['DOW_number'] < end_date)]
                else:
                    start_date, end_date = int(days_of_week[date1]) + 7 - 4, int(days_of_week[date1]) + 1
                    df = df.loc[(df['DOW_number'] > start_date) | (df['DOW_number'] < end_date)]

                fig = px.line(x=df['hour'], y=df['Value'], color=df['DOW'])
            else:
                fig = {}

        else:
            trend = 'days'
            if pd.to_datetime(date) in df['date'].values:
                start_date, end_date = (pd.to_datetime(date) - pd.to_timedelta(4, unit='d')), (pd.to_datetime(date) + pd.to_timedelta(1, unit='d'))
                df = df.loc[(df['date'] > start_date) & (df['date'] < end_date)]
                df = df.groupby(['date', 'hour'])['Value'].mean().reset_index()
                df['date'] = df['date'].astype(str)
                fig = px.line(x=df['hour'], y=df['Value'], color=df['date'])
            else:
                fig = {}

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
