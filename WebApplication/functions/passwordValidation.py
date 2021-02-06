import re


def validate(password):
    if re.match('[a-zA-Z0-9]{6,}', password) is None:
        return 'Password must have at least 6 characters!', False
    elif re.match('.*[A-Z]+.*', password) is None:
        return 'The password must contain at least one upper case letter!', False
    elif re.match('.*[0-9]+.*', password) is None:
        return 'The password must contain at least one digit!', False
    else:
        return 'Valid password!', True
