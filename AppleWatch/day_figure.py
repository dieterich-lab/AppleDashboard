import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def day_figure_update(date, value, group, patient, bar_value, df):
    """

    :param date:
    :param value:
    :param group:
    :param patient:
    :param bar_value:
    :param df:
    :return:
    """

    if len(patient) == 0:
        fig = {}
    else:
        df = df.loc[df["@sourceName"] == patient]
        if group == 'M':
            value = value[-1]

            df = df.loc[df['month'] == value]
        elif group == 'W':
            value = value[-1]
            df = df.loc[df['week'] == value]
        elif group == 'DOW':
            value = value[-1]
            days_of_week = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6,
                            "Sunday": 7}
            df = df.loc[df['DOW_number'] == days_of_week[value]]

            max_value = df['date'].max()
            df = df.loc[df['date'] == max_value]
        else:
            date = pd.to_datetime(date[-1])
            if pd.to_datetime(date) in df['date'].values:
                df = df.loc[df['date'] == date]
            else:
                df = pd.DataFrame(columns = ['@type', 'name'])

        df1 = df.loc[df['@type'] == 'HKQuantityTypeIdentifierHeartRate']
        df2 = df.loc[df['name'] == bar_value]

        if not df2.empty:
            df2 = df2.resample('5Min', on='@startDate').sum().reset_index()
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=df1['@startDate'], y=df1['@Value'], name="Heart Rate"),secondary_y=False)
            fig.add_trace(go.Bar(x=df2['@startDate'], y=df2['@Value'], name='{}'.format(bar_value)),secondary_y=True)
            fig.update_layout(
                height=400,
                template='plotly_white',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ))
            fig.update_xaxes(title_text="Time")
            fig.update_yaxes(title_text='{}'.format(bar_value), secondary_y=False)
        else:
            fig = {}

    return fig
