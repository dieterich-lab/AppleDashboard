import pandas as pd
import numpy as np

def table(df,group):



    if group == 'M':
        df = df.groupby(["@sourceName",'month', 'date', 'name'])['@Value'].sum().reset_index()
        df3 = df.groupby(["@sourceName",'month', 'name'])['@Value'].mean().reset_index()
        df2 = df.groupby(["@sourceName", 'month', 'name'])['@Value'].sum().reset_index()

    elif group == 'W':
        df = df.groupby(["@sourceName",'week', 'date', 'name'])['@Value'].sum().reset_index()
        df2 = df.groupby(["@sourceName", 'week', 'name'])['@Value'].sum().reset_index()
        df3 = df.groupby(["@sourceName",'week', 'name'])['@Value'].mean().reset_index()

    elif group == 'DOW':
        df = df.groupby(["@sourceName",'DOW', 'date', 'name'])['@Value'].sum().reset_index()
        df3 = df.groupby(["@sourceName",'DOW', 'name'])['@Value'].mean().reset_index()
        df2 = df.groupby(["@sourceName",'DOW', 'name'])['@Value'].sum().reset_index()

    else:
        df3 = df.groupby(["@sourceName",'date', 'name'])['@Value'].mean().reset_index()
        df2 = df.groupby(["@sourceName",'date', 'name'])['@Value'].sum().reset_index()

    #result = pd.merge(df1, df2, on=["@sourceName", 'month', 'name'])
    #result = pd.merge(result, df3, on=["@sourceName", 'month', 'name'])
    try:
        table = pd.pivot_table(df2,index=['date','@sourceName'],columns='name',values='@Value', aggfunc=np.sum).reset_index()
    except:
        table = pd.pivot_table(df2, index=['month', '@sourceName'], columns='name', values='@Value',
                               aggfunc=np.sum).reset_index()

    return table

