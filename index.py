import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
from apps import AppleWatch,Medicaldata
import dash_daq as daq
from db import connect_db
from modules.import_scheduler import Scheduler
import os




# change color of background
colors = {'background': '#f4f4f2', 'text': '#7FDBFF'}



# Creating layout
app.layout = html.Div([

    dbc.Container(
    style={'backgroundColor': colors['background']},
    children =[
        dbc.Card(html.Div(
        className="row header",
        children = [html.Img(src=app.get_asset_url("logo.jpg"),style={'height':'5%', 'width':'5%','margin-left': '15px'}),
                html.H1('HiGHmed Patient Dashboard',style={"font-size": "3rem", "margin-top": "15px","margin-left": "25px"}),
                    ])),

        dbc.Card(html.Div(
            id="tabs",
            className="row tabs",
            children=[
            dcc.Link('Dashboard for individual Patient', href='/'),
            dcc.Link('Patient statistics', href='/',)])),
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
    tabs = [
        dcc.Link("Dashboard for individual Patient", href='/apps/AppleWatch'),
        dcc.Link("Patient statistics", href='http://0.0.0.0:800/scatter_plot'),
    ]
    if pathname == "http://0.0.0.0:800/scatter_plot":
        tabs[1] = dcc.Link(
            dcc.Markdown("**&#9632 Patient statistics**"), href="http://0.0.0.0:800/scatter_plot"
        )

        return Medicaldata.layout, tabs

    tabs[0] = dcc.Link(
            dcc.Markdown("**&#9632 Dashboard for individual Patient**"),
            href='/apps/AppleWatch',
        )
    return AppleWatch.layout, tabs


if __name__ == '__main__':
    app.run_server(debug=True)