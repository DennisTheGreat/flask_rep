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


@app.route('/users/create/', methods=['GET', 'POST'])
def create_user_view():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_email = request.form.get('user_email')

        if all([username, password, user_email]):
            new_user = Users(username=username,
                             password=password,
                             user_email=user_email)
            db.session.add(new_user)
            db.session.commit()
            return redirect('login')
        else:
            error = 'Fill all data'
    return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(user_email=email,
                                     password=password).first()
        if not user:
            error = 'email or password wrong'
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
