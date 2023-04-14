from app import app
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import dcc, html
import modules.load_data_to_comparison_tab as ld
import modules.load_data_to_tab_health_data as ldd
import plotly.express as px
from db import connect_db
from Comparison import plots as p
from Comparison.selection_card import selection

rdb = connect_db()
label_activity, labels = ld.activity_type(rdb), ldd.label(rdb)
selection_health, selection_workout = selection(labels, label_activity)


layout = html.Div([
    dbc.Row([dbc.Col(selection_health)]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='scatter_plot')), style={'height': '100%'}))]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='box_plot')), style={'height': '100%'}), lg=6),
             dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='histogram_plot')), style={'height': '100%'}), lg=6)]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='linear_plot')), style={'height': '100%'}), lg=6),
            dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id='linear_plot1')), style={'height': '100%'}), lg=6)]),
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
     Input('Bar chart', 'value')])
def update_figures(group, linear, bar):
    df = ld.plots_comparison(rdb, group, linear, bar)
    df_linear = ld.plots_linear(rdb, group, linear, bar)
    if df.empty:
        fig_scatter, fig_box_plot, fig_histogram, fig1, fig2 = {}, {}, {}, {}, {}
    else:
        df_scatter = df.pivot(index=[group, 'date'], columns='key', values='Value').reset_index()
        fig_scatter = px.scatter(df_scatter, x=bar, y=linear, color=group, template='plotly_white',
                                 labels={bar: bar + ' [' + labels[bar] + ']',
                                         linear: linear + ' [' + labels[linear] + ']'})
        fig_scatter.update_layout(title='Comparison of all Patients based on two entities', title_x=0.5)
        fig_box_plot, fig_histogram = p.figure_box_hist(df, group, linear, bar, labels)
        fig1, fig2 = p.figure_linear_plot(df_linear, group, linear, bar, labels)
    return fig_scatter, fig_box_plot, fig_histogram,  fig1, fig2


# update workouts figures depending on the drop-dwons
@app.callback(
    [Output('workout_plot', 'figure'),
     Output('workout_plot2', 'figure')],
    [Input('group', 'value'),
     Input('Bar chart2', 'value')])
def update_workouts_figure(gr, bar):
    df_box, df_scatter = ld.workout_hr_comparison(rdb, gr, bar)
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
    df = ld.day_night(rdb, gr)
    if df.empty:
        fig = {}
    else:
        fig = px.box(df, x='day_night', y="Heart Rate", labels={"Heart Rate": "Average Heart Rate [bpm]"}, color=gr,
                     template='plotly_white')
        fig.update_layout(title='Comparison of Heart Rate during day and night', title_x=0.5)
    return fig
