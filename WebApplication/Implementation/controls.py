from flask import Blueprint
from Implementation.functions.convert import toInt
from Implementation.functions.time import getTime
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required
from Implementation import firebase

controls = Blueprint('controls', __name__)


@controls.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    status = firebase.get('SwitchIntervalsOn', 'Value')
    if request.method == 'POST':
        variable = request.form.get('outputValue1')
        if variable is not None:
            firebase.put('DesiredTempRoom1/Zapier', 'Value', int(variable))
        else:
            variable = request.form.get('outputValue2')
            firebase.put('DesiredTempRoom2/Zapier', 'Value', int(variable))
    return render_template('controlPage.html', status=status)


@controls.route('/switchIntervalsOn', methods=['GET', 'POST'])
@login_required
def switchIntervalsOn():
    if request.method == 'POST':
        switchIntervalsOn = toInt(request.form.get('switchIntervalsOn'))
        firebase.put('SwitchIntervalsOn', 'Value', switchIntervalsOn)
    return redirect(url_for('controls.home'))


@controls.route('/setIntervalsForWorkingDays', methods=['GET', 'POST'])
@login_required
def setIntervalsForWorkingDays():
    MIN = 15
    MAX = 32
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

        if int(temperatureAB) < MIN or int(temperatureAB) > MAX or int(temperatureBC) < MIN or int(
                temperatureBC) > MAX or int(temperatureCD) < MIN or int(temperatureCD) > MAX or int(
            temperatureDA) < MIN or int(temperatureDA) > MAX:
            flash('The values of temperatures should be between 15 and 32 degrees!', 'warning')
        else:
            if timeObjectA < timeObjectB < timeObjectC < timeObjectD:
                try:
                    firebase.put('Intervals/WorkingDay', 'A', a)
                    firebase.put('Intervals/WorkingDay', 'B', b)
                    firebase.put('Intervals/WorkingDay', 'C', c)
                    firebase.put('Intervals/WorkingDay', 'D', d)

                    firebase.put('Intervals/WorkingDay', 'TemperatureAB', int(temperatureAB))
                    firebase.put('Intervals/WorkingDay', 'TemperatureBC', int(temperatureBC))
                    firebase.put('Intervals/WorkingDay', 'TemperatureCD', int(temperatureCD))
                    firebase.put('Intervals/WorkingDay', 'TemperatureDA', int(temperatureDA))

                    flash('Intervals were set successfully!', 'info')
                except Exception as err:
                    flash('An error ocurred while setting intervals: {0}'.format(err), 'warning')
            else:
                flash('Time intervals must be set chronologically!', 'warning')
    return render_template('schedulingPage.html')


@controls.route('/setIntervalsForWeekend', methods=['GET', 'POST'])
@login_required
def setIntervalsForWeekend():
    MIN = 15
    MAX = 32
    if request.method == 'POST':
        a = request.form.get('firstWeekendInterval')
        b = request.form.get('secondWeekendInterval')

        temperatureAB = request.form.get('temperatureFirstWInterval')
        temperatureBA = request.form.get('temperatureSecondWInterval')

        timeObjectA = getTime(a)
        timeObjectB = getTime(b)

        if int(temperatureAB) < MIN or int(temperatureAB) > MAX or int(temperatureBA) < MIN or int(
                temperatureBA) > MAX:
            flash('The values of temperatures should be between 15 and 32 degrees!', 'warning')
        else:
            if timeObjectA < timeObjectB:
                try:
                    firebase.put('Intervals/Weekend', 'A', a)
                    firebase.put('Intervals/Weekend', 'B', b)

                    firebase.put('Intervals/Weekend', 'TemperatureAB', int(temperatureAB))
                    firebase.put('Intervals/Weekend', 'TemperatureBA', int(temperatureBA))

                    flash('Intervals were set successfully!', 'info')
                except Exception as err:
                    flash('An error ocurred while setting intervals: {0}'.format(err), 'warning')
            else:
                flash('Time intervals must be set chronologically!', 'warning')
    return render_template('schedulingPage.html')
