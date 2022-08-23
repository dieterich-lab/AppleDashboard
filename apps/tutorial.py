from dash import html
from app import app

layout = html.Div([
    html.H1('Tutorial'), html.Br(),
    html.P('There are four tabs at the top of the page.'),
    html.P('1. The first tab shows the dashboard for an individual patient.'),
    html.Img(src=app.get_asset_url("patient_health_data_1.png"), style={'height': '50%', 'width': '50%'}),
    html.Img(src=app.get_asset_url("patient_health_data_2.png"), style={'height': '50%', 'width': '50%'}),
    html.P('2. The second tab shows workouts activity and heart rate during workout for individual patient.'),
    html.Img(src=app.get_asset_url("workout_1.png"), style={'height': '50%', 'width': '50%'}),
    html.Img(src=app.get_asset_url("workout_2.png"), style={'height': '50%', 'width': '50%'}),
    html.P('3. The third tab allows you to compare data collected by the Apple Watch between patients, '
           'patient age or patient gender.'),
    html.Img(src=app.get_asset_url("comparison_1.png"), style={'height': '50%', 'width': '50%'}),
    html.Img(src=app.get_asset_url("comparison_2.png"), style={'height': '50%', 'width': '50%'}),
    html.Img(src=app.get_asset_url("comparison_3.png"), style={'height': '50%', 'width': '50%'}),
    html.Img(src=app.get_asset_url("comparison_4.png"), style={'height': '50%', 'width': '50%'}),
    html.P('4. The fourth tab shows ECG with detected RR peaks and HRV analysis in the time domain.'),
    html.Img(src=app.get_asset_url("ecg_1.png"), style={'height': '50%', 'width': '50%'}),
    html.Img(src=app.get_asset_url("ecg_2.png"), style={'height': '50%', 'width': '50%'}),
])






