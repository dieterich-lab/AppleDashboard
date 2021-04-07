import pandas as pd
import numpy as np


def table(df, group,  linear,bar,):

    df_linear = df[df.name.isin([linear])].drop(columns=['sum'])
    df_bar = df[df.name.isin([bar])].drop(columns=['mean'])
    df_linear = df_linear.rename(columns={"mean": "Value"})
    df_bar = df_bar.rename(columns={"sum": "Value"})
    result = df_bar.append(df_linear)

    if group == 'M':
        table_summary = pd.pivot_table(result, index=['month'], columns='name', values='Value',
                                       aggfunc=np.sum).reset_index()
    elif group == 'W':
        table_summary = pd.pivot_table(result, index=['week'], columns='name', values='Value',
                                       aggfunc=np.sum).reset_index()
    elif group == 'DOW':
        table_summary = pd.pivot_table(result, index=['DOW'], columns='name', values='Value',
                                       aggfunc=np.sum).reset_index()
    else:
        result['date'] = pd.to_datetime(result['date']).dt.date
        table_summary = pd.pivot_table(result, index=['date'], columns='name', values='Value',
                                       aggfunc=np.sum).reset_index()

    return table_summary


def table2(df, patient):
    df = df.loc[df["Patient"] == patient]
    table_ecg = df.drop(["Patient"], axis=1)
    return table_ecg
