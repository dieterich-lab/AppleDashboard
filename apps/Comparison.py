from app import app
from dash.dependencies import Input, Output, ALL
import dash_bootstrap_components as dbc
from dash import dcc, html
import modules.load_data_from_database as ldd
import time
import plotly.express as px

from db import connect_db

from Comparison import plots as p
from Comparison.selection_card import selection

# Selection
selection_health, selection_workout = selection()

# connection with database
rdb = connect_db()

layout = html.Div([
    dbc.Row([dbc.Col(selection_health)]),

    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='scatter_plot')), style={'height': '100%'}))]),

    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='box_plot')), style={'height': '100%'}), lg=6),
             dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='histogram_plot')), style={'height': '100%'}), lg=6)]),

    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='linear_plot')), style={'height': '100%'}),lg=6),
            dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='linear_plot1')), style={'height': '100%'}),lg=6)]),
    dbc.Row([dbc.Col(selection_workout)]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='workout_plot')), style={'height': '100%'}))]),

    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='workout_plot2')), style={'height': '100%'}))]),

    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='during_night_day_plot')), style={'height': '100%'}))]),
])


# update box plot,histogram and scatter plot depending on the drop-downs
@app.callback(
    [Output('scatter_plot', 'figure'),
     Output('box_plot', 'figure'),
     Output('histogram_plot', 'figure'),
     Output('linear_plot', 'figure'),
     Output('linear_plot1', 'figure')],
    [Input('group', 'value'),
     Input('linear plot', 'value'),
     Input('Bar chart', 'value')]
)
def update_figures(gr, linear, bar):

    df = ldd.plots_comparison(rdb, gr, linear, bar)
    if df.empty:
        fig_scatter, fig_box_plot, fig_histogram = {}, {}, {}
    else:
        df_scatter = df.pivot(index=[gr, 'date'], columns='type', values='Value').reset_index()
        fig_scatter = px.scatter(df_scatter, x=bar, y=linear, color=gr, template='plotly_white')
        fig_box_plot, fig_histogram = p.figure_box_hist(df, gr, linear, bar)

    df_linear, df_bar = ldd.linear_plot(rdb, gr, linear, bar)
    if df_linear.empty:
        fig1, fig2 = {}, {}
    else:
        fig1, fig2 = p.figure_linear_plot(df_linear, df_bar, gr, linear, bar)

    return fig_scatter, fig_box_plot, fig_histogram,  fig1, fig2


# update workouts figures depending on the drop-dwons
@app.callback(
    [Output('workout_plot', 'figure'),
     Output('workout_plot2', 'figure')],
    [Input('group', 'value'),
     Input('Bar chart2', 'value')]
)
def update_workouts_figure(gr, bar):

    df_box, df_scatter = ldd.workout_hr_comparison(rdb, gr, bar)
    if df_box.empty:
        fig_box, fig_linear = {}, {}
    else:
        fig_box, fig_linear = p.figure_workout_plot(df_box, df_scatter, gr, bar)

    return fig_box, fig_linear


# update day_night box plot depending on the drop-downs
@app.callback(
    Output('during_night_day_plot', 'figure'),
    Input('group', 'value')
)
def update_day_night_box(gr):
    df = ldd.day_night(rdb, gr)
    if df.empty:
        fig = {}
    else:
        fig = px.box(df, x='day_night', y="Heart rate", color=gr, template='plotly_white')

    return fig


