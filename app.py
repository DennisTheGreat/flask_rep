from flask import Flask
from flask import request
from flask_login import logout_user
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy
from dark_sky_api import DarkSky

app = Flask(__name__)
db = SQLAlchemy(app)
app.secret_key = '1f59ae2ad5dbb81ba6fea2a20c2f5db5'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

if not db:
    raise SystemExit('DB not loaded')
from config import DevelopmentConfig
from models import Users

app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/users/<id>/')
def hello_world(id):
    user = Users.query.get(id)
    return user.user_email


@app.route('/users/create/')
def create_user_view():
    email = request.args.get('user_email')
    user = Users.query.filter_by(user_email=email).first()
    if not user:
        created_user = Users(user_email=email)
        db.session.add(created_user)
        db.session.commit()
        return "test user {} created".format(created_user.user_email)
    return "found user {}".format(user.user_email)


@app.route('/login/')
def login():
    email = request.args.get('user_email')
    user = Users.query.filter_by(user_email=email).first()
    if not user:
        return "no such user"
    login_user(user)
    return "User logged in"


@app.route("/user_profile/")
@login_required
def settings():
    return "User profile page"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first()


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "user logout"


@app.route('/w/')
@login_required
def dark_sky_new():
    city = request.args.get('city')
    params = request.args.get('params')
    units = request.args.get('units')
    weather = DarkSky()
    weather.set_api_key(app.secret_key)
    weather.set_api_params(params)
    weather.set_locate(city)
    weather.set_units(units)
    return weather.get_response()
