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




# connection with database
rdb=connect_db()
df = ldd.Card(rdb)

month =['January', 'February', 'March', 'April','May', 'June', 'July', 'August','September','October','November','December']
day_of_week=['Monday', 'Tuesday', 'Wednesday', 'Thursday','Friday', 'Saturday', 'Sunday']


# Selection
selection = selection()

# Cards
cards1=Cards_view()


layout= html.Div([
            dbc.Col(
            html.Div(dash_table.DataTable(
                id='table1',
                page_size=10,

                editable=True,

                style_table={'overflowX': 'auto'},
                style_cell={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'minWidth': '180px'
                },


                sort_action='native',
                filter_action='native',
                sort_mode="multi",
                column_selectable="multi",
                selected_columns=[],
                selected_rows=[],
            ))),
            html.Div(id='datatable-interactivity-container'),
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col(dbc.Card(dbc.Col(selection)), width=3),
                dbc.Col(dcc.Graph(id='example-graph1', )),
            ]),
            dbc.Row([
            dbc.Col([(card) for card in cards1], width=4),
            dbc.Col([dbc.Col(dcc.Graph(id='example-graph2', ))])]),
            html.Div(id='tabs-content2'),
            html.Div(id='output-state'),


        ])

@app.callback(
    Output('table1', 'style_data_conditional'),
    Input('table1', 'selected_columns')
)
def update_styles(selected_columns):

    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


@app.callback(
    [Output('table1', 'data'),
     Output('table1', 'columns'),
     Output('table1', 'row_deletable'),
     Output('table1', 'row_selectable')],
     Input('group by', "value")
)
def update_table(value):
    result = table(df, value)
    data = result.to_dict('records')
    columns=[{"name": i, "id": i, "deletable": True, "selectable": True} for i in result.columns]
    fixed_columns = {'headers': True, 'data': 1}

    return data,columns,True,"multi"




@app.callback(
    Output('datatable-interactivity-container', "children"),
    Input('table1', "derived_virtual_data"),
    Input('table1', "derived_virtual_selected_rows"),
    Input('group by', "value"))
def update_graphs(rows, derived_virtual_selected_rows,value):

    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
    result = table(df, value)
    dff = result if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff["country"],
                        "y": dff[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in ["pop", "lifeExp", "gdpPercap"] if column in dff
    ]


@app.callback(Output('tabs-content2', 'children'),[Input('group by', 'value')])
def render_content2(tab):
    if tab == 'D':
        return html.Div([


            html.Br(),
            dbc.Col([dbc.Col(dcc.Graph(id='example-graph4',
                                       hoverData={'points': [{'customdata': '1'}]}))]),
            html.Br(),
            dbc.Card([dbc.Row([dbc.Col([
                    "Number:",
                    dcc.Dropdown(
                        id='numbera',
                    ),],width=1)]),
                dbc.Row([dbc.Col(dcc.Graph(id='example-graph3', ))])])
        ])
    else:
        return html.Div([
            html.Br(),
        ])


@app.callback(
    Output('dropdown-container', 'children'),
    [Input('group by', "value")],
)
def Update_selection(value):
    if value == 'M':
        new_dropdown = html.Div([dcc.Dropdown(
            id= {
            'type': 'filter-dropdown',
            'index': 0
        },
            options=[{'label': name, 'value': i} for (i,name) in enumerate(month,1)],
            value='1'
        )])
    elif value == 'W':
        week = []
        for i in range(1, 53):
            a = dt.strptime('2020 {} 1'.format(i), '%G %V %u').date()
            b = dt.strptime('2020 {} 7'.format(i), '%G %V %u').date()
            c = str(a)+'-'+ str(b)
            week.append(c)

        new_dropdown = html.Div([dcc.Dropdown(
            id={
            'type': 'filter-dropdown',
            'index': 0
        },
            options=[{'label': name, 'value': i} for (i,name) in enumerate(week,1)],
            value='1'
        )])
    elif value == 'DOW':
        new_dropdown = html.Div([dcc.Dropdown(
            id={
            'type': 'filter-dropdown',
            'index': 1
        },
            options=[{'label': name, 'value': i} for (i,name) in enumerate(day_of_week,1)],
            value = '1'
        )])
    elif value == 'D':
        new_dropdown = html.Div([dcc.DatePickerSingle(
            id={
            'type': 'filter-dropdown',
            'index': 0
        },
            min_date_allowed=dt(2015, 8, 5),
            max_date_allowed=dt(2021, 9, 19),
            initial_visible_month=dt(2020, 3, 27),
            display_format='D/M/Y',
            date=date(2020,2,27)),])

    return new_dropdown


