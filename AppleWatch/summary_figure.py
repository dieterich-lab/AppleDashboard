from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np


def update_figure(df, linear, bar, index, labels):
    """ Update the "summary figure" in the Patient tab depending on drop downs """
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if bar in df.columns:
        fig.add_trace(go.Bar(x=df[index], y=df[bar], name=F'{bar}'), secondary_y=False)
    if linear and set(linear) <= set(df.columns):
        for i in linear:
            df_linear = df[[index, i]]
            df_linear = df_linear.replace('', np.nan).dropna(subset=[i])
            fig.add_trace(go.Scatter(x=df_linear[index], y=df_linear[i], name=F'{i}', mode='lines+markers'),
                          secondary_y=True)
    fig = update_figure_summary(bar, fig, index, labels)
    return fig


def update_figure_summary(bar, fig, index, labels):
    fig.update_layout(
        height=400,
        title=F'Apple Health data grouped by {index}',
        template='plotly_white',
        xaxis_title="Time",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
    fig.update_yaxes(title_text=F'{bar} [{labels[bar]}]', secondary_y=False)
    return fig
