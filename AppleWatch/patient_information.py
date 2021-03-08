import dash_core_components as dcc
import dash_html_components as html
from db import connect_db

rdb = connect_db()


def patient_information():
    information = [dcc.Tab(
        label='About',
        value='what-is',
        children=html.Div(className='control-tab', children=[
            html.H4(className='what-is', children='Information about patient'),
            html.A('Download data', id='my-link2'),
            html.P(id="text", className="card-text")
        ]))]
    return information


# change value in card depend from this what is chosen in selector
def info(df, df2, df_time, patient):
    height = df[df['@sourceName'] == patient].iloc[0]['@Value']
    days = df_time[df_time['@sourceName'] == patient].iloc[0]['count']

    height = height
    df2 = df2[df2['Patient'] == patient]
    if 'Inconclusive' not in df2.values:
        inconclusive_ecg = 0
    else:
        inconclusive_ecg = df2[(df2['Patient'] == patient) & (df2['Classification'] == 'Inconclusive')].iloc[0]['count']
    if 'Irregular' not in df2.values:
        irregular_ecg = 0
    else:
        irregular_ecg = df2[(df2['Patient'] == patient) & (df2['Classification'] == 'Irregular')].iloc[0]['count']
    if 'Heart Rate Over 120' not in df2.values:
        over_150 = 0
    else:
        over_150 = df2[(df2['Patient'] == patient) & (df2['Classification'] == 'Heart Rate Over 120')].iloc[0]['count']
    if 'Heart Rate Under 50' not in df2.values:
        under_50 = 0
    else:
        under_50 = df2[(df2['Patient'] == patient) & (df2['Classification'] == 'Heart Rate Under 50')].iloc[0]['count']

    if patient == 'Patient1':
        age = '26'
        sex = 'female'
    else:
        age = '32'
        sex = 'male'

    text = html.Br(),'Age: {}'.format(age), html.Br(), 'Sex: {}'.format(sex), html.Br(),\
           'Height:{}'.format(height), html.Br(), 'Patient disease: None', \
           html.Br(), 'Number of inconclusive ECG: {}'.format(inconclusive_ecg), html.Br(),\
           'Number of irregular ECG: {}'.format(irregular_ecg), html.Br(),\
           'Over 120: {}'.format(over_150), html.Br(), 'Under 50: {}'.format(under_50), html.Br(),\
           'The number of days the Apple Watch has been worn for at least 6h: {}'.format(days)

    return text
