from flask import abort
from functools import wraps
from flask_login import current_user


# The role of wrapper is to verify if the current user is administrator
def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not current_user.admin_role:
            return abort(401) # If the logged user is not administrator, the UNAUTHORIZED error code is returned
        return f(*args, **kwargs) # Return the function with args and kwargs

    return wrap
