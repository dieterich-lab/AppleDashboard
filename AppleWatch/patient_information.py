
import dash_core_components as dcc
import dash_html_components as html

import modules.load_data_from_database as ldd
from db import connect_db

rdb = connect_db()


def patient_information():
    information = [dcc.Tab(
        label='About',
        value='what-is',
        children=html.Div(className='control-tab', children=[
            html.H4(className='what-is', children='Information about patient'),
            html.P(id="text", className="card-text")
        ]))]
    return information

# change value in card depend from this what is chosen in selector
def info(df,ECG_irregular, ECG_inconclusive, ECG_over_120, ECG_under_50, patient):
    height = df[df['@sourceName'] == patient].iloc[0]['@Value']
    weight = df[df['@sourceName'] == patient].iloc[1]['@Value']

    height = height
    weight = weight

    if ECG_inconclusive.empty or patient not in ECG_inconclusive.values: inconclusive_ecg=0
    else: inconclusive_ecg = ECG_inconclusive[ECG_inconclusive['Patient'] == patient ].iloc[0]['count']
    if ECG_irregular.empty or patient not in ECG_irregular.values: irregular_ecg=0
    else: irregular_ecg = ECG_irregular[ECG_irregular['Patient'] == patient].iloc[0]['count']
    if ECG_over_120.empty or patient not in ECG_over_120.values: over_150=0
    else: over_150 = ECG_over_120[ECG_over_120['Patient'] == patient].iloc[0]['count']
    if ECG_under_50.empty or patient not in ECG_under_50.values: under_50=0
    else: under_50 = ECG_under_50[ECG_under_50['Patient'] == patient].iloc[0]['count']

    if patient == 'Patient1':
        age = '26'
        sex = 'female'
    else:
        age = '32'
        sex = 'male'

    text = 'Age: {}'.format(age), html.Br(), 'Sex: {}'.format(sex), html.Br(), 'Weight: {}'.format(weight), html.Br(),\
           'Height:{}'.format(height), html.Br(), 'Patient disease: None', \
           html.Br(), 'Number of inconclusive ECG: {}'.format(inconclusive_ecg), html.Br(),\
           'Number of irregular ECG: {}'.format(irregular_ecg), html.Br(),\
           'Over 150: {}'.format(over_150), html.Br(), 'Under 50: {}'.format(under_50), html.Br(),html.Br()

           #'The number of days the Apple Watch has been worn for at least 6h: {}'.format(under_50)

    return text
