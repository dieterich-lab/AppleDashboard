
import numpy as np
def calculate_HRR():
    # HRR

    df = df.loc[df['Name'] == 'Patient 1']
    df2 = df2.loc[(df2['Name'] == 'Patient 1') & (df2['type'] ==  'HKQuantityTypeIdentifierHeartRate' )]
    result = []
    result_max = []
    result_min = []
    HR_average = []
    for i in range(len(df)):
        end_workout = str(df.iloc[i]['End_Date'])
        after_workout_1_m = str(df.iloc[i]['End_Date']+ np.timedelta64(1, 'm'))
        df_HRR = df2[(df2['Date'] > end_workout) & (df2['Date'] < after_workout_1_m)]
        try:
            a = df_HRR['Value'].values[0] - df_HRR['Value'].values[-1]
            average = df_HRR['Value'].mean()
            max_value = df_HRR['Value'].max()
            min_value = df_HRR['Value'].min()
            result.append(a)
            result_max.append(max_value)
            result_min.append(min_value)
            HR_average.append(average)
        except:
            result.append(0)
            result_max.append(0)
            result_min.append(0)
            HR_average.append(0)
    df['HRR'] = result
    df['HR_max'] = result_max
    df['HR_min'] = result_min
    df['HR_average'] = HR_average
    df['speed'] = df['distance'] / df['duration']
    df['HR-RS_index'] = df['HR_average'] / df['speed']
    df.to_csv('workout')
    fig = {}

    ## Speed



    return fig

