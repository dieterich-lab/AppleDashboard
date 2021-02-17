import pandas as pd
import xmltodict
import pytz

appended_data = []
for i in range(1, 3):
    # export data from xml file
    input_path = '/home/magda/__git__/new/AppleDashboard/import/export{}.xml'.format(i)
    with open(input_path, 'r') as xml_file:
        input_data = xmltodict.parse(xml_file.read())

    records_list = input_data['HealthData']['Record']
    df = pd.DataFrame(records_list)
    df['@sourceName'] = df['@sourceName'].apply(lambda x: 'Patient{}'.format(i))

    xml_file.close()

    appended_data.append(df)

df = pd.concat(appended_data)
# convert time to you time zone
convert_tz = lambda x: x.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT+1'))
format = '%Y-%m-%d %H:%M:%S %z'

df['@creationDate'] = pd.to_datetime(df['@creationDate']).map(convert_tz)
df['@startDate'] = pd.to_datetime(df['@startDate']).map(convert_tz)
df['@endDate'] = pd.to_datetime(df['@endDate']).map(convert_tz)

# Remove not necessary data
df = df.drop(['@device','MetadataEntry', 'HeartRateVariabilityMetadataList'], axis=1)
df=df[df['@type'].isin(['HKQuantityTypeIdentifierRestingHeartRate','HKQuantityTypeIdentifierWalkingHeartRateAverage','HKQuantityTypeIdentifierHeartRate','HKQuantityTypeIdentifierStepCount','HKQuantityTypeIdentifierAppleExerciseTime','HKQuantityTypeIdentifierActiveEnergyBurned'])]
df["@value"] = pd.to_numeric(df["@value"])
df.to_csv('apple.csv',index=False)