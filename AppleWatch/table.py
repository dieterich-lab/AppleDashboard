import pandas as pd
import numpy as np


def table(df, patient, group, linear, bar):


    df['date'] = pd.to_datetime(df['date']).dt.date
    df = df.loc[df["@sourceName"] == patient]
    df_linear = df[df.name.isin([linear])]
    df_bar = df[df.name.isin([bar])]

    if group == 'M':
        df2 = df_bar.groupby(["@sourceName", 'month', 'name'])['@Value'].sum().reset_index()
        df3 = df_linear.groupby(["@sourceName", 'month', 'name'])['@Value'].mean().reset_index()
        #df = df.groupby(["@sourceName", 'month', 'date', '@type'])['@Value'].sum().reset_index()
        #df3 = df.groupby(["@sourceName", 'month', '@type'])['@Value'].mean().reset_index()

        result = df2.append(df3)
        table = pd.pivot_table(result, index=['month'], columns='name', values='@Value',
                               aggfunc=np.sum).reset_index()

    elif group == 'W':
        df2 = df_bar.groupby(["@sourceName", 'week', 'name'])['@Value'].sum().reset_index()
        df3 = df_linear.groupby(["@sourceName", 'week', 'name'])['@Value'].mean().reset_index()
        #df = df.groupby(["@sourceName", 'month', 'date', '@type'])['@Value'].sum().reset_index()
        #df3 = df.groupby(["@sourceName", 'month', '@type'])['@Value'].mean().reset_index()

        result = df2.append(df3)
        table = pd.pivot_table(result, index=['week'], columns='name', values='@Value',
                               aggfunc=np.sum).reset_index()

    elif group == 'DOW':
        df2 = df_bar.groupby(["@sourceName", 'DOW', 'name'])['@Value'].sum().reset_index()
        df3 = df_linear.groupby(["@sourceName", 'DOW', 'name'])['@Value'].mean().reset_index()
        #df = df.groupby(["@sourceName", 'month', 'date', '@type'])['@Value'].sum().reset_index()
        #df3 = df.groupby(["@sourceName", 'month', '@type'])['@Value'].mean().reset_index()
        result = df2.append(df3)
        table = pd.pivot_table(result, index=['DOW'], columns='name', values='@Value',
                               aggfunc=np.sum).reset_index()

    else:
        df2 = df_bar.groupby(["@sourceName", 'date', 'name'])['@Value'].sum().reset_index()
        df3 = df_linear.groupby(["@sourceName", 'date', 'name'])['@Value'].mean().reset_index()
        #df = df.groupby(["@sourceName", 'month', 'date', '@type'])['@Value'].sum().reset_index()
        #df3 = df.groupby(["@sourceName", 'month', '@type'])['@Value'].mean().reset_index()
        result = df2.append(df3)
        table = pd.pivot_table(result,index=['date'],columns='name',values='@Value', aggfunc=np.sum).reset_index()

    return table

