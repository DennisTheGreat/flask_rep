from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig


app = Flask(__name__)
db = SQLAlchemy(app)
from models import Users
from profile import logout
from weather_forecast import dark_sky_new
if not db:
    raise SystemExit('DB not loaded')
app.secret_key = 'xxxxyyyyzzzz'
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



