import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import AppleWatch,Medicaldata,Questionnaire


app.layout = html.Div([
    dcc.Location(id='url', refresh=False,pathname = '/apps/AppleWatch',href='/apps/AppleWatch'),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/AppleWatch':
        return AppleWatch.layout
    elif pathname == '/apps/Questionnaire':
        return Questionnaire.layout
    elif pathname == '/apps/Medicaldata':
        return Medicaldata.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)