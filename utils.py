

from functools import wraps
from werkzeug.exceptions import abort


def login_required(session):
    def deco(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if session.get('logged_in'):
                return func(*args, **kwargs)
            else:
                return abort(403)

        return decorated_view

    return deco
