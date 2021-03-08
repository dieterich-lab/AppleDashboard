import pandas as pd
import numpy as np


def table(df, patient, group, linear, bar):
    """

    :param df:
    :param patient:
    :param group:
    :param linear:
    :param bar:
    :return:
    """
    df['date'] = pd.to_datetime(df['date']).dt.date
    df = df.loc[df["@sourceName"] == patient]
    df_linear = df[df.name.isin([linear])]
    df_bar = df[df.name.isin([bar])]

    if group == 'M':
        df2 = df_bar.groupby(["@sourceName", 'month', 'name'])['@Value'].sum().reset_index()
        df3 = df_linear.groupby(["@sourceName", 'month', 'name'])['@Value'].mean().reset_index()
        result = df2.append(df3)
        table_summary = pd.pivot_table(result, index=['month'], columns='name', values='@Value',
                                       aggfunc=np.sum).reset_index()

    elif group == 'W':
        df2 = df_bar.groupby(["@sourceName", 'week', 'name'])['@Value'].sum().reset_index()
        df3 = df_linear.groupby(["@sourceName", 'week', 'name'])['@Value'].mean().reset_index()
        result = df2.append(df3)
        table_summary = pd.pivot_table(result, index=['week'], columns='name', values='@Value',
                                       aggfunc=np.sum).reset_index()

    elif group == 'DOW':
        df2 = df_bar.groupby(["@sourceName", 'DOW','DOW_number', 'name'])['@Value'].sum().reset_index()
        df3 = df_linear.groupby(["@sourceName", 'DOW','DOW_number', 'name'])['@Value'].mean().reset_index()
        result = df2.append(df3)
        result = result.sort_values(by=['DOW_number'])
        table_summary = pd.pivot_table(result, index=['DOW'], columns='name', values='@Value',
                                       aggfunc=np.sum).reset_index()

    else:
        df2 = df_bar.groupby(["@sourceName", 'date', 'name'])['@Value'].sum().reset_index()
        df3 = df_linear.groupby(["@sourceName", 'date', 'name'])['@Value'].mean().reset_index()
        result = df2.append(df3)
        table_summary = pd.pivot_table(result, index=['date'], columns='name', values='@Value',
                                       aggfunc=np.sum).reset_index()

    return table_summary


def table2(df, patient):
    df = df.loc[df["Patient"] == patient]
    table_ecg = df.drop(["Patient"], axis=1)
    return table_ecg
