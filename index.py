from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
from apps import AppleWatch, Workouts, Comparison, HRV, Questionnaire, tutorial

# change color of background
colors = {'background': '#f4f4f2', 'text': '#7FDBFF'}

class DataStore():

    # for filter
    csv_ecg = None
    csv_ecgs = None
    csv_apple = None


data_store = DataStore()

# Creating layout
app.layout = html.Div([

    dbc.Container(
    style={'backgroundColor': colors['background']},
    children =[
        dbc.Card(html.Div(

        className="row header",
        children=[dbc.Col(html.Img(src=app.get_asset_url("logo.jpg"),style={ 'width':'60%','margin-left': '15px'}),lg=1),
                dbc.Col(html.H1('HiGHmed Patient Dashboard',style={"font-size": "3rem", "margin-top": "30px","vertical-align": "middle"}),lg=8),
                dbc.Col(html.A(dcc.Link(html.H2('Tutorial',style={"font-size": "2rem", "margin-top": "20px","vertical-align": "middle"}),
                                   href='/apps/tutorial')),lg=3)
                    ])),

        dbc.Card(html.Div(
            id="tabs",
            className="row tabs",
            children=[
            dcc.Link('Patient Health data', href='/'),
            dcc.Link('Patient Workouts', href='/'),
            dcc.Link('Patient Comparison', href='/'),
            dcc.Link('ECG analyze', href='/'),
           ])),

        dcc.Location(id='url', refresh=False),
        # content will be rendered in this element
        html.Div(id='page_content')],
        fluid=True)
])


@app.callback(
    [
        Output("page_content", "children"),
        Output("tabs", "children"),
    ],
    [Input("url", "pathname")],
)
def display_page(pathname):
    dcc.Link("back", href='/apps/tutorial'),
    tabs = [
        dcc.Link("Patient health data", href='/apps/AppleWatch'),
        dcc.Link("Patient Workouts", href='/apps/Workouts'),
        dcc.Link("Patient Comparison", href='/apps/Comparison'),
        dcc.Link("ECG analyze", href='/apps/HRV')
    ]

    if pathname == "/apps/Workouts":
        tabs[1] = dcc.Link(
            dcc.Markdown("**&#9632 Patient Workouts**"), href="/apps/Workouts"
        )

        return Workouts.layout, tabs
    elif pathname == "/apps/Comparison":
        tabs[2] = dcc.Link(
            dcc.Markdown("**&#9632 Patient comparison**"), href="/apps/Comparison"
        )

        return Comparison.layout, tabs
    elif pathname == "/apps/HRV":
        tabs[3] = dcc.Link(
            dcc.Markdown("**&#9632 ECG analyze**"), href="/apps/HRV"
        )

        return HRV.layout, tabs

    elif pathname == "/apps/tutorial":

        return tutorial.layout, tabs

    tabs[0] = dcc.Link(
            dcc.Markdown("**&#9632 Patient health data**"),
            href='/apps/AppleWatch',
        )
    return AppleWatch.layout, tabs


if __name__ == '__main__':
    app.run_server(debug=True)