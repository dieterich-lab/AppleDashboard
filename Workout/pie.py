import plotly.express as px


def update_pie(df, group, what):
    """ Update pie figure in Workout tab depending on drop downs"""
    if group == 'M': index = 'month'
    elif group == 'W': index = 'week'
    elif group == 'DOW': index = 'DOW'
    else: index = 'date'

    df_activity = df.groupby(['type']).sum().reset_index()
    df = df.groupby([index]).sum().reset_index()
    df_activity['%'] = 100 * df_activity[what] / df[what].values[0]
    fig = px.pie(df_activity, values='%', names='type')

    return fig
