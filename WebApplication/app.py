import os
from firebase import firebase
from firebase.firebase import FirebaseAuthentication
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from functions.wrappers import admin_required
from functions.convert import toBoolean, toInt
from functions.time import getTime
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user

firebase = firebase.FirebaseApplication(str(os.environ.get('FIREBASE_URL')))
authentication = FirebaseAuthentication(str(os.environ.get('DATABASE_SECRET')),
                                        str(os.environ.get('APP_ACCOUNT')),
                                        extra={'uid': str(os.environ.get('USER_ID'))})
firebase.authentication = authentication

app = Flask(__name__)

app.config['SECRET_KEY'] = str(os.environ.get('FLASK_SECRET_KEY'))
app.config['SQLALCHEMY_DATABASE_URI'] = str(os.environ.get('SQLITE_URL'))
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
csrf = CSRFProtect(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    admin_role = db.Column(db.Boolean, default=False)


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


@app.route('/room', methods=['POST', 'GET'])
@login_required
def room():
    temp1 = firebase.get('CurrentTempRoom1', 'Value')
    temp2 = firebase.get('CurrentTempRoom2', 'Value')
    hum1 = firebase.get('HumidityRoom1', 'Value')
    hum2 = firebase.get('HumidityRoom2', 'Value')
    desiredTemperature1 = firebase.get('DesiredTempRoom1/Zapier', 'Value')
    desiredTemperature2 = firebase.get('DesiredTempRoom2/Zapier', 'Value')
    status = firebase.get('SwitchIntervalsOn', 'Value')
    if request.method == 'POST':
        variable = request.form.get('outputValue1')
        if variable is not None:
            firebase.put('DesiredTempRoom1/Zapier', 'Value', int(variable))
            return render_template('controlPage.html', tempR1=temp1, tempR2=temp2, humR1=hum1, humR2=hum2,
                                   desiredTemperature1=int(variable), desiredTemperature2=desiredTemperature2,
                                   status=status)
        else:
            variable = request.form.get('outputValue2')
            firebase.put('DesiredTempRoom2/Zapier', 'Value', int(variable))
            return render_template('controlPage.html', tempR1=temp1, tempR2=temp2, humR1=hum1, humR2=hum2,
                                   desiredTemperature1=desiredTemperature1, desiredTemperature2=int(variable),
                                   status=status)
    return render_template('controlPage.html', tempR1=temp1, tempR2=temp2, humR1=hum1, humR2=hum2,
                           desiredTemperature1=desiredTemperature1, desiredTemperature2=desiredTemperature2,
                           status=status)


@app.route('/switchIntervalsOn', methods=['GET', 'POST'])
@login_required
def switchIntervalsOn():
    if request.method == 'POST':
        switchIntervalsOn = toInt(request.form.get('switchIntervalsOn'))
        firebase.put('SwitchIntervalsOn', 'Value', switchIntervalsOn)
    return redirect(url_for('room'))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_to_login = Users.query.filter_by(username=username).first()
        if user_to_login:
            if bcrypt.check_password_hash(user_to_login.password, password):
                login_user(user_to_login)
                return redirect(url_for('room'))
            else:
                flash('Wrong credentials!', 'warning')
                return redirect(url_for('login'))
        else:
            flash('This account does not exist in our database! Please contact the administrator for creating one!',
                  'warning')
            return redirect(url_for('login'))
    return render_template('loginPage.html')


@app.route('/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        confirm_password = request.form.get('confirmPassword')
        admin_role = toBoolean(request.form.get('admin_role'))
        if bcrypt.check_password_hash(password, confirm_password):
            user = Users(username=username, password=password, admin_role=admin_role)
            try:
                db.session.add(user)
                db.session.commit()
                flash('You successfully created a new account!', 'info')
                return redirect(url_for('register'))
            except:
                flash('There was a problem creating this new account!', 'warning')
                return redirect(url_for('register'))
        else:
            flash('The passwords do not match!', 'warning')
            return redirect(url_for('register'))
    return render_template('registerPage.html')


@app.route('/viewAccounts', methods=['GET', 'POST'])
@login_required
@admin_required
def viewAccounts():
    users = Users.query.all()
    return render_template('accountsPage.html', users=users)


@app.route('/deleteAccount/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def deleteAccount(id):
    user = Users.query.filter_by(id=id).first()
    try:
        db.session.delete(user)
        db.session.commit()
        flash('The account was successfully deleted!', 'info')
        return redirect(url_for('viewAccounts'))
    except:
        flash('There was a problem deleting the account!', 'warning')
        return redirect(url_for('viewAccounts'))


@app.route('/giveAdminRights/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def giveAdminRights(id):
    user = Users.query.filter_by(id=id).first()
    try:
        user.admin_role = True
        db.session.commit()
        flash('Succesfully updated the admin rights!', 'info')
        return redirect(url_for('viewAccounts'))
    except:
        flash('There was a problem updating the admin rights!', 'warning')
        return redirect(url_for('viewAccounts'))


@app.route('/removeAdminRights/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def removeAdminRights(id):
    user = Users.query.filter_by(id=id).first()
    try:
        user.admin_role = False
        db.session.commit()
        flash('Succesfully updated the admin rights!', 'info')
        return redirect(url_for('viewAccounts'))
    except:
        flash('There was a problem updating the admin rights!', 'warning')
        return redirect(url_for('viewAccounts'))


@app.route('/changePassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    if request.method == 'POST':
        currentPassword = request.form.get('currentPassword')
        newPassword = request.form.get('newPassword')
        confirmNewPassword = request.form.get('confirmNewPassword')
        if bcrypt.check_password_hash(current_user.password, currentPassword):
            if newPassword == confirmNewPassword:
                try:
                    current_user.password = bcrypt.generate_password_hash(newPassword).decode('utf-8')
                    db.session.commit()
                    flash('Successfully changed password!', 'info')
                    return redirect(url_for('changePassword'))
                except:
                    flash('There was a problem changing the password!', 'warning')
                    return redirect(url_for('changePassword'))
            else:
                flash('The passwords do not match!', 'warning')
                return redirect(url_for('changePassword'))
        else:
            flash('Wrong password! Please try again', 'warning')
            return redirect(url_for('changePassword'))
    return render_template('changePasswordPage.html')


@app.route('/setIntervalsForWorkingDays', methods=['GET', 'POST'])
@login_required
def setIntervalsForWorkingDays():
    if request.method == 'POST':
        a = request.form.get('firstWorkingDayInterval')
        b = request.form.get('secondWorkingDayInterval')
        c = request.form.get('thirdWorkingDayInterval')
        d = request.form.get('fourthWorkingDayInterval')

        temperatureAB = request.form.get('temperatureFirstWDInterval')
        temperatureBC = request.form.get('temperatureSecondWDInterval')
        temperatureCD = request.form.get('temperatureThirdWDInterval')
        temperatureDA = request.form.get('temperatureFourthWDInterval')

        timeObjectA = getTime(a)
        timeObjectB = getTime(b)
        timeObjectC = getTime(c)
        timeObjectD = getTime(d)

        if timeObjectA < timeObjectB < timeObjectC < timeObjectD:
            try:
                firebase.put('WorkingDay', 'A', a)
                firebase.put('WorkingDay', 'B', b)
                firebase.put('WorkingDay', 'C', c)
                firebase.put('WorkingDay', 'D', d)

                firebase.put('WorkingDay', 'TemperatureAB', int(temperatureAB))
                firebase.put('WorkingDay', 'TemperatureBC', int(temperatureBC))
                firebase.put('WorkingDay', 'TemperatureCD', int(temperatureCD))
                firebase.put('WorkingDay', 'TemperatureDA', int(temperatureDA))

                flash('Intervals were set successfully!', 'info')
            except Exception as err:
                flash('An error ocurred while setting intervals: {0}'.format(err), 'warning')
        else:
            flash('Time intervals must be set chronologically!', 'warning')
    return render_template('schedulingPage.html')


@app.route('/setIntervalsForWeekend', methods=['GET', 'POST'])
@login_required
def setIntervalsForWeekend():
    if request.method == 'POST':
        a = request.form.get('firstWeekendInterval')
        b = request.form.get('secondWeekendInterval')

        temperatureAB = request.form.get('temperatureFirstWInterval')
        temperatureBA = request.form.get('temperatureSecondWInterval')

        timeObjectA = getTime(a)
        timeObjectB = getTime(b)

        if timeObjectA < timeObjectB:
            try:
                firebase.put('Weekend', 'A', a)
                firebase.put('Weekend', 'B', b)

                firebase.put('Weekend', 'TemperatureAB', int(temperatureAB))
                firebase.put('Weekend', 'TemperatureBA', int(temperatureBA))

                flash('Intervals were set successfully!', 'info')
            except Exception as err:
                flash('An error ocurred while setting intervals: {0}'.format(err), 'warning')
        else:
            flash('Time intervals must be set chronologically!', 'warning')
    return render_template('schedulingPage.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
