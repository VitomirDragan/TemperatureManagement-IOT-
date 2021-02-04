from flask import abort
from functools import wraps
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not current_user.admin_role:
            return abort(401)
        return f(*args, **kwargs)

    return wrap
