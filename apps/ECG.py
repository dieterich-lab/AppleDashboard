import dash_bootstrap_components as dbc
import modules.load_data_to_ecg_tab as ld
import plotly.express as px
from dash.dependencies import Input, Output
from dash import dcc, html, dash_table
from app import app
from db import connect_db

from ECG_analyze.selection_card import selection
from ECG_analyze.ECG_plot import update_ecg_figure

hrv_features = ['hrv', 'sdnn', 'senn', 'sdsd', 'pnn20', 'pnn50']

rdb = connect_db()
df = ld.table_hrv(rdb)
selection = selection(hrv_features)

layout = html.Div([
    dbc.Row([dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='ecg_plot')), style={'height': '100%'}))]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card([
        html.A('Download table', id='link-hrv'),
        dash_table.DataTable(
            id='hrv_table',
            style_table={'overflowX': 'auto'},
            page_size=11,
            filter_action='native',
            sort_action="native",
            sort_mode="multi",
            selected_rows=[0],
            row_selectable='single',
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }],
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            })], style={'height': '100%'}))]),
    html.Br(),
    dbc.Row(dbc.Col(dbc.Card([dbc.Row([
        dbc.Col(dbc.Card(selection), lg=2),
        dbc.Col(dbc.Card(dcc.Graph(id='scatter_plot_hrv')), lg=10)])]))),
    html.Br(),
    dbc.Row(dbc.Col(dbc.Card([dbc.Col(html.Br()),
                              dbc.Col(dcc.Dropdown(id='group',
                                                   style={'width': '150px'},
                                                   options=[{'label': name, 'value': name} for name in hrv_features],
                                                   value=hrv_features[1],
                                                   clearable=False)),
                              dbc.Col(dcc.Graph(id='box_plot_hrv'))], style={'height': '100%'}))),


])


# update ECG figure
@app.callback(
    Output('ecg_plot', 'figure'),
    [Input('hrv_table', "selected_rows"),
     Input("hrv_table", 'data')])
def update_ecg(data, data_tab):
    if not data_tab:
        fig = {}
    else:
        patient, day, time = data_tab[data[0]]['patient_id'], data_tab[data[0]]['day'], data_tab[data[0]]['time']
        fig, df_data = update_ecg_figure(day, time, patient, 'R_peaks')
    return fig


# update scatter plot figure
@app.callback(
    Output('scatter_plot_hrv', 'figure'),
    [Input("x axis", "value"),
     Input("y axis", 'value')])
def update_scatter_plot_ecg(x_axis, y_axis):
    df_scatter = ld.scatter_plot_ecg(rdb, x_axis, y_axis)
    if df.empty:
        fig = {}
    else:
        fig = px.scatter(df_scatter, x=x_axis, y=y_axis, template='plotly_white', color="patient_id")
    return fig


# update box_plot figure
@app.callback(Output('box_plot_hrv', 'figure'),
              Input("group", 'value'))
def update_box_plot_ecg(y_axis):
    df_box_plot = ld.box_plot_ecg(rdb, y_axis)
    if df.empty:
        fig = {}
    else:
        fig = px.box(df_box_plot, x="patient_id", y=y_axis, template='plotly_white')
    return fig
