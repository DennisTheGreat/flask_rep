from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig


app = Flask(__name__)
db = SQLAlchemy(app)
if not db:
    raise SystemExit('DB not loaded')
app.secret_key = 'xxxxyyyyzzzz'
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


from weather_forecast import dark_sky
from profile import profile_sys
app.register_blueprint(dark_sky)
app.register_blueprint(profile_sys)




