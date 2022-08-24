import plotly.express as px


def workout_figure(data, df):
    """ Update workout figure in Workout tab depending on drop downs"""
    fig = px.scatter(x=df['date'], y=df['value'], template="plotly_white")

    start_date, end_date = list(map(str, data['start_date'].values)), list(map(str, data['end_date'].values))
    key = list(map(str, data['key'].values))

    for i, j, k in zip(start_date, end_date, key):
        fig.add_vline(x=i, line_width=3, line_dash="dash", line_color="green")
        fig.add_vline(x=j, line_width=3, line_dash="dash", line_color="red")
        fig.add_vrect(x0=i, x1=j, annotation_text=k, annotation_textangle=-90,
                      annotation_position="bottom left", annotation=dict(font_size=15, font_family="Times New Roman"),
                      fillcolor="green", opacity=0.25, line_width=0)
    fig.update_layout(title='Heart Rate before, during and after the workout')
    fig.update_yaxes(title_text='Heart Rate [bpm]')
    fig.update_xaxes(title_text='Time')

    return fig
