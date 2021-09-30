import pandas as pd
import pytz
from os import listdir
from os.path import isfile, join
import numpy as np

df = pd.DataFrame(columns=['patient', 'Date', 'Day', 'number', 'Classification', 'data'])
only_files = [f for f in listdir('./import/electrocardiograms3/') if isfile(join('./import/electrocardiograms3/', f))]

patient = 'Patient 1'
for ecg_file in only_files:
    path = './import/electrocardiograms3/{0}'.format(ecg_file)

    ecg = pd.read_csv(path,sep=";",names=['Name'])
    data = ecg["Name"][10:].str.replace(',', '.').astype(float).to_list()

    ecg_file = ecg_file.replace('ecg_', '').replace('.csv', '')
    if '_' not in ecg_file:
        ecg_file = ecg_file + '_0'
        date = ecg['Name'][2].replace("Aufzeichnungsdatum,", "")
        date = date.replace("Recorded Date,", "")
        print(date)
        date = pd.to_datetime(date).replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT+1'))
        classification = ecg['Name'][2].replace("Classification,","")

        day, number = ecg_file[:10], ecg_file[-1]
        datu = np.array(data)

        ecg_data = {'patient': patient, 'Date': date, 'Day': day, 'number': number,'Classification': classification,
                    'data': data}

        df = df.append(ecg_data, ignore_index=True)

