import dash
import dash_bootstrap_components as dbc
from db import connect_db
from modules.import_scheduler import Scheduler
import os

rdb=connect_db()

# Import data using function scheduler from package modules
if os.environ.get('IMPORT_DISABLED') is None:
    scheduler = Scheduler(rdb)
    scheduler.start()
    scheduler.stop()

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

