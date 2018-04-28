from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_sqlalchemy import SQLAlchemy

from utils import login_required

app = Flask(__name__)
db = SQLAlchemy(app)
app.secret_key = 'xxxxyyyyyzzzzz'

if not db:
    raise SystemExit('DB not loaded')
from config import DevelopmentConfig
from models import Users

app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def main_view():
    return render_template('index.html')


@app.route('/users/<id>/')
def hello_world(id):
    user = Users.query.get(id)
    return render_template('template.html', user=user)


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('username')
        # password = request.form.get('password')
        user = Users.query.filter_by(user_email=email).first()
        if not user:
            error = 'email'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('hello_world', **{'id': user.id}))
    return render_template('login.html', error=error)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    flash('You were logged out')
    return "user logout"


@app.route('/test_perm')
@login_required(session)
def test_view():
    return 'Authorized'