# callback for card
@app.callback(
    [Output("RestingHeartRate", "children"),
     Output("WalkingHeartRate", "children"),
     Output("step", "children"),
     Output("HeartRate_mean", "children"),
     Output("Exercise_minute", "children"),
     Output("ActivitySummary2", "children")],
    [Input({"index":ALL,'type':'filter-dropdown'}, 'date'),
     Input({"index":ALL,'type':'filter-dropdown'}, 'value'),
     Input("group by", "value"),
     Input("patients1","value"),
     Input("choice", "value")],
)
def Update_Card(date,value,group,patient1,choice):
    if not date and not value:
        RestingHeartRate,WalkingHeartRate,step,HeartRate_mean,Exercise_minute,ActivitySummary2=0,0,0,0,0,0,
    else:
        date = pd.to_datetime(date[-1])
        value = value[-1]
        RestingHeartRate,WalkingHeartRate,step,HeartRate_mean,Exercise_minute,ActivitySummary2= Card(date,value,group,patient1,choice,df)
    return RestingHeartRate,WalkingHeartRate,step,HeartRate_mean,Exercise_minute,ActivitySummary2


# callback for trend_figure
@app.callback(
    Output('example-graph2', 'figure'),
    [Input( {"index":ALL,'type':'filter-dropdown'}, 'value'),
     Input({'index':ALL,'type':'filter-dropdown'}, 'date'),
     Input('linear plot', 'value'),
     Input("group by", "value"),
     Input("patients1", "value"),],
)
def Update_figure_trend(value,date,input_value,group,patient1):
    if date and value:
        date = pd.to_datetime(date[-1])
        value = value[-1]
        figa=figur_trend(date,value,input_value,group,patient1,df)
    else:
        figa = {}

    return figa


@app.callback(
    Output('example-graph1', 'figure'),
    [Input('linear plot', 'value'),
     Input('Bar chart', 'value'),
     Input("group by", "value"),
     Input("patients1", "value"),]
)
def Update_summary_figure(input_value1,input_value2,group,patient1):
    fig=figur2(input_value1,input_value2,group,patient1,df)
    return fig


# Selected Data in the Histogram updates the Values in the DatePicker
@app.callback(
    Output({'index': ALL,'type':'filter-dropdown'}, 'date'),
    [Input("example-graph1", "selectedData"), Input("example-graph1", "clickData")],
)
def update_bar_selector(value, clickData):
    holder = ['2020-02-27']
    if clickData:
        holder=[]
        holder.append(str(clickData["points"][0]["x"]))
    if value:
        holder=[]
        for x in value["points"]:
            holder.append(str(int(x["x"])))
    return list(set(holder))


@app.callback(
    Output('example-graph4', 'figure'),
    [Input({"index":ALL,'type':'filter-dropdown'}, 'date'),
     Input("patients1", "value"),]
)
def Update_figure_day(date,patient1):
    for date in date:
        date = pd.to_datetime(date)
    if date == None or not date :
        fig3={}
    else:
        fig3=figur3 (date,patient1,df)
    return fig3


@app.callback(
    Output('numbera', 'options'),
    [Input({"index":ALL,'type':'filter-dropdown'}, 'date')],)
def number_ECG(date):
    df_ECG = ['0']
    for date in date:
        if date == None or not date :
            df_ECG = ['0']
        else:
            date = pd.to_datetime(date).date()
            df_ECG = ldd.ECG_number(ldd.rdb, date)
            if len(df_ECG) == 0:
                df_ECG = ['0']
    return [{'label': i, 'value': i} for i in df_ECG]


@app.callback(
    Output('numbera', 'value'),
    [Input('numbera', 'options')])
def set_number_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('example-graph3', 'figure'),
    [Input({"index":ALL,'type':'filter-dropdown'}, 'date'),
     Input('numbera', 'value'),
     Input("patients1", "value"),]
)
def Update_ECG(date,num,patient1):
    fig={}
    for date in date:
        if date == None or not date :
            fig={}
        else:
            date = pd.to_datetime(date).date()
            fig=figur_ECG(date,num,patient1)
    return fig

