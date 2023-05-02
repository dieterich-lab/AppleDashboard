import plotly.express as px


def figure_trend(df, group):
    """ Update the "trend figure" in the Patient tab depending on drop-downs """
    if group == 'M':
        color, trend = "month", "months"
    elif group == 'W':
        color, trend = "week", "weeks"
    elif group == "DOW":
        color, trend = "DOW", "days"
    else:
        color, trend = 'date', 'days'

    fig = px.line(x=df['hour'], y=df['Value'], color=df[color])
    fig.update_layout(
        height=400,
        title='Trend from last 4 {}'.format(trend),
        template='plotly_white',
        xaxis_title="Time [hr]",
        yaxis_title='Heart Rate',
        legend=dict(
            yanchor="bottom",
            y=0.9,
            xanchor="right",
            x=1))

    return fig
