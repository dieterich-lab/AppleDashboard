import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
from apps import AppleWatch,Medicaldata,Questionnaire

# change color of background
colors = {
    'background': '#e7e7e7',
    'text': '#7FDBFF'
}

# Creating layout
app.layout = html.Div([

    # Rendering after open the program
    dcc.Location(id='url', refresh=False,pathname='/apps/Medicaldata',href='/apps/Medicaldata'),

    dbc.Container(
    style={'backgroundColor': colors['background']},
    children =[
        dbc.Row(dbc.Col(html.H1('HiGHmed patient dashboard',style={'textAlign': 'center',}),)),

        html.Div([
            dcc.Link('Apple Watch', href='/apps/AppleWatch', className="tab", ),
            dcc.Link('Medical data', href='/apps/Medicaldata', className="tab ", ),
            dcc.Link('Questionnaire', href='/apps/Questionnaire', className="tab ", )],),
        # content will be rendered in this element
        html.Div(id='page-content')],
        fluid=True)
])

# calllback for rendering pages
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