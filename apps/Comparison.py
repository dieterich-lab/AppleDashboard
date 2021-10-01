from app import app
from dash.dependencies import Input, Output, ALL
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import modules.load_data_from_database_comparison as lddc

from db import connect_db

from Comparison.box_plot import figure_boxplot, figure_scatter_plot,figure_linear_plot,figure_workout_plot
from Comparison.selection_card import selection

# Selection
selection = selection()

# connection with database
rdb = connect_db()

layout = html.Div([
    dbc.Row([dbc.Col(selection)]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='box_plot'), style={'height': '100%'}), lg=6),
             dbc.Col(dbc.Card(dcc.Graph(id='histogram_plot'), style={'height': '100%'}), lg=6)]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='scatter_plot'), style={'height': '100%'}))]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='linear_plot'), style={'height': '100%'}))]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='workout_plot'), style={'height': '100%'}))]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='during_night_day_plot'), style={'height': '100%'}))]),
])



@app.callback(
    [Output('box_plot', 'figure'),
     Output('histogram_plot', 'figure'),
     Output('scatter_plot', 'figure'),
     Output('linear_plot', 'figure'),
     Output('workout_plot', 'figure')],
    [Input('group', 'value'),
     Input('linear plot', 'value'),
     Input('Bar chart', 'value'),
     Input('Bar chart2', 'value')]
)
def figures(gr,linear, bar, bar2):
    df1 = lddc.box_plot(rdb, linear, bar)
    df2 = lddc.scatter_plot(rdb, linear, bar)
    df = lddc.linear_plot(rdb, linear)

    data = lddc.Heart_Rate_workout_comparison(rdb, bar2)

    fig_box_plot,fig_histogram = figure_boxplot(df1, gr,)
    fig3 = figure_scatter_plot(df2, gr, linear, bar)
    fig4 = figure_linear_plot(df, gr, linear)
    fig5 = figure_workout_plot(data, gr)
    return fig_box_plot, fig_histogram, fig3, fig4, fig5
