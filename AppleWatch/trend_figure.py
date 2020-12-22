import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go




def figur_trend(date, date1, input_value, group,patient1,df):
    if len(patient1)==0:
        figa={}
    else:
        df = df.loc[df["@sourceName"] == patient1]
        df = df.loc[df['@type'] == 'HKQuantityTypeIdentifierHeartRate']
        if group == 'M':
            if int(date1) < 10:
                dateu='2020-0{}'.format(date1)
            else:
                dateu='2020-0{}'.format(date1)
            if dateu in df['month'].values:
                if int(date1) > 3:
                    if date1 < 10:
                        start_date,end_date ='2020-0{}'.format(int(date1) - 4), '2020-0{}'.format(int(date1) + 1)
                    else:
                        start_date, end_date = '2020-{}'.format(int(date1) - 4), '2020-{}'.format(int(date1) + 1)
                    df = df.loc[(df['month'] > start_date) & (df['month'] < end_date)]
                else:
                    start_date, end_date = '2020-0{}'.format(int(date1) + 12 - 4), '2020-0{}'.format(int(date1) + 1)
                    df = df.loc[(df['month'] > start_date) | (df['month'] < end_date)]
                df = df.groupby(['month', 'hour'])['@Value'].mean().reset_index()
                df['month'] = df['month'].astype(str)
                figa = px.line(x=df['hour'], y=df['@Value'], color=df['month'])
            else :
                figa={}

        elif group == 'W':
            if int(date1) in df['week'].values:
                if int(date1) > 3:
                    start_date, end_date = int(date1) - 4, int(date1) + 1
                    df = df.loc[(df['week'] > start_date) & (df['week'] < end_date)]
                else:
                    start_date, end_date = int(date1) + 53 - 4, int(date1) + 1
                    df = df.loc[(df['week'] > start_date) | (df['week'] < end_date)]
                df = df.groupby(['week', 'hour'])['@Value'].mean().reset_index()
                df['week'] = df['week'].astype(str)
                figa = px.line(x=df['hour'], y=df['@Value'], color=df['week'])
            else:
                figa={}

        elif group == 'DOW':
            if int(date1) in df['DOW'].values:
                if int(date1) > 3:
                    start_date, end_date = int(date1) - 4, int(date1) + 1
                    df = df.loc[(df['DOW'] > start_date) & (df['DOW'] < end_date)]
                else:
                    start_date, end_date = int(date1) + 7 - 4, int(date1) + 1
                    df = df.loc[(df['DOW'] > start_date) | (df['DOW'] < end_date)]

                df = df.groupby(['DOW', 'hour'])['@Value'].mean().reset_index()
                df['DOW'] = df['DOW'].astype(str)
                figa = px.line(x=df['hour'], y=df['@Value'], color=df['DOW'])
            else:
                figa={}

        else:
            if pd.to_datetime(date) in df['date'].values:
                start_date, end_date = (pd.to_datetime(date) - pd.to_timedelta(4, unit='d')), (pd.to_datetime(date) + pd.to_timedelta(1, unit='d'))
                df = df.loc[(df['date'] > start_date) & (df['date'] < end_date)]
                df = df.groupby(['date', 'hour'])['@Value'].mean().reset_index()
                df['date'] = df['date'].astype(str)
                figa = px.line(x=df['hour'], y=df['@Value'], color=df['date'])
            else:
                figa={}

    if figa:
        figa.update_layout(
            height=400,
            title='Trend from last 4 days',
            template='plotly_white',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ))
        figa.update_xaxes(title_text="hour")
        figa.update_yaxes(title_text='Heart Rate')
    else:
        figa = {
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

    return figa