from flask import Blueprint
from flask_login import login_required, current_user
from Implementation.functions.wrappers import admin_required
from Implementation.functions.passwordValidation import validate
from Implementation import Users, bcrypt, db
from Implementation.functions.convert import toBoolean
from flask import render_template, request, url_for, flash, redirect

accounts = Blueprint('accounts', __name__)  # Create blueprint for accounts logic


@accounts.route('/register', methods=['GET', 'POST'])
@login_required  # Access function only if exists an user logged in
@admin_required  # Access function if the user logged in is administrator
def register():
    if request.method == 'POST':  # Verify if there is a POST request
        username = request.form.get('username')  # Get the username from the form
        password = bcrypt.generate_password_hash(request.form.get('password')).decode(
            'utf-8')  # Hash the password read from the form
        confirm_password = request.form.get('confirmPassword')  # Get the password typed in the confirm password field
        admin_role = toBoolean(request.form.get('admin_role'))  # Read and convert the value from the admin role field
        if bcrypt.check_password_hash(password,
                                      confirm_password):  # Verify if the password and the confirmed password are the same
            errorMessage, validationStatus = validate(
                confirm_password)  # Validate the password. Make sure that it is secure enough
            if (validationStatus):  # Verify if the validation returned true
                user = Users(username=username, password=password, admin_role=admin_role)  # Create a new user account
                try:
                    db.session.add(user)  # Add user in the database
                    db.session.commit()  # Commit the changes
                    flash('You successfully created a new account!', 'info')
                    return redirect(url_for('accounts.register'))  # Return to the register page
                except:
                    # In case of failure, display a message and return to register page
                    flash('There was a problem creating this new account!', 'warning')
                    return redirect(url_for('accounts.register'))
            else:
                flash(errorMessage, 'warning')  # If password is not secure, display an error message
        else:
            # If the passwords do not match, an error message will be displayed and the user will be redirected to register page
            flash('The passwords do not match!', 'warning')
            return redirect(url_for('accounts.register'))
    return render_template('registerPage.html')  # Process and display the 'registerPage.html'


@accounts.route('/viewAccounts', methods=['GET', 'POST'])
@login_required
@admin_required
def viewAccounts():
    users = Users.query.all()  # Get all users from database
    return render_template('accountsPage.html',
                           users=users)  # Display 'accountsPage.html' which will contain all the users


@accounts.route('/deleteAccount/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def deleteAccount(id):
    user = Users.query.filter_by(id=id).first()  # Get the user specified by id
    try:
        db.session.delete(user)  # Delete the user from database
        db.session.commit()  # Commit the changes
        flash('The account was successfully deleted!', 'info')
        return redirect(url_for('accounts.viewAccounts'))  # The user is redirected to viewAccounts page
    except:
        """ In case of error while deleting user, a message will be displayed and the user will be redirected
        to viewAccounts page """
        flash('There was a problem deleting the account!', 'warning')
        return redirect(url_for('accounts.viewAccounts'))


@accounts.route('/giveAdminRights/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def giveAdminRights(id):
    user = Users.query.filter_by(id=id).first()  # Get the user specified by id
    try:
        user.admin_role = True  # Set the admin_role to True, indicating that the user will have admin rights
        db.session.commit()  # Commit the changes
        flash('Succesfully updated the admin rights!', 'info')
        return redirect(url_for('accounts.viewAccounts'))  # Redirect to viewAccounts page
    except:
        """ In case of error while updating user rights, a message will be displayed and the user will be redirected
        to viewAccounts page """
        flash('There was a problem updating the admin rights!', 'warning')
        return redirect(url_for('accounts.viewAccounts'))


@accounts.route('/removeAdminRights/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def removeAdminRights(id):
    user = Users.query.filter_by(id=id).first()  # Get the user specified by id
    try:
        user.admin_role = False  # Set the admin_role to FALSE, indicating that the admin rights of the user will be removed
        db.session.commit()  # Commit the changes
        flash('Succesfully updated the admin rights!', 'info')
        return redirect(url_for('accounts.viewAccounts'))  # Redirect to viewAccounts page
    except:
        """In case of error while updating user rights, a message will be displayed and the user will be redirected
         to viewAccounts page """
        flash('There was a problem updating the admin rights!', 'warning')
        return redirect(url_for('accounts.viewAccounts'))


@accounts.route('/changePassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    if request.method == 'POST':  # Verify if there is a POST request
        currentPassword = request.form.get('currentPassword')  # Get the current password from the form
        newPassword = request.form.get('newPassword')  # Get the new password from the form
        confirmNewPassword = request.form.get(
            'confirmNewPassword')  # Get the password typed in the confirm password field
        if bcrypt.check_password_hash(current_user.password,
                                      currentPassword):  # Verify if the password introduced in the current password field is the same as the password from the database
            if newPassword == confirmNewPassword:  # Verify if the new password and the confirmed password are the same
                errorMessage, validationStatus = validate(
                    confirmNewPassword)  # Validate the password. Make sure that it is secure enough
                if (validationStatus):  # Verify if the validation returned true
                    try:
                        current_user.password = bcrypt.generate_password_hash(newPassword).decode(
                            'utf-8')  # Hash the password read from the form
                        db.session.commit()  # Commit the changes
                        flash('Password changed successfully!', 'info')
                        return redirect(url_for('accounts.changePassword'))  # Redirect user to changePassword page
                    except:
                        """In case of error while saving the new password in database, a message will be displayed and the user will be redirected
                         to viewAccounts page """
                        flash('There was a problem changing the password!', 'warning')
                        return redirect(url_for('accounts.changePassword'))
                else:
                    flash(errorMessage, 'warning')  # If password is not secure, display an error message
            else:
                # If the passwords do not match, an error message will be displayed and the user will be redirected to changePassword page
                flash('The passwords do not match!', 'warning')
                return redirect(url_for('accounts.changePassword'))
        else:
            # If the current password introduced by user is wrong, an error message will be displayed and the user will be redirected to changePassword page
            flash('Wrong password! Please try again!', 'warning')
            return redirect(url_for('accounts.changePassword'))
    return render_template('changePasswordPage.html')  # Process and display the 'changePasswordPage.html'
