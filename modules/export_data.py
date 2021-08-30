import pandas as pd
import xmltodict
import pytz
from os import listdir
from os.path import isfile, join
import numpy as np


def export_me_data_from_apple_watch(file):
    # export data from xml file
    input_path = './import/{}'.format(file)

    with open(input_path, 'r', errors='ignore') as xml_file:
        input_data = xmltodict.parse(xml_file.read())

    # import health data
    records_list = input_data['HealthData']['Record']
    df = pd.DataFrame(records_list)

    n = int(''.join(filter(str.isdigit, file)))

    # rename @sourceName
    df = df[df['@sourceName'].str.contains("Watch")]
    df['@sourceName'] = df['@sourceName'].apply(lambda x: 'Patient {}'.format(n))

    # Remove not necessary data
    df = df.drop(['@sourceVersion', '@device', 'MetadataEntry', 'HeartRateVariabilityMetadataList', '@endDate',
                  '@creationDate'], axis=1)

    # convert time to you time zone
    df['@startDate'] = pd.to_datetime(df['@startDate']).map(
        lambda x: x.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT+1')))
    xml_file.close()

    return df


def calculate_HRR(df_HR, df_workout):
    # HRR

    df_HR = df_HR.loc[df_HR['@type'] == 'HKQuantityTypeIdentifierHeartRate']
    result_1_min = []
    result_2_min = []
    result_max = []
    result_min = []
    HR_average = []
    df_HR['@value'] = pd.to_numeric(df_HR['@value'])
    df_workout['@totalDistance'],df_workout['@duration'] = pd.to_numeric(df_workout['@totalDistance']),pd.to_numeric(df_workout['@duration'])
    for i in range(len(df_workout)):
        start_workout = str(df_workout.iloc[i]['@startDate'])
        end_workout = str(df_workout.iloc[i]['@endDate'])
        after_workout_1_m = str(df_workout.iloc[i]['@endDate']+ np.timedelta64(1, 'm'))
        after_workout_2_m = str(df_workout.iloc[i]['@endDate'] + np.timedelta64(2, 'm'))
        df_HRR = df_HR[(df_HR['@startDate'] > start_workout) & (df_HR['@startDate'] < end_workout)]
        df_HRR_1_min = df_HR[(df_HR['@startDate'] > end_workout) & (df_HR['@startDate'] < after_workout_1_m)]
        df_HRR_2_min = df_HR[(df_HR['@startDate'] > end_workout) & (df_HR['@startDate'] < after_workout_2_m)]
        try:
            HRR_1_min = df_HRR_1_min['@value'].values[0] - df_HRR_1_min['@value'].values[-1]
            HRR_2_min = df_HRR_2_min['@value'].values[0] - df_HRR_2_min['@value'].values[-1]
            average = df_HRR['@value'].mean()
            max_value = df_HRR['@value'].max()
            min_value = df_HRR['@value'].min()
            result_1_min.append(HRR_1_min)
            result_2_min.append(HRR_2_min)
            result_max.append(max_value)
            result_min.append(min_value)
            HR_average.append(average)
        except:
            result_1_min.append(0)
            result_2_min.append(0)
            result_max.append(0)
            result_min.append(0)
            HR_average.append(0)

    df = pd.DataFrame(
        {'HRR_1_min': result_1_min,
         'HRR_2_min': result_2_min,
         'HR_max': result_max,
         'HR_min': result_min,
         'HR_average': HR_average,
         'speed': df_workout['@totalDistance'] / df_workout['@duration'],
         })
    df['HR-RS_index'] = df['HR_average'] / df['speed']
    df_workout = pd.concat([df_workout, df], axis=1)

    return df_workout


def export_health_data_from_apple_watch(file):

    # export data from xml file
    input_path = './import/{}'.format(file)

    with open(input_path, 'r', errors='ignore') as xml_file:
        input_data = xmltodict.parse(xml_file.read())

    # import health data
    records_list = input_data['HealthData']['Record']
    df = pd.DataFrame(records_list)

    n = int(''.join(filter(str.isdigit, file)))

    # rename @sourceName
    df = df[df['@sourceName'].str.contains("Watch")]
    df['@sourceName'] = df['@sourceName'].apply(lambda x: 'Patient {}'.format(n))

    # Remove not necessary data
    df = df.drop(['@sourceVersion', '@device', 'MetadataEntry', 'HeartRateVariabilityMetadataList', '@endDate',
                      '@creationDate'],axis=1)

    # convert time to you time zone
    df['@startDate'] = pd.to_datetime(df['@startDate']).map(
        lambda x: x.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT+1')))
    xml_file.close()

    return df


def export_workout_data_from_apple_watch(file):

    # export data from xml file
    input_path = './import/{}'.format(file)

    with open(input_path, 'r') as xml_file:
        input_data = xmltodict.parse(xml_file.read())

    # import health data
    workouts_list = input_data['HealthData']['Workout']
    df = pd.DataFrame(workouts_list)

    n = int(''.join(filter(str.isdigit, file)))

    # rename @sourceName
    df = df[df['@sourceName'].str.contains("Watch")]
    df['@sourceName'] = df['@sourceName'].apply(lambda x: 'Patient {}'.format(n))
    # Remove not necessary data
    df = df.drop(['@sourceVersion', '@device', 'WorkoutRoute', 'WorkoutEvent', 'MetadataEntry','@creationDate'], axis=1)
    df['@workoutActivityType'] = df['@workoutActivityType'].str.replace('HKWorkoutActivityType','')
    # convert time to you time zone
    df['@startDate'] = pd.to_datetime(df['@startDate']).map(
        lambda x: x.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT+1')))
    df['@endDate'] = pd.to_datetime(df['@endDate']).map(
        lambda x: x.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT+1')))


    xml_file.close()

    return df


def export_ecg_data_from_apple_watch(directories):

    df = pd.DataFrame(columns=['patient', 'Date', 'Day', 'number', 'Classification', 'data'])
    # Loading ECG data to database
    for i in directories:
        # export all ecg.csv files
        only_files = [f for f in listdir('./import/{}/'.format(i)) if isfile(join('./import/{}/'.format(i), f))]

        n = int(''.join(filter(str.isdigit, i)))
        patient = 'Patient {}'.format(n)

        for ecg_file in only_files:
            path = './import/{0}/{1}'.format(i, ecg_file)

            ecg = pd.read_csv(path, error_bad_lines=False, warn_bad_lines=False)
            ecg.reset_index(level=0, inplace=True)

            data = pd.to_numeric(ecg['index'][8:]).to_list()
            ecg_file = ecg_file.replace('ecg_', '').replace('.csv', '')
            if '_' not in ecg_file:
                ecg_file = ecg_file + '_0'
            date = ecg['Name'][1]
            classification = ecg['Name'][2]

            day, number = ecg_file[:10], ecg_file[-1]

            df = df.append({'patient': patient, 'Date': date, 'Day': day, 'number': number,
                            'Classification': classification, 'data': data}, ignore_index=True)

    return df
