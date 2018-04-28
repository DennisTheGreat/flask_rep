from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from dark_sky_api import DarkSky
from utils import login_required
from flask import session


app = Flask(__name__)
db = SQLAlchemy(app)
app.secret_key = 'xxxxyyyyzzzz'


if not db:
    raise SystemExit('DB not loaded')
from config import DevelopmentConfig
from models import Users


app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/users/<id>/')
def hello_world(id):
    from flask import render_template
    user = Users.query.get(id)
    return render_template('index.html', user=user)


@app.route('/users/create/')
def create_user_view():
    email = request.args.get('user_email')
    name = request.args.get('name')
    user = Users.query.filter_by(user_email=email).first()
    if not user:
        created_user = Users(user_email=email, user_name=name)
        db.session.add(created_user)
        db.session.commit()
        return "test user {} created".format(created_user.user_email)
    return "found user {} {}".format(user.user_email, user.user_name)


@app.route('/login/')
def login():
    email = request.args.get('user_email')
    user = Users.query.filter_by(user_email=email).first()
    if not user:
        return "no such user"
    session['logged_in'] = True
    return "Login {} {}".format(user.user_email, user.user_name)


@app.route("/user_profile/")
@login_required(session)
def settings():
    return "User profile page"


@app.route("/logout")
@login_required(session)
def logout():
    session['logged_in'] = False
    return "user logout"


@app.route('/test_perms')
def login_required():
    return 'Authorized'


@app.route('/w/')
@login_required(session)
def dark_sky_new():
    city = request.args.get('city')
    params = request.args.get('params')
    units = request.args.get('units')
    weather = DarkSky()
    weather.set_api_key('1f59ae2ad5dbb81ba6fea2a20c2f5db5')
    weather.set_api_params(params)
    weather.set_locate(city)
    weather.set_units(units)
    return weather.get_response()
