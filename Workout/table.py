import pandas as pd
import numpy as np

def grouping1(df, patient, group):
    df = df.loc[df["Name"] == patient]
    if group == 'M':
        df = df.groupby(['month', 'name'])['Value'].agg(['sum', 'mean']).reset_index()
    elif group == 'W':
        df = df.groupby(['week', 'name'])['Value'].agg(['sum', 'mean']).reset_index()
    elif group == 'DOW':
        df = df.groupby(['DOW', 'DOW_number', 'name'])['Value'].agg(['sum', 'mean']).reset_index()
        df = df.sort_values(by=['DOW_number'])
    else:
        df = df.groupby(['date', 'name'])['Value'].agg(['sum', 'mean']).reset_index()
    return df


def grouping2(df, patient, group):
    df = df.loc[df["Name"] == patient]
    if group == 'M':
        df_sum = df.groupby(['month', 'date', 'name'])['Value'].sum().reset_index()
        df_sum_mean = df_sum.groupby(['month', 'name'])['Value'].mean().reset_index()

    elif group == 'W':
        df_sum = df.groupby(['week', 'date', 'name'])['Value'].sum().reset_index()
        df_sum_mean = df_sum.groupby(['week', 'name'])['Value'].mean().reset_index()

    elif group == 'DOW':
        df_sum = df.groupby(['DOW', 'DOW_number', 'date', 'name'])['Value'].sum().reset_index()
        df_sum_mean = df_sum.groupby(['DOW', 'DOW_number', 'name'])['Value'].mean().reset_index()

    return df_sum_mean


def table(df, group,  patient,bar,):
    df = df[['type','duration','distance','EnergyBurned','Start_Date','End_Date']]
    df =df.round(2)

    return df