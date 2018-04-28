from app import app
from app import db
from flask import request
from flask import redirect
from flask import session
from utils import login_required
from models import Users


@app.route('/users/create/')
def create_user_view():
    email = request.args.get('user_email')
    name = request.args.get('user_name')
    password = request.args.get('user_password')
    user = Users.query.filter_by(user_email=email, password=password).first()
    if not user:
        created_user = Users(user_email=email, user_name=name, password=password)
        db.session.add(created_user)
        db.session.commit()
        return redirect(login)
    return "found user {} {}".format(user.user_email, user.user_name)


@app.route('/login/')
def login():

    email = request.args.get('user_email')
    password = request.args.get('user_password')
    user = Users.query.filter_by(user_email=email, password=password).first()
    if not user:
        return "Wrong email or pass"
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