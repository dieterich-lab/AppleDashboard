from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
"""
def update_figure(df, group,bar):


    df = df[df['type'] == 'HKWorkoutActivityTypeCycling']

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if group == 'M':
        fig.add_trace(go.Scatter(x=df['month'], y=df['Value']), secondary_y=True)
    elif group == 'W':
        fig.add_trace(go.Scatter(x=df['week'], y=df['Value']), secondary_y=True)
    elif group == 'DOW':
        fig.add_trace(go.Scatter(x=df['DOW'], y=df['Value']), secondary_y=True)
    else:
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

    df['%'] = 100 * df['@totalEnergyBurned'] / df.groupby('month')['@totalEnergyBurned'].transform('sum')
    fig2 = px.pie(df, values='duration %', names='@workoutActivityType')

    return fig


workouts['date'] = workouts['@startDate'].map(get_date)
workouts['month'] = workouts['@startDate'].map(get_month)
Patient1 = workouts[workouts['@sourceName'] == 'Patient1 iPhone']
data1 = Patient1.loc[Patient1['date'] == '2020-05-17']


df = workouts.groupby(by=["@workoutActivityType", "@sourceName",'month']).sum()
df = Patient1.groupby(by=["@workoutActivityType", 'month']).sum().reset_index()


df_date = Patient1.groupby(by=["@workoutActivityType", 'date']).sum().reset_index()
df_date_walking = df_date[df_date["@workoutActivityType"] == 'HKWorkoutActivityTypeWalking']


df_date_running = df_date[df_date["@workoutActivityType"] == 'HKWorkoutActivityTypeRunning']
df_date_running['speed'] = df_date_running['@totalDistance']/df_date_running['@duration']

df_date_hiking = df_date[df_date["@workoutActivityType"] == 'HKWorkoutActivityTypeHiking']
df_date_hiking['speed'] = df_date_hiking['@totalDistance']/df_date_hiking['@duration']

df_date_cycling = df_date[df_date["@workoutActivityType"] == 'HKWorkoutActivityTypeCycling']
df_date_cycling['speed'] = df_date_cycling['@totalDistance']/df_date_cycling['@duration']
"""
"""
fig = px.bar(df_date_cycling, x='date', y='speed')
fig.show()

"""