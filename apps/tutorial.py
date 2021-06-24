import dash_html_components as html
from app import app

layout = html.Div([
    html.H1('Tutorial'),
    html.P('There are two tabs at the top of the page the first shows the dashboard for that patient, the second tab is '
           'not currently available.'
           'Under the tabs there are selectors, the first selector is used to choose the patient whose data is to be '
           'visualized, the second selector is used to set how the parameters are grouped by day/week/month. The next two'
           'following selector relates to the parameters to be displayed in graphs shown and the last selector sets the '
           'time window for which the parameters are calculated.'),
    html.Div([html.Img(src=app.get_asset_url("selector.png"),style={'height':'75%', 'width':'75%'}),], style={'textAlign': 'center'}),
    html.P('Below the selector is a section with a card component. The first card shows the most important information '
           'about the patient height, age, how all ECGs have been classified that have been collected by the Apple Watch.'
           ' The values in this card update based on which patient is selected. In this panel, the user can also choose '
           'to download the data in a tabular csv format to share the results or to conduct additional analyses. Next '
           'to the information card, there are six cards with the most important parameters: Resting/walking heart rate, '
           'step count, activity time, calories burned. The values are updated whenever a patient is selected and can '
           'be grouped by day/week/month. '),
    html.Div([html.Img(src=app.get_asset_url("cards.png"),style={'height':'75%', 'width':'75%'}),], style={'textAlign': 'center'}),
    html.P('A single table and graph is displayed below the cards, which shows values across the range of data '
           'collected and can be grouped by day/week/month. The graph is interconnected with the following two: '
           'Choosing a day/week/month in the former one will plot the data in the subsequent graphs according to this '
           'selected time window.'),
    html.Div([html.Img(src=app.get_asset_url("summary.png"),style={'height':'75%', 'width':'75%'}),], style={'textAlign': 'center'}),
    html.P('Next is a graph shows the values collected on a single day.'),
    html.Div([html.Img(src=app.get_asset_url("day_figure.png"),style={'height':'50%', 'width':'50%'}),], style={'textAlign': 'center'}),
    html.P('The graph below shows the heart rate trend over the last 4 days/weeks/months depending '
           'on how data are grouped.'),
    html.Div([html.Img(src=app.get_asset_url("tren_figure.png"),style={'height':'50%', 'width':'50%'}),], style={'textAlign': 'center'}),
    html.P('The last part contains a table with all ECG measurements collected by the Apple Watch for one '
           'patient. These ECGs are annotated with a classification in regard to measurement outcome (Sinus rhythm, '
           'atrial fibrillation, heart rate over 120/ under 50, inconclusive). The table allows the user to select one '
           'ECG for plotting. The plot of the selected ECG is displayed next to the table, giving the user the option to'
           'zoom into areas of interest. Additionally, it is also possible to download the data that is plotted on the '
           'graph.'),
    html.Div([html.Img(src=app.get_asset_url("ECG.png"),style={'height':'75%', 'width':'75%'}),], style={'textAlign': 'center'}),
    html.P('Group by month'),
    html.Div([html.Img(src=app.get_asset_url("month.png"),style={'height':'50%', 'width':'50%'}),], style={'textAlign': 'center'}),
    html.P('Group by week'),
    html.Div([html.Img(src=app.get_asset_url("week.png"),style={'height':'50%', 'width':'50%'}),], style={'textAlign': 'center'}),
])






