import plotly.express as px


def update_pie(df, group, what, value):
    """ Update pie figure in Workout tab depending on drop downs"""
    df_activity = df.groupby(['key']).sum().reset_index()
    df = df.groupby([group]).sum().reset_index()
    df_activity['%'] = 100 * df_activity[what] / df[what].values[0]
    fig = px.pie(df_activity, values='%', names='key')
    fig.update_layout(title=F'Types of workout {value}')
    return fig
