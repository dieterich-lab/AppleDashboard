from plotly.subplots import make_subplots
import plotly.graph_objects as go


def update_figure(df, bar,linear,  group):
    df_linear = df[df['name'] == bar].drop(columns=['sum'])
    df_bar = df[df['name'] == linear].drop(columns=['mean'])
    df_linear = df_linear.rename(columns={"mean": "Value"})
    df_bar = df_bar.rename(columns={"sum": "Value"})
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if group == 'M':

        fig.add_trace(go.Bar(x=df_bar['month'], y=df_bar['Value'], name='{}'.format(bar)), secondary_y=False)
        fig.add_trace(go.Scatter(x=df_linear['month'], y=df_linear['Value'], name='{}'.format(linear)), secondary_y=True)
    elif group == 'W':
        fig.add_trace(go.Bar(x=df_bar['week'], y=df_bar['Value'], name='{}'.format(bar)), secondary_y=False)
        fig.add_trace(go.Scatter(x=df_linear['week'], y=df_linear['Value'], name='{}'.format(linear)), secondary_y=True)
    elif group == 'DOW':
        fig.add_trace(go.Bar(x=df_bar['DOW'], y=df_bar['Value'], name='{}'.format(bar)), secondary_y=False)
        fig.add_trace(go.Scatter(x=df_linear['DOW'], y=df_linear['Value'], name='{}'.format(linear)), secondary_y=True)
    else:
        fig.add_trace(go.Bar(x=df_bar['date'], y=df_bar['Value'], name='{}'.format(bar)), secondary_y=False)
        fig.add_trace(go.Scatter(x=df_linear['date'], y=df_linear['Value'], name='{}'.format(linear)), secondary_y=True)
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
    fig.update_yaxes(title_text='{}'.format(linear), secondary_y=True)
    fig.update_yaxes(title_text='{}'.format(bar), secondary_y=False)
    return fig
