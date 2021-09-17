from app import app
from dash.dependencies import Input, Output, ALL
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import modules.load_data_from_database as ldd

from db import connect_db


from Comparison.box_plot import figure_boxplot, figure_histogram,figure_scatter_plot,figure_linear_plot,figure_workout_plot
from Comparison.selection_card import selection




# Selection
selection = selection()

# connection with database
rdb = connect_db()

# get data from database

#dum = calculate_HRR(data,df)

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


# update table1 depends what values are chosen in selector
@app.callback(
    [Output('box_plot', 'figure'),
     Output('histogram_plot', 'figure'),
     Output('scatter_plot', 'figure'),
     Output('linear_plot', 'figure'),
     Output('workout_plot', 'figure')],
    [Input('group', 'value'),
     Input('group by', "value"),
     Input('linear plot', 'value'),
     Input('Bar chart', 'value'),
     Input('Bar chart2', 'value')]
)
def figures(gr,group, linear, bar, bar2):
    df1,df3 = ldd.box_plot1(rdb, linear, bar)
    df = ldd.linear_plot(rdb, group, linear)
    df2 = ldd.scatter_plot(rdb, group, linear, bar)
    data = ldd.Heart_Rate_workout_comparison(rdb, bar2)

    fig = figure_boxplot(df1, df3, gr, linear,bar)
    fig2 = figure_histogram(df1, gr, linear)
    fig3 = figure_scatter_plot(df2, gr, group, linear, bar)
    fig4 = figure_linear_plot(df, gr, group, linear)
    fig5 = figure_workout_plot(data, gr)
    return fig, fig2, fig3, fig4, fig5
