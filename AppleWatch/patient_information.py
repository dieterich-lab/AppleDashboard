import dash_core_components as dcc
import dash_html_components as html
from db import connect_db
import modules.load_data_from_database as ldd

rdb = connect_db()


def patient_information():
    information = [dcc.Tab(
        label='About',
        value='what-is',
        children=html.Div(className='control-tab', children=[
            html.H4(className='what-is', children='Information about patient'),
            html.A('Download data', id='my-link2'),
            html.P(id="text", className="card-text"),

        ]))]
    return information


# change value in card depend from this what is chosen in selector
def info(patient):
    age_gender=ldd.age_sex(rdb,patient)
    height = ldd.weight_and_height(rdb, patient)
    df2, df4 = ldd.irregular_ecg(rdb, patient)
    days = ldd.number_of_days_more_6(rdb,patient)


    if 'Inconclusive' in df2.values:
        inconclusive_ecg =  df2[df2['Classification'] == 'Inconclusive'].iloc[0]['count']
    elif 'Uneindeutig' in df2.values:
        inconclusive_ecg = df2[df2['Classification'] == 'Uneindeutig'].iloc[0]['count']
    else:
        inconclusive_ecg = 0
    if 'Irregular' not in df2.values:
        irregular_ecg = 0
    else:
        irregular_ecg = df2[df2['Classification'] == 'Irregular'].iloc[0]['count']
    if 'Heart Rate Over 120' not in df2.values:
        over_150 = 0
    else:
        over_150 = df2[df2['Classification'] == 'Heart Rate Over 120'].iloc[0]['count']
    if 'Heart Rate Under 50' in df2.values:
        under_50 = df2[df2['Classification'] == 'Heart Rate Under 50'].iloc[0]['count']
    elif 'Herzfrequenz unter 50' in df2.values:
        under_50 = df2[df2['Classification'] == 'Herzfrequenz unter 50'].iloc[0]['count']
    else:
        under_50 = 0


    age = age_gender['Age'][0]
    sex = age_gender['Sex'][0]


    text = html.Br(),'Age: {}'.format(age), html.Br(), 'Sex: {}'.format(sex), html.Br(),\
           'Height: {}'.format(height), html.Br(), 'Patient disease: None', \
           html.Br(), 'Number of inconclusive ECG: {}'.format(inconclusive_ecg), html.Br(),\
           'Number of irregular ECG: {}'.format(irregular_ecg), html.Br(),\
           'Over 120: {}'.format(over_150), html.Br(), 'Under 50: {}'.format(under_50), html.Br(),\
           'The number of days the Apple Watch has been worn for at least 6h: {}'.format(days)

    return text
