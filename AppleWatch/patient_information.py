from dash import dcc
from dash import html
from db import connect_db
import modules.load_data_from_database as ldd

rdb = connect_db()


def patient_information():
    """ Return: Card with patient information """
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
    """ Change values in information card depend from this what is chosen in drop down """

    age, sex = ldd.age_sex(rdb, patient)

    text = ('Age: {}'.format(age), html.Br(), 'Sex: {}'.format(sex), html.Br(), 'Patient disease: None')

    return text
