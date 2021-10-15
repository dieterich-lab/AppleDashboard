from app import app
from dash.dependencies import Input, Output, ALL
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import modules.load_data_from_database_comparison as lddc
import time

from db import connect_db

from Comparison.box_plot import figure_boxplot,figure_linear_plot,figure_workout_plot
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
    dbc.Row([dbc.Col(dbc.Card(dbc.Row([dbc.Card(dcc.Graph(id='box_plot'),style={'width': '45%'}),
                                       dbc.Card( dcc.Graph(id='box_plot2'),style={'width': '55%'})])), lg=6),
             dbc.Col(dbc.Card(dbc.Row([dbc.Card(dcc.Graph(id='histogram_plot'),style={'width': '45%'}),
                                       dbc.Card( dcc.Graph(id='histogram_plot2'),style={'width': '55%'})])), lg=6)]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='linear_plot'), style={'height': '100%'}))]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='linear_plot1'), style={'height': '100%'}))]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='workout_plot'), style={'height': '100%'}))]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='during_night_day_plot'), style={'height': '100%'}))]),
])



@app.callback(
    [Output('box_plot', 'figure'),
     Output('box_plot2', 'figure'),
     Output('histogram_plot', 'figure'),
     Output('histogram_plot2', 'figure'),
     Output('scatter_plot', 'figure')],
    [Input('group', 'value'),
     Input('linear plot', 'value'),
     Input('Bar chart', 'value')]
)
def figures1(gr,linear, bar):

    start_time = time.time()
    df1 = lddc.plots(rdb,gr, linear, bar)
    fig_box_plot,fig_box_plot2,fig_histogram, fig_histogram2,fig3 = figure_boxplot(df1, gr,linear,bar)
    end_time = time.time()
    times = end_time - start_time
    print('t1',times)

    return fig_box_plot,fig_box_plot2, fig_histogram,fig_histogram2, fig3

""""""
@app.callback(
    [Output('linear_plot', 'figure'),
     Output('linear_plot1', 'figure')],
    [Input('group', 'value'),
     Input('linear plot', 'value'),
     Input('Bar chart', 'value')]
)
def figures(gr,linear, bar):

    start_time = time.time()
    df = lddc.linear_plot(rdb, linear)
    fig4 = figure_linear_plot(df, gr, linear)
    end_time = time.time()
    times = end_time - start_time
    print('t2',times)

    return fig4,fig4



@app.callback(
     Output('workout_plot', 'figure'),
    [Input('group', 'value'),
     Input('Bar chart2', 'value')]
)
def fig(gr,bar2):

    data = lddc.Heart_Rate_workout_comparison(rdb,gr, bar2)
    fig5 = figure_workout_plot(data,gr,bar2)

    return fig5
