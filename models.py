from flask_login import UserMixin

from forecast_app import db


class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String())

    def __repr__(self):
        return '<id {}>'.format(self.id)