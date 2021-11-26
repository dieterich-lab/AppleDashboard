from dash import dcc
from dash import html
from db import connect_db
import modules.load_data_from_database as ldd

rdb = connect_db()


def patient_information():
    """
    return: Card with patient information
    """
    information = [dcc.Tab(
        label='About',
        value='what-is',
        children=html.Div(className='control-tab', children=[
            html.H4(className='what-is', children='Information about patient'),
            html.A('Download data', id='my-link2'),
            html.P(id="text", className="card-text"),

        ]))]
    return information


def info(patient):
    """
    change value in information card depend from this what is chosen in selector

    :param patient: patient id/number
    :return: text: updated information about patient

    """

    age, sex = ldd.age_sex(rdb, patient)
    ecg_classification = ldd.irregular_ecg(rdb, patient)
    days = ldd.number_of_days_more_6(rdb, patient)

    def intersperse(lst, item):
        result = [item] * (len(lst) * 2 - 1)
        result[0::2] = lst
        return result

    ecg_classification.insert(1, 'separator', ':')
    x = ecg_classification.to_string(header=False,
                                     index=False,
                                     index_names=False).split('\n')

    ecg_classification = tuple(intersperse(x, html.Br()))

    text = (html.Br(), 'Age: {}'.format(age), html.Br(), 'Sex: {}'.format(sex), html.Br(), 'Patient disease: None',
            html.Br()) + ecg_classification + \
           (html.Br(), 'The number of days the Apple Watch has been worn for at least 6h: {}'.format(days))

    return text
