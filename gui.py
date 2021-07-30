from flaskwebgui import FlaskUI
from main import app

FlaskUI(app, width=1200, height=500).run()