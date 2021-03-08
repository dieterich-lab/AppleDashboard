from plotly.subplots import make_subplots
import plotly.graph_objects as go


def figure_summary_update(input_value1, input_value2, group, patient, df):
    """
    This function update first figure which show data for full range
    
    :param input_value1: What data should be showed as a linear on plot 
    :param input_value2: What data should be showed as a barchart on plt
    :param group: information
    :param patient: which patient was chosen
    :param df: DataFrame containing all data
    :return: Plotly figure
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if len(patient) == 0:
        fig = {}
    else:
        df = df.loc[df["@sourceName"] == patient]

        if group == 'M':
            df1 = df.groupby(['month', 'name'])['@Value'].mean().reset_index()
            df2 = df.groupby(['month', 'name'])['@Value'].sum().reset_index()
            df1 = df1.loc[df1['name'] == input_value1]
            df2 = df2.loc[df2['name'] == input_value2]

            fig.add_trace(go.Bar(x=df2['month'], y=df2['@Value'], name='{}'.format(input_value2)), secondary_y=False)
            fig.add_trace(go.Scatter(x=df1['month'], y=df1['@Value'], name='{}'.format(input_value1)), secondary_y=True)

        elif group == 'W':
            df1 = df.groupby(['week', 'name'])['@Value'].mean().reset_index()
            df2 = df.groupby(['week', 'name'])['@Value'].sum().reset_index()
            df1 = df1.loc[df1['name'] == input_value1]
            df2 = df2.loc[df2['name'] == input_value2]

            fig.add_trace(go.Bar(x=df2['week'], y=df2['@Value'], name='{}'.format(input_value2)), secondary_y=False)
            fig.add_trace(go.Scatter(x=df1['week'], y=df1['@Value'], name='{}'.format(input_value1)), secondary_y=True)

        elif group == 'DOW':
            df1 = df.groupby(['DOW','DOW_number', 'name'])['@Value'].mean().reset_index()
            df2 = df.groupby(['DOW','DOW_number', 'name'])['@Value'].sum().reset_index()
            df1 = df1.loc[df1['name'] == input_value1]
            df2 = df2.loc[df2['name'] == input_value2]
            df1 = df1.sort_values(by=['DOW_number'])
            df2 = df2.sort_values(by=['DOW_number'])
            fig.add_trace(go.Bar(x=df2['DOW'], y=df2['@Value'], name='{}'.format(input_value2)), secondary_y=False)
            fig.add_trace(go.Scatter(x=df1['DOW'], y=df1['@Value'], name='{}'.format(input_value1)), secondary_y=True)
        else:

            df1 = df.groupby(['date', 'name'])['@Value'].mean().reset_index()
            df2 = df.groupby(['date', 'name'])['@Value'].sum().reset_index()
            df1 = df1.loc[df1['name'] == input_value1]
            df2 = df2.loc[df2['name'] == input_value2]

            fig.add_trace(go.Bar(x=df2['date'], y=df2['@Value'], name='{}'.format(input_value2)), secondary_y=False)
            fig.add_trace(go.Scatter(x=df1['date'], y=df1['@Value'], name='{}'.format(input_value1)), secondary_y=True)

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
        fig.update_yaxes(title_text='{}'.format(input_value1), secondary_y=True)
        fig.update_yaxes(title_text='{}'.format(input_value2), secondary_y=False)
    return fig
