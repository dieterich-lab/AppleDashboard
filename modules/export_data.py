import pandas as pd
import xmltodict
import pytz
from os import listdir
from os.path import isfile, join


def export_health_data_from_apple_watch(files):
    appended_data = []
    for i in files:
        # export data from xml file
        input_path = './import/{}'.format(i)

        with open(input_path, 'r', errors='ignore') as xml_file:
            input_data = xmltodict.parse(xml_file.read())

        # import health data
        records_list = input_data['HealthData']['Record']
        df = pd.DataFrame(records_list)

        n = int(''.join(filter(str.isdigit, i)))

        # rename @sourceName
        df = df[df['@sourceName'].str.contains("Watch")]
        df['@sourceName'] = df['@sourceName'].apply(lambda x: 'Patient {}'.format(n))

        # Remove not necessary data
        df = df.drop(['@sourceVersion', '@device', 'MetadataEntry', 'HeartRateVariabilityMetadataList', '@endDate',
                      '@creationDate'],
                     axis=1)

        # convert time to you time zone
        df['@startDate'] = pd.to_datetime(df['@startDate']).map(
            lambda x: x.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT+1')))
        appended_data.append(df)
        xml_file.close()

    df = pd.concat(appended_data)

    return df


def export_workout_data_from_apple_watch(files):
    appended_data = []
    for i in files:
        # export data from xml file
        input_path = './import/{}'.format(i)

        with open(input_path, 'r') as xml_file:
            input_data = xmltodict.parse(xml_file.read())

        # import health data
        workouts_list = input_data['HealthData']['Workout']
        df = pd.DataFrame(workouts_list)

        n = int(''.join(filter(str.isdigit, i)))

        # rename @sourceName
        df = df[df['@sourceName'].str.contains("Watch")]
        df['@sourceName'] = df['@sourceName'].apply(lambda x: 'Patient {}'.format(n))

        # Remove not necessary data
        df = df.drop(['@sourceVersion', '@device', 'WorkoutRoute', 'WorkoutEvent', 'MetadataEntry',
                      '@creationDate'], axis=1)

        # convert time to you time zone
        df['@startDate'] = pd.to_datetime(df['@startDate']).map(
            lambda x: x.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT+1')))
        df['@endDate'] = pd.to_datetime(df['@endDate']).map(
            lambda x: x.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT+1')))
        appended_data.append(df)
        xml_file.close()

    df = pd.concat(appended_data)

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
