import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go




def figur3(date,patient1,df):
    if len(patient1)==0:
        fig3={}
    else:
        df = df.loc[df["@sourceName"] == patient1]
        HeartRate = df.loc[df['@type'] == 'HKQuantityTypeIdentifierHeartRate']
        ActCal = df.loc[df['@type'] == 'HKQuantityTypeIdentifierActiveEnergyBurned']

        if pd.to_datetime(date) in df['date'].values:


            HeartRate1 = HeartRate.loc[HeartRate['date'] == date]

            ActCal1 = ActCal.loc[ActCal['date'] == date]

            if not ActCal1.empty:
                ActCal1 = ActCal1.resample('5Min', on='@creationDate').sum().reset_index()

                fig3 = make_subplots(specs=[[{"secondary_y": True}]])

                fig3.add_trace(go.Scatter(x=HeartRate1['@creationDate'], y=HeartRate1['@Value'], name="Heart Rate"), secondary_y=False)
                fig3.add_trace(go.Bar(x=ActCal1['@creationDate'], y=ActCal1['@Value'], name="Active Calories"), secondary_y=True)

                fig3.update_layout(
                    height=400,
                    template='plotly_white',
                    legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ))
                fig3.update_xaxes(title_text="Time")
            else:

                fig3 = {}
        else:
            fig3={}
    return fig3