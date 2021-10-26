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
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='during_night_day_plot'), style={'height': '100%'}))]),
])



@app.callback(
    [Output('box_plot', 'figure'),
     Output('histogram_plot', 'figure'),
     Output('scatter_plot', 'figure')],
    [Input('group', 'value'),
     Input('linear plot', 'value'),
     Input('Bar chart', 'value')]
)
def figures1(gr,linear, bar):

    start_time = time.time()
    df1 = lddc.plots(rdb,gr, linear, bar)
    end_time = time.time()
    times = end_time - start_time
    print('t1 query',times)
    
    start_time = time.time()
    fig_box_plot,fig_histogram, fig3 = figure_boxplot(df1, gr,linear,bar)
    end_time = time.time()
    times = end_time - start_time
    print('t1 plot',times)

    return fig_box_plot, fig_histogram, fig3

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

    df1,df2 = lddc.linear_plot(rdb, gr, linear, bar)

    fig1,fig2 = figure_linear_plot(df1,df2,gr,linear,bar)
    end_time = time.time()
    times = end_time - start_time
    print('t2',times)


    return fig1,fig2



@app.callback(
    [Output('workout_plot', 'figure'),
     Output('workout_plot2', 'figure')],
    [Input('group', 'value'),
     Input('Bar chart2', 'value')]
)
def fig(gr,bar2):

    data = lddc.Heart_Rate_workout_comparison(rdb,gr, bar2)
    df = lddc.Heart_Rate_workout_changes(rdb, gr, bar2)
    fig5,fig2 = figure_workout_plot(data,gr,bar2,df)




    return fig5,fig2

"""
# Callback for toggling topic descriptions based on bubble chart
@app.callback(Output('box_plot', 'figure'),
              [Input('group', 'value'),
               Input('linear plot', 'value'),
               Input('Bar chart', 'value'),
              Input('box_plot2', 'restyleData')])
def update_topics_highlighted(gr, linear, bar,selected_topics):
    print(selected_topics)
    df1, df2 = lddc.linear_plot(rdb, gr, linear, bar)
    fig_box_plot, fig_box_plot2, fig_histogram, fig_histogram2, fig3 = figure_boxplot(df1, gr, linear, bar)

    return fig_box_plot
"""
