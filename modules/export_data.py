import pandas as pd
from datetime import date, datetime
import pytz
import re
from os import listdir
from os.path import isfile, join
import numpy as np
from ecgdetectors import Detectors
from modules.HRV_frequency_domain_analyze import frequencydomain
from modules.HRV_time_domain_analyze import time_domain_analyze
from dateutil.relativedelta import relativedelta


def basic_information(input_data, n):
    """
    If user provided basic information about himself such as: age,gender, blood group, skin type.
    This function extract this information from Apple Watch.

    """

    # get patient ID(number)
    patient = 'Patient {}'.format(n)

    # extract basic information
    records_list = [input_data['HealthData']['Me']]
    df = pd.DataFrame(records_list)

    sex = df['@HKCharacteristicTypeIdentifierBiologicalSex'][0]
    blood_group = df['@HKCharacteristicTypeIdentifierBloodType'][0]
    skin_type = df['@HKCharacteristicTypeIdentifierFitzpatrickSkinType'][0]
    birth = df['@HKCharacteristicTypeIdentifierDateOfBirth'][0]

    # Remove not necessary prefix
    sex = sex.replace('HKBiologicalSex', '')
    blood_group = blood_group.replace('HKBloodType', '')
    skin_type = skin_type.replace('HKFitzpatrickSkinType', '')

    # calculate age
    today = date.today()
    birth = datetime.fromisoformat(birth)
    time_difference = relativedelta(today, birth)
    age = time_difference.years

    data = [patient, n, age, sex, blood_group, skin_type]

    return data


