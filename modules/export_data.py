from datetime import date, datetime
import pytz
import re
import numpy as np
import pandas as pd
from ecgdetectors import Detectors
from modules.HRV_time_domain_analyze import time_domain_analyze
from dateutil.relativedelta import relativedelta


def basic_information(input_data, n):
    """
    If user provided basic information about himself such as: age,gender, blood group, skin type.
    This function extract this information from Apple Watch.
    """
    patient = 'Patient {}'.format(n)
    birth, blood_group, sex, skin_type = extract_basic_information_from_export_file(input_data)
    age = calculate_patient_age(birth)

    return pd.DataFrame([[patient, n, age, sex, blood_group, skin_type]],
                        columns=['patient', 'index', 'age', 'sex', 'blood_group', 'skin_type'])


def extract_basic_information_from_export_file(input_data):
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
    return birth, blood_group, sex, skin_type


def calculate_patient_age(birth):
    if birth != '':
        today = date.today()
        birth = datetime.fromisoformat(birth)
        time_difference = relativedelta(today, birth)
        age = time_difference.years
    else:
        age = birth
    return age


def export_health_data_from_apple_watch(input_data, n):
    """
    This function extract health data from Apple Watch.
    """
    # import health data
    records_list = input_data['HealthData']['Record']
    df = pd.DataFrame(records_list)
    df = df.drop(['@sourceVersion', '@device', 'MetadataEntry', 'HeartRateVariabilityMetadataList', '@endDate',
                  '@creationDate'], axis=1)

    df_other_sources = df[~df['@sourceName'].str.contains("Watch")]
    # df_other_sources['@sourceName'] = df_other_sources['@sourceName'].apply(lambda x: 'Patient {}'.format(n))

    df = df[df['@sourceName'].str.contains("Watch")]  # DataFrame contain data only from Apple Watch
    df['@sourceName'] = df['@sourceName'].apply(lambda x: 'Patient {}'.format(n))

    # remove not necessary prefix 'HKQuantityTypeIdentifier'
    df['@type'] = df['@type'].apply(lambda x: x.replace('HKQuantityTypeIdentifier', ''))
    df['@type'] = df['@type'].apply(lambda x: x.replace('HKCategoryTypeIdentifier', ''))
    df['@type'] = df['@type'].apply(lambda x: re.sub(r'(?<![A-Z\W])(?=[A-Z])', ' ', x).lstrip(' '))

    convert_time_zone(df, '@startDate')
    df = df.reset_index(level=0)

    return df, df_other_sources, df['@startDate'].min(), df['@startDate'].max()


def convert_time_zone(df, column):
    date_value = df[column].min()
    zone = date_value[20:23].replace('0', '')
    df[column] = pd.to_datetime(df[column]).map(
        lambda x: x.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT{}'.format(zone))))


def export_workout_data_from_apple_watch(input_data, n):
    """
    This function extract workout data from Apple Watch.
    """

    # import workout data
    workouts_list = input_data['HealthData']['Workout']
    df = pd.DataFrame(workouts_list)
    df['@sourceName'] = df['@sourceName'].apply(lambda x: 'Patient {}'.format(n))

    # Remove not necessary data and prefix 'HKWorkoutActivityType'
    df = df.drop(['@sourceVersion', '@device', 'WorkoutRoute', 'WorkoutEvent', 'MetadataEntry', '@creationDate'],
                 axis=1)
    df['@workoutActivityType'] = df['@workoutActivityType'].str.replace('HKWorkoutActivityType', '')

    convert_time_zone(df, '@startDate')
    convert_time_zone(df, '@endDate')

    return df


def export_ecg_data_from_apple_watch(files, directory, patient):
    """
    This function extract ECG data from Apple Watch and calculate time domain and frequency domain HRV parameters
    """
    df = pd.DataFrame(columns=['patient', 'Date', 'Day', 'number', 'Classification', 'data', 'hrv', 'sdnn', 'senn',
                               'sdsd', 'pnn20', 'pnn50'])

    for i, ecg_file in enumerate(files):
        path = './import/{0}/{1}'.format(directory, ecg_file)
        ecg = pd.read_csv(path, sep=";", names=['Name'])
        ecg_file = ecg_file.replace('ecg_', '').replace('.csv', '')

        if '_' not in ecg_file:
            day, number = ecg_file[:10], 0
        else:
            day, number = ecg_file[:10], ecg_file[-1]

        date_ecg_zone = convert_time_zone_ecg(ecg)
        classification = ecg['Name'][3].split(",", 1)[1]
        data = ecg["Name"][10:].str.replace(',', '.').astype(float).to_list()

        try:
            RRints = detect_r_peaks(511, data)
            rr_intervals = (RRints / 511) * 1000
            if len(rr_intervals) > 1:
                time_domain_features_dict = time_domain_analyze(rr_intervals)
            else:
                time_domain_features_dict = {'hrv': 0, 'sdnn': 0, 'senn': 0, 'sdsd': 0, 'pnn20': 0, 'pnn50': 0}
        except:
            time_domain_features_dict = {'hrv': 0, 'sdnn': 0, 'senn': 0, 'sdsd': 0, 'pnn20': 0, 'pnn50': 0}

        ecg_data = {'patient': patient, 'Date': date_ecg_zone, 'Day': day, 'number': number,
                    'Classification': classification, 'data': ''}
        df_data = pd.DataFrame({**ecg_data, **time_domain_features_dict}, index=[i])
        df_data.at[i, 'data'] = data
        df = pd.concat([df, df_data])
    df = df.reset_index(level=0)
    return df


def convert_time_zone_ecg(ecg):
    date_ecg = ecg['Name'][2][-25:]
    zone = date_ecg[20:23].replace('0', '')
    date_ecg_zone = pd.to_datetime(date_ecg).replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT{}'.
                                                                                               format(zone)))
    return date_ecg_zone


