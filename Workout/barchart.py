from plotly.subplots import make_subplots
import plotly.graph_objects as go


def update_figure(df,group):

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if group == 'M':
        df = df.groupby(['month']).sum().reset_index()
        fig.add_trace(go.Bar(x=df['month'], y=df['duration']), secondary_y=True)
    elif group == 'W':
        df = df.groupby(['week']).sum().reset_index()
        fig.add_trace(go.Bar(x=df['week'], y=df['duration']), secondary_y=True)
    elif group == 'DOW':

        df = df.groupby(['DOW','DOW_number',]).sum().reset_index()
        fig.add_trace(go.Bar(x=df['DOW'], y=df['duration']), secondary_y=True)
    else:
        df = df.groupby(['date']).sum().reset_index()

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

    """
    df_HRR = pd.read_csv('workout')
    df_HRR = df_HRR[df_HRR['HRR'] > 0]

    fig5 = px.scatter(x=df_HRR['Start_Date'],y=df_HRR['HRR'])

    fig6 = px.scatter(x=df_HRR['Start_Date'],y=df_HRR['HR_max'])

    fig7 = px.scatter(x=df_HRR['Start_Date'],y=df_HRR['HR_min'])

    fig8 = px.scatter(x=df_HRR['Start_Date'], y=df_HRR['HR-RS_index'])
    """
    return fig