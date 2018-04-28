from flask import Flask
from flask import request
from flask_login import logout_user
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)
app.secret_key = 'xxxxyyyyyzzzzz'

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
    print(user.user_email)
    return user.user_email


@app.route('/users/create', methods=['POST'])
def create_user_view():
    if request.form:
        new_user_email = request.form['user_email']
        user_exists = Users.query.filter_by(user_email=new_user_email).first()

        if not user_exists:
            new_user_model = Users(user_email=new_user_email)
            db.session.add(new_user_model)
            db.session.commit()
            created_user = Users.query.filter_by(user_email=new_user_email).first()
            return "New User crested: {} : {}"\
                .format(created_user.id, created_user.user_email)
        return "User already exists {} : {}".format(user_exists.id, user_exists.user_email)


@app.route('/login')
def login():
    email = request.args.get('user_email')
    user = Users.query.filter_by(user_email=email).first()
    if not user:
        return "no such user"
    login_user(user)
    return "User logged in"


@app.route("/user_profile")
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
