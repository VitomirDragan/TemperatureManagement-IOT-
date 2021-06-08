from flask import Blueprint
from Implementation.functions.convert import toInt
from Implementation.functions.time import getTime
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required
from Implementation import firebase

controls = Blueprint('controls', __name__)


@controls.route('/home', methods=['POST', 'GET'])
@login_required  # Access function only if an user is logged in
def home():
    status = firebase.get('SwitchIntervalsOn',
                          'Value')  # Read the variable from database that indicates the operating mode of the system
    if request.method == 'POST':  # Verify if there is a POST request
        variable = request.form.get('outputValue1')  # Read value of temperature set by user for the first room
        if variable is not None:
            firebase.put('DesiredTempRoom1/Zapier', 'Value', int(variable))  # Save desired temperature in database
        else:
            variable = request.form.get('outputValue2')  # Read value of temperature set by user for the second room
            firebase.put('DesiredTempRoom2/Zapier', 'Value', int(variable))  # Save desired temperature in database
    return render_template('controlPage.html', status=status)  # Process and display 'controlPage.html' template


@controls.route('/switchIntervalsOn', methods=['GET', 'POST'])
@login_required
def switchIntervalsOn():
    if request.method == 'POST':  # Verify if there is a POST request
        switchIntervalsOn = toInt(request.form.get(
            'switchIntervalsOn'))  # Read the new value of the switchIntervalsOn variable. Indicates the system operating mode
        firebase.put('SwitchIntervalsOn', 'Value', switchIntervalsOn)  # Save the updated value in database
    return redirect(url_for('controls.home'))  # Redirect to controls page


@controls.route('/setIntervalsForWorkingDays', methods=['GET', 'POST'])
@login_required
def setIntervalsForWorkingDays():
    MIN = 15  # Set the minimum value o temperature accepted by system
    MAX = 32  # Set the maximum value o temperature accepted by system
    if request.method == 'POST':  # Verify if there is a POST request
        # Read the beginning and ending of each interval
        a = request.form.get('firstWorkingDayInterval')
        b = request.form.get('secondWorkingDayInterval')
        c = request.form.get('thirdWorkingDayInterval')
        d = request.form.get('fourthWorkingDayInterval')

        # Read temperature for each interval
        temperatureAB = request.form.get('temperatureFirstWDInterval')
        temperatureBC = request.form.get('temperatureSecondWDInterval')
        temperatureCD = request.form.get('temperatureThirdWDInterval')
        temperatureDA = request.form.get('temperatureFourthWDInterval')

        # Create date-time object for each beginning and ending of interval
        timeObjectA = getTime(a)
        timeObjectB = getTime(b)
        timeObjectC = getTime(c)
        timeObjectD = getTime(d)

        if int(temperatureAB) < MIN or int(temperatureAB) > MAX or int(temperatureBC) < MIN or int(
                temperatureBC) > MAX or int(temperatureCD) < MIN or int(temperatureCD) > MAX or int(
            temperatureDA) < MIN or int(temperatureDA) > MAX:
            # If the temperature values are not in range, an error message will be displayed
            flash('The values of temperatures should be between 15 and 32 degrees!', 'warning')
        else:
            if timeObjectA < timeObjectB < timeObjectC < timeObjectD:  # Verify if time intervals are set chronologically
                try:
                    # Save time intervals in database
                    firebase.put('Intervals/WorkingDay', 'A', a)
                    firebase.put('Intervals/WorkingDay', 'B', b)
                    firebase.put('Intervals/WorkingDay', 'C', c)
                    firebase.put('Intervals/WorkingDay', 'D', d)

                    # Save temperature values in database
                    firebase.put('Intervals/WorkingDay', 'TemperatureAB', int(temperatureAB))
                    firebase.put('Intervals/WorkingDay', 'TemperatureBC', int(temperatureBC))
                    firebase.put('Intervals/WorkingDay', 'TemperatureCD', int(temperatureCD))
                    firebase.put('Intervals/WorkingDay', 'TemperatureDA', int(temperatureDA))

                    flash('Intervals were set successfully!', 'info')
                except Exception as err:
                    # If an error occurs while saving intervals and temperature values in database, the error message will be displayed
                    flash('An error ocurred while setting intervals: {0}'.format(err), 'warning')
            else:
                # If time intervals are not set chronologically, the error message will be displayed
                flash('Time intervals must be set chronologically!', 'warning')
    return render_template('schedulingPage.html')  # Process and display 'schedulingPage.html'


@controls.route('/setIntervalsForWeekend', methods=['GET', 'POST'])
@login_required
def setIntervalsForWeekend():
    MIN = 15  # Set the minimum value o temperature accepted by system
    MAX = 32  # Set the maximum value o temperature accepted by system
    if request.method == 'POST':  # Verify if there is a POST request
        # Save time intervals in database
        a = request.form.get('firstWeekendInterval')
        b = request.form.get('secondWeekendInterval')

        # Save temperature values in database
        temperatureAB = request.form.get('temperatureFirstWInterval')
        temperatureBA = request.form.get('temperatureSecondWInterval')

        # Create date-time object for each beginning and ending of interval
        timeObjectA = getTime(a)
        timeObjectB = getTime(b)

        if int(temperatureAB) < MIN or int(temperatureAB) > MAX or int(temperatureBA) < MIN or int(
                temperatureBA) > MAX:
            # If the temperature values are not in range, an error message will be displayed
            flash('The values of temperatures should be between 15 and 32 degrees!', 'warning')
        else:
            if timeObjectA < timeObjectB:
                try:
                    # Save time intervals in database
                    firebase.put('Intervals/Weekend', 'A', a)
                    firebase.put('Intervals/Weekend', 'B', b)

                    # Save temperature values in database
                    firebase.put('Intervals/Weekend', 'TemperatureAB', int(temperatureAB))
                    firebase.put('Intervals/Weekend', 'TemperatureBA', int(temperatureBA))

                    flash('Intervals were set successfully!', 'info')
                except Exception as err:
                    # If an error occurs while saving intervals and temperature values in database, the error message will be displayed
                    flash('An error ocurred while setting intervals: {0}'.format(err), 'warning')
            else:
                # If time intervals are not set chronologically, the error message will be displayed
                flash('Time intervals must be set chronologically!', 'warning')
    return render_template('schedulingPage.html')  # Process and display 'schedulingPage.html'
