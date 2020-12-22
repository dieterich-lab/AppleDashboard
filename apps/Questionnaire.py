from app import app


import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,ALL
from datetime import datetime as dt
import pandas as pd
from datetime import date
import dash_table
import modules.load_data_from_database as ldd
from db import connect_db
from AppleWatch.Card import Card,Cards_view
from AppleWatch.trend_figure import figur_trend
from AppleWatch.summary_figure import figur2
from AppleWatch.day_figure import figur3
from AppleWatch.ECG import figur_ECG
from AppleWatch.selection_card import selection
from AppleWatch.table import table





layout= html.Div([

            dbc.Row([
                dbc.Col(dbc.Card(dbc.Col(selection)), width=3),
                dbc.Col([dbc.Col(dcc.Graph(id='example-graph2', ))], )]),
            dbc.Row([dbc.Col(dcc.Graph(id='example-graph1', ))]),
            html.Div(id='tabs-content2'),
            html.Div(id='output-state'),
            html.Div( dash_table.DataTable(
                id='table',
                page_size=10,
                style_table={'overflowX': 'auto'},
            )),


        ])