def export_health_data_from_apple_watch(input_data, n):
    """
    This function extract health data from Apple Watch.

    Example of health data:
    HKQuantityTypeIdentifierActiveEnergyBurned
    HKQuantityTypeIdentifierAppleExerciseTime
    HKQuantityTypeIdentifierBasalEnergyBurned

    """

    # import health data
    records_list = input_data['HealthData']['Record']
    df = pd.DataFrame(records_list)

    # Remove not necessary data
    df = df.drop(['@sourceVersion', '@device', 'MetadataEntry', 'HeartRateVariabilityMetadataList', '@endDate',
                  '@creationDate'], axis=1)

    df = df[df['@sourceName'].str.contains("Watch")]  # DataFrame contain data only from Apple Watch
    df2 = df[~df['@sourceName'].str.contains("Watch")]  # DataFrame contain data only from Apple Watch

    # rename @sourceName
    df['@sourceName'] = df['@sourceName'].apply(lambda x: 'Patient {}'.format(n))

    # add a patient column for DataFrame with sources other than Apple Watch
    df2['Patient'] = 'Patient {}'.format(n)

    # get min and max data
    min_date = df['@startDate'].min()
    max_date = df['@startDate'].max()

    # remove not necessary prefix 'HKQuantityTypeIdentifier'
    df['@type'] = df['@type'].apply(lambda x: x.replace('HKQuantityTypeIdentifier', ''))
    df['@type'] = df['@type'].apply(lambda x: x.replace('HKCategoryTypeIdentifier', ''))
    df['@type'] = df['@type'].apply(lambda x: re.sub(r'(?<![A-Z\W])(?=[A-Z])', ' ', x).lstrip(' '))

    # convert time zone
    zone = min_date[20:23].replace('0', '')
    df['@startDate'] = pd.to_datetime(df['@startDate']).map(
        lambda x: x.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT{}'.format(zone))))


    return df, df2, min_date, max_date


def export_workout_data_from_apple_watch(input_data, n):
    """
    This function extract workout data from Apple Watch.

    Example of workout data:
    HKWorkoutActivityTypeWalking
    HKWorkoutActivityTypeCycling
    HKWorkoutActivityTypeRunning
    """

    # import workout data
    workouts_list = input_data['HealthData']['Workout']
    df = pd.DataFrame(workouts_list)

    # rename @sourceName
    df['@sourceName'] = df['@sourceName'].apply(lambda x: 'Patient {}'.format(n))

    # Remove not necessary data and prefix 'HKWorkoutActivityType'
    df = df.drop(['@sourceVersion', '@device', 'WorkoutRoute', 'WorkoutEvent', 'MetadataEntry', '@creationDate'], axis=1)
    df['@workoutActivityType'] = df['@workoutActivityType'].str.replace('HKWorkoutActivityType', '')

    # convert time zone
    date = df['@startDate'][0]
    zone = date[20:23].replace('0', '')
    df['@startDate'] = pd.to_datetime(df['@startDate']).map(
        lambda x: x.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT{}'.format(zone))))
    df['@endDate'] = pd.to_datetime(df['@endDate']).map(
        lambda x: x.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT{}'.format(zone))))

    return df


def export_ecg_data_from_apple_watch(directories):
    """
    This function extract ECG data from Apple Watch and calculate time domain and frequency domain HRV parameters

    """

    # create DataFrame with all parameters
    df = pd.DataFrame(columns=['patient', 'Date', 'Day', 'number', 'Classification', 'data', 'hrv', 'SDNN', 'SENN',
                               'SDSD', 'pNN20', 'pNN50', 'lf', 'hf', 'lf_hf_ratio', 'total_power', 'vlf'])

    # Loading ECG data to database
    for i in directories:
        # export all ecg.csv files from selected directory
        only_files = [f for f in listdir('./import/{}/'.format(i)) if isfile(join('./import/{}/'.format(i), f))]

        # get patient ID(number)
        n = int(''.join(filter(str.isdigit, i)))
        patient = 'Patient {}'.format(n)

        for ecg_file in only_files:
            path = './import/{0}/{1}'.format(i, ecg_file)

            ecg = pd.read_csv(path, sep=";", names=['Name'])
            ecg_file = ecg_file.replace('ecg_', '').replace('.csv', '')

            #
            if '_' not in ecg_file:
                day, number = ecg_file[:10], 0
            else:
                day, number = ecg_file[:10], ecg_file[-1]

            # get date and covert time zone
            date = ecg['Name'][2][-25:]
            zone = date[20:23].replace('0', '')
            date = pd.to_datetime(date).replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT{}'.format(zone)))

            # get classification from Apple Watch
            classification = ecg['Name'][3].split(",", 1)[1]

            # get ECG date replace ',' with '.'
            data = ecg["Name"][10:].str.replace(',', '.').astype(float).to_list()

            # calculate RR intervals
            data_array = np.array(data)
            r_peaks = detect_r_peaks(511, data_array)
            RRints = np.diff(r_peaks)
            RRints = (RRints / 511) * 1000

            # calculate parameters for time and frequency domain
            try:
                RRints = np.array(RRints)
                frequency_domain_features = {'lf': 0, 'hf': 0, 'lf_hf_ratio': 0, 'total_power': 0, 'vlf': 0}
                #frequency_domain_features = frequencydomain(RRints)
                time_domain_features = time_domain_analyze(RRints)
            except:
                time_domain_features = {'hrv': 0, 'SDNN': 0, 'SENN': 0, 'SDSD': 0, 'pNN20': 0, 'pNN50': 0}
                frequency_domain_features = {'lf': 0, 'hf': 0, 'lf_hf_ratio': 0, 'total_power': 0, 'vlf': 0}

            ecg_data = {'patient': patient, 'Date': date, 'Day': day, 'number': number,
                        'Classification': classification, 'data': data}

            merge = {**ecg_data, **time_domain_features, **frequency_domain_features}  # merge all three tables

            df = df.append(merge, ignore_index=True)

    return df


def calculate_HRR(df_hr, df_workout):
    """
    This function calculate average, min, max heart rate during workout and Heart rate recovery after 1 and 2 minute.
    """

    result_1_min, result_2_min, result_max, result_min, HR_average = [], [], [], [], []

    # get heart rate values
    df_HR = df_hr.loc[df_hr['@type'] == 'Heart Rate'].copy(deep=True)
    df_HR['@value'] = df_HR['@value'].apply(pd.to_numeric)

    df_workout['@totalDistance'], df_workout['@duration'] = pd.to_numeric(df_workout['@totalDistance']), \
                                                            pd.to_numeric(df_workout['@duration'])
    for i in range(len(df_workout)):
        start_workout, end_workout = str(df_workout.iloc[i]['@startDate']), str(df_workout.iloc[i]['@endDate'])

        # get time after 1 and 2 workout
        after_workout_1_m = str(df_workout.iloc[i]['@endDate'] + np.timedelta64(1, 'm'))
        after_workout_2_m = str(df_workout.iloc[i]['@endDate'] + np.timedelta64(2, 'm'))

        # get values of heart rater during workout and after workout
        df_HRR = df_HR[(df_HR['@startDate'] > start_workout) & (df_HR['@startDate'] < end_workout)]
        df_HRR_1_min = df_HR[(df_HR['@startDate'] > end_workout) & (df_HR['@startDate'] < after_workout_1_m)]
        df_HRR_2_min = df_HR[(df_HR['@startDate'] > end_workout) & (df_HR['@startDate'] < after_workout_2_m)]

        try:
            HRR_1_min = df_HRR_1_min['@value'].values[0] - df_HRR_1_min['@value'].values[-1]
            HRR_2_min = df_HRR_2_min['@value'].values[0] - df_HRR_2_min['@value'].values[-1]
            average, max_value, min_value = df_HRR['@value'].mean(), df_HRR['@value'].max(), df_HRR['@value'].min()
            result_1_min.append(HRR_1_min)
            result_2_min.append(HRR_2_min)
            result_max.append(max_value)
            result_min.append(min_value)
            HR_average.append(average)
        except:
            result_1_min.append(0), result_2_min.append(0), result_max.append(0), result_min.append(0)
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


def detect_r_peaks(SampleRate, data):
    """
    R peaks detection and RR intervals calculation
    """

    detectors = Detectors(SampleRate)  # use library for peak detection to get array of r peak positions
    r_peaks = detectors.engzee_detector(data)
    r_peaks = np.array(r_peaks)  # convert list to array
    return r_peaks