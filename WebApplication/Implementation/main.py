import os
from Implementation import Users, bcrypt
from flask_login import login_required, login_user, logout_user
from flask import render_template, request, url_for, flash, redirect, Blueprint

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_to_login = Users.query.filter_by(username=username).first()
        if user_to_login:
            if bcrypt.check_password_hash(user_to_login.password, password):
                login_user(user_to_login)
                return redirect(url_for('controls.home'))
            else:
                flash('Wrong credentials!', 'warning')
                return redirect(url_for('main.login'))
        else:
            flash('This account does not exist in our database! Please contact the administrator for creating one!',
                  'warning')
            return redirect(url_for('main.login'))
    return render_template('loginPage.html', username=os.environ.get('APP_ACCOUNT'),
                           password=os.environ.get('APP_PASSWORD'))


@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
