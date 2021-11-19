from app import app
from dash.dependencies import Input, Output, ALL
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import modules.load_data_from_database as ldd
import time

from db import connect_db

from Comparison import plots as p
from Comparison.selection_card import selection

# Selection
selection = selection()

# connection with database
rdb = connect_db()

layout = html.Div([
    dbc.Row([dbc.Col(selection)]),

    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='scatter_plot'), style={'height': '100%'}))]),

    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='box_plot'), style={'height': '100%'}), lg=6),
             dbc.Col(dbc.Card(dcc.Graph(id='histogram_plot'), style={'height': '100%'}), lg=6)]),

    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='linear_plot'), style={'height': '100%'}),lg=6),
            dbc.Col(dbc.Card(dcc.Graph(id='linear_plot1'), style={'height': '100%'}),lg=6)]),

    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='workout_plot'), style={'height': '100%'}))]),

    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='workout_plot2'), style={'height': '100%'}))]),

    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='during_night_plot'), style={'height': '100%'}))]),

    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='during_day_plot'), style={'height': '100%'}))]),

    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='during_night_day_plot'), style={'height': '100%'}))]),
])


# update box plot,histogram and scatter plot depends what was selected in drop down
@app.callback(
    [Output('box_plot', 'figure'),
     Output('histogram_plot', 'figure'),
     Output('scatter_plot', 'figure'),
     Output('linear_plot', 'figure'),
     Output('linear_plot1', 'figure')],
    [Input('group', 'value'),
     Input('linear plot', 'value'),
     Input('Bar chart', 'value')]
)
def figures(gr, linear, bar):

    df = ldd.plots(rdb, gr, linear, bar)
    df1, df2 = ldd.linear_plot(rdb, gr, linear, bar)
    fig_box_plot, fig_histogram, fig3 = p.figure_boxplot(df, gr, linear, bar)
    fig1, fig2 = p.figure_linear_plot(df1, df2, gr, linear, bar)

    return fig_box_plot, fig_histogram, fig3, fig1, fig2


@app.callback(
    [Output('workout_plot', 'figure'),
     Output('workout_plot2', 'figure')],
    [Input('group', 'value'),
     Input('Bar chart2', 'value')]
)
def fig(gr, bar2):

    data = ldd.Heart_Rate_workout_comparison(rdb, gr, bar2)
    df = ldd.Heart_Rate_workout_changes(rdb, gr, bar2)
    fig5, fig2 = p.figure_workout_plot(data, gr, bar2, df)

    return fig5, fig2


@app.callback(
    [Output('during_night_day_plot', 'figure'),
     Output('during_night_plot', 'figure'),
     Output('during_day_plot', 'figure')
     ],
    [Input('group', 'value'),
     Input('Bar chart2', 'value')]
)
def figu(gr, bar2):
    print('what is wrnog?')
    day_night = ldd.day_night(rdb)
    fig,fig1,fig2 = p.figure_day_night_plot(day_night)

    return fig,fig1,fig2


