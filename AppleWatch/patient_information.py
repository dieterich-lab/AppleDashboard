from dash import dcc
from dash import html


def patient_information():
    """ Return: Card with patient information """
    information = [dcc.Tab(
        label='About',
        value='what-is',
        children=html.Div(className='control-tab', children=[
            html.H4(className='what-is', children='Information about patient'),
            html.P(id="text", className="card-text")]))]
    return information


def info(age, sex, ecg_classification, days):
    """ Change values in information card depend from this what is chosen in drop down """

    ecg_classification.insert(1, 'separator', ':')
    x = ecg_classification.to_string(header=False, index=False, index_names=False).split('\n')
    ecg_classification = tuple(intersperse(x, html.Br()))

    text = (html.Br(), 'Age: {}'.format(age), html.Br(), 'Sex: {}'.format(sex), html.Br(), 'Patient disease: None',
            html.Br()) + ecg_classification + \
           (html.Br(), 'The number of days the Apple Watch has been worn for at least 6h: {}'.format(days))

    return text


def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result
