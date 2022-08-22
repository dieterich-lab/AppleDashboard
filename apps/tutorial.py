from dash import html
from app import app

layout = html.Div([
    html.H1('Tutorial'), html.Br(),
    html.P('There are four tabs at the top of the page.'),
    html.P('1. The first tab shows the dashboard for individual patient.'),
    html.P('2. The second tab shows the workouts activity and heart rate during the workout for individual patient.'),
    html.P('3. The third tab let to compare data collected by Apple Watch between patient, age of patient or gender of '
           'patients.'),
    html.P('4. The fourth tab shows ECG with detected RR peaks and HRV analyse in time domain.'),

])






