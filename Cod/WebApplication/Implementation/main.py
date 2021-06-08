import os
from Implementation import Users, bcrypt
from flask_login import login_required, login_user, logout_user
from flask import render_template, request, url_for, flash, redirect, Blueprint

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Verify if there is a POST request
        username = request.form.get('username')  # Get the username from the form
        password = request.form.get('password')  # Get the password from the form
        user_to_login = Users.query.filter_by(username=username).first()  # Find the user specified by username
        if user_to_login:  # Verify if an user was found
            if bcrypt.check_password_hash(user_to_login.password, password):  # Verify if the passwords matches
                login_user(user_to_login)  # Log in the user
                return redirect(url_for('controls.home'))  # Redirect to home page
            else:
                # If the credentials are wrong, a message will be displayed and the user will be redirected to login
                flash('Wrong credentials!', 'warning')
                return redirect(url_for('main.login'))
        else:
            # If the account does not exist, a message will be displayed and the user will be redirected to login
            flash('This account does not exist in our database! Please contact the administrator for creating one!',
                  'warning')
            return redirect(url_for('main.login'))
    return render_template('loginPage.html', username=os.environ.get('APP_ACCOUNT'),
                           password=os.environ.get('APP_PASSWORD'))  # Process and display the loginPage.html


@main.route('/logout', methods=['GET', 'POST'])
@login_required  # Access function only if an user is logged in
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('main.login'))  # Redirect the user to login page
