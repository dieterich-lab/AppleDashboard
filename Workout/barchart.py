from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import datetime

def update_figure(df,patient, group,bar, date, df2):
    print(group)
    df2 = df2.loc[(df2['Name'] == patient) & (df2['date'] == date)]
    df_new = df.loc[(df['Name'] == patient) & (df['date'] == date)]
    df = df.loc[df['Name'] == patient]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if group == 'M':
        df_activity = df.groupby(['month','type']).sum().reset_index()
        df = df.groupby(['month']).sum().reset_index()
        df_activity['%'] = 100 * df_activity[df_activity['month'] == '2020-03']['duration'] / \
                           df[df['month'] == '2020-03']['duration'].values[0]
        fig2 = px.pie(df_activity, names='type')
        fig.add_trace(go.Bar(x=df['month'], y=df['duration']), secondary_y=True)
    elif group == 'W':
        df_activity = df.groupby(['week', 'type']).sum().reset_index()
        df = df.groupby(['week']).sum().reset_index()
        df_activity['%'] = 100 * df_activity[df_activity['week'] == '2020/14']['duration'] / \
                           df[df['week'] == '2020/14']['duration'].values[0]
        fig2 = px.pie(df_activity, names='type')
        fig.add_trace(go.Bar(x=df['week'], y=df['duration']), secondary_y=True)
    elif group == 'DOW':
        df_activity = df.groupby(['DOW', 'DOW_number','type']).sum().reset_index()
        df = df.groupby(['DOW','DOW_number',]).sum().reset_index()
        print(df)
        df_activity['%'] = 100 * df_activity[df_activity['DOW_number'] == 6]['duration'] / \
                           df[df['DOW_number'] == 6]['duration'].values[0]
        fig2 = px.pie(df_activity, names='type')
        fig.add_trace(go.Bar(x=df['DOW'], y=df['duration']), secondary_y=True)
    else:
        df_activity = df.groupby(['date', 'type']).sum().reset_index()
        df_activity['%'] = 100 * df_activity[df_activity['date'] == date]['duration'] / \
                           df[df['date'] == date]['duration'].values[0]
        df = df.groupby(['date']).sum().reset_index()
        print(df_activity[df_activity['date'] == date])
        fig2 = px.pie(df_activity[df_activity['date'] == date], names='type')
        fig.add_trace(go.Bar(x=df['date'],  y=df['duration']), secondary_y=True),
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




    fig3 =px.scatter(x=df2['Date'],y=df2['Value'])

    x=str(df_new['Start_Date'].values[0])
    x2 = str(df_new['End_Date'].values[0])
    x3= df_new['End_Date'].values[0] + np.timedelta64(3,'m')
    x1 = str(df_new['End_Date'].values[0] + np.timedelta64(1, 'm'))
    x3 = str(x3)
    fig3.add_vline(x=x, line_width=3, line_dash="dash", line_color="green")
    fig3.add_vline(x=x2, line_width=3, line_dash="dash", line_color="green")
    fig3.add_vline(x=x3, line_width=3, line_dash="dash", line_color="green")

    df_new_new = df2[(df2['Date'] > x2) & (df2['Date'] < x3)]
    fig4 = px.scatter(x=df_new_new['Date'],y=df_new_new['Value'])
    #fig4.add_vline(x=x2, line_width=3, line_dash="dash", line_color="green")

    df_HRR = pd.read_csv('workout')
    df_HRR = df_HRR[df_HRR['HRR'] > 0]

    fig5 = px.scatter(x=df_HRR['Start_Date'],y=df_HRR['HRR'])

    fig6 = px.scatter(x=df_HRR['Start_Date'],y=df_HRR['HR_max'])

    fig7 = px.scatter(x=df_HRR['Start_Date'],y=df_HRR['HR_min'])

    fig8 = px.scatter(x=df_HRR['Start_Date'], y=df_HRR['HR-RS_index'])

    return fig, fig2, fig3, fig4, fig5, fig6, fig7, fig8