import re


# The role of the function is to validate password
def validate(password):
    if re.match('[a-zA-Z0-9]{6,}', password) is None:  # Verify that the password has at least 6 characters
        return 'Password must have at least 6 characters!', False
    elif re.match('.*[A-Z]+.*', password) is None:  # Verify if password has at least one upper case
        return 'The password must contain at least one upper case letter!', False
    elif re.match('.*[0-9]+.*', password) is None:  # Verify if the password has at least one digit
        return 'The password must contain at least one digit!', False
    else:
        return 'Valid password!', True  # Return error message and validation status
