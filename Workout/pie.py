import plotly.express as px


def update_pie(df,group,what):
    df = df[(df['duration'] > 10) & (df['duration'] < 300)]
    if group == 'M':
        df_activity = df.groupby(['type']).sum().reset_index()
        df = df.groupby(['month']).sum().reset_index()
        df_activity['%'] = 100 * df_activity[what] / df[what].values[0]

    elif group == 'W':
        df_activity = df.groupby(['type']).sum().reset_index()
        df = df.groupby(['week']).sum().reset_index()
        df_activity['%'] = 100 * df_activity[what] / df[what].values[0]

    elif group == 'DOW':
        df_activity = df.groupby(['DOW', 'DOW_number','type']).sum().reset_index()
        df = df.groupby(['DOW', 'DOW_number', ]).sum().reset_index()
        df_activity['%'] = 100 * df_activity[what] / df[what].values[0]
    else:
        df_activity = df.groupby(['type']).sum().reset_index()
        df = df.groupby(['date']).sum().reset_index()

        df_activity['%'] = 100 * df_activity[what] / df[what].values[0]
    fig2 = px.pie(df_activity, values='%', names='type')

    return fig2