def calculate_hrr(df_health_data, df_workout):
    """
    This function calculate average, min, max heart rate during workout and Heart rate recovery after 1 and 2 minute.
    """
    df_hr = df_health_data.loc[df_health_data['@type'] == 'Heart Rate'].copy(deep=True)
    df_hr['@value'] = df_hr['@value'].apply(pd.to_numeric)

    df_workout['@totalDistance'] = pd.to_numeric(df_workout['@totalDistance'])
    df_workout['@duration'] = pd.to_numeric(df_workout['@duration'])

    result = {'hrr_1_min': [0], 'hrr_2_min': [0], 'hr_max': [0], 'hr_min': [0], 'hr_average': [0]}

    for i in range(len(df_workout)):
        calculate_heart_rate_during_exercises(df_hr, df_workout, i, result)

    df = pd.DataFrame(result)
    df = df.iloc[1:, :]
    df['speed'] = df_workout['@totalDistance'] / df_workout['@duration']
    df['hr-rs_index'] = df['hr_average'] / df['speed']

    df_workout = pd.concat([df_workout, df], axis=1)
    df_workout = df_workout.reset_index(level=0)

    return df_workout


def calculate_heart_rate_during_exercises(df_hr, df_workout, i, result):
    # get time after 1 and 2 minutes of workout
    after_workout_1_m = str(df_workout.iloc[i]['@endDate'] + np.timedelta64(1, 'm'))
    after_workout_2_m = str(df_workout.iloc[i]['@endDate'] + np.timedelta64(2, 'm'))
    start_workout, end_workout = str(df_workout.iloc[i]['@startDate']), str(df_workout.iloc[i]['@endDate'])
    # get values of heart rate during workout and after workout
    df_hrr = df_hr[(df_hr['@startDate'] > start_workout) & (df_hr['@startDate'] < end_workout)]
    df_hrr_1_min = df_hr[(df_hr['@startDate'] > end_workout) & (df_hr['@startDate'] < after_workout_1_m)]
    df_hrr_2_min = df_hr[(df_hr['@startDate'] > end_workout) & (df_hr['@startDate'] < after_workout_2_m)]
    try:
        hrr_1_min = df_hrr_1_min['@value'].values[0] - df_hrr_1_min['@value'].values[-1]
        hrr_2_min = df_hrr_2_min['@value'].values[0] - df_hrr_2_min['@value'].values[-1]
        average, max_value, min_value = df_hrr['@value'].mean(), df_hrr['@value'].max(), df_hrr['@value'].min()
    except:
        hrr_1_min, hrr_2_min, average, max_value, min_value = 0, 0, 0, 0, 0
    result['hrr_1_min'].append(hrr_1_min)
    result['hrr_2_min'].append(hrr_2_min)
    result['hr_max'].append(max_value)
    result['hr_min'].append(min_value)
    result['hr_average'].append(average)


def detect_r_peaks(sample_rate, data):
    """
    R peaks detection and RR intervals calculation
    """
    data_array = np.array(data)
    detectors = Detectors(sample_rate)  # use library for peak detection to get array of r peak positions
    r_peaks = detectors.engzee_detector(data_array)
    return np.array(r_peaks)
