from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
from apps import AppleWatch, Workouts, Comparison, ECG, tutorial

# change color of background
colors = {'background': '#f4f4f2', 'text': '#7FDBFF'}

# Creating layout
app.layout = html.Div([

    dbc.Container(style={'backgroundColor': colors['background']},
                  children=[dbc.Card(html.Div(className="row header",
                                              children=[dbc.Col(html.Img(src=app.get_asset_url("logo.jpg"),
                                                                         style={'width': '60%', 'margin-left': '15px'}),
                                                                lg=1),
                                                        dbc.Col(html.H1('HiGHmed Patient Dashboard',
                                                                        style={"font-size": "3rem",
                                                                               "margin-top": "30px"}), lg=8),
                                                        dbc.Col(html.A(dcc.Link(html.H2('Tutorial',
                                                                                        style={"font-size": "2rem",
                                                                                               "margin-top": "20px"}),
                                                                                href='/apps/tutorial')), lg=3)])),
                            # Tabs
                            dbc.Card(html.Div(id="tabs", className="row tabs",
                                              children=[dcc.Link('Patient Health Data', href='/'),
                                                        dcc.Link('Patient Workouts', href='/'),
                                                        dcc.Link('Patient Comparison', href='/'),
                                                        dcc.Link('ECG Analyze', href='/')])),

                            dcc.Location(id='url', refresh=False),

                            # content will be rendered in this element
                            html.Div(id='page_content')],
                  fluid=True)])


# callback to update tabs
@app.callback([Output("page_content", "children"),
               Output("tabs", "children")],
              [Input("url", "pathname")])
def display_page(pathname):
    dcc.Link("back", href='/apps/tutorial'),
    tabs = [dcc.Link("Patient Health Data", href='/apps/AppleWatch'),
            dcc.Link("Patient Workouts", href='/apps/Workouts'),
            dcc.Link("Patient Comparison", href='/apps/Comparison'),
            dcc.Link("ECG Analyze", href='/apps/ECG')]

    if pathname == "/apps/Workouts":
        tabs[1] = dcc.Link(dcc.Markdown("**&#9632 Patient Workouts**"), href="/apps/Workouts")
        return Workouts.layout, tabs
    elif pathname == "/apps/Comparison":
        tabs[2] = dcc.Link(dcc.Markdown("**&#9632 Patient Comparison**"), href="/apps/Comparison")
        return Comparison.layout, tabs
    elif pathname == "/apps/ECG":
        tabs[3] = dcc.Link(dcc.Markdown("**&#9632 ECG Analyze**"), href="/apps/ECG")
        return ECG.layout, tabs
    elif pathname == "/apps/tutorial":
        return tutorial.layout, tabs

    tabs[0] = dcc.Link(dcc.Markdown("**&#9632 Patient Health Data**"), href='/apps/AppleWatch')
    return AppleWatch.layout, tabs


if __name__ == '__main__':
    app.run_server(debug=True)
