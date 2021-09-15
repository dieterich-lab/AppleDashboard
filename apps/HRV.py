from app import app
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, ALL
from dash import dcc
from dash import html
import modules.load_data_from_database as ldd
import plotly.express as px
import pandas as pd
from dash import dash_table

from db import connect_db


from ECG_analyze.selection_card import selection
from ECG_analyze.ECG_plot import update_ecg_figure


# Selection
selection = selection()

# connection with database
rdb = connect_db()

# get data from database

#dum = calculate_HRR(data,df)

layout = html.Div([
    dbc.Row([dbc.Col(selection)]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='ecg_plot'), style={'height': '100%'}))]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dash_table.DataTable(
            id='ecg_table',
            style_table={'overflowX': 'auto'},
            page_size=11,
            filter_action='native',
            sort_action="native",
            sort_mode="multi",
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            }

        ), style={'height': '100%'}))]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='scatter_plot_ecg'), style={'height': '100%'}))]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='box_plot_ecg'), style={'height': '100%'}))]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Graph(id='fix_tool'), style={'height': '100%'}))]),

])


# update table2
@app.callback(
    [Output('ecg_table', 'data'),
     Output('ecg_table', 'columns'),
     Output('ecg_table', 'row_selectable'),
     Output('ecg_table', 'selected_rows')],
    Input("patient", "value")
)
def update_table_ecg(patient):
    df, df2, df3 = ldd.irregular_ecg(rdb, patient)
    data = df3.to_dict('records')
    columns = [{"name": i, "id": i} for i in df3.columns]
    return data, columns, 'single', [0]

# update ECG figure
@app.callback(
    Output('ecg_plot', 'figure'),
    [Input('ecg_table', "selected_rows"),
     Input("patient", "value"),
     Input("ecg_table", 'data')]
)
def update_ecg2(data, patient,data_tab):
    if not data_tab:
        fig = {}
    else:
        day = data_tab[data[0]]['Day']
        number = data_tab[data[0]]['number']
        fig, df_ecg = update_ecg_figure(day, number, patient)
    return fig


@app.callback(
    Output('scatter_plot_ecg', 'figure'),
    [Input('patient', "value"),
     Input("x axis", "value"),
     Input("y axis", 'value')]
)
def update_scatter_plot_ecg(patient, x_axis, y_axis):
    df = ldd.scatter_plot_ecg(rdb, patient, x_axis, y_axis)
    fig = px.scatter(df, x=x_axis, y=y_axis)
    return fig

# update scatter_plot figure
@app.callback(
    Output('box_plot_ecg', 'figure'),
     Input("x axis", 'value')
)
def update_box_plot_ecg(x_axis):
    df = ldd.box_plot_ecg(rdb,x_axis)
    fig = px.box(df, x="Patient", y=x_axis)
    return fig
