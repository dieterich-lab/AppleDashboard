import modules.load_data_from_database as ldd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def figur2(input_value1,input_value2,group,patient1,df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if len(patient1)==0:
        fig={}
    else:
        df = df.loc[df["@sourceName"] == patient1]

        if group == 'M':
            df1 = df.groupby(['month','name'])['@Value'].mean().reset_index()
            df2 = df.groupby(['month','name'])['@Value'].sum().reset_index()
            df1 = df1.loc[df1['name'] == input_value1]
            df2 = df2.loc[df2['name'] == input_value2]

            fig.add_trace(go.Bar(x=df2['month'], y=df2['@Value'], name="Active Calories"), secondary_y=False)
            fig.add_trace(go.Scatter(x=df1['month'], y=df1['@Value'], name="Heart Rate"), secondary_y=True)

        elif group == 'W':

            df1 = df.groupby(['week','name'])['@Value'].mean().reset_index()
            df2 = df.groupby(['week','name'])['@Value'].sum().reset_index()
            df1 = df1.loc[df1['name'] == input_value1]
            df2 = df2.loc[df2['name'] == input_value2]

            fig.add_trace(go.Bar(x=df2['week'], y=df2['@Value'], name="Active Calories"), secondary_y=False)
            fig.add_trace(go.Scatter(x=df1['week'], y=df1['@Value'], name="Heart Rate"), secondary_y=True)

        elif group == 'DOW':

            df1 = df.groupby(['DOW','name'])['@Value'].mean().reset_index()
            df2 = df.groupby(['DOW','name'])['@Value'].sum().reset_index()
            df1 = df1.loc[df1['name'] == input_value1]
            df2 = df2.loc[df2['name'] == input_value2]

            fig.add_trace(go.Bar(x=df2['DOW'], y=df2['@Value'], name="Active Calories"), secondary_y=False)
            fig.add_trace(go.Scatter(x=df1['DOW'], y=df1['@Value'], name="Heart Rate"), secondary_y=True)
        else:

            df1 = df.groupby(['date','name'])['@Value'].mean().reset_index()
            df2 = df.groupby(['date','name'])['@Value'].sum().reset_index()
            df1 = df1.loc[df1['name'] == input_value1]
            df2 = df2.loc[df2['name'] == input_value2]

            fig.add_trace(go.Bar(x=df2['date'], y=df2['@Value'], name="Active Calories"), secondary_y=False)
            fig.add_trace(go.Scatter(x=df1['date'], y=df1['@Value'], name="Heart Rate"), secondary_y=True)

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
        fig.update_yaxes(title_text='{}'.format(input_value1), secondary_y=True)
        fig.update_yaxes(title_text='{}'.format(input_value2), secondary_y=False)

    return fig