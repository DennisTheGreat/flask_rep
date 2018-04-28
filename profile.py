from app import app
from app import db
from flask import request
from flask import redirect
from flask import session
from flask import render_template
from utils import login_required
from models import Users


@app.route('/users/create/', methods=['GET', 'POST'])
def create_user_view():
    error = None
    if request.method == 'POST':
        email = request.args.get('user_email')
        name = request.args.get('user_name')
        password = request.args.get('user_password')
        user = Users.query.filter_by(user_email=email, password=password).first()
        if not user:
            if all([name, password, email]):
                created_user = Users(
                                     user_email=email,
                                     user_name=name,
                                     password=password
                                    )
                db.session.add(created_user)
                db.session.commit()
                return redirect(login)
            else:
                error = 'Fill all data'
        else:
            error = 'User already registered'
    return render_template('register.html', error=error)


@app.route('/login/')
def login():
    error = None
    email = request.args.get('user_email')
    password = request.args.get('user_password')
    user = Users.query.filter_by(user_email=email, password=password).first()
    if not user:
        error = 'email or password wrong'
    else:
        session['logged_in'] = True
    return render_template('login.html', error=error)


@app.route("/user_profile/")
@login_required(session)
def settings():
    return "User profile page"


@app.route("/logout")
@login_required(session)
def logout():
    session['logged_in'] = False
    return "user logout"