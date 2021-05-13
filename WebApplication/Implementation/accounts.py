from flask import Blueprint
from flask_login import login_required, current_user
from Implementation.functions.wrappers import admin_required
from Implementation.functions.passwordValidation import validate
from Implementation import Users, bcrypt, db
from Implementation.functions.convert import toBoolean
from flask import render_template, request, url_for, flash, redirect

accounts = Blueprint('accounts', __name__)


@accounts.route('/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        confirm_password = request.form.get('confirmPassword')
        admin_role = toBoolean(request.form.get('admin_role'))
        if bcrypt.check_password_hash(password, confirm_password):
            errorMessage, validationStatus = validate(confirm_password)
            if (validationStatus):
                user = Users(username=username, password=password, admin_role=admin_role)
                try:
                    db.session.add(user)
                    db.session.commit()
                    flash('You successfully created a new account!', 'info')
                    return redirect(url_for('accounts.register'))
                except:
                    flash('There was a problem creating this new account!', 'warning')
                    return redirect(url_for('accounts.register'))
            else:
                flash(errorMessage, 'warning')
        else:
            flash('The passwords do not match!', 'warning')
            return redirect(url_for('accounts.register'))
    return render_template('registerPage.html')


@accounts.route('/viewAccounts', methods=['GET', 'POST'])
@login_required
@admin_required
def viewAccounts():
    users = Users.query.all()
    return render_template('accountsPage.html', users=users)


@accounts.route('/deleteAccount/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def deleteAccount(id):
    user = Users.query.filter_by(id=id).first()
    try:
        db.session.delete(user)
        db.session.commit()
        flash('The account was successfully deleted!', 'info')
        return redirect(url_for('accounts.viewAccounts'))
    except:
        flash('There was a problem deleting the account!', 'warning')
        return redirect(url_for('accounts.viewAccounts'))


@accounts.route('/giveAdminRights/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def giveAdminRights(id):
    user = Users.query.filter_by(id=id).first()
    try:
        user.admin_role = True
        db.session.commit()
        flash('Succesfully updated the admin rights!', 'info')
        return redirect(url_for('accounts.viewAccounts'))
    except:
        flash('There was a problem updating the admin rights!', 'warning')
        return redirect(url_for('accounts.viewAccounts'))


@accounts.route('/removeAdminRights/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def removeAdminRights(id):
    user = Users.query.filter_by(id=id).first()
    try:
        user.admin_role = False
        db.session.commit()
        flash('Succesfully updated the admin rights!', 'info')
        return redirect(url_for('accounts.viewAccounts'))
    except:
        flash('There was a problem updating the admin rights!', 'warning')
        return redirect(url_for('accounts.viewAccounts'))


@accounts.route('/changePassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    if request.method == 'POST':
        currentPassword = request.form.get('currentPassword')
        newPassword = request.form.get('newPassword')
        confirmNewPassword = request.form.get('confirmNewPassword')
        if bcrypt.check_password_hash(current_user.password, currentPassword):
            if newPassword == confirmNewPassword:
                errorMessage, validationStatus = validate(confirmNewPassword)
                if (validationStatus):
                    try:
                        current_user.password = bcrypt.generate_password_hash(newPassword).decode('utf-8')
                        db.session.commit()
                        flash('Password changed successfully!', 'info')
                        return redirect(url_for('accounts.changePassword'))
                    except:
                        flash('There was a problem changing the password!', 'warning')
                        return redirect(url_for('accounts.changePassword'))
                else:
                    flash(errorMessage, 'warning')
            else:
                flash('The passwords do not match!', 'warning')
                return redirect(url_for('accounts.changePassword'))
        else:
            flash('Wrong password! Please try again!', 'warning')
            return redirect(url_for('accounts.changePassword'))
    return render_template('changePasswordPage.html')
