from app import app
from dash.dependencies import Input, Output, ALL
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import modules.load_data_from_database as ldd

from db import connect_db


from Comparison.box_plot import figure_boxplot, figure_histogram,figure_scatter_plot
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
])


# update table1 depends what values are chosen in selector
@app.callback(
    [Output('box_plot', 'figure'),
     Output('histogram_plot', 'figure'),
     Output('scatter_plot', 'figure')],
    [Input('group by', "value"),
    Input('linear plot', 'value'),
    Input('Bar chart', 'value')]
)
def figures(group, linear, bar):
    df1,df3 = ldd.box_plot1(rdb, linear, bar)
    df = ldd.histogram_plot(rdb, group, linear)
    df2 = ldd.scatter_plot(rdb, group, linear, bar)
    fig = figure_boxplot(df1,df3)
    fig2 = figure_histogram(df1)
    fig3 = figure_scatter_plot(df2, group, linear, bar)

    return fig, fig2, fig3